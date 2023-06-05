odoo.define('o_ecare_appointment_reporting.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
const { loadBundle } = require("@web/core/assets");
var core = require('web.core');
var QWeb = core.qweb;
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var _t = core._t;
var session = require('web.session');
var web_client = require('web.web_client');
var abstractView = require('web.AbstractView');
var EcareAppointmentReporting = AbstractAction.extend({
    contentTemplate:'EcareAppointmentReporting',

    events: {
            'click #print': 'print',
            'click #print_excel': 'print_excel',
            'click #search_button':'onChangeFilter',
//            'change #invoice_type':'onChangeFilter',
            'click #close_duration_filter': 'close_duration_filter',
            'click #page':'changePage',
            'click #previous_page_btn': 'changePage',
            'click #next_page_btn': 'changePage',
        },

    init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['ReportingAppointmentCustom'];

    },


    willStart: function() {
        var self = this;
        return Promise.all([loadBundle(this), this._super()]).then(function() {

            return self.fetch_data();
        });
    },



    start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                var body = document.querySelector('body');
                body.classList.remove("o_web_client");
                self.render_dashboards();
            });
        },



    render_dashboards: function(){
        var self = this;
        self.$el.html(QWeb.render("ReportingAppointmentCustom", {widget: self}));
    },

    on_reverse_breadcrumb: function() {
        var self = this;
        web_client.do_push_state({});
        this.fetch_data().then(function() {
            self.$('.o_ecare_appointment_reporting').empty();
            self.render_dashboards();
        });
    },

    print: function(e){
                var self = this;

                var payment_mode = document.getElementById('payment_mode').value;
                var invoice_type = document.getElementById('invoice_type').value;
                var user_id = self.getValueOfElement("user_list");

                var date = $("#date_picker").datepicker().val();
                var date_end = $("#date_picker_end").datepicker().val();

                var print_report = rpc.query({
                    model: 'ec.slot.reporting',
                    method: 'print_cash_report',
                    args: [date, date_end, payment_mode, invoice_type, user_id],
            })
            .then(function(result) {
                return self.do_action(result)
            });

        return $.when(print_report);
    },

    print_excel: function(e){
                var self = this;

                var payment_mode = document.getElementById('payment_mode').value;
                var invoice_type = document.getElementById('invoice_type').value;
                var user_id = self.getValueOfElement("user_list");

                var payment_date = $("#date_picker").datepicker().val();
                var payment_date_end = $("#date_picker_end").datepicker().val();

                var print_report = rpc.query({
                model: 'ec.slot.reporting',
                method: 'print_cash_report_excel',
                args: [payment_date, payment_date_end, payment_mode, invoice_type, user_id],
            })
            .then(function(result) {
                return self.do_action(result)
            });

        return $.when(print_report);
    },
    getValueOfElement: function(elementId){
        let product_id = document.getElementById("user_list");
        let selectedIndex = product_id.selectedIndex;
        if (selectedIndex > 0){ // If it is ID
            let selectedOptionAttribute = product_id.options[selectedIndex].attributes;
            product_id = selectedOptionAttribute.userid.value
        }else{ // Incase it is 0 it means All is selected so change it to All
            product_id = "All"
        }
        return product_id;

    },
    onChangeFilter:function(e){
        var self = this;
        var payment_mode = document.getElementById('payment_mode').value;
        var invoice_type = document.getElementById('invoice_type').value;

        var user_id = self.getValueOfElement("user_list");

        var payment_date = $("#date_picker").datepicker().val();
        var payment_date_end = $("#date_picker_end").datepicker().val();
         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "cash_detail_report",
            args: [20,0, payment_mode, invoice_type, payment_date, payment_date_end, user_id],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
                 self.invoice_type = res['invoice_type'];
                 self.payment_methods = res['payment_methods']
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.user_list = res['users_list'];
                 self.date_picker_field = res['date_picker_field'];
                 self.date_picker_field_end = res['date_picker_field_end'];
                 self.summary_block = res['summary_block'];
                 localStorage['payment_date'] = res['date_picker_field'];
                 localStorage['payment_date_end'] = res['date_picker_field_end'];
                 self.selected_user_id = res['selected_user_id'];
                 self.$el.html(QWeb.render("ReportingAppointmentCustom", {widget: self}));

        });
         return $.when(def1);

    },
    changePage:function(e){
        if(e.currentTarget.id == 'page'){
            var pageNo = e.currentTarget.attributes.pageNo.nodeValue;
         }
         else if(e.currentTarget.id == 'next_page_btn'){
            var pageNo = parseInt(document.querySelector('a.activeButton').getAttribute('pageno')) + 1;
         }else if (e.currentTarget.id == 'previous_page_btn'){
            var pageNo = parseInt(document.querySelector('a.activeButton').getAttribute('pageno')) - 1;
         }

        var self = this;
        var payment_mode = document.getElementById('payment_mode').value;
        var invoice_type = document.getElementById('invoice_type').value;

        var user_id = self.getValueOfElement("user_list");

        var payment_date = $("#date_picker").datepicker().val();

        var payment_date_end = $("#date_picker_end").datepicker().val();

          var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "cash_detail_report",
            args: [20,pageNo, payment_mode, invoice_type, payment_date, payment_date_end, user_id],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
                 self.invoice_type = res['invoice_type'];
                 self.payment_methods = res['payment_methods']
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.summary_block = res['summary_block'];
                 self.date_picker_field = res['date_picker_field'];
                 self.date_picker_field_end = res['date_picker_field_end'];
                 localStorage['payment_date'] = res['date_picker_field'];
                 localStorage['payment_date_end'] = res['date_picker_field_end'];
                 self.user_list = res['users_list'];
                 self.selected_user_id = res['selected_user_id'];

                 self.$el.html(QWeb.render("ReportingAppointmentCustom", {widget: self}));
        });
         return $.when(def1);
    },
    close_duration_filter: function (e){
        var self = this;
        self.duration = '';
        self.$el.html(QWeb.render("ReportingAppointmentCustom", {widget: self}));
    },

                 onClickSlot: function (e){
                    var self = this;
//                    e.stopPropagation();
//                    e.preventDefault();
                if(e.currentTarget.attributes.class.nodeValue == 'booked'){
//                   return self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
                }
                else if(e.currentTarget.attributes.class.nodeValue == 'available'){
                    var sub_category = e.currentTarget.attributes.sub_category.nodeValue;
                    var category_id = e.currentTarget.attributes.category_id.nodeValue;
                    var start_time = e.currentTarget.attributes.start_time.nodeValue;
                    var end_time = e.currentTarget.attributes.end_time.nodeValue;
                    var date = e.currentTarget.attributes.date.nodeValue;
                    var options = {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                    };
                    this.do_action({
                            name: _t("New Appointments"),
                            type: 'ir.actions.act_window',
                            res_model: 'ec.booked.slot.record',
            //                'res_id': parseInt(slot),
                            view_mode: 'form',
                            views: [[false, 'form']],
                            target: 'new',
                            context: {
                            default_category: parseInt(category_id),
                            default_start: start_time,
                            default_stop: end_time,
                            default_date: date,
                            default_sub_category: parseInt(sub_category),
//                            default_date: parseInt(date),
                            },
                       }, {
                            on_close: function () {
                            self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("ReportingAppointmentCustom", {widget: self}));
                            });

                            }});
                       }
            },
    fetch_data: function() {
        var self = this;

        var payment_mode = "All Modes";
        var invoice_type = "All Types";
        var user_id = "All";

        self.report_type = 'all_records';
        self.duration = ""
        let payment_date = localStorage['payment_date'] ? localStorage['payment_date'] : new Date().toISOString().split('T')[0];
        let payment_date_end = localStorage['payment_date_end'] ? localStorage['payment_date_end'] : new Date().toISOString().split('T')[0];

         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "cash_detail_report",
            args: [20,0, payment_mode, invoice_type, payment_date, payment_date_end, user_id],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
                 self.invoice_type = res['invoice_type'];
                 self.payment_methods = res['payment_methods']
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.summary_block = res['summary_block'];
                 self.date_picker_field = res['date_picker_field'];
                 self.date_picker_field_end = res['date_picker_field_end'];
                 localStorage['payment_date'] = res['date_picker_field'];
                 localStorage['payment_date_end'] = res['date_picker_field_end'];
                 self.user_list = res['users_list'];
                 self.selected_user_id = res['selected_user_id'];

        });
         return $.when(def1);

    },

});

core.action_registry.add('ecare_appointment_reporting', EcareAppointmentReporting);
return EcareAppointmentReporting;

});


