$(document).ready(function () {

  $activeStep = -1;
  var current_url = $("#current_url").val();
    if (!localStorage.getItem('activeStep')) {
        localStorage.setItem('activeStep', 1);

        $.get(current_url, '', function (data) {
            $("#stepContainer1").append(data);
        });

    } else {
        $activeStep = localStorage.getItem('activeStep');

        switch ($activeStep) {
            case "1":
                $("li.event").addClass('active');

                $.get(current_url, '', function (data) {
                    $("#stepContainer1").append(data);
                });
                break;
            case "2":

                if ($("#items_cant").val() === "0") {
                    $(".btn-next").attr("disabled", "disabled").removeClass('btn-success');
                }

                $("li.event").removeClass('active').addClass('complete');
                $("li.items").addClass('active');
                $('.step-pane[data-step="1"]').toggleClass("hidden")
                $('.step-pane[data-step="2"]').toggleClass('active').toggleClass('hidden');

                $(".btn-prev").removeProp("disabled").addClass('btn-success');

                localStorage.getItem('proposalId');
                var items_url = '/proposal/' + localStorage.getItem('proposalId') + '/items';
                $.get(items_url, '', function (data) {
                    $('#stepContainer2').append(data);
                });
                break;
            case "3":

                step3Settings();
                break;
            default :
                defaultSettings();
                break;
        }

    }
    function defaultSettings() {
        localStorage.setItem('activeStep', 1);
        $("li.event").addClass('active');

        $.get(current_url, '', function (data) {
            $("#stepContainer1").append(data);
        });
    }

    function step3Settings() {
        $(".steps > li").not(".confirm").addClass('complete');
        $(".steps > li.confirm").addClass('active');

        $('.step-pane[data-step="1"]').addClass("hidden");
        $('.step-pane[data-step="2"]').addClass("hidden").removeClass('active');
        $('.step-pane[data-step="3"]').toggleClass('active').toggleClass('hidden');

        $('.btn-next > span').text("Finalizar");
        $('.btn-prev').removeProp('disabled').addClass('btn-success');

        var confirm_url = '/proposal/' + localStorage.getItem('proposalId');
        $.get(confirm_url, '', function (data) {
            $('#stepContainer3').append(data);
        });
    }


    $('.btn-next').click(function (event) {

        $activeStepLi = $("ul.steps li.active");
        //   var idStep = $activeStep.data('step');
        var url = $activeStepLi.data('url');
        var eventId = $activeStepLi.data('event-id');
        $activeStep = localStorage.getItem('activeStep');
        switch ($activeStep) {
            case "1":
                if (eventId == -1) {
                    var form_data = $("#eventForm").serialize();
                    set_csrf_token();
                    $.ajax({
                            url: current_url,
                            type: "POST",
                            data: form_data,
                            success: function (data, textStatus) {
                                localStorage.setItem('activeStep', 2);
                                localStorage.setItem('proposalId', data.proposal_id);

                                var proposal_id = data.proposal_id;
                                var items_url = '/proposal/' + proposal_id + '/items';
                                $.get(items_url, '', function (data) {
                                    $('#stepContainer2').append(data);
                                    $("#stepContainer1").empty().append(data.responseText);
                                });
                                /*Wizard*/
                                $("li.event").removeClass('active').addClass('complete');
                                $("li.items").addClass('active');
                                //$("ul.steps li.active").toggleClass('selected').toggleClass('active').addClass('complete');
                                $('ul.steps li[data-step="2"]').addClass('active');

                                $('.step-pane[data-step="1"]').toggleClass("hidden")
                                $('.step-pane[data-step="2"]').toggleClass('active').toggleClass('hidden');

                                $(".btn-prev").removeProp("disabled").addClass('btn-success');

                                /*Botones proposal/XXX/event/ */
                            },
                            error: function (data, txtStatus) {
                                $("#stepContainer1").empty().append(data.responseText);

                            }
                        }
                    )
                }
                else {
//                     $.ajax({
//                            url: url,
//                            success: function (data, textStatus) {
//                                $.get('/proposal//items/', '', function (data) {
//                                    $('#items').append(data);
//
//                                });
//                            }
//                        }
//                    )
                }
                break;

            case "2":

                $.ajax({
                        url: url + localStorage.getItem('proposalId'),
                        success: function (data, textStatus) {
                            localStorage.setItem('activeStep', 3);
                            //$('#stepContainer3').html(data);

                            localStorage.setItem('activeStep', 3);


                            step3Settings();
                        },
                        error: function (data, txtStatus) {
                            //$("#stepContainer1").empty().append(data.responseText);

                            alert("error");

                        }
                    }
                )
                break;

            case "3":
                toastr.success('Se ha creado correctamente el presupuesto');
                localStorage.setItem('activeStep', -1);

                    window.location.href = '/proposal/';
                //$('#stepContainer3').empty();
                // window.location.href('/proposal/');
                // /*Wizard*/
                // $("ul.steps li").removeClass('selected').removeClass('active').removeClass('complete');
                //defaultSettings();

                break;
        }


        //event.preventDefault();
        //$.ajax({
        //        url: $.CustomDatatableFormObject.get_url_edit(),
        //        success: function (data, textStatus) {
        //            $('.modal-body').append(data);
        //        }
        //    }
        //)
//AQUI
//        var url = $(this).attr('data-url');
//        $.get(url, '', function (data) {
//            $('#customer-form').append(data);
//            $('#add_client').show();
//            console.log($('#newCustomerForm'));
//        });
        //  $(this).hide();
    });


    $('.btn-prev').click(function (event) {

        $activeStepLi = $("ul.steps li.active");
        //   var idStep = $activeStep.data('step');
        var url = $activeStepLi.data('url');
        var eventId = $activeStepLi.data('event-id');
        $activeStep = localStorage.getItem('activeStep');

        switch ($activeStep) {


            case "2":



                var event_url = '/proposal/' +  localStorage.getItem('proposalId') + '/event/';

              //  $.get(event_url, '', function (data) {

//                    $('#stepContainer1').append(data);
//                    $("#stepContainer2").hide();
//                        $('.step-pane[data-step="1"]').toggleClass('active').toggleClass('hidden');
//                                $('.step-pane[data-step="2"]').toggleClass('active').toggleClass('hidden');


          //      });
              localStorage.setItem('activeStep', 1);
                 window.location.href = event_url;

                break;

            case "3":
                localStorage.setItem('activeStep', 2);


                break;
        }


        //event.preventDefault();
        //$.ajax({
        //        url: $.CustomDatatableFormObject.get_url_edit(),
        //        success: function (data, textStatus) {
        //            $('.modal-body').append(data);
        //        }
        //    }
        //)
//AQUI
//        var url = $(this).attr('data-url');
//        $.get(url, '', function (data) {
//            $('#customer-form').append(data);
//            $('#add_client').show();
//            console.log($('#newCustomerForm'));
//        });
        //  $(this).hide();
    });


    $('#load_client_form').click(function (event) {
        event.preventDefault();
        var url = $(this).attr('data-url');
        $.get(url, '', function (data) {
            $('#customer-form').append(data);
            $('#add_client').show();
        });
        $(this).hide();
    });

    function set_csrf_token() {
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    //alert(csrftoken);
                }
            }
        });
    }

    $('#add_client').click(function (event) {

//        event.preventDefault();
//        var url = $('#newCustomerForm').attr('action');
//
//        var data = $('#newCustomerForm').serialize();
//        console.log(url);
//        console.log(data);
//        set_csrf_token();
//        $.ajax({
//            url: url,
//            type: 'POST',
//            data: data,
//            statusCode: {
//                200: function (response) {
//                    $(this).hide();
//                    $('#customer-form').empty();
//                    $('#load_client_form').show();
//                    var url_reload = $('#add_client').attr('data-url')
//                    console.log(response.id);
//                    $.get(url_reload, {id: response.id}, function (data) {
//                        $('#customer_field').html(data);
//                    });
//                    $('#add_client').hide();
//                },
//                400: function (response) {
//
//                    $('#customer-form').empty();
//                    $('#customer-form').append(response.responseText);
//                }
//            }
//        });
        //$.post(url, data, function(response, status){
        //    console.log(response);
        //    console.log(status);
        //    if(status == 200){
        //
        //    }else if (status == 400){
        //
        //    }
        //})


    });

});
