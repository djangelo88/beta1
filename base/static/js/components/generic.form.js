/**
 * Created by Hector on 18/11/2016.
 */
$(document).ready(function () {
    //Adicionar / Editar
    var current_url = '';
    $("#genericModal").on('shown.bs.modal', function (e) {
//
        var $button = $(e.relatedTarget) // Button that triggered the modal
        var elem_id = $button.data('elem-id') // Extract info from data-* attributes
        var modal_title = $button.data('modal-title') // Extract info from data-* attributes
        $form = $("#" + $button.data('form'));
        $container = $("#" + $button.data('container'));

        current_url = $button.data('current-url');

        var modal = $(this)
        modal.find('.modal-title').text(modal_title);


        if ($button.hasClass('add')) {

            $('#saveAdd').show();
            $('#save').show();
            $('#saveEdit').hide();
            $('.modal-body').toggleClass('success');

            var add_url = $button.data('url')
            $("#action_url").val(add_url);
            localStorage.setItem('action_url', add_url);

            $.ajax({
                    url: add_url,
                    success: function (data, textStatus) {
                        $('.modal-body').empty().html(data);
                        $($form.selector).attr('action', add_url);
                    }
                }
            )

        } else if ($button.hasClass('edit')) {
            $('#saveAdd').hide();
            $('#save').hide();
            $('#saveEdit').show();
            $('.modal-body').toggleClass('warning');

            var edit_url = $button.data('edit-url')

            $("#action_url").val(edit_url);
            localStorage.setItem('action_url', edit_url);
            $.ajax({
                    url: edit_url,
                    success: function (data, textStatus) {
                        $('.modal-body').empty().html(data);
                        $($form.selector).attr('action', edit_url);

                    }
                }
            )
        }

    }).on('hidden.bs.modal', function (e) {
        //$('.modal-body').empty();
        $('.modal-body').removeClass('success').removeClass('warning');

//          $("div.modal-backdrop.fade.in").hide();
//              window.location.reload();
//            alert("xxxx");

        $.ajax({
            url: current_url,
            type: 'GET',
            success: function (response) {
//                    console.log(response);
                $($container).empty().html(response);
            }, error: function (response) {

            }
        })
//            console.debug($(".modal-body form"));
        $($form.selector).remove();
        localStorage.removeItem('action_url');

    });


    $("#save").click(function (event) {
        SaveFunction(event, true, true);
    });
    $("#saveAdd").click(function (event) {

        $.when(SaveFunction(event, false, true))
            .done(function () {
                $(".form-control").val('');
                $("div.text-validation-error").remove();
                $(".has-error").removeClass('has-error');
                //OpenAddModal();

            });
    });

    $("#saveEdit").click(function (event) {
        SaveEditFunction(event);
    });

    function OpenAddModal() {
        $('#saveAdd').show();
        $('#save').show();
        $('#saveEdit').hide();
    }

    function SaveFunction(event, hideModal, isAdd) {
        event.preventDefault();
        $form1 = $($form.selector).get(0);

        $form1.action = localStorage.getItem('action_url');


        var data = new FormData($form1);
        //console.debug($($form1).attr('action'));

        $.ajax({
            url: $($form1).attr('action'),
            type: $($form1).attr('method'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                if (isAdd) {
                    toastr.info('Se ha agregado correctamente el elemento especificado');
                } else {
                    toastr.info('Se ha actualizado correctamente el elemento especificado');
                }

                if (hideModal) {
                    $("#genericModal").modal('hide');
//                setTimeout(function(){
//                window.location.href = "";
//                },1500);
                }

            }, error: function (data) {
                $(".modal-body").empty().append(data.responseText);

            }
        });

        return false;
    }

    function SaveEditFunction(event) {
        SaveFunction(event, true, false);
    }


});
