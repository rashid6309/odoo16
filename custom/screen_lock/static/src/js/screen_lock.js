/* Screen Lock Module - Browser Compatible Implementation */

(function() {
    'use strict';

    function ScreenLockManager() {
        this.isLocked = false;
        this.init();
    }

    ScreenLockManager.prototype.init = function() {
        this.createLockOverlay();
        this.addToUserMenu();
        this.setupGlobalFunction();
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

    ScreenLockManager.prototype.lockScreen = function() {
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

        // Show overlay
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
        
        var checkUserMenu = setInterval(function() {
            var userMenu = document.querySelector('.o_user_menu');
            if (userMenu) {
                clearInterval(checkUserMenu);
                
                // Check if already added
                if (document.querySelector('.lock-screen-menu-item')) {
                    return;
                }
                
                var lockScreenItem = document.createElement('a');
                lockScreenItem.className = 'dropdown-item lock-screen-menu-item';
                lockScreenItem.href = '#';
                lockScreenItem.innerHTML = '<i class="fa fa-lock me-2"></i>Lock Screen';
                
                lockScreenItem.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Close dropdown
                    var dropdown = document.querySelector('.o_user_menu .dropdown-menu');
                    if (dropdown) {
                        dropdown.classList.remove('show');
                    }
                    
                    self.lockScreen();
                });
                
                var dropdownMenu = userMenu.querySelector('.dropdown-menu');
                if (dropdownMenu) {
                    var separator = dropdownMenu.querySelector('.dropdown-divider');
                    if (separator) {
                        dropdownMenu.insertBefore(lockScreenItem, separator);
                    } else {
                        dropdownMenu.appendChild(lockScreenItem);
                    }
                }
            }
        }, 100);
        
        setTimeout(function() {
            clearInterval(checkUserMenu);
        }, 10000);
    };

    // Initialize when DOM is ready
    function initScreenLock() {
        if (!document.getElementById('screen_lock_overlay')) {
            new ScreenLockManager();
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
                    new ScreenLockManager();
                }
            }, 500);
        }
    }).observe(document, { subtree: true, childList: true });

})();