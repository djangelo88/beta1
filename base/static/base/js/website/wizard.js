/**
 * Created by Hector on 07/12/2016.
 */
$(document).ready(function () {
    /*Get active step*/
    $activeStep = $("#website-wizard-container ul.steps li.active");
    $current_url = $activeStep.data('url');
    $step_id = $activeStep.data('step');

    /*Get active form*/
    $form = $("#stepContainer" + $step_id + " form");

    /*Set visible active pane*/
    $('.step-pane[data-step="' + $step_id + '"]').toggleClass("hidden").toggleClass('active');

    /*Set .btn-prev behavior*/
    if ($step_id != "1") {
        $(".btn-prev").removeAttr("disabled").addClass('btn-success');
    }
    if ($step_id == 7) {
        //console.debug($step_id);
        $('.btn-next span').empty();
        //$('.btn-next').hidden();
        $('.btn-next span').append("Finalizar");

    }

    //var i = 1;
    //while(i < $activeStep){
    //    $('#website-wizard-container ul.steps li[data-step="'+i+'"]').addClass('complete');
    //    i++;
    //}


    $('.btn-next').click(function (event) {

        //console.debug($form.length);
        //console.debug($form[0].id);
        //console.debug($form.id);
        //console.debug($step_id);
        if ($form.length > 0 && ($form[0].id != "gallery_form" && $form.id != "menu_form" )) {
            $($form).submit();
        } else {
            //console.debug($form);
            if ($step_id != 7) {
                $next_step_id = $step_id + 1;
                $nextStep = $('#website-wizard-container ul.steps li[data-step="' + $next_step_id + '"]').data('url');
                window.location.href = $nextStep
            } else {
                window.location.href = '/site/congrats';
            }

        }
    });

    $('.btn-prev').click(function (event) {
        $prev_step_id = $step_id - 1;
        $prevStep = $('#website-wizard-container ul.steps li[data-step="' + $prev_step_id + '"]').data('url');
        window.location.href = $prevStep

    });


})