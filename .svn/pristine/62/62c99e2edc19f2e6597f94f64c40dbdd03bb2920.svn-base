/**
 * Created by maykel on 2/01/17.
 */
function Eliminar() {
    if ($('.item_price').length>0) {
        if(parseInt($('.item_price').length) == 1){
            $('#id_min').val('1');
            $('#id_max').val('2');
            $('#id_price').val('0.00');
        }else if(parseInt($('.item_price').length) > 1){
            $('#id_min').val(parseInt($('.item_price')[$('.item_price').length - 2].children[1].children.max_value.value) + 1);
            $('#id_max').val(parseInt($('.item_price')[$('.item_price').length - 2].children[1].children.max_value.value) + 2);
            $('#id_price').val(parseFloat($('.item_price')[$('.item_price').length - 2].children[2].children.price_value.value));
        }
        $('.item_price').last().remove();
    }
}
function soloLetras(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = "0123456789";
    especiales = [8, 37, 39, 46];

    tecla_especial = false
    for(var i in especiales) {
        if(key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }
    if(letras.indexOf(tecla) == -1 && !tecla_especial)
        return false;
}

function Adicionar() {
    var min_val = $('#id_min').val();
    var max_val = $('#id_max').val();
    var price_val = $('#id_price').val();

    var html = "<div id='item_price' class='form-group col-xs-12 item_price no-padding'>" +
        "<div class='form-group col-xs-3 no-padding-right'>" +
        "<input class='form-control min_value' id='min_value' readonly='readonly' value='" + min_val + "' name='min' rows='5' type='number'>" +
        "</div>" +
        "<div class='form-group col-xs-3 no-padding-right'>" +
        "<input class='form-control max_value' id='max_value' name='max' readonly='readonly' type='number' min='" + max_val + "' rows='5' value='" + max_val + "' >" +
        "</div>" +
        "<div class='form-group col-xs-3 no-padding-right'>" +
        "<input class='form-control price_value' id='price_value' name='price' onkeypress='return soloLetras(event)' type='number' rows='5' value='" + price_val + "' step='0.01' min='0'>" +
        "</div>";

    var price = parseFloat($('#id_price').val());
    if (price <= 0) {
        toastr.error('El precio no puede ser cero.');
        return
    } else {
        //$('.max_value')[$('.max_value').length - 1].readOnly = true;
        //$('.price_value')[$('.price_value').length - 1].readOnly = true;
        $('#items_list').append(html);
        $('#id_min').val(parseInt(max_val) + 1);
        $('#id_max').val(parseInt(max_val) + 2);
        $('#id_price').val(price_val);


    }
}


