/**
 * Created by Hector on 18/11/2016.
 */
$(document).ready(function () {
    //Adicionar / Editar

    $('.remove-menu').click(function (e) {
        //{#            e.preventDefault();#}
        var $button = $(e.currentTarget) // Button that triggered the modal

        var remove_url = $button.data('url-remove');
        var url = $button.data('url');
        var container_id = $button.data('container');
        $container = $("#"+container_id);

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
                            url: remove_url,
                            type: "GET",
                            statusCode: {
                                200: function (response) {
                                    swal("Eliminado!", "Se ha eliminado correctamente el elemento seleccionado.", "success");
                                    $($container).empty().html(response);
                                },
                                405: function () {

                                },
                                500: function (response) {
                                    swal("Error!", "Ha existido un error al eliminar el elemento seleccionado", "error");

                                }
                            }}
                    )
                } else {
                    swal("Cancelado", "No se ha realizado ninguna acción", "error");
                }
            });
    });

});
