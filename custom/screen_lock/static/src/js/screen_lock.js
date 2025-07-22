/* Screen Lock Module - Vanilla JavaScript Implementation */

(function() {
    'use strict';

    class ScreenLockManager {
        constructor() {
            this.isLocked = false;
            this.init();
        }

        init() {
            this.createLockOverlay();
            this.addToUserMenu();
            this.setupGlobalFunction();
        }

        createLockOverlay() {
            // Create lock overlay HTML
            const overlayHTML = `
                <div id="screen_lock_overlay" class="o_screen_lock_overlay" style="display: none;">
                    <div class="screen-lock-overlay">
                        <div class="lock-screen">
                            <div class="text-center">
                                <img id="lock_user_image" src="/web/static/img/user_menu_avatar.png" 
                                     class="user-image mb-3" alt="User Avatar"/>
                                <h4 class="user-name mb-3" id="lock_user_name">User</h4>
                                <div class="pin-container">
                                    <input type="password" 
                                           id="lock_pin_input"
                                           class="pin-input form-control mb-2" 
                                           placeholder="Enter PIN"
                                           maxlength="4"/>
                                    <div id="lock_error_msg" class="invalid-feedback d-block" style="display: none;">
                                        Invalid PIN. Please try again.
                                    </div>
                                    <button id="lock_unlock_btn" class="unlock-btn btn btn-primary w-100">
                                        <i class="fa fa-unlock"></i> Unlock
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Add to body
            document.body.insertAdjacentHTML('beforeend', overlayHTML);

            // Add event listeners
            document.getElementById('lock_unlock_btn').addEventListener('click', () => {
                this.unlockScreen();
            });

            document.getElementById('lock_pin_input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.unlockScreen();
                }
            });

            document.getElementById('lock_pin_input').addEventListener('input', () => {
                this.hideError();
            });
        }

        setupGlobalFunction() {
            window.lockScreen = () => {
                this.lockScreen();
            };
        }

        async lockScreen() {
            this.isLocked = true;
            
            // Get current user info
            try {
                const userInfo = await this.getCurrentUser();
                this.updateUserDisplay(userInfo);
            } catch (error) {
                console.error('Error getting user info:', error);
            }

            // Show overlay
            const overlay = document.getElementById('screen_lock_overlay');
            overlay.style.display = 'flex';
            
            // Clear PIN input
            document.getElementById('lock_pin_input').value = '';
            this.hideError();
            
            // Prevent scrolling
            document.body.style.overflow = 'hidden';
            
            // Focus on input
            setTimeout(() => {
                document.getElementById('lock_pin_input').focus();
            }, 100);
        }

        async unlockScreen() {
            const pinInput = document.getElementById('lock_pin_input');
            const pin = pinInput.value;

            if (!pin) {
                this.showError('Please enter your PIN');
                return;
            }

            try {
                const result = await this.makeRPCCall('/screen_lock/verify', { pin: pin });
                
                if (result.success) {
                    this.isLocked = false;
                    document.getElementById('screen_lock_overlay').style.display = 'none';
                    document.body.style.overflow = '';
                    pinInput.value = '';
                    this.hideError();
                    this.showNotification('Screen unlocked successfully', 'success');
                } else {
                    this.showError('Incorrect PIN. Please try again.');
                    pinInput.value = '';
                    setTimeout(() => {
                        pinInput.focus();
                    }, 100);
                }
            } catch (error) {
                console.error('Error verifying PIN:', error);
                this.showError('Error verifying PIN. Please try again.');
                pinInput.value = '';
            }
        }

        async makeRPCCall(url, params) {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: params,
                    id: Math.floor(Math.random() * 1000)
                })
            });
            
            const data = await response.json();
            return data.result;
        }

        async getCurrentUser() {
            try {
                const result = await this.makeRPCCall('/web/session/get_session_info', {});
                return {
                    name: result.name || 'User',
                    uid: result.uid || 1
                };
            } catch (error) {
                return { name: 'User', uid: 1 };
            }
        }

        updateUserDisplay(userInfo) {
            document.getElementById('lock_user_name').textContent = userInfo.name;
            document.getElementById('lock_user_image').src = `/web/image/res.users/${userInfo.uid}/image_128`;
        }

        showError(message) {
            const errorElement = document.getElementById('lock_error_msg');
            const pinInput = document.getElementById('lock_pin_input');
            
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            pinInput.classList.add('is-invalid');
        }

        hideError() {
            const errorElement = document.getElementById('lock_error_msg');
            const pinInput = document.getElementById('lock_pin_input');
            
            errorElement.style.display = 'none';
            pinInput.classList.remove('is-invalid');
        }

        showNotification(message, type = 'info') {
            // Simple notification
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show`;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10002;
                min-width: 300px;
            `;
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 3000);
        }

        addToUserMenu() {
            const checkUserMenu = setInterval(() => {
                const userMenu = document.querySelector('.o_user_menu');
                if (userMenu) {
                    clearInterval(checkUserMenu);
                    
                    // Check if already added
                    if (document.querySelector('.lock-screen-menu-item')) {
                        return;
                    }
                    
                    const lockScreenItem = document.createElement('a');
                    lockScreenItem.className = 'dropdown-item lock-screen-menu-item';
                    lockScreenItem.href = '#';
                    lockScreenItem.innerHTML = '<i class="fa fa-lock me-2"></i>Lock Screen';
                    
                    lockScreenItem.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Close dropdown
                        const dropdown = document.querySelector('.o_user_menu .dropdown-menu');
                        if (dropdown) {
                            dropdown.classList.remove('show');
                        }
                        
                        this.lockScreen();
                    });
                    
                    const dropdownMenu = userMenu.querySelector('.dropdown-menu');
                    if (dropdownMenu) {
                        const separator = dropdownMenu.querySelector('.dropdown-divider');
                        if (separator) {
                            dropdownMenu.insertBefore(lockScreenItem, separator);
                        } else {
                            dropdownMenu.appendChild(lockScreenItem);
                        }
                    }
                }
            }, 100);
            
            setTimeout(() => {
                clearInterval(checkUserMenu);
            }, 10000);
        }
    }

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
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            setTimeout(() => {
                if (!document.getElementById('screen_lock_overlay')) {
                    new ScreenLockManager();
                }
            }, 500);
        }
    }).observe(document, { subtree: true, childList: true });

})();