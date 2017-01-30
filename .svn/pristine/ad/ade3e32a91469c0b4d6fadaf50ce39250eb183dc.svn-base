/**
 * Created by amado on 25/01/17.
 */
app.controller('StripeController',[
    '$scope','StripeService','NotificationService','$state',
    function ($scope, StripeService,NotificationService, $state) {
        var action = ($state.current.data.action);

        StripeService.publishableKey().success(function(data){
           $scope.publishable_key = data.publishable_key;
            $scope.set_key($scope.publishable_key);

        });

        $scope.set_key = function (key) {
           if(window.Stripe !== undefined && window.Stripe !== null)
            {
                window.Stripe.setPublishableKey(key);
            }
        }
        
        $scope.payment = function () {
            var $form = $('#payment-form');
            console.log($form);
            $form.find('.submit').prop('disabled', true);
            if(window.Stripe !== undefined && window.Stripe !== null){
                window.Stripe.card.createToken($form, function (status, response) {
                        // Grab the form:
                        var $form = $('#payment-form');

                        if (response.error) { // Problem!

                            // Show the errors on the form:
                            $form.find('.payment-errors').text(response.error.message);
                            $form.find('.submit').prop('disabled', false); // Re-enable submission

                        } else { // Token was created!

                            // Get the token ID:
                            var token = response.id;

                            if (action === 'subscribe'){
                               StripeService.subscribe({stripeToken:token})
                                .success(function (response) {
                                    NotificationService.success('','Su suscripcion fue creada satisfactoriamente');
                                    //$scope.$apply(function(){
                                    //    $scope.business = response;
                                    //});
                                    $scope.business = response;
                                    $state.go('profile');
                                })
                                .error(function(response){
                                       $form.find('.submit').prop('disabled', false); // Re-enable submission
                                       NotificationService.error('','Ha ocurrido un error al procesar los datos, por favor' +
                                           ' intente de nuevo');
                                });

                            }else if(action === 'changecard'){
                                StripeService.changeCard({stripeToken:token})
                                    .success(function (response) {
                                        NotificationService.success('','Su tarjeta ha sido actualizada');
                                        $scope.business = response;
                                        $state.go('profile');
                                    }).error(function (response) {
                                        $form.find('.submit').prop('disabled', false);
                                         NotificationService.error('','Ha ocurrido un error al procesar los datos, por favor' +
                                           ' intente de nuevo');
                                    });
                            }

                            // Insert the token ID into the form so it gets submitted to the server:
                            //$form.append($('<input type="hidden" name="stripeToken">').val(token));
                            //
                            //// Submit the form:
                            //$form.get(0).submit();
                        }
                    }
                );
            }

        }


    //$scope.logo = 'adfaf';
    //    $scope.pelotero = 'Picaso';
    //    console.log('Stripe');
    //
    //    $scope.pay = function(){
    //        var val = 4;
    //        window.Stripe.connect(val, function(data){
    //            console.log($scope.logo);
    //            console.log(data);
    //            $scope.pelotero = 'Samon';
    //            $('.payment-errors').html('Hola mundo!!!');
    //        });
    //    }
    }
]);