odoo.define('ecare_medical_history.integer_widget_color', function (require) {
    "use strict";
const { registry } = require('@web/core/registry');
const {Field} = require('@web/views/fields/field');
var rpc = require('web.rpc');
const { Component, onWillUpdateProps, onMounted, useRef } = owl

class ConditionColorWidget extends Field {
//    static template = 'FloatToIntFieldTemplate'
   async setup() {
        super.setup();
        this.input = useRef('inputfloat');
        this.input_id = this.props.id;
        var labelName = this.props.name;
        var timeline_id = this.props.record.data.id;
            onMounted(() => {
//               $('label[for="' + labelName + '"]').css('color', 'red');
               this.checkFunction(labelName, timeline_id);
            });
            onWillUpdateProps(nextProps => {
              this.checkFunction(labelName, timeline_id);
            });



        console.log(this.props);
        console.log(timeline_id);
        console.log(this);
    }



   async checkFunction(labelName, timeline_id)
    {
        var redFieldNames = [
            'tubal_patency_test',
            'tubal_patency_test_dropdown',
            'uterine_tubal_anomalies',
            'male_semen_analysis',
            'counselling_multiple_birth',
            'counselling_failure_treatment',
            'counselling_lower_success_rate',
            'counselling_high_bmi',
            'diagnosis_cervical_incompetence',
            'menopause_sign_suspicion',
            'female_ot_ti_bmi'
        ];
        var blueFieldNames = [
        ];

        for (var i = 0; i < redFieldNames.length; i++) {
            await rpc.query({
            model: 'ec.repeat.consultation',
            method: 'get_field_data_condition',
            args: [redFieldNames[i], timeline_id],
            })
            .then(function(result) {
                if (result){
                 $('label[for="' + redFieldNames[i] + '"]').css('color', 'red');
                }
                else{
                $('label[for="' + redFieldNames[i] + '"]').css('color', 'black');
                }
            });

        }


    }
    onFloatToInt(ev){

     var divName = this.props.name;
     var targetDiv = $('div[name="' + divName + '"]');

//     console.log(elementId);
     $(targetDiv).css('color', 'red');
//     $(document).on('focusout', selector, function (e, selectorToPass) {
//            var elementId = "#" + e.target.id;
//            $(elementId).css('color', 'black');
//            if (limit2 != null) {
//                if (parseFloat(e.target.value) < limit || parseFloat(e.target.value) > limit2) {
//                    $(elementId).css('color', 'red');
//                }
//            } else {
//                if (parseFloat(e.target.value) < limit) {
//                    $(elementId).css('color', 'red');
//                }
//            }
//        });
//    console.log(this);
//        var inputValue = ev.target.value;
//        if (!isNaN(inputValue)){
//            var floatValue = parseFloat(inputValue);
//            var roundValue = Math.round(floatValue);
//            this.value = roundValue
//            this.props.update(inputValue);
//        }
    }
}
registry.category("fields").add("condition_color_widget", ConditionColorWidget);

});