odoo.define('o_ecare_services_reporting.Dashboard', function (require) {
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
var EcareServicesReporting = AbstractAction.extend({
    contentTemplate:'EcareServicesReporting',

    events: {
            'click .report_type_btn': 'view_report',
            'click #print': 'print',
            'click #print_excel': 'print_excel',
            'click #search_button':'onChangeFilter',
            'click #close_duration_filter': 'close_duration_filter',
            'click #page':'changePage',
            'click #previous_page_btn': 'changePage',
            'click #next_page_btn': 'changePage',
        },

    init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['ReportingServicesCustom'];

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
        const schedule_id = document.getElementById("rescheduled_slot");

        if (schedule_id != null && localStorage['isReschedule'])
        {
        self.$el.html(QWeb.render("ReportingSwitchAppointment", {widget: self}));
        document.getElementsByClassName("o_main_navbar")[0].style.visibility="hidden";
        localStorage['reschedule_slot_id'] = schedule_id.innerText;
        }
        else
        {
        document.getElementsByClassName("o_main_navbar")[0].style.visibility="visible";
        self.$el.html(QWeb.render("ReportingServicesCustom", {widget: self}));
        }
    },

    on_reverse_breadcrumb: function() {
        var self = this;
        web_client.do_push_state({});
        this.fetch_data().then(function() {
            self.$('.o_ecare_services_reporting').empty();
            self.render_dashboards();
        });
    },

    print:function(e){
        var self = this;

        var payment_mode = document.getElementById('payment_mode').value;
        var invoice_type = document.getElementById('invoice_type').value;

        // Getting the product_id
        var product_id = self.getValueOfProduct("product_list")

        var date = $("#date_picker").datepicker().val();
        var date_end = $("#date_picker_end").datepicker().val();

        var print_report = rpc.query({
            model: 'ec.slot.reporting',
            method: 'print_services_report',
            args: [date, date_end, payment_mode, invoice_type, product_id],
        })
        .then(function(result) {
            return self.do_action(result)
        });

        return $.when(print_report);
    },
    print_excel:function(e){
        var self = this;

        var payment_mode = document.getElementById('payment_mode').value;
        var invoice_type = document.getElementById('invoice_type').value;

        // Getting the product_id
        var product_id = self.getValueOfProduct("product_list")

        var date = $("#date_picker").datepicker().val();

        var date_end = $("#date_picker_end").datepicker().val();
        var print_report = rpc.query({
            model: 'ec.slot.reporting',
            method: 'print_services_report_excel',
            args: [date, date_end, payment_mode, invoice_type, product_id],
        })
        .then(function(result) {
            return self.do_action(result)

        });

        return $.when(print_report);
    },
    onChangeFilter:function(e){
        var self = this;
        var payment_mode = document.getElementById('payment_mode').value;
        var invoice_type = document.getElementById('invoice_type').value;

        // Getting the product_id
        var product_id = self.getValueOfProduct("product_list")

        var services_date = $("#date_picker").datepicker().val();
        var services_date_end = $("#date_picker_end").datepicker().val();

         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "services_cash_report",
            args: [20,0, payment_mode, invoice_type, services_date, services_date_end, product_id],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
                 self.selected_product = res['selected_product'];
                 self.invoice_type = res['invoice_type'];
                 self.payment_methods = res['payment_methods']
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.summary_block = res['summary_block'];
                 self.date_picker_field = res['date_picker_field'];
                 self.date_picker_field_end = res['date_picker_field_end'];
                 localStorage['services_date'] = res['date_picker_field'];
                 self.selected_product_id = res['selected_product_id'];

                 localStorage['services_date_end'] = res['date_picker_field_end'];

                 self.$el.html(QWeb.render("ReportingServicesCustom", {widget: self}));

        });
         return $.when(def1);

    },
    getValueOfProduct: function(elementId){
        let product_id = document.getElementById(elementId);
        let selectedIndex = product_id.selectedIndex;
        if (selectedIndex > 0){ // If it is ID
            let selectedOptionAttribute = product_id.options[selectedIndex].attributes;
            product_id = selectedOptionAttribute.productid.value
        }else{ // Incase it is 0 it means All is selected so change it to All
            product_id = "All"
        }
        return product_id;

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

        // Getting the product_id
        var product_id = self.getValueOfProduct("product_list")


        var services_date = $("#date_picker").datepicker().val();
        var services_date_end = $("#date_picker_end").datepicker().val();

          var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "services_cash_report",
            args: [20,pageNo, payment_mode, invoice_type, services_date, services_date_end, product_id],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
                 self.payment_mode = res['payment_mode'];
                 self.product_list = res['product_list'];
                 self.invoice_type = res['invoice_type'];
                 self.payment_methods = res['payment_methods']
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.summary_block = res['summary_block'];
                 self.selected_product_id = res['selected_product_id'];
                 self.date_picker_field = res['date_picker_field'];
                 self.date_picker_field_end = res['date_picker_field_end'];
                 localStorage['services_date'] = res['date_picker_field'];
                 localStorage['services_date_end'] = res['date_picker_field_end'];

                 self.$el.html(QWeb.render("ReportingServicesCustom", {widget: self}));

        });
         return $.when(def1);
    }
    ,
    view_report:function(e){
                        var self = this;
                        if(e.currentTarget.attributes.report_type.nodeValue == "all_records"){
                            self.report_type = "all_records";
                        }
                        if(e.currentTarget.attributes.report_type.nodeValue == "summary"){
                                self.report_type = "summary";
                        }
                         self.$el.html(QWeb.render("ReportingServicesCustom", {widget: self}));
    },
    close_duration_filter: function (e){
        var self = this;
        self.duration = '';
        self.$el.html(QWeb.render("ReportingServicesCustom", {widget: self}));
    },

    fetch_data: function() {
        var self = this;
        var payment_mode = "All Modes";
        var invoice_type = "All Types";
        var product_id = "All";

        var services_date = localStorage['services_date'] ? localStorage['services_date'] : new Date().toISOString().split('T')[0];
        var services_date_end = localStorage['services_date_end'] ? localStorage['services_date_end'] : new Date().toISOString().split('T')[0];

        self.report_type = 'all_records';
        self.duration = "";

         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "services_cash_report",
            args: [20, 0, payment_mode, invoice_type, services_date, services_date_end, product_id],
        })
        .then(function (res) {
             self.notification = res['notification'];
             self.header = res['header'][0];
             self.data = res['data'];
             self.selected_product_id = res['selected_product_id'];
             self.payment_mode = res['payment_mode'];
             self.product_list = res['product_list'];
             self.selected_product = res['selected_product'];
             self.invoice_type = res['invoice_type'];
             self.payment_methods = res['payment_methods']
             self.total_pages = res['total_pages'];
             self.active_page = res['active_page'];
             self.summary_block = res['summary_block'];
             self.date_picker_field = res['date_picker_field'];
             self.date_picker_field_end = res['date_picker_field_end'];

             localStorage['services_date'] = res['date_picker_field'];
             localStorage['services_date_end'] = res['date_picker_field_end'];
        });
         return $.when(def1);

    },

});

core.action_registry.add('ecare_services_reporting', EcareServicesReporting);

return EcareServicesReporting;

});


