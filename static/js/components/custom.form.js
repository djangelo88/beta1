/**
 * Created by Hector on 18/11/2016.
 */
$(document).ready(function () {



    //Adicionar / Editar
    $($.CustomDatatableFormObject.modal_dialog_id).on('show.bs.modal', function (e) {

        var $button = $(e.relatedTarget) // Button that triggered the modal
        var elem_id = $button.data('elem-id') // Extract info from data-* attributes
        var modal_title = $button.data('modal-title') // Extract info from data-* attributes

        $.CustomDatatableFormObject.model_id = elem_id;

        var modal = $(this)
        modal.find('.modal-title').text(modal_title)

        if ($button.hasClass('add')) {
            OpenAddModal();
            if ($button.hasClass('from-event')) {
                $('#saveAdd').hide();
            } else {
                $('#saveAdd').show();
            }
            $('#edit').hide();
            $('#save').show();
            $('#saveEdit').hide();
            $('.modal-body').toggleClass('success');

        } else if ($button.hasClass('edit')) {
            $('#edit').hide();
            $('#saveAdd').hide();
            $('#save').hide();
            $('#saveEdit').show();
            $('.modal-body').toggleClass('warning');

            $.ajax({
                    url: $.CustomDatatableFormObject.get_url_edit(),
                    success: function (data, textStatus) {
                        $('.modal-body').append(data);
                    }
                }
            )
        } else if ($button.hasClass('view')) {
            $('#edit').show();
            $('#saveAdd').hide();
            $('#save').hide();
            $('#saveEdit').hide();
            $('.modal-body').toggleClass('info');

            $.ajax({
                    url: $.CustomDatatableFormObject.get_url_edit(),
                    success: function (data, textStatus) {
                        $('.modal-body').append(data);
                    }
                }
            )


        }

    }).on('hidden.bs.modal', function (e) {
        $('.modal-body').empty();
        $('.modal-body').removeClass('success').removeClass('warning').removeClass('info');

        if ($.CustomDatatableFormObject.has_fn_callback && ($.CustomDatatableFormObject.model_id != -1 && $.CustomDatatableFormObject.model_id)) {
            $.CustomDatatableFormObject.fn_callback()
        }


    }).on('shown.bs.modal', function (e) {

        if ($(".modal-body").hasClass('info')) {
            $(".modal-body input").attr('disabled', true);
            $(".modal-body select").attr('disabled', true);
            $(".input-group-btn button").attr('disabled', true);
            $(".modal-body textarea").attr('disabled', true);
        }


    });
    $('#edit').click(function () {
        $(".modal-body input").removeAttr('disabled');
        $(".modal-body select").removeAttr('disabled');
        $(".input-group-btn button").removeAttr('disabled');
        $(".modal-body textarea").removeAttr('disabled');

        $('.modal-body').removeClass('success').removeClass('info');
        $('.modal-body').addClass('warning');

        $('h4.modal-title').text("Editar contacto");

        $('#edit').hide();
         $("#saveEdit").show();



    });


    $("#save").click(function () {
        SaveFunction(true);

    });
    $("#saveAdd").click(function () {

        $.when(SaveFunction(false))
            .done(function () {
                $('.modal-body').empty();
                OpenAddModal();
            });
    });

    $("#saveEdit").click(function () {
        SaveEditFunction();
    });

    function OpenAddModal() {
        $('#saveAdd').show();
        $('#save').show();
        $('#saveEdit').hide();
        return $.ajax({
                url: $.CustomDatatableFormObject.get_url_add(),
                success: function (data, textStatus) {
                    $('.modal-body').append(data);
                }
            }
        )
    }

    function SaveFunction(hideModal) {

        var form_data = $($.CustomDatatableFormObject.form_id).serialize();
        //console.debug($.CustomDatatableFormObject.get_url_add());
        //console.debug(form_data);

        set_csrf_token();
        return $.ajax({
            type: "POST",
            url: $.CustomDatatableFormObject.get_url_add(),
            data: form_data,
            success: function (data, status_code) {

                $.CustomDatatableFormObject.model_id = data.id;

                if (hideModal) {
                    $($.CustomDatatableFormObject.modal_dialog_id).modal('toggle');
                }

                $.when($.ajax({url: $.CustomDatatableFormObject.get_url_base()})).done(function () {
                    toastr.info('Se ha agregado correctamente el elemento especificado');
                    UpdateDataTable();
                })


            },
            error: function (data) {
                console.debug(data);
                $(".modal-body").empty().append(data.responseText);

            }
        });

    }

    function SaveEditFunction() {

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
        // set_csrf_token();
        console.debug($.CustomDatatableFormObject.get_url_edit());
        var form_data = $($.CustomDatatableFormObject.form_id).serialize();
        return $.ajax({
            type: "POST",
            url: $.CustomDatatableFormObject.get_url_edit(),
            data: form_data,
            success: function (data, status_code) {

                console.debug(status_code);
                $.when($.ajax({url: $.CustomDatatableFormObject.get_url_base()})).done(function () {
                    toastr.info('Se actualizado correctamente el elemento');
                    UpdateDataTable();
                    $($.CustomDatatableFormObject.modal_dialog_id).modal('toggle');
                })


            },
            error: function (data) {
                console.debug(data);
                $(".modal-body").empty().append(data.responseText);

            }
        });
    }

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


});
