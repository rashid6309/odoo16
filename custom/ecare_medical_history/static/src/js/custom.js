odoo.define('ecare_medical_history.FirstConsultation', function (require) {
'use strict';
const { registry } = require('@web/core/registry');
const { FormRenderer } = require('@web/views/form/form_renderer');
const { formView } = require('@web/views/form/form_view');
const Dialog = require('web.Dialog');
 var rpc = require('web.rpc');
class FirstConsultationFormController extends FormRenderer {
   setup() {
       super.setup();
       console.log(this.env.config.bannerRoute);
                var self = this;
               console.log(this.bannerRoute);
               const response = rpc.query({
                route: this.env.config.bannerRoute,
                params: [11],
            });

   }
   _MoreOptions(){
            console.log(this);
                   var dialog = new Dialog(null, {
                       title: "js class blog",
                       size: 'medium',
                       $content: $('<div/>', {
                           html: 'hai'
                       }),
                       buttons: [{
                           text: "Close",
                           close: true
                       }]
                   });
                   dialog.open();
   }
}

const PickingFormView = {
   ...formView,
   Renderer: FirstConsultationFormController,
};
registry.category("views").add("banner_summary_route", PickingFormView);

});

//odoo.define('ecare_medical_history.inject_summary', function (require) {
//    "use strict";
//
//    var core = require('web.core');
//    var session = require('web.session');
//    var Widget = require('web.Widget');
//
//    var _t = core._t;
//
//    var InjectSummary = Widget.extend({
//        start: function () {
//        alert('hello');
//            // Check if we are on a form view
//            if (session.model === 'ec.first.consultation' && session.view_type === 'form') {
//                // Retrieve the current form view's DOM element
//                var $formView = $('.o_form_view');
//
//                // Render and inject the global summary template
//                var $summaryTemplate = $(core.qweb.render('ecare_medical_history.EcSummaryBoardCustom'));
//                $formView.prepend($summaryTemplate);
//            }
//        },
//    });
//
//    core.action_registry.add('ecare_medical_history.inject_summary', InjectSummary);
//
//    return InjectSummary;
//});

//
//odoo.define('ecare_medical_history.custom_template_widget', function (require) {
//    "use strict";
//
//
//    var FormController = require('web.FormController');
//
//    FormController.include({
//        /**
//         * This method is called when the form view is initialized.
//         */
//        init: function (parent, model, renderer, params) {
//            this._super.apply(this, arguments);
//            alert("Custom JavaScript code executed on form load.");
//            // Check if the current form view matches the one you want to target
//            if (this.modelName === 'your_model' && this.viewType === 'form' && this.viewRef === 'your_module.your_form_view') {
//                // Your custom code here
//                console.log("Custom JavaScript code executed on form load.");
//            }
//        },
//    });
//});
//
//
//
//
//odoo.define('ecare_medical_history.custom_template_widget', function (require) {
//    "use strict";
//
//    var core = require('web.core');
//    var FormView = require('web.FormView');
//
//    var _t = core._t;
//
//    FormView.include({
//        load_record: function (record) {
//            this._super.apply(this, arguments);
//
//            // Check if you are on the Sale Order form view
//            if (this.model === 'sale.order' && this.viewType === 'form') {
//                // Render and insert the custom template using QWeb
//                var $customTemplate = $(core.qweb.render('your_module.CustomTemplate'));
//                this.$('.o_form_view').prepend($customTemplate);
//            }
//        },
//    });
//});
//
//
//odoo.define('ecare_medical_history.US_treeView', function (require) {
//    "use strict";
//
////    var field_registry = require('web.field_registry');
//    var Widget = require('web.Widget');
//    var AbstractField = require('web.AbstractField');
//    var core = require('web.core');
//    var qweb = core.qweb;
//    var registry = require('web.core.registry');
//
//    var USTreeView = Widget.extend({
//
//        init: function (parent, state, params) {
//        this._super(parent);
//        alert('hello');
//    },
//    _render: function () {
//        var self = this;
//        alert('hello');
//    },
//    });
//
//    registry.category("fields").add('US_treeView', USTreeView);
//    return USTreeView;
//});


//odoo.define('ecare_medical_history.SummeryController', function (require) {
//    "use strict";
//
//    var AbstractController = require('web.AbstractController');
//    var Context = require('web.Context');
//    return AbstractController.include({
//        /**
//         * @override
//         * @param {Widget} parent
//         * @param {DiagramModel} model
//         * @param {DiagramRenderer} renderer
//         * @param {Object} params
//         */
//        init: function (parent, model, renderer, params) {
//            this._super.apply(this, arguments);
//            alert("Custom");
//            this.summeryRoute = params.summeryRoute;
//        },
//        /**
//         * Renders the html provided by the route specified by the
//         * summeryRoute attribute on the controller (summery_route in the template).
//         * Renders it before the view output and add a css class 'o_has_banner' to it.
//         * There can be only one banner displayed at a time.
//         *
//         * If the banner contains stylesheet links or js files, they are moved to <head>
//         * (and will only be fetched once).
//         *
//         * Route example:
//         * @http.route('/module/hello', auth='user', type='json')
//         * def hello(self):
//         *     return {'html': '<h1>hello, world</h1>'}
//         *
//         * @private
//         * @returns {Deferred}
//         */
//        _renderSummery: function () {
//        alert("Custom");
//            if (this.summeryRoute !== undefined) {
//                var self = this;
//                var patient_id;
//                var evalContext = new Context(self.initialState.context).eval();
//                patient_id = evalContext.default_patient;
//                var hash = window.location.hash.replace('#', '');
//                hash = JSON.parse('{"' + decodeURI(hash.replace(/&/g, "\",\"").replace(/=/g, "\":\"")) + '"}')
//
//                if (patient_id === undefined) {
//                alert("Custom");
//                    if (hash.model === "ec.medical.patient") {
//                        patient_id = parseInt(hash.id);
//                    }
//                    else {
//
//                    }
//                    if (patient_id === undefined) {
//                        try {
//                            patient_id = self.initialState.data.patient.res_id;
//                        }
//                        catch (e) {
//                        }
//                    }
//
//                }
//
//
//                return this.dp
//                    .add(this._rpc({
//                        route: this.summeryRoute,
//                        params: {
//                            patient_id: patient_id === undefined ? false : patient_id,
//                            model_context: evalContext,
//                        }
//                    })
//                    )
//                    .then(function (response) {
//                        var $summery = $(response.html);
//                        var defs = [];
//                        $('link[rel="stylesheet"]', $summery).each(function (i, link) {
//                            defs.push(ajax.loadCSS(link.href));
//                            link.remove();
//                        });
//                        $('script[type="text/javascript"]', $summery).each(function (i, js) {
//                            defs.push(ajax.loadJS(js.src));
//                            js.remove();
//                        });
//                        return $.when.apply($, defs).then(function () {
//                            $("#patient_summery").remove();
//                            $('.o_group.o_inner_group.oe_button_box').css({ 'width': '100%', 'text-align': 'center' })
//                            $summery.insertAfter($("table.oe_button_box.o_inner_group"));
//                            self._$summery = $summery;
//                        });
//                    });
//            }
//            return $.when();
//        },
//
//        _update: function (params, options) {
//            this._super.apply(this, arguments)
//            this._renderSummery()
//            this._pushState();
//            return this._renderBanner();
//        },
//
//    });
//
//});
//
//odoo.define('ecare_medical_history.SummeryView', function (require) {
//    "use strict";
//    var AbstractView = require('web.AbstractView');
//    return AbstractView.include({
//        init: function (viewInfo, params) {
//        alert("Custom");
//            this._super.apply(this, arguments);
//            this.controllerParams.summeryRoute = this.arch.attrs.summery_route;
//        },
//    })
//});


/** @odoo-module **/
