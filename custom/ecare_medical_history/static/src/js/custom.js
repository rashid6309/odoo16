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


odoo.define('ecare_medical_history.owl_test', function (require) {
"use strict";
   const AbstractField = require('web.AbstractFieldOwl');
   const fieldRegistry = require('web.field_registry_owl');
    const { registry } = require('@web/core/registry');
    const { useInputField } = require("@web/views/fields/input_field_hook");
    const { useService } = require("@web/core/utils/hooks");


    var time = require('web.time');
    var rpc = require('web.rpc');
    var translation = require('web.translation');
    var _t = translation._t;
    const { Component,useRef} = owl;
    const { CharField }  = require("@web/views/fields/char/char_field");

     class DomainSelectorTextField extends Component {

       setup(){
           super.setup();
           this.action = useService("action");
           this.input = useRef('inputdate')
           useInputField({ getValue: () => this.props.value || "", refName: "inputdate" });
           useInputField({ getValue: () => this.props.record.data || "", refName: "patient_data" });
       }


       async _onEditPatientProfile(){
       console.log(this.props.record.data.patient_id);
       var patient = this.props.record.data.patient_id;
            this.action.doActionButton({
                type: "object",
                resId: this.props.value[0],
                name: "action_open_patient_time_view",
                context: patient,
                resModel: "ec.patient.timeline",
                onClose: async () => {
                    await this.props.record.model.root.load();
                    this.props.record.model.notify();
                },
            });
        }

    }

    DomainSelectorTextField.template = "ecare_medical_history.FieldDateMultipleDate";
    registry.category("fields").add("banner_summary_widget", DomainSelectorTextField);
});


/** @odoo-module **/
