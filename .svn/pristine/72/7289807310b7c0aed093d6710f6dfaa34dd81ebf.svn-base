/**
 * Created by maykel on 22/12/16.
 */
$(document).ready(function(){
   //$('#publish_link').hide();

   $('#publish_link').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/site/publish/",
            type: "GET",
            success: function (response) {
                //toastr.info('Su website se ha publicado correctamente.')
                window.location.href = "/site/congrats"
            },
            error: function () {
                return
            }
        });

    });

    $('#upublish_link').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/site/unpublish/",
            type: "GET",
            success: function (response) {
                //toastr.info('Su website se ha despublicado por tanto no estara visible a sus usuarios.')
                window.location.href = "/site/congrats"

            },
            error: function () {
                return
            }
        });

    });
});