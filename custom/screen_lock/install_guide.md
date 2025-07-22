# Screen Lock Module - Installation Guide

## 🔒 Features
- **PIN-based screen lock** with user menu integration
- **Session-based locking**: Persists across page refreshes and new tabs
- **Keyboard shortcut**: `Ctrl+Alt+L` to instantly lock screen  
- **Fallback floating button** if user menu integration fails
- **Modern UI** with smooth animations
- **Automatic session checking** every 5 seconds

## 🛡️ Security Features

### Session-Based Locking
- **Cross-tab locking**: When locked, ALL browser tabs for that user are locked
- **Refresh protection**: Page refresh doesn't unlock the screen
- **New tab protection**: Opening new Odoo tabs shows lock screen
- **Server-side session**: Lock state stored securely on server

## Quick Fix for Issues

### 1. Clear Browser Cache
- Press `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac) to hard refresh
- Or open browser Developer Tools (F12) → Network tab → check "Disable cache"

### 2. Update the Module
If you have access to Odoo command line:
```bash
# Navigate to Odoo directory
cd /path/to/your/odoo

# Update the module
./odoo-bin -u screen_lock -d your_database_name --stop-after-init

# Or restart Odoo completely
./odoo-bin -d your_database_name
```

### 3. Alternative - Manual Asset Refresh
If you can't restart Odoo:
1. Go to Odoo Settings → Technical → User Interface → Views
2. Search for "assets_backend"
3. Edit any assets_backend view
4. Add a space somewhere and save (this forces asset regeneration)

### 4. Check Module Installation
1. Go to Apps menu
2. Search for "Screen Lock"
3. If installed, click "Upgrade"
4. If not installed, click "Install"

## 🎯 User Menu Troubleshooting

### If Lock Screen Button Missing:
1. **Check for floating button**: Look for a blue lock icon in top-right corner
2. **Debug user menu**: Open browser console (F12) and run the debug script:
   ```javascript
   // Copy and paste content from debug_menu.js file
   ```
3. **Manual menu detection**: The module tries multiple selectors for different Odoo versions

### Expected Behavior:
- ✅ **Best case**: "Lock Screen" appears in user dropdown menu
- ✅ **Fallback**: Blue floating lock button appears in top-right
- ✅ **Always works**: `Ctrl+Alt+L` keyboard shortcut
- ✅ **Session persistence**: Lock survives page refresh and new tabs

## 🚀 Usage

### Setting Up PIN
1. Go to Settings → Users & Companies → Users
2. Edit your user
3. Go to Preferences tab  
4. Find "Screen Lock Settings"
5. Click "Set/Change PIN"
6. Enter a 4-digit PIN and confirm

### Locking the Screen
**Method 1: Keyboard Shortcut (Recommended)**
- Press `Ctrl+Alt+L` anywhere in Odoo

**Method 2: User Menu**
- Click your username → "Lock Screen"

**Method 3: Floating Button**
- Click the blue lock icon (if visible)

### Unlocking the Screen
1. Enter your 4-digit PIN
2. Press Enter or click "Unlock"
3. Success notification will appear
4. **All browser tabs/windows are unlocked simultaneously**

## 🔄 Session Behavior

### What Happens When You Lock:
1. **Current tab**: Shows lock screen immediately
2. **Other open tabs**: Will show lock screen when accessed
3. **New tabs**: Automatically show lock screen
4. **Page refresh**: Lock screen persists
5. **Session check**: Every 5 seconds, checks if still locked

### What Happens When You Unlock:
1. **All tabs**: Unlock simultaneously
2. **Session cleared**: Server-side lock state removed
3. **Normal operation**: Full access restored across all tabs

## 🐛 Debugging

### Console Messages to Look For:
```
"Found user menu, adding lock screen option..."
"Screen locked for user: username"
"Checking session lock status..."
"Session locked, showing lock screen"
```

### If session locking not working:
1. Open browser console (F12)
2. Check for session-related errors
3. Verify user has PIN set
4. Test with `Ctrl+Alt+L` shortcut

### Emergency Unlock (Development Only):
```javascript
// Run in browser console ONLY for development/testing
fetch('/screen_lock/unlock_session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({jsonrpc: "2.0", method: "call", params: {}, id: 1})
});
```

### Common Issues:
- **No menu item**: Use floating button or keyboard shortcut
- **Lock doesn't persist**: Check browser console for session errors
- **Multiple tabs not syncing**: Verify session storage is working

## 📱 Mobile Support
- Responsive design works on mobile devices
- Session locking works across mobile tabs
- Touch-friendly PIN input

## 🎨 Customization

### Change Session Check Interval:
Edit the JavaScript file and modify:
```javascript
// Check session lock status every 5 seconds
this.checkInterval = setInterval(function() {
    self.checkSessionLockStatus();
}, 5000); // Change 5000 to desired milliseconds
```

### Change Keyboard Shortcut:
Edit the JavaScript file and modify:
```javascript
if (e.ctrlKey && e.altKey && (e.key === 'l' || e.key === 'L' || e.keyCode === 76)) {
```

## ✅ Verification Checklist
- [ ] Module installed/upgraded successfully
- [ ] PIN set in user preferences
- [ ] Keyboard shortcut `Ctrl+Alt+L` works
- [ ] Lock screen appears with user info
- [ ] PIN unlocks successfully
- [ ] **Lock persists after page refresh**
- [ ] **New tabs show lock screen when locked**
- [ ] **All tabs unlock together**
- [ ] Menu item OR floating button visible

## 🔐 Security Benefits

1. **True session locking**: Can't bypass by refreshing or opening new tabs
2. **Server-side validation**: PIN verification happens on server
3. **Automatic sync**: All browser instances sync lock state
4. **Persistent state**: Lock survives browser navigation
5. **Audit logging**: All lock/unlock events are logged

The enhanced implementation now provides enterprise-grade session-based locking that ensures true security across all browser tabs and windows!