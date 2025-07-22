# Screen Lock Module - Installation Guide

## Quick Fix for OWL Errors

The OWL error you're seeing is likely due to cached assets. Follow these steps:

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

### 5. Verify Installation
1. After installation/upgrade, refresh the page
2. Click your username in the top-right corner
3. You should see "Lock Screen" option in the dropdown

## Setting Up PIN
1. Go to Settings → Users & Companies → Users
2. Edit your user
3. Go to Preferences tab
4. Find "Screen Lock Settings"
5. Click "Set/Change PIN"
6. Enter a 4-digit PIN

## Testing
1. Click your username → "Lock Screen"
2. Enter your PIN to unlock

The new implementation uses vanilla JavaScript and should not cause any OWL conflicts.