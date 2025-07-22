// Debug script to find user menu in Odoo 16
// Run this in browser console to see available menu structures

console.log('=== SCREEN LOCK DEBUG: Finding User Menu ===');

// Common selectors for user menu in different Odoo versions
var selectors = [
    '.o_user_menu',
    '.oe_topbar_name', 
    '.o_main_navbar .dropdown',
    'nav .navbar-nav .dropdown',
    '.navbar-nav .dropdown',
    '.o_main_navbar .o_user_menu',
    '.navbar .dropdown',
    '.navbar-right .dropdown',
    '[data-toggle="dropdown"]',
    '.navbar-nav .nav-item.dropdown'
];

console.log('Checking selectors...');

selectors.forEach(function(selector, index) {
    var element = document.querySelector(selector);
    if (element) {
        console.log('✅ Found element with selector:', selector);
        console.log('   Element:', element);
        console.log('   Classes:', element.className);
        console.log('   HTML:', element.outerHTML.substring(0, 200) + '...');
        
        // Check for dropdown menu
        var dropdown = element.querySelector('.dropdown-menu') || 
                      element.querySelector('.dropdown-content') ||
                      element.querySelector('ul');
        if (dropdown) {
            console.log('   📋 Dropdown found:', dropdown.className);
        }
        console.log('---');
    } else {
        console.log('❌ Not found:', selector);
    }
});

// Check for any dropdown elements
console.log('\n=== All dropdown elements ===');
var dropdowns = document.querySelectorAll('.dropdown, [class*="dropdown"], [class*="menu"]');
console.log('Found', dropdowns.length, 'potential dropdown elements');

dropdowns.forEach(function(dropdown, index) {
    if (index < 10) { // Limit output
        console.log(index + ':', dropdown.className, dropdown.tagName);
    }
});

// Check navbar
console.log('\n=== Navbar elements ===');
var navbars = document.querySelectorAll('nav, .navbar, [class*="navbar"]');
navbars.forEach(function(nav, index) {
    console.log(index + ':', nav.className, nav.tagName);
});

console.log('\n=== END DEBUG ===');
console.log('Copy this output and send it to help diagnose the user menu location.');