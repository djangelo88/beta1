/**
 * Created by amado on 18/11/16.
 */
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

    $('#send_invoice').click(function (event) {

        var url = $(this).attr('data-url');
        set_csrf_token();
        $.ajax({url: url,
            type: 'POST',
            data: {},
            statusCode: {
                200: function (response) {
                    //$('#send_invoice').hide();
                      toastr.success('Se ha enviado la factura');
                },
                404: function (response) {

                },
                500: function (response) {
                    toastr.error('Lo sentimos, Ha existido un error al procesar su solicitud');
                }
            }});
    });
});