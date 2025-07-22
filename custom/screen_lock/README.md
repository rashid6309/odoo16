# Screen Lock Module for Odoo 16

This module adds screen lock functionality to Odoo 16 Community Edition. Users can set a 4-digit PIN and lock their screen, requiring the PIN to unlock.

## Features

- **PIN-based Screen Lock**: Users can set a 4-digit PIN for screen locking
- **User Menu Integration**: Lock screen option appears in the user dropdown menu
- **Modern UI**: Beautiful lock screen overlay with smooth animations
- **Secure**: PIN is stored securely and verified server-side
- **Easy Setup**: Simple wizard for PIN configuration

## Installation

1. Copy the `screen_lock` folder to your Odoo custom addons directory
2. Update your Odoo configuration to include the custom addons path
3. Restart Odoo server
4. Go to Apps menu and install "Screen Lock using PIN"

## Usage

### Setting up PIN

1. Go to **Settings > Users & Companies > Users**
2. Edit your user record
3. Go to the **Preferences** tab
4. Find the **Screen Lock Settings** section
5. Click **Set/Change PIN** button
6. Enter a 4-digit PIN and confirm it
7. Click **Set PIN**

Alternatively, you can go to **Settings > Screen Lock** menu to set up your PIN.

### Locking the Screen

1. Click on your user name in the top-right corner
2. Select **Lock Screen** from the dropdown menu
3. The screen will be locked immediately

### Unlocking the Screen

1. Enter your 4-digit PIN in the lock screen
2. Press Enter or click the **Unlock** button
3. If the PIN is correct, the screen will unlock

## Technical Details

- **Compatibility**: Odoo 16 Community Edition
- **Dependencies**: base, web
- **Framework**: Uses modern OWL components
- **Storage**: PIN is stored on res.users model
- **Security**: Server-side PIN verification with logging

## File Structure

```
screen_lock/
├── __init__.py
├── __manifest__.py
├── README.md
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── res_users.py
│   └── screen_lock_wizard.py
├── security/
│   └── ir.model.access.csv
├── static/src/
│   ├── css/
│   │   └── screen_lock.css
│   ├── js/
│   │   └── screen_lock.js
│   └── xml/
│       └── screen_lock.xml
└── views/
    └── screen_lock_views.xml
```

## Security Notes

- PINs are stored as plain text in the database (consider encryption for production)
- Failed unlock attempts are logged
- Screen lock prevents normal UI interaction
- Only affects the current browser session

## Troubleshooting

### Lock Screen button not appearing
- Refresh the page
- Check if the module is properly installed
- Ensure you have proper user permissions

### Can't unlock screen
- Ensure your PIN is exactly 4 digits
- Check browser console for errors
- Contact administrator if you forgot your PIN

### Module installation issues
- Check Odoo logs for errors
- Ensure all dependencies are installed
- Verify file permissions

## Support

This module is provided as-is for Odoo 16 Community Edition. For issues or improvements, please check the module code and logs.