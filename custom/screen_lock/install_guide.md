# Screen Lock Module - Installation Guide

## 🔒 Features
- **PIN-based screen lock** with user menu integration
- **Keyboard shortcut**: `Ctrl+Alt+L` to instantly lock screen  
- **Fallback floating button** if user menu integration fails
- **Modern UI** with smooth animations

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

## 🐛 Debugging

### If user menu integration fails:
1. Open browser console (F12)
2. Look for messages starting with "Screen Lock:"
3. Check if you see:
   - "Found user menu, adding lock screen option..."
   - "User menu not found, trying alternative approach..."
   - "Floating lock button added"

### Common Issues:
- **No menu item**: Use floating button or keyboard shortcut
- **Keyboard shortcut not working**: Check browser console for errors
- **PIN not working**: Verify PIN is set in user preferences

### Debug Menu Structure:
1. Open browser console (F12)
2. Run the debug script from `debug_menu.js`
3. Copy the output to help diagnose menu issues

## 📱 Mobile Support
- Responsive design works on mobile devices
- Floating button adapts to smaller screens
- Touch-friendly PIN input

## 🎨 Customization

### Change Keyboard Shortcut:
Edit the JavaScript file and modify this line:
```javascript
if (e.ctrlKey && e.altKey && (e.key === 'l' || e.key === 'L' || e.keyCode === 76)) {
```

### Change Floating Button Position:
Edit the CSS file and modify:
```css
.floating-lock-btn {
    top: 80px !important;
    right: 20px !important;
}
```

## ✅ Verification Checklist
- [ ] Module installed/upgraded successfully
- [ ] PIN set in user preferences
- [ ] Keyboard shortcut `Ctrl+Alt+L` works
- [ ] Lock screen appears with user info
- [ ] PIN unlocks successfully
- [ ] Menu item OR floating button visible

The new implementation provides multiple ways to access screen lock functionality, ensuring it works even if the user menu structure varies between Odoo installations.