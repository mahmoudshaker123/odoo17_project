/** @odoo-module */
odoo.define('your_module.notification_counter', function (require) {
    "use strict";

    var core = require('web.core');
    var bus = require('bus.bus');
    var session = require('web.session');

    bus.on('notification', this, function (notifications) {
        _.each(notifications, function (notification) {
            if (notification[0] === 'simple_notification') {
                // Update the notification counter dynamically
                var message = notification[1].message;
                alert(message);  // Display the notification
                // Optionally, refresh the counter
            }
        });
    });

    bus.start_polling();
});
