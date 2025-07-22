odoo.define('screen_lock.ScreenLock', function (require) {
    "use strict";

    var core = require('web.core');
    var Session = require('web.session');
    var Widget = require('web.Widget');

    var ScreenLock = Widget.extend({
        template: 'ScreenLockOverlay',
        events: {
            'click .unlock-btn': 'unlockScreen',
        },
        init: function (parent) {
            this._super.apply(this, arguments);
            this.isLocked = false;
        },
        start: function () {
            this._super.apply(this, arguments);
            this.checkLockStatus();
            // Add Lock Screen button to the top bar
            this.$el.appendTo($('.o_main_navbar')).prepend('<button class="lock-screen-btn btn btn-primary">Lock Screen</button>');
            $('.lock-screen-btn').on('click', this.lockScreen.bind(this));
        },
        checkLockStatus: function () {
            var self = this;
            Session.rpc('/screen_lock/check', {}).then(function (result) {
                self.isLocked = result.locked;
                self.renderElement();
            });
        },
        lockScreen: function () {
            this.isLocked = true;
            this.renderElement();
        },
        unlockScreen: function (ev) {
            var pin = $('.pin-input').val();
            var self = this;
            Session.rpc('/screen_lock/verify', {pin: pin}).then(function (result) {
                if (result.success) {
                    self.isLocked = false;
                    self.renderElement();
                } else {
                    alert('Incorrect PIN');
                }
            });
        },
    });

    core.action_registry.add('screen_lock', ScreenLock);

    core.bus.on('lock_screen', null, function () {
        var screenLock = new ScreenLock();
        screenLock.appendTo($('body')).then(function () {
            screenLock.lockScreen();
        });
    });

    return ScreenLock;
});