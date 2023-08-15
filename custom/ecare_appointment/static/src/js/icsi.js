odoo.define('o_ecare_appointment_dashboard.Dashboard', function (require) {
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
var EcareAppointmentDashboard = AbstractAction.extend({
    contentTemplate:'EcareAppointmentDashboard',

    events: {
             'change #date_picker': 'date_picker_function',
             'click .create_new_appointment': 'create_new_appointment',
             'click .edit_appointment': 'edit_appointment',
             'click .shift_appointments_slot': 'shift_appointments_slot',
             'click #slotDetails ':'onClickSlot',
             'click #switchSlotDetails':'onClickSwitchSlot',
             'click #cancel ':'onCancel',
             'click #switch ':'onSwitch',
             'click #invoice':'createInvoice',
             'click #primary_category' : 'onClickPrimaryCategory',
             'click #category ':'onClickCategory',
             'click #slideRight' : 'onSlideRight',
             'click #slideLeft' : 'onSlideLeft',
             'click #dateLeft' : 'decreaseDate',
             'click #dateRight' : 'increaseDate',
             'click #today_date' : 'today_date_function',
             'click #print_slot_report' : 'print_slot_report',
             'click #history' :  'history_function',
             'click #cancel_appointment' : 'cancel_appointment',
             'click #block_slot' : 'block_slot',
             'click #show_patient_profile': 'show_patient_profile',


        },

    init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['DashboardAppointmentCustom'];
        this.today_sale = [];

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
                body.classList.add("o_web_client")
                self.render_dashboards();
            });
        },



    render_dashboards: function(){
        var self = this;
        let schedule_id = document.getElementById("rescheduled_slot");

        if (schedule_id != null && localStorage['isReschedule'])
        {
            self.$el.html(QWeb.render("DashboardSwitchAppointment", {widget: self}));
            document.getElementsByClassName("o_main_navbar")[0].style.visibility="hidden";
            localStorage['reschedule_slot_id'] = schedule_id.innerText;
        }
        else
        {
            document.getElementsByClassName("o_main_navbar")[0].style.visibility="visible";
            self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
        }
    },

    on_reverse_breadcrumb: function() {
        var self = this;
        web_client.do_push_state({});
        this.fetch_data().then(function() {
            self.$('.o_ecare_appointment_dashboard').empty();
            self.render_dashboards();
        });
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
                    var configurator_id = document.getElementById("configurator_id").value;
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
                            default_configurator: parseInt(configurator_id),
//                            default_date: parseInt(date),
                            },
                       }, {
                            on_close: function () {
                            self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });

                            }});
                       }
            },
          cancel_appointment: function (e){
                    var self = this;
                    e.stopPropagation();
                    e.preventDefault();

                       
                        var slot_id = e.currentTarget.attributes.booked_slot_id.nodeValue;

                        var update_slot_record = rpc.query({
                                model: 'ec.booked.slot.record',
                                method: 'cancel_booking',
                                args: [parseInt(slot_id)],
                            })
                            .then(function(result) {
                            self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });

                            });

                                return $.when(update_slot_record);



            },
            block_slot: function (e){
                var self = this;
                e.stopPropagation();
                e.preventDefault();
                var sub_category = e.currentTarget.attributes.sub_category.nodeValue;
                var category_id = e.currentTarget.attributes.category_id.nodeValue;
                var start_time = e.currentTarget.attributes.start_time.nodeValue;
                var end_time = e.currentTarget.attributes.end_time.nodeValue;
                var date = e.currentTarget.attributes.date.nodeValue;


                rpc.query({
                    model: 'ec.booked.slot.record',
                    method: 'get_block_slot_form_view_id',
                    args: [],
                })
                .then(function(result) {
                    self.do_action({
                        name: _t("Block Appointment"),
                        type: 'ir.actions.act_window',
                        res_model: 'ec.booked.slot.record',
                        view_mode: 'form',
                        views: [[result, 'form']],
                        target: 'new',
                         context: {
                            default_category: parseInt(category_id),
                            default_start: start_time,
                            default_stop: end_time,
                            default_date: date,
                            default_sub_category: parseInt(sub_category),
                            default_state: 'Blocked'
                            },
                        },{
                            on_close: function () {
                            self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });

                            }})
                });




            },
          onClickSwitchSlot: function (e){

                    var self = this;
                    e.stopPropagation();
                    e.preventDefault();

                        if (confirm('Are you sure, you want to switch the slot here?')) {

                            if (localStorage['reschedule_slot_id'] != null && localStorage['reschedule_slot_id'] !='' && localStorage['reschedule_slot_id'] != undefined)
                                {
                                     var booked_slot_id = localStorage['reschedule_slot_id']


                                }else{
                                     var booked_slot_id = localStorage['booked_slot_id'];

                                }

                        var sub_category = e.currentTarget.attributes.sub_category.nodeValue;
                        var category_id = e.currentTarget.attributes.category_id.nodeValue;
                        var start_time = e.currentTarget.attributes.start_time.nodeValue;
                        var end_time = e.currentTarget.attributes.end_time.nodeValue;
                        var date = e.currentTarget.attributes.date.nodeValue;
                        var configurator_id = document.getElementById("configurator_id").value;

                        var update_slot_record = rpc.query({
                                model: 'ec.booked.slot.record',
                                method: 'switch_slot_record',
                                args: [parseInt(booked_slot_id.replace(",","")),start_time, end_time, date, parseInt(category_id), parseInt(sub_category), parseInt(configurator_id)],
                            })
                            .then(function(result) {
                            self.fetch_data().then(function(res){
                                  localStorage.removeItem("booked_slot_id");
                                  localStorage.removeItem("reschedule_slot_id");
                                  localStorage.removeItem("isReschedule");
                                  self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });

                            });

                                return $.when(update_slot_record);
                        } else {
                        }


            },
                 onSwitch: function (e){
                    var self = this;
                    document.getElementsByClassName("o_main_navbar")[0].style.visibility="hidden";
                    var slot_id = e.currentTarget.attributes.booked_slot_id.nodeValue;
                    localStorage['booked_slot_id'] = slot_id;
                   return self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
            },
                 createInvoice: function (e){
                    var self = this;
                    let partner_id = e.currentTarget.attributes.partner_id.nodeValue;
                    let sub_category_id = e.currentTarget.attributes.sub_category_id.nodeValue;
                    var options = {
                        on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                    };
//                    console.log(self)
                    this.do_action({
                        name: _t("Create Invoice"),
                        type: 'ir.actions.act_window',
                        res_model: 'account.move',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'current',
                        context: {
                            default_move_type: 'out_invoice',
                            default_partner_id: parseInt(partner_id),
                            default_tertiary_category_id: parseInt(sub_category_id),
                        },
                    }, options)

            },

            onSlideLeft: function (ev){
                     var self = this;
                     ev.preventDefault();
                    document.getElementById('container_slider').scrollLeft -= 20;
            },
            onSlideRight: function (ev){
                   var self = this;
                   ev.preventDefault();
                    document.getElementById('container_slider').scrollLeft += 20;
            },

            decreaseDate: function (ev){
                    var self = this;
                   let _date = document.getElementById('date_picker').value
                   var datatoday = new Date(_date);
                    var datatodays = datatoday.setDate(new Date(datatoday).getDate() - 1);
                    var todate = new Date(datatodays);
                    document.getElementById('date_picker').value = todate.toISOString().split('T')[0];
                     var active_parent_category_id = self.primaryActiveId;
                    var self = this;
                    var active_category_id = self.activeId;

                    var date = $("#date_picker").datepicker().val();



                    var update_table = rpc.query({
                            model: 'ec.slot.category',
                            method: 'get_slots_record_category_day_data',
                            args: [date, parseInt(active_category_id), parseInt(active_parent_category_id) ],
                        })
                        .then(function(result) {

                                 self.notification = result.notification;

                                      self.day_name = result.day_name;
                                      self.configurator_id = result['configurator_id'];
                                      self.appointment_categories = result['appointment_categories'];
                                      self.appointment_sub_categories = result['appointment_sub_categories'];
                                      self.slot_record_list = result['slot_record_list'];
                                      self.date_picker_field = result['date_picker_field'];
                                      localStorage['local_date'] =  result['date_picker_field'];
                                      self.activeId = result['active_category_id'];
                                      self.primaryActiveId = result['active_parent_category_id'];
                                      localStorage['local_activeId'] =  result['active_category_id'];
                                      localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                                      const schedule_id = document.getElementById("rescheduled_slot");
                                    if(localStorage['booked_slot_id'] || localStorage['reschedule_slot_id']){
                                        self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
                                    }else{
                                    self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));

                                    }



                        });

                    return $.when(update_table);



            },
            today_date_function:function(ev){
              var self = this;
               ev.stopPropagation();
               ev.preventDefault();
               var datatoday = new Date();
                var date = datatoday.toISOString().split('T')[0];
                document.getElementById('date_picker').value = datatoday.toISOString().split('T')[0];
                var active_category_id = self.activeId;
                 var active_parent_category_id = self.primaryActiveId;

            var update_table = rpc.query({
                model: 'ec.slot.category',
                method: 'get_slots_record_category_day_data',
                args: [date, parseInt(active_category_id) , parseInt(active_parent_category_id)],
            })
            .then(function(result) {

                            self.notification = result.notification;
                             self.day_name = result.day_name;
                             self.configurator_id = result['configurator_id'];
                            self.appointment_categories = result['appointment_categories'];
                            self.appointment_sub_categories = result['appointment_sub_categories'];
                            self.slot_record_list = result['slot_record_list'];
                            self.date_picker_field = result['date_picker_field'];
                            self.activeId = result['active_category_id'];
                            self.primaryActiveId = result['active_parent_category_id'];
                            localStorage['local_date'] =  result['date_picker_field'];
                            localStorage['local_activeId'] = result['active_category_id'];
                            localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                             if(localStorage['booked_slot_id'] || localStorage['reschedule_slot_id']){
                                        self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
                                    }else{
                                    self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));

                                    }

            });

        return $.when(update_table);

            }
            ,
            increaseDate: function (ev){
                    var self = this;
                    let _date = document.getElementById('date_picker').value;
                    var active_category_id = self.activeId;
                     var active_parent_category_id = self.primaryActiveId;
                   var datatoday = new Date(_date);
                    var datatodays = datatoday.setDate(new Date(datatoday).getDate() + 1);
                    var todate = new Date(datatodays);
                    document.getElementById('date_picker').value = todate.toISOString().split('T')[0];
                    var date = $("#date_picker").datepicker().val();

                    var update_table = rpc.query({
                            model: 'ec.slot.category',
                            method: 'get_slots_record_category_day_data',
                            args: [date, parseInt(active_category_id) , parseInt(active_parent_category_id)],
                        })
                        .then(function(result) {

                                    self.notification = result.notification;
                                    self.day_name = result.day_name;
                                    self.configurator_id = result['configurator_id'];
                                    self.appointment_categories = result['appointment_categories'];
                                    self.appointment_sub_categories = result['appointment_sub_categories'];
                                    self.slot_record_list = result['slot_record_list'];
                                    self.date_picker_field = result['date_picker_field'];
                                    self.activeId = result['active_category_id'];
                                    self.primaryActiveId = result['active_parent_category_id'];
                                    localStorage['local_date'] =  result['date_picker_field'];
                                    localStorage['local_activeId'] =  result['active_category_id'];
                                    localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                                    if(localStorage['booked_slot_id'] || localStorage['reschedule_slot_id']){
                                        self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
                                    }else{
                                    self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));

                                    }
                        });

                    return $.when(update_table);
            },
             onCancel: function (e){
                    var self = this;
                    document.getElementsByClassName("o_main_navbar")[0].style.visibility="visible";
                    e.stopPropagation();
                    e.preventDefault();
                    localStorage.removeItem("booked_slot_id");
                    localStorage.removeItem("reschedule_slot_id");
                    localStorage.removeItem("isReschedule");

            return self.$el.html(QWeb.render('DashboardAppointmentCustom', {widget: self}));

            },

        total_appointments_show: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Appointments"),
            type: 'ir.actions.act_window',
            res_model: 'ec.booked.slot.record',
            view_mode: 'kanban,form',
            views: [[false, 'list'],[false, 'form']],
            target: 'current'
        }, options)
    },
        total_appointments_show_new: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Appointments"),
            type: 'ir.actions.act_window',
            res_model: 'ec.booked.slot.record',
            view_mode: 'kanban,form',
            views: [[false, 'list'],[false, 'form']],
            target: 'new'
        }, options)
    },

        //Switch Appointment
        shift_appointments_slot: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Switch Appointment"),
            type: 'ir.actions.client',
            tag: 'ecare_appointment_dashboard',
            target: 'new'
        }, options)
    },


    //New Appointment
        create_new_appointment: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Projects"),
            type: 'ir.actions.act_window',
            res_model: 'ec.booked.slot.record',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
        }, options)
    },


//    slideRight: function(ev) {
//        var self = this;
//        ev.preventDefault();
//
////        alert("Hello");
//        document.getElementById('containerSlide3').scrollLeft += 20;
//
//
//    },
    date_picker_function: function(ev) {
        var self = this;
        ev.stopPropagation();
        ev.preventDefault();
        var posted = 1;
        var active_category_id = self.activeId;
        var active_parent_category_id = self.primaryActiveId;


        var date = $("#date_picker").datepicker().val();

        var update_table = rpc.query({
                model: 'ec.slot.category',
                method: 'get_slots_record_category_day_data',
                args: [date, parseInt(active_category_id) , parseInt(active_parent_category_id)],
            })
            .then(function(result) {

                            self.notification = result.notification;
                             self.day_name = result.day_name;
                             self.configurator_id = result['configurator_id'];
                             self.appointment_categories = result['appointment_categories'];
                             self.appointment_sub_categories = result['appointment_sub_categories'];
                             self.slot_record_list = result['slot_record_list'];
                             self.date_picker_field = result['date_picker_field'];
                             localStorage['local_date'] =  result['date_picker_field'];
                             localStorage['local_activeId'] =  result['active_category_id'];
                             localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                             self.activeId = result['active_category_id'];
                             self.primaryActiveId = result['active_parent_category_id'];
                              if(localStorage['booked_slot_id'] || localStorage['reschedule_slot_id']){
                                        self.$el.html(QWeb.render('DashboardSwitchAppointment', {widget: self}));
                                    }else{
                                    self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));

                                    }
            });

        return $.when(update_table);
    },


    //Edit Appointment
        edit_appointment: function(e) {
        var self = this;

        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        var appointment_id = e.currentTarget.attributes.value.nodeValue;
        this.do_action({
            name: _t("Edit Slot"),
            type: 'ir.actions.act_window',
            res_model: 'ec.booked.slot.record',
            res_id: parseInt(appointment_id),
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
        }, {
            on_close: function () {
            self.fetch_data().then(function(res){

                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });

            }});
    },
       history_function: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        var appointment_id = e.currentTarget.attributes.value.nodeValue;
        this.do_action({
            name: _t("Edit Slot"),
            type: 'ir.actions.act_window',
            res_model: 'ec.booked.slot.record',
            res_id: parseInt(appointment_id),
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'current'
        }, {
            on_close: function () {
            self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });
            }
        });
    },
    appointment_unlink_btn: function(ev) {
        ev.preventDefault();
        var appointment_id = ev.target.value;
        rpc.query({
                model: 'ec.booked.slot.record',
                method: 'unlink_record',
                args: [appointment_id],

            })
            .then(function(result) {
                self.fetch_data().then(function(res){
                                 self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                            });
            })
    },
    print_slot_report: function(ev) {
        var self = this;
        var day_name = self.day_name;

        var appointment_sub_categories = self.appointment_sub_categories;
        var slot_record_list = self.slot_record_list;
        var date_picker_field = self.date_picker_field;
        var activeId = self.activeId;
        var local_date = localStorage['local_date'];
        var local_activeId = localStorage['local_activeId'];

        ev.stopPropagation();
        ev.preventDefault();

        var print_report = rpc.query({
                model: 'ec.slot.reporting',
                method: 'print_slot_report',
                args: [day_name, appointment_sub_categories, slot_record_list, date_picker_field, local_activeId],
            })
            .then(function(result) {
            return self.do_action(result)
            });

        return $.when(print_report);
    },
        onClickPrimaryCategory: function(ev) {
        ev.preventDefault();
        var self = this;
        var primary_category_id = ev.target.value;
        let local_activeId = localStorage['local_activeId'] ? localStorage['local_activeId'] : null
         let local_date = localStorage['local_date'] ? localStorage['local_date'] : new Date().toISOString().split('T')[0];
        rpc.query({
                model: 'ec.slot.category',
                method: 'get_slots_record_category_day_data',
                args: [local_date,null,parseInt(primary_category_id)],

            })
            .then(function(result) {
                self.notification = result.notification;
                self.day_name = result.day_name;
                self.configurator_id = result['configurator_id'];
                self.appointment_categories = result['appointment_categories'];
                self.appointment_sub_categories = result['appointment_sub_categories'];
                self.slot_record_list = result['slot_record_list'];
                self.activeId = result['active_category_id'];
                self.primaryActiveId = result['active_parent_category_id'];
                self.date_picker_field = result['date_picker_field'];
                localStorage['local_date'] =  result['date_picker_field'];
                localStorage['local_activeId'] = result['active_category_id'];
                localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
            })
    },

 onClickCategory: function(ev) {
        ev.preventDefault();
        var self = this;
        var primary_category_id = self.primaryActiveId;
        var category_id = ev.target.value;
        let local_activeId = localStorage['local_activeId'] ? localStorage['local_activeId'] : null
         let local_date = localStorage['local_date'] ? localStorage['local_date'] : new Date().toISOString().split('T')[0];
        rpc.query({
                model: 'ec.slot.category',
                method: 'get_slots_record_category_day_data',
                args: [local_date,parseInt(category_id),parseInt(primary_category_id)],

            })
            .then(function(result) {
                self.notification = result.notification;
                self.day_name = result.day_name;
                self.configurator_id = result['configurator_id'];
                self.appointment_categories = result['appointment_categories'];
                self.appointment_sub_categories = result['appointment_sub_categories'];
                self.slot_record_list = result['slot_record_list'];
                self.activeId = result['active_category_id'];
                self.primaryActiveId = result['active_parent_category_id'];
                self.date_picker_field = result['date_picker_field'];
                localStorage['local_date'] =  result['date_picker_field'];
                localStorage['local_activeId'] = result['active_category_id'];
                localStorage['local_primaryActiveId']=result['active_parent_category_id'];
                self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
            })
    },

    fetch_data: function() {
        var self = this;
         const reschedule_category_id = document.getElementById("rescheduled_slot_category");
         let reschedule_category = reschedule_category_id ? reschedule_category_id.innerText : null;
         let activeId_from_localStorage = localStorage['local_activeId'] ? localStorage['local_activeId'] : 0;
         document.getElementsByClassName("o_main_navbar")[0].style.visibility="visible";
        let local_activeId = (reschedule_category_id && !reschedule_category == '') ? reschedule_category_id.innerText : activeId_from_localStorage;
        let local_primaryActiveId = localStorage['local_primaryActiveId'] ? localStorage['local_primaryActiveId']: 0;
            localStorage.removeItem("booked_slot_id");
            localStorage.removeItem("reschedule_slot_id");
            let local_date = localStorage['local_date'] ? localStorage['local_date'] : new Date().toISOString().split('T')[0];

        var def1 = self._rpc({
            model: "ec.slot.category",
            method: "get_slots_record_category_day_data",
            args: [local_date,parseInt(local_activeId),parseInt(local_primaryActiveId)],
        })
        .then(function (res) {
//                    console.log("Uncomment this if required to see the fetched data");
//                    console.log(res);
                    self.notification = res['notification'];
                    self.day_name = res['day_name'];
                    self.primary_categories = res['primary_categories'];
                    self.appointment_categories = res['appointment_categories'];
                    self.activeId = res['active_category_id'];
                    self.primaryActiveId = res['active_parent_category_id'];
                    self.configurator_id = res['configurator_id'];
                    self.appointment_sub_categories = res['appointment_sub_categories'];
                    self.slot_record_list = res['slot_record_list'];
                    self.date_picker_field = res['date_picker_field'];
                    localStorage['local_activeId'] = res['active_category_id'];
                    localStorage['local_primaryActiveId']=res['active_parent_category_id'];
                    localStorage['local_date'] = res['date_picker_field'];

        });

        return $.when(def1);
    },

    show_patient_profile: function(e){
        var self = this;
        var patient_id = parseInt(e.currentTarget.attributes.patient_id.nodeValue);

        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
              name: _t("Edit Profile"),
              type: 'ir.actions.act_window',
              res_model: 'ec.medical.patient',
              res_id: patient_id,
              view_mode: 'form',
              view_id: ('ecare_core.ec_patient_form_view').id,
              views: [[false, 'form']],
              target: 'new',
        },{
            on_close: function() {
            self.fetch_data().then(function(res) {
                self.$el.html(QWeb.render("DashboardAppointmentCustom", {widget: self}));
                });
            }
        });
    }

});

core.action_registry.add('ecare_appointment_dashboard', EcareAppointmentDashboard);

return EcareAppointmentDashboard;

});


