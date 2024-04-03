
odoo.define('ecare_medical_history.EditableTreeExtend', function (require) {
    "use strict";
    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        _renderRows: function () {
            var self = this;
            var $rows = this._super();
            if (this.addCreateLine) {
                var last_element = $rows.slice(-1)[0];
                if (last_element[0].innerText === "Add a line" && (self.state.model === "ec.obstetrics.history")) {
                    var les = $rows.pop()
                    $rows.splice(0, 0, les)
                }
            }
            return $rows;
        },
    });
});