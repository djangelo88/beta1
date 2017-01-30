/**
 * Created by Hector on 04/01/2017.
 */
$(document).ready(function () {

 //$alerts = $(".messages > div.alert ");
 $alerts = $(".django-messages > div.alert ");

    for(var i =0; i < $alerts.length; i++){

        $custom_alert = $alerts[i];
        $custom_message = $($custom_alert).children("p")[0].innerText;

        if($($custom_alert).hasClass('success')){
            toastr.success($custom_message);
        }else if($($custom_alert).hasClass('error')){
            toastr.error($custom_message);
        }
        else if($($custom_alert).hasClass('info')){
            toastr.info($custom_message);
        }
    }

    $alerts.remove();


});
