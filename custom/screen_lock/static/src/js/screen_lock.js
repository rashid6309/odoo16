/* Screen Lock Module - Session-Based Locking */

(function() {
    'use strict';

    function ScreenLockManager() {
        this.isLocked = false;
        this.sessionLocked = false;
        this.checkInterval = null;
        this.init();
    }

    ScreenLockManager.prototype.init = function() {
        var self = this;
        this.createLockOverlay();
        this.addToUserMenu();
        this.setupGlobalFunction();
        this.setupKeyboardShortcut();
        
        // Check session lock status on page load
        this.checkSessionLockStatus().then(function() {
            // Start periodic session check
            self.startSessionCheck();
        });
    };

    ScreenLockManager.prototype.createLockOverlay = function() {
        var self = this;
        
        // Create lock overlay HTML
        var overlayHTML = 
            '<div id="screen_lock_overlay" class="o_screen_lock_overlay" style="display: none;">' +
                '<div class="screen-lock-overlay">' +
                    '<div class="lock-screen">' +
                        '<div class="text-center">' +
                            '<img id="lock_user_image" src="/web/static/img/user_menu_avatar.png" class="user-image mb-3" alt="User Avatar"/>' +
                            '<h4 class="user-name mb-3" id="lock_user_name">User</h4>' +
                            '<div class="pin-container">' +
                                '<input type="password" id="lock_pin_input" class="pin-input form-control mb-2" placeholder="Enter PIN" maxlength="4"/>' +
                                '<div id="lock_error_msg" class="invalid-feedback d-block" style="display: none;">Invalid PIN. Please try again.</div>' +
                                '<button id="lock_unlock_btn" class="unlock-btn btn btn-primary w-100"><i class="fa fa-unlock"></i> Unlock</button>' +
                                '<div class="mt-2 text-muted small">Press Ctrl+Alt+L to lock screen</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>';

        // Add to body
        document.body.insertAdjacentHTML('beforeend', overlayHTML);

        // Add event listeners
        document.getElementById('lock_unlock_btn').addEventListener('click', function() {
            self.unlockScreen();
        });

        document.getElementById('lock_pin_input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.keyCode === 13) {
                self.unlockScreen();
            }
        });

        document.getElementById('lock_pin_input').addEventListener('input', function() {
            self.hideError();
        });
    };

    ScreenLockManager.prototype.setupGlobalFunction = function() {
        var self = this;
        window.lockScreen = function() {
            self.lockScreen();
        };
    };

    ScreenLockManager.prototype.setupKeyboardShortcut = function() {
        var self = this;
        
        document.addEventListener('keydown', function(e) {
            // Don't trigger shortcut if screen is already locked
            if (self.sessionLocked) {
                return;
            }
            
            // Ctrl+Alt+L to lock screen
            if (e.ctrlKey && e.altKey && (e.key === 'l' || e.key === 'L' || e.keyCode === 76)) {
                e.preventDefault();
                e.stopPropagation();
                self.lockScreen();
            }
        });
        
        // Show notification about shortcut on first load (only if not locked)
        setTimeout(function() {
            if (!self.sessionLocked && !localStorage.getItem('screen_lock_shortcut_shown')) {
                self.showNotification('Tip: Press Ctrl+Alt+L to quickly lock your screen!', 'info');
                localStorage.setItem('screen_lock_shortcut_shown', 'true');
            }
        }, 2000);
    };

    ScreenLockManager.prototype.checkSessionLockStatus = function() {
        var self = this;
        return this.makeRPCCall('/screen_lock/check', {})
            .then(function(result) {
                if (result && result.session_locked) {
                    self.sessionLocked = true;
                    self.showLockScreenImmediately();
                } else {
                    self.sessionLocked = false;
                }
                return result;
            })
            .catch(function(error) {
                console.error('Error checking session lock status:', error);
                return { session_locked: false };
            });
    };

    ScreenLockManager.prototype.startSessionCheck = function() {
        var self = this;
        
        // Check session lock status every 5 seconds
        this.checkInterval = setInterval(function() {
            self.checkSessionLockStatus();
        }, 5000);
    };

    ScreenLockManager.prototype.showLockScreenImmediately = function() {
        var self = this;
        this.isLocked = true;
        
        // Get current user info
        this.getCurrentUser()
            .then(function(userInfo) {
                self.updateUserDisplay(userInfo);
            })
            .catch(function(error) {
                console.error('Error getting user info:', error);
            });

        // Show overlay immediately
        var overlay = document.getElementById('screen_lock_overlay');
        overlay.style.display = 'flex';
        
        // Clear PIN input
        document.getElementById('lock_pin_input').value = '';
        this.hideError();
        
        // Prevent scrolling
        document.body.style.overflow = 'hidden';
        
        // Focus on input
        setTimeout(function() {
            document.getElementById('lock_pin_input').focus();
        }, 100);
    };

    ScreenLockManager.prototype.lockScreen = function() {
        var self = this;
        
        // First lock the session on server
        this.makeRPCCall('/screen_lock/lock_session', {})
            .then(function(result) {
                if (result && result.success) {
                    self.sessionLocked = true;
                    self.showLockScreenImmediately();
                } else {
                    self.showNotification('Error: ' + (result.error || 'Cannot lock screen'), 'danger');
                }
            })
            .catch(function(error) {
                console.error('Error locking session:', error);
                self.showNotification('Error locking screen. Please try again.', 'danger');
            });
    };

    ScreenLockManager.prototype.unlockScreen = function() {
        var self = this;
        var pinInput = document.getElementById('lock_pin_input');
        var pin = pinInput.value;

        if (!pin) {
            this.showError('Please enter your PIN');
            return;
        }

        this.makeRPCCall('/screen_lock/verify', { pin: pin })
            .then(function(result) {
                if (result && result.success) {
                    self.isLocked = false;
                    self.sessionLocked = false;
                    document.getElementById('screen_lock_overlay').style.display = 'none';
                    document.body.style.overflow = '';
                    pinInput.value = '';
                    self.hideError();
                    self.showNotification('Screen unlocked successfully', 'success');
                } else {
                    self.showError('Incorrect PIN. Please try again.');
                    pinInput.value = '';
                    setTimeout(function() {
                        pinInput.focus();
                    }, 100);
                }
            })
            .catch(function(error) {
                console.error('Error verifying PIN:', error);
                self.showError('Error verifying PIN. Please try again.');
                pinInput.value = '';
            });
    };

    ScreenLockManager.prototype.makeRPCCall = function(url, params) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        try {
                            var data = JSON.parse(xhr.responseText);
                            resolve(data.result);
                        } catch (e) {
                            reject(e);
                        }
                    } else {
                        reject(new Error('HTTP ' + xhr.status));
                    }
                }
            };
            
            var payload = JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                params: params,
                id: Math.floor(Math.random() * 1000)
            });
            
            xhr.send(payload);
        });
    };

    ScreenLockManager.prototype.getCurrentUser = function() {
        var self = this;
        return this.makeRPCCall('/web/session/get_session_info', {})
            .then(function(result) {
                return {
                    name: result.name || 'User',
                    uid: result.uid || 1
                };
            })
            .catch(function(error) {
                return { name: 'User', uid: 1 };
            });
    };

    ScreenLockManager.prototype.updateUserDisplay = function(userInfo) {
        document.getElementById('lock_user_name').textContent = userInfo.name;
        document.getElementById('lock_user_image').src = '/web/image/res.users/' + userInfo.uid + '/image_128';
    };

    ScreenLockManager.prototype.showError = function(message) {
        var errorElement = document.getElementById('lock_error_msg');
        var pinInput = document.getElementById('lock_pin_input');
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        pinInput.classList.add('is-invalid');
    };

    ScreenLockManager.prototype.hideError = function() {
        var errorElement = document.getElementById('lock_error_msg');
        var pinInput = document.getElementById('lock_pin_input');
        
        errorElement.style.display = 'none';
        pinInput.classList.remove('is-invalid');
    };

    ScreenLockManager.prototype.showNotification = function(message, type) {
        type = type || 'info';
        
        var notification = document.createElement('div');
        notification.className = 'alert alert-' + type + ' alert-dismissible fade show';
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '10002';
        notification.style.minWidth = '300px';
        
        notification.innerHTML = message + 
            '<button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>';
        
        document.body.appendChild(notification);
        
        setTimeout(function() {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 3000);
    };

    ScreenLockManager.prototype.addToUserMenu = function() {
        var self = this;
        var attempts = 0;
        var maxAttempts = 50; // Try for 5 seconds
        
        var checkUserMenu = setInterval(function() {
            attempts++;
            
            // Try multiple selectors for user menu
            var userMenu = document.querySelector('.o_user_menu') || 
                          document.querySelector('.oe_topbar_name') ||
                          document.querySelector('.o_main_navbar .dropdown') ||
                          document.querySelector('nav .navbar-nav .dropdown');
            
            if (userMenu || attempts >= maxAttempts) {
                clearInterval(checkUserMenu);
                
                if (!userMenu) {
                    console.log('User menu not found, trying alternative approach...');
                    self.addFloatingLockButton();
                    return;
                }
                
                // Check if already added
                if (document.querySelector('.lock-screen-menu-item')) {
                    return;
                }
                
                console.log('Found user menu, adding lock screen option...');
                
                var lockScreenItem = document.createElement('a');
                lockScreenItem.className = 'dropdown-item lock-screen-menu-item';
                lockScreenItem.href = '#';
                lockScreenItem.innerHTML = '<i class="fa fa-lock me-2"></i>Lock Screen <small class="text-muted">(Ctrl+Alt+L)</small>';
                
                lockScreenItem.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Don't allow locking if already locked
                    if (self.sessionLocked) {
                        return;
                    }
                    
                    // Close dropdown
                    var dropdown = userMenu.querySelector('.dropdown-menu') || 
                                  userMenu.querySelector('.dropdown-content');
                    if (dropdown) {
                        dropdown.classList.remove('show', 'open');
                    }
                    
                    self.lockScreen();
                });
                
                // Try to find dropdown menu
                var dropdownMenu = userMenu.querySelector('.dropdown-menu') ||
                                  userMenu.querySelector('.dropdown-content') ||
                                  userMenu.querySelector('ul');
                
                if (dropdownMenu) {
                    // Find a good place to insert
                    var separator = dropdownMenu.querySelector('.dropdown-divider') ||
                                   dropdownMenu.querySelector('.divider') ||
                                   dropdownMenu.querySelector('li.divider');
                    
                    if (separator) {
                        dropdownMenu.insertBefore(lockScreenItem, separator);
                    } else {
                        dropdownMenu.appendChild(lockScreenItem);
                    }
                    
                    console.log('Lock screen menu item added successfully');
                } else {
                    console.log('Dropdown menu not found, adding floating button...');
                    self.addFloatingLockButton();
                }
            }
        }, 100);
    };

    ScreenLockManager.prototype.addFloatingLockButton = function() {
        var self = this;
        
        // Create floating lock button if user menu integration fails
        var floatingButton = document.createElement('div');
        floatingButton.id = 'floating_lock_button';
        floatingButton.className = 'floating-lock-btn';
        floatingButton.innerHTML = '<i class="fa fa-lock"></i>';
        floatingButton.title = 'Lock Screen (Ctrl+Alt+L)';
        
        // Style the floating button
        floatingButton.style.cssText = 
            'position: fixed;' +
            'top: 80px;' +
            'right: 20px;' +
            'width: 50px;' +
            'height: 50px;' +
            'background: #007bff;' +
            'color: white;' +
            'border-radius: 50%;' +
            'display: flex;' +
            'align-items: center;' +
            'justify-content: center;' +
            'cursor: pointer;' +
            'z-index: 1000;' +
            'box-shadow: 0 2px 10px rgba(0,0,0,0.3);' +
            'transition: all 0.3s ease;';
        
        floatingButton.addEventListener('click', function() {
            if (!self.sessionLocked) {
                self.lockScreen();
            }
        });
        
        floatingButton.addEventListener('mouseenter', function() {
            if (!self.sessionLocked) {
                this.style.transform = 'scale(1.1)';
                this.style.background = '#0056b3';
            }
        });
        
        floatingButton.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = '#007bff';
        });
        
        document.body.appendChild(floatingButton);
        
        console.log('Floating lock button added');
    };

    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        var screenLockManager = window.screenLockManagerInstance;
        if (screenLockManager && screenLockManager.checkInterval) {
            clearInterval(screenLockManager.checkInterval);
        }
    });

    // Initialize when DOM is ready
    function initScreenLock() {
        if (!document.getElementById('screen_lock_overlay')) {
            window.screenLockManagerInstance = new ScreenLockManager();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScreenLock);
    } else {
        initScreenLock();
    }

    // Also reinitialize on page changes
    var lastUrl = location.href;
    new MutationObserver(function() {
        var url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            setTimeout(function() {
                if (!document.getElementById('screen_lock_overlay')) {
                    window.screenLockManagerInstance = new ScreenLockManager();
                }
            }, 500);
        }
    }).observe(document, { subtree: true, childList: true });

})();