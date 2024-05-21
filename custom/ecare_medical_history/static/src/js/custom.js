// If it is not used till production then remove this widget "FirstConsultation" //
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
        _MoreOptions() {
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


odoo.define('ecare_medical_history.patient_banner', function (require) {
    "use strict";
    // const AbstractField = require('web.AbstractFieldOwl');
    // const fieldRegistry = require('web.field_registry_owl');
    const { registry } = require('@web/core/registry');
    const { useInputField } = require("@web/views/fields/input_field_hook");
    const { useService } = require("@web/core/utils/hooks");
    // var time = require('web.time');
    var rpc = require('web.rpc');
    const Dialog = require('web.Dialog');
    const { onWillStart } = owl;

    // var translation = require('web.translation');
    // var _t = translation._t;
    // const { CharField }  = require("@web/views/fields/char/char_field");

    const { Component, useRef } = owl;

    class PatientBanner extends Component {
        setup() {
            super.setup();
            this.action = useService("action");

            onWillStart(async () => {
                await this._prepare_banner_data_values()
            });

            // This will be required for mapping inputs
//            this.input = useRef('inputdate')
//            useInputField({ getValue: () => this.props.value || "", refName: "inputdate" });
//            useInputField({ getValue: () => this.props.record.data || "", refName: "patient_data" });
        }


        async _prepare_banner_data_values(){
            var self = this;

            let patient_id = this.props.value[0];
            await rpc.query({
                model: 'ec.medical.patient',
                method: 'get_banner_data_values',
                args: [patient_id],
            })
            .then(function(result) {
                self.data_values = result;
            });
        }

        async _onEditPatientProfile() {
        var self = this;
        await this.props.record.save().then(function(result) {
            console.log(result);
           const errorSpan = document.querySelector('span.text-danger.small.ms-2');
            if (!result) {

                // Handle the scenario where the error span exists
                // For example, display an error message to the user
                console.error("Error: Unable to save. Please correct the errors.");
                return;
            }
            else{
            self.action.doActionButton({
                type: "object",
                resId: self.props.value[0],
                name: "action_open_patient_time_view",
                context: self.props.value,
                resModel: "ec.patient.timeline",
                onClose: async () => {
                    await self.props.record.model.root.load();
                    self.props.record.model.notify();
                },
            });

            }
            });
        }

//        async _onEndPatientTreatment() {
//        var self = this;
//        await this.props.record.save().then(function(result) {
//            console.log(result);
//           const errorSpan = document.querySelector('span.text-danger.small.ms-2');
//            if (!result) {
//
//                // Handle the scenario where the error span exists
//                // For example, display an error message to the user
//                console.error("Error: Unable to save. Please correct the errors.");
//                return;
//            }
//            else{
//            self.action.doActionButton({
//                type: "object",
//                resId: self.props.value[0],
//                name: "action_end_patient_treatment",
//                context: self.props.value,
//                resModel: "ec.patient.timeline",
//                doActionButton: async () => {
//                    await self.props.record.model.root.load();
//                    self.props.record.model.notify();
//                },
//            });
//
//            }
//            });
//        }

        async _onEditPatientSemen() {
        await this.props.record.save();
            this.action.doActionButton({
                type: "object",
                resId: this.props.value[0],
                name: "action_open_patient_semen_view",
                context: this.props.value,
                resModel: "ec.patient.timeline",
                onClose: async () => {
                    await this.props.record.model.root.load();
                    this.props.record.model.notify();
                },
            });
        }

        async _onEditPatientTimeline() {
        var self = this;
        await this.props.record.save().then(function(result) {
           console.log(result);
           const errorSpan = document.querySelector('span.text-danger.small.ms-2');
           if (!result) {

                // Handle the scenario where the error span exists
                // For example, display an error message to the user
                console.error("Error: Unable to save. Please correct the errors.");
                return;
            }
            else{
                self.action.doActionButton({
                type: "object",
                resId: self.props.value[0],
                name: "action_open_patient_timeline_view",
                context: self.props.value,
                resModel: "ec.patient.timeline",
                onClose: async () => {
                    await self.props.record.model.root.load();
                    self.props.record.model.notify();
                   },
            });

            }
            });
        }

    }

    PatientBanner.template = "ecare_medical_history.FieldDateMultipleDate";
    registry.category("fields").add("banner_summary_widget", PatientBanner);
});


/** @odoo-module **/
