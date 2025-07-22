/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

// Screen Lock Overlay Component
export class ScreenLockOverlay extends Component {
    setup() {
        this.state = useState({
            isLocked: false,
            pin: "",
            error: false,
        });
        
        this.rpc = useService("rpc");
        this.user = useService("user");
        this.notification = useService("notification");
        
        onMounted(() => {
            this.setupGlobalLockFunction();
        });
    }

    setupGlobalLockFunction() {
        // Make lock screen function globally available
        window.lockScreen = () => {
            this.lockScreen();
        };
    }

    lockScreen() {
        this.state.isLocked = true;
        this.state.pin = "";
        this.state.error = false;
        // Prevent scrolling when locked
        document.body.style.overflow = "hidden";
        // Focus on PIN input
        setTimeout(() => {
            const pinInput = document.querySelector('.pin-input');
            if (pinInput) {
                pinInput.focus();
            }
        }, 100);
    }

    async unlockScreen() {
        if (!this.state.pin) {
            this.state.error = true;
            this.notification.add(_t("Please enter your PIN"), {
                type: "warning",
            });
            return;
        }
        
        try {
            const result = await this.rpc("/screen_lock/verify", {
                pin: this.state.pin,
            });
            
            if (result.success) {
                this.state.isLocked = false;
                this.state.pin = "";
                this.state.error = false;
                document.body.style.overflow = "";
                this.notification.add(_t("Screen unlocked successfully"), {
                    type: "success",
                });
            } else {
                this.state.error = true;
                this.state.pin = "";
                this.notification.add(_t("Incorrect PIN. Please try again."), {
                    type: "danger",
                });
                // Refocus on input
                setTimeout(() => {
                    const pinInput = document.querySelector('.pin-input');
                    if (pinInput) {
                        pinInput.focus();
                    }
                }, 100);
            }
        } catch (error) {
            console.error("Error verifying PIN:", error);
            this.state.error = true;
            this.state.pin = "";
            this.notification.add(_t("Error verifying PIN. Please try again."), {
                type: "danger",
            });
        }
    }

    onPinInput(ev) {
        this.state.pin = ev.target.value;
        this.state.error = false;
    }

    onKeyPress(ev) {
        if (ev.key === "Enter") {
            this.unlockScreen();
        }
        // Prevent other key combinations when locked
        if (this.state.isLocked && ev.key === "Escape") {
            ev.preventDefault();
            ev.stopPropagation();
        }
    }
}

ScreenLockOverlay.template = "screen_lock.ScreenLockOverlay";

// Register the main component
registry.category("main_components").add("ScreenLockOverlay", ScreenLockOverlay);

// Add lock screen button to user menu
function addLockScreenToUserMenu() {
    // Wait for the user menu to be available
    const checkUserMenu = setInterval(() => {
        const userMenu = document.querySelector('.o_user_menu');
        if (userMenu) {
            clearInterval(checkUserMenu);
            
            // Check if lock screen button already exists
            if (document.querySelector('.lock-screen-menu-item')) {
                return;
            }
            
            // Create lock screen menu item
            const lockScreenItem = document.createElement('a');
            lockScreenItem.className = 'dropdown-item lock-screen-menu-item';
            lockScreenItem.href = '#';
            lockScreenItem.innerHTML = '<i class="fa fa-lock me-2"></i>Lock Screen';
            
            lockScreenItem.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Close the dropdown
                const dropdown = document.querySelector('.o_user_menu .dropdown-menu');
                if (dropdown) {
                    dropdown.classList.remove('show');
                }
                
                // Trigger lock screen
                if (window.lockScreen) {
                    window.lockScreen();
                }
            });
            
            // Find the user menu dropdown
            const dropdownMenu = userMenu.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                // Add before the last separator or at the end
                const separator = dropdownMenu.querySelector('.dropdown-divider');
                if (separator) {
                    dropdownMenu.insertBefore(lockScreenItem, separator);
                } else {
                    dropdownMenu.appendChild(lockScreenItem);
                }
            }
        }
    }, 100);
    
    // Clear interval after 10 seconds to avoid infinite checking
    setTimeout(() => {
        clearInterval(checkUserMenu);
    }, 10000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addLockScreenToUserMenu);
} else {
    addLockScreenToUserMenu();
}

// Also try to add when the page changes (for SPA navigation)
let lastUrl = location.href;
new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        setTimeout(addLockScreenToUserMenu, 500);
    }
}).observe(document, { subtree: true, childList: true });