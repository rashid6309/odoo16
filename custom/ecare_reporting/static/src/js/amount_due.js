odoo.define('o_ecare_amount_due_reporting.Dashboard', function (require) {
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
var EcareAmountDueReporting = AbstractAction.extend({
    contentTemplate:'EcareAmountDueReportingTemplate',

    events: {
            'click #print': 'print',
            'click #print_excel': 'print_excel',
            'click #search_button':'onChangeFilter',
//            'change #invoice_type':'onChangeFilter',
            'click #close_duration_filter': 'close_duration_filter',
            'click #page':'changePage',
        },

    init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['EcareAmountDueReporting'];

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
//                     body.classList.remove("o_web_client");
                self.render_dashboards();
            });
        },



    render_dashboards: function(){
        var self = this;
        self.$el.html(QWeb.render("EcareAmountDueReporting", {widget: self}));
    },

    on_reverse_breadcrumb: function() {
        var self = this;
        web_client.do_push_state({});
        this.fetch_data().then(function() {
            self.$('.o_ecare_amount_due_reporting').empty();
            self.render_dashboards();
        });
    },

    print:function(e){
                 var self = this;
                var due_payment_date = $("#date_picker").datepicker().val();
                var print_report = rpc.query({
                model: 'ec.slot.reporting',
                method: 'print_amount_due_report',
                args: [due_payment_date],
            })
            .then(function(result) {
            return self.do_action(result)

            });

        return $.when(print_report);
    },
    print_excel:function(e){
                 var self = this;
                 var due_payment_date = $("#date_picker").datepicker().val();
                var print_report = rpc.query({
                model: 'ec.slot.reporting',
                method: 'print_amount_due_report_excel',
                args: [due_payment_date],
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

         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "amount_due_cases",
            args: [50,0],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
//                 alert(self.payment_mode);
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.total_amount = res['total_amount'];
                 self.total_discount = res['total_discount'];
                 self.$el.html(QWeb.render("EcareAmountDueReporting", {widget: self}));

        });
         return $.when(def1);

    },
    changePage:function(e){
        var self = this;
        var pageNo = e.currentTarget.attributes.pageNo.nodeValue;
          var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "amount_due_cases",
            args: [50,0],
        })
        .then(function (res) {

                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
//                 alert(self.payment_mode);
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.total_amount = res['total_amount'];
                 self.total_discount = res['total_discount'];
                 self.$el.html(QWeb.render("EcareAmountDueReporting", {widget: self}));

        });
         return $.when(def1);
    },
    close_duration_filter: function (e){
        var self = this;
        self.duration = '';
        self.$el.html(QWeb.render("EcareAmountDueReporting", {widget: self}));
    },

    fetch_data: function() {
        var self = this;

        var payment_mode = "All Modes";
        var invoice_type = "All Types";

        self.report_type = 'all_records';
        self.duration = ""
         var def1 = self._rpc({
            model: "ec.slot.reporting",
            method: "amount_due_cases",
            args: [50,0],
        })
        .then(function (res) {
                 self.notification = res['notification'];
                 self.header = res['header'][0];
                 self.data = res['data'];
                 self.payment_mode = res['payment_mode'];
//                 alert(self.payment_mode);
                 self.total_pages = res['total_pages'];
                 self.active_page = res['active_page'];
                 self.total_amount = res['total_amount'];
                 self.total_discount = res['total_discount'];

        });
         return $.when(def1);

    },

});

core.action_registry.add('ecare_amount_due_reporting', EcareAmountDueReporting);
return EcareAmountDueReporting;

});


