odoo.define('ecare_medical_history.integer_widget_color', function (require) {
    "use strict";
const { registry } = require('@web/core/registry');
const {Field} = require('@web/views/fields/field');
const { Component, onMounted, useRef } = owl

class FloatToIntWidget extends Field {
//    static template = 'FloatToIntFieldTemplate'
    setup() {
        super.setup();
        this.input = useRef('inputfloat');
        this.input_id = this.props.id;
        var labelName = this.props.name;
            onMounted(() => {
               $('label[for="' + labelName + '"]').css('color', 'red');
            });



        console.log(this.props);
        console.log(this);
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
registry.category("fields").add("integer_widget", FloatToIntWidget);

});