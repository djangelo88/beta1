/**
 * Created by Hector on 18/11/2016.
 */
$(document).ready(function () {
    //Adicionar / Editar

    $("#menuModal").on('shown.bs.modal',function (e) {

        var $button = $(e.relatedTarget) // Button that triggered the modal
        var elem_id = $button.data('elem-id') // Extract info from data-* attributes
        var modal_title = $button.data('modal-title') // Extract info from data-* attributes

//        $.CustomDatatableFormObject.model_id = elem_id;

        var modal = $(this)
        modal.find('.modal-title').text(modal_title);


        if ($button.hasClass('add')) {
//            OpenAddModal();
            $('#saveAdd').show();
            $('#save').show();
            $('#saveEdit').hide();
            $('.modal-body').toggleClass('success');

            var add_url = $button.data('url')
            $("#action_url").val(add_url);

            $.ajax({
                    url: add_url,
                    success: function (data, textStatus) {
                        $('.modal-body').empty().html(data);
                        $('#menu_form').attr('action', add_url);

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


            $.ajax({
                    url: edit_url,
                    success: function (data, textStatus) {
                        $('.modal-body').empty().html(data);
                        $('#menu_form').attr('action', edit_url);

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
                url:'/site/menu',
                type:'GET',
                success: function(response){
//                    console.log(response);
                    $("#stepContainer4").empty().html(response);
                },error:function(response){

                }
            })
//            console.debug($(".modal-body form"));
            $("#menu_form").remove();

        });


    $("#save").click(function (event) {
        SaveFunction(event,true,true);
    });
    $("#saveAdd").click(function (event) {

        $.when(SaveFunction(event,false,true))
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

    function SaveFunction(event,hideModal,isAdd) {
        event.preventDefault();
        $form = $('#menu_form').get(0);
        var data = new FormData($form);


        $.ajax({
            url: $($form).attr('action'),
            type: $($form).attr('method'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                if(isAdd)
                {
                    toastr.info('Se ha agregado correctamente el elemento especificado');
                }else{
                    toastr.info('Se ha actualizado correctamente el elemento especificado');
                }

                if(hideModal){
                    $("#menuModal").modal('hide');
//                setTimeout(function(){
//                window.location.href = "";
//                },1500);
                }

            },error:function(data){
                $(".modal-body").empty().append(data.responseText);

                $('#menu_form').attr('action', $("#action_url").val());
            }
        });

        return false;

    }

    function SaveEditFunction(event) {
        SaveFunction(event,true,false);
    }



});
