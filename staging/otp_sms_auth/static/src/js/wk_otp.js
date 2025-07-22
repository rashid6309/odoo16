/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('otp_sms_auth.wk_otp', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');
    var x;
    $(document).ready(function () {
        $(".wk_login").on('change', 'input:radio[name="radio-login"]', function () {
            if ($(this).val() == 'radiemail') {
                $('.field-login').show();
                $('.field-mobile').hide();
            } else if ($(this).val() == 'radiomobile') {
                $('.field-mobile').show();
                $('.field-login').hide();
                $('#login').prop('required',false);
            }
        });

    });

    $("#login_next").click(function () {
        $(".wk_back_btn").show();
        $(".alert-danger").hide()
        var $radio_login = $('.mobile_login_container').find('input[name="radio-login"]:checked').val();
        var $login_val = $('.mobile_login_container').find('input[name="login"]').val();
        var $mobile_val = $('.mobile_login_container').find('input[name="mobile"]').val();
        var $error = $('.mobile_login_container').find('.wk_guest_login_error');
        $error.hide();
        var errors = false;
        if ($radio_login == 'radiemail') {
            if ($login_val == '') {
                errors = true;
                $error.attr("class", "alert alert-danger wk_guest_login_error");
                $error.html(_t(" Email is required field."));
                $error.show();
                $(".wk_back_btn").hide();
                return false;
            }

        } else if ($radio_login == 'radiomobile') {
            if ($mobile_val == '') {
                errors = true;
                $error.attr("class", "alert alert-danger wk_guest_login_error");
                $error.html(_t(" مطلوب إدخال رقم الجوال."));
                $error.show();
                $(".wk_back_btn").hide();
                return false;
            }
        }
        $(".mobile_login_container").hide();
        $(".pwd_otp_container").show();
    });

    function generateLoginOtp() {
        var $pwd_opt_error = $('.pwd_otp_container').find('.wk_guest_login_error');
        var $main_login_error = $(".main_login_container").find('.wk_guest_login_error');
        var $radio_login = $('.mobile_login_container').find('input[name="radio-login"]:checked').val();
        var $login_val = $('.mobile_login_container').find('input[name="login"]').val();
        var $mobile_val = $('.mobile_login_container').find('input[name="mobile"]').val();
        $("#otplogincounter").html("");
        $(".main_login_error").hide();

        ajax.jsonRpc("/send/otp", 'call', { 'email': $login_val, "loginOTP": 'loginOTP', 'mobile': $mobile_val, 'logintype': $radio_login })
            .then(function (data) {
                if (data) {
                    if (data.email) {
                        if (data.email.status == 1) {
                            $("#password").value = ''
                            $('.pwd_otp_container').hide();
                            $(".main_login_container").show();
                            $(".main_login_otp_container").show();
                            $(".password_container").hide();
                            $main_login_error.attr('class', 'alert alert-success wk_guest_login_error');
                            $main_login_error.html(_t(data.email.message));
                            $main_login_error.show();
                            $(".wk_multi_login").removeAttr("disabled");
                            var countDown = data.email.otp_time;
                            if (x){
                                clearInterval(x);
                            }
                            x = setInterval(function () {
                                countDown = countDown - 1;
                                $("#otplogincounter").html("ستنتهي صلاحية رمز التحقق في " + countDown + " ثانية.");
                                if (countDown < 0) {
                                    clearInterval(x);
                                    $("#otplogincounter").html("<a class='btn btn-link pull-right' id='wk_guest_login_resend' href='#'>إعادة إرسال رمز التحقق</a>");
                                    $(".wk_multi_login").attr("disabled", true);
                                    document.getElementById("wk_guest_login_resend").addEventListener("click", generateLoginOtp, false);
                                }
                            }, 1000);
                        }
                        else {
                            $pwd_opt_error.attr('class', 'alert alert-danger wk_guest_login_error');
                            $pwd_opt_error.html(_t(data.email.message));
                            $pwd_opt_error.show();
                        }
                    }
                }
            });
    }

    $(".wk_guest_login_resend").click(function () {
        generateLoginOtp();
    });

    $(".otp_option_next_btn").click(function (event) {
        $(".wk_back_btn").show();
        $(".alert-danger").hide()
        var $radio_otp = $('.pwd_otp_container').find('input[name=radio-otp]:checked').val();
        if ($radio_otp == 'radiopwd') {
            $(".main_login_container").show();
            $(".pwd_otp_container").hide();
            $(".main_login_otp_container").hide();
        }
        else {
            generateLoginOtp();
        }
    });
});
