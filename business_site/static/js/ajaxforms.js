/**
 * Created by maykel on 17/12/16.
 */

$(document).ready(function () {
    //load data on form
    $('.edit').click(function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {

                $('#id_name').val(response['name']);
                $('#id_description').val(response['description']);
                $('#current_img').attr('src', '/media/' + response['image']);
                $('#form_image').attr('action', url);
                $('#plus').attr('value', 'Editar');
                $('#plus').attr('data-name', 'edit');
                $('#plus').removeClass('btn-success').addClass('btn-warning');

            },
            error: function () {
                return
            }
        });
    });
    $("#reset").click(function () {

        if ($("#plus").val() != "+") {
            $('#plus').attr('value', '+');
            $('#plus').addClass('btn-success').removeClass('btn-warning');
              $('#current_img').attr('src', '');

        }
    });

    //if($('#plus').attr('data-name')=='edit'){
    //     $('#form_image').ajaxForm({
    //        success: function (response) {
    //            console.log('edit');
    //            //console.log($.get("/site/photos/"));
    //            $.ajax({
    //                url: "/site/photos/",
    //                type: "GET",
    //                success: function (data) {
    //                    console.log(data);
    //                   // $("#tableContainer").empty().append(data);
    //                    //$('#images_table').dataTable({
    //                    //    "language": {"url": "/static/i18n/Spanish.json"},
    //                    //    "paging": false,
    //                    //    "ordering": false,
    //                    //    "info": false,
    //                    //    "searching": false
    //                    //});
    //                }
    //            });
    //        },
    //        error:function(response){
    //            console.log(response);
    //        }
    //    });
    //}


    //
    ////submit photoedit form
    //$('#plus').click(function(e) {
    //    e.preventDefault();

    //$('#form_image').ajaxForm({
    //    success: function (response) {
    //        //console.log($.get("/site/photos/"));
    //        //$.ajax({
    //        //    url: "/site/photos/",
    //        //    type: "GET",
    //        //    success: function (data) {
    //        //        console.log(data);
    //        //       // $("#tableContainer").empty().append(data);
    //        //        //$('#images_table').dataTable({
    //        //        //    "language": {"url": "/static/i18n/Spanish.json"},
    //        //        //    "paging": false,
    //        //        //    "ordering": false,
    //        //        //    "info": false,
    //        //        //    "searching": false
    //        //        //});
    //        //    }
    //        //});
    //    },
    //    error:function(response){
    //        console.log(response);
    //    }
    //});
    //});
    //
    //    function UpdateDataTable() {
    //            $.ajax({
    //                type: 'GET',
    //                url: '/site/photos/',
    //                success: function (data) {
    //                    console.debug(data);
    //                    $("#tableContainer").empty().append(data);
    //                    $('#images_table').dataTable({
    //                        "language": {"url": "/static/i18n/Spanish.json"},
    //                        "paging": false,
    //                        "ordering": false,
    //                        "info": false,
    //                        "searching": false
    //                    });
    //                }
    //            });
    //        }
});