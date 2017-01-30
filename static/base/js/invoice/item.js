/**
 * Created by amado on 18/11/16.
 */
$(document).ready(function(){

  //Eliminar
    $('.remove').click(function (e) {

        //e.preventDefault();
        var $button = $(e.currentTarget) // Button that triggered the modal
        var elem_id = $button.data('elem-id');
        $.CustomDatatableFormObject.model_id = elem_id;
        //console.debug($.CustomDatatableFormObject.get_url_delete());

        swal({
                title: "Confirma que desea eliminar?",
                text: "Si lo elimina ya no podrá deshacer los cambios!",
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


                    $.ajax({
                            url: $.CustomDatatableFormObject.get_url_delete(),
                            //url: '/proposal/delete/'+$.CustomDatatableFormObject.model_id+'/',
                            type: "POST",
                            statusCode: {
                                200: function () {
                                    swal("Eliminado!", "Se ha eliminado correctamente el elemento seleccionado.", "success");
                                    UpdateDataTable();
                                },
                                405: function () {

                                },
                                400: function (response) {
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

    function UpdateDataTable() {

        $.ajax({
            type: 'GET',
            url: $.CustomDatatableFormObject.get_url_base(),
            success: function (data) {
                $($.CustomDatatableFormObject.datatable_container).empty().append(data);
                //$("#tableContainer").empty().append(data);
                $($.CustomDatatableFormObject.datatable_id).dataTable();
                //$('#customers_table').dataTable();
            }
        });
    }

});

