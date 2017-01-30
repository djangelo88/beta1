/**
 * Created by Hector on 18/11/2016.
 */
$(document).ready(function () {
    //Adicionar / Editar
  //  console.debug($.CustomDatatableFormObject['model_name']);

    $("#itemModal").on('shown.bs.modal', function (e) {

        var $button = $(e.relatedTarget) // Button that triggered the modal
        var elem_id = $button.data('elem-id') // Extract info from data-* attributes
        var modal_title = $button.data('modal-title') // Extract info from data-* attributes

        $.CustomDatatableFormObject.model_id = elem_id;
        //console.debug(elem_id);

        var modal = $(this)
        modal.find('.modal-title').text(modal_title)

        if ($button.hasClass('add')) {
            OpenAddModal();
            $('#saveAdd').show();
            $('#save').show();
            $('#saveEdit').hide();
            $('.modal-body').toggleClass('success');

        } else if ($button.hasClass('edit')) {
            $('#saveAdd').hide();
            $('#save').hide();
            $('#saveEdit').show();
            $('.modal-body').toggleClass('warning');

            var edit_url = $button.data('url')


            $.ajax({
                    url: edit_url,
                    success: function (data, textStatus) {
                        $('.modal-body').empty().html(data);
                    }
                }
            )
        }

    }).on('hidden.bs.modal', function (e) {
        //$('.modal-body').empty();
        $('.modal-body').removeClass('success').removeClass('warning');
        //
        //if ($.CustomDatatableFormObject.has_fn_callback && ($.CustomDatatableFormObject.model_id != -1 && $.CustomDatatableFormObject.model_id)) {
        //    $.CustomDatatableFormObject.fn_callback()
        //}
//          $("div.modal-backdrop.fade.in").hide();
  window.location.reload();
//            alert("xxxx");
    });


    $("#save").click(function () {
        SaveFunction(true);


    });
    $("#saveAdd").click(function () {

        $.when(SaveFunction(false))
            .done(function () {
                $("#item_form .form-control").val('');
                $("#id_discount").val('0');
                $("#id_tax").val($("#taxes_value").val());
                $("#item_form div.text-validation-error").remove();
                $("#item_form .has-error").removeClass('has-error');
                //OpenAddModal();
            });
    });

    $("#saveEdit").click(function () {
        SaveEditFunction();
    });

    function OpenAddModal() {
        $('#saveAdd').show();
        $('#save').show();
        $('#saveEdit').hide();

        //var url = '/proposal/'+ localStorage.getItem('proposalId') +'/items/list/';
        //
        //return $.get({
        //        url: url,
        //        data:{id_item:localStorage.getItem('proposalId')},
        //        success: function (data, textStatus) {
        //            $('.modal-body').append(data);
        //        }
        //    }
        //)

    }

    function SaveFunction(hideModal) {

        //console.debug(form_data);

        var url = $('#item_form').attr('action');
        //var load_url = $('#items_container').attr('data-url-load');
        //var items_url = '/proposal/' + localStorage.getItem('proposalId') + '/items/list/';
        var items_url = '/proposal/' + localStorage.getItem('proposalId') + '/items/list/';
        var form_data = $('#item_form').serialize();
        //console.debug(url);

        set_csrf_token();
        return $.ajax({
            type: "POST",
            url: url,
            data: form_data,
            success: function (data, status_code) {

                // $.CustomDatatableFormObject.model_id = data.id;

                $.when($.ajax({
                    url: items_url, success: function (data) {
                        $('#items_container').html(data);
                    }
                })).done(function () {
                    toastr.info('Se ha agregado correctamente el elemento especificado');
                    // UpdateDataTable();
                })

                if (hideModal) {
                    $("#itemModal").modal('hide');

                }


            },
            error: function (data) {
                console.debug(data);
                $(".modal-body").empty().append(data.responseText);
                //$("#itemModal").modal('toggle');
            }
        });

    }

    function SaveEditFunction() {

        var url = $('#item_form').attr('action');

        set_csrf_token();
        var  itemId = $('#item_form').attr('data-item-id');
        //var  url = '/proposal/' + localStorage.getItem('proposalId') + '/items/'+itemId+'/';
        // set_csrf_token();
        var form_data = $("#item_form").serialize();
        return $.ajax({
            type: "POST",
            url: url,
            data: form_data,
            success: function (data, status_code) {

                 var items_url = '/proposal/' + localStorage.getItem('proposalId') + '/items/list/';
                $.when($.ajax({
                    url: items_url, success: function (data) {
                        $('#items_container').html(data);
                    }
                })).done(function () {
                     toastr.info('Se actualizado correctamente el elemento');

                })
                    $("#itemModal").modal('hide');


            },
            error: function (data) {
                console.debug(data);
                $(".modal-body").empty().append(data.responseText);

            }
        });


    }

    //function UpdateDataTable() {
    //    $.ajax({
    //        type: 'GET',
    //        url: $.CustomDatatableFormObject.get_url_base(),
    //        success: function (data) {
    //            $($.CustomDatatableFormObject.datatable_container).empty().append(data);
    //            //$("#tableContainer").empty().append(data);
    //            $($.CustomDatatableFormObject.datatable_id).dataTable();
    //            //$('#customers_table').dataTable();
    //        }
    //    });
    //}

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
