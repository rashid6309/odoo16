/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('otp_auth.wk_otp_login', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');
    var x;

    $(".login_container_next_btn").click(function () {
        $(".wk_back_btn").show();
        $(".alert-danger").hide()
        var $login_val = $('.mobile_login_container').find('input[name="login"]').val();
        var $error = $('.mobile_login_container').find('.wk_guest_login_error');
        $error.hide();
        var errors = false;
        if ($login_val == '') {
            errors = true;
            $error.attr("class", "alert alert-danger wk_guest_login_error");
            $error.html(_t(" Email is required field."));
            $error.show();
            $(".wk_back_btn").hide();
            return false;
        }
        $(".mobile_login_container").hide();
        $(".pwd_otp_container").show();
    });

    $(".otp_option_next_btn").click(function () {
        $(".wk_back_btn").show();
        $(".alert-danger").hide()
        var $radio_otp = $('.pwd_otp_container').find('input[name=radio-otp]:checked').val();
        if ($radio_otp == 'radiopwd') {
            $(".main_login_container").show();
            $(".pwd_otp_container").hide();
            $(".main_login_otp_container").hide();
            $(".password_container").show();
        }
        else {
            if ($(".otp-inputbar").length >= 7) {

                $('.oe_login_form').css('max-width', '400px')
            }
            generateLoginOtp();

        }
    });

    $("#password").keyup(function () {
        if ($(this).val() == '') {
            $(".wk_multi_login").attr("disabled", "disabled");
        }
        else {
            $(".wk_multi_login").removeAttr("disabled");
        }
    });

    function generateLoginOtp() {
        var $pwd_opt_error = $('.pwd_otp_container').find('.wk_guest_login_error');
            var $main_login_error = $(".main_login_container").find('.wk_guest_login_error');
            var $login_val = $('.mobile_login_container').find('input[name="login"]').val();
            $("#otplogincounter").html("");
            $(".main_login_error").hide();
        if ($login_val){
            ajax.jsonRpc("/send/otp", 'call', { 'email': $login_val, "loginOTP": 'loginOTP' })
                .then(function (data) {
                    if (data) {
                        if (data.email) {
                            console.log(data)
                            if (data.email.status == 1) {
                                $("#password").value = ''
                                $('.pwd_otp_container').hide();
                                $(".main_login_container").show();
                                $(".main_login_otp_container").show();
                                $(".password_container").hide();
                                $("#passwologinrd").value = data.email
                                $main_login_error.attr('class', 'alert alert-success wk_guest_login_error');
                                $main_login_error.html(_t(data.email.message));
                                $main_login_error.show();
                                $(".wk_multi_login").removeAttr("disabled");
                                var countDown = data.email.otp_time;
                                console.log(countDown)
                                if (x) {
                                    clearInterval(x);
                                }
                                x = setInterval(function () {
                                    countDown = countDown - 1;
                                    $("#otplogincounter").html("OTP will expire in " + countDown + " seconds.");
                                    if (countDown < 0) {
                                        clearInterval(x);
                                        $("#otplogincounter").html("<a class='btn btn-link pull-right' id='wk_guest_login_resend' href='#'>Resend OTP</a>");
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
    }
    $(".wk_guest_login_resend").click(function () {
        generateLoginOtp();
    });

    $(".wk_back_btn").click(function () {
        $(".wk_guest_login_error").hide();
        if ($(".pwd_otp_container").css("display") == 'block') {
            $(".wk_back_btn").hide();
            $(".mobile_login_container").show();
            $(".main_login_container").hide();
            $(".pwd_otp_container").hide();
        }
        else if ($(".main_login_container").css("display") == 'block') {
            $(".pwd_otp_container").show();
            $(".main_login_container").hide();
            $(".mobile_login_container").hide();
        }
    });


    $(".wk_multi_login").click(function () {
        if ($(".main_login_otp_container").css("display") == 'block') {
            var temp = ''
            $(".otp-inputbar").each(function (index) {
                if ($(this).val() === 0) {
                    temp += "0"
                }
                temp += String($(this).val())
            });
            // CUSTOMIZATION ACC. to ARABIC
            var new_temp = temp.split("")
            temp = (new_temp.reverse()).join("")
            // END CUSTOMIZATION ACC. to ARABIC
            if ((temp.length) == $(".otp-inputbar").length) {
                $("#password").val(parseInt(temp))
            }
        }
    });

    $(".otp-inputbar").keypress(function (e) {
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
            return false;
        }
    });
    $(".otp-inputbar").on("keyup keypress", function (e) {
        if ($(this).val()) {
          // $(this).next().focus(); --origional
          // CUSTOMIZATION ACC. to ARABIC
          $(this).prev().focus();
          // END CUSTOMIZATION ACC. to ARABIC
        }
        var KeyID = e.keyCode;
        switch (KeyID) {
            case 8:
                $(this).val("");
                // $(this).prev().focus(); ---origional
               // CUSTOMIZATION ACC. to ARABIC
                $(this).next().focus();
                // END CUSTOMIZATION ACC. to ARABIC
                break;
            case 46:
                $(this).val("");
                $(this).prev().focus();
                break;
            default:
                break;
        }
    });
});
