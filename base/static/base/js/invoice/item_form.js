$(document).ready(function () {

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

    //$('#button_save_item').click(function (event) {
    //    event.preventDefault();
    //    set_csrf_token();
    //
    //    var url = $('#item_form').attr('action');
    //    var load_url = $('#items_container').attr('data-url-load');
    //
    //    var data = $('#item_form').serialize();
    //    $.ajax({
    //        url: url, data: data, statusCode: {
    //            200: function (response) {
    //                console.log(load_url);
    //                $.get(load_url, '', function (response) {
    //                    $('#items_container').html(response);
    //                    $('#form_container').hide();
    //                });
    //            },
    //            400: function (response) {
    //                $('#form_container').html(response.responseText);
    //            },
    //            404: function () {
    //
    //            },
    //            500: function () {
    //
    //            }
    //        }, type: 'POST'
    //    })
    //});

    //$('.remove').click(function (event) {
    //    event.preventDefault();
    //    var url = $(this).attr('data-url');
    //    set_csrf_token();
    //    $.post(url, {}, function (response) {
    //        var url = '/proposal/'+ localStorage.getItem('proposalId') +'/items/list/';
    //
    //
    //
    //
    //    }
    //    );
    //});


     //Eliminar
    $('.remove').click(function (e) {


        //e.preventDefault();
        var $button = $(e.currentTarget) // Button that triggered the modal
       var url_delete = $(this).attr('data-url');

        var url_base = '/'+$.CustomDatatableFormObject.model_name+'/'+ localStorage.getItem('proposalId') +'/items/';

        swal({
                title: "Confirma que desea eliminar?",
                text: "Si elimina el elemento ya no podrá deshacer los cambios!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Aceptar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {
                if (isConfirm) {


                     set_csrf_token();


                    $.ajax({
                            url: url_delete,
                            type: "POST",
                            statusCode: {
                                200: function () {
                                    swal("Eliminado!", "Se ha eliminado correctamente el elemento seleccionado.", "success");
                                    $.ajax({
                                        url:url_base,
                                        success: function(data){
                                             $("#stepContainer2").html(data);
                                             console.debug(url_base);
                                        }
                                    });

                                },
                                405: function () {

                                },
                                500: function (response) {
                                    swal("Error!", "Ha existido un error al eliminar el elemento seleccionado", "error");
                                    console.log(response.responseText);

                                }
                            }
                        }
                    )
                } else {
                    swal("Cancelado", "No se ha realizado ninguna acción", "error");
                }
            });
    });



});
