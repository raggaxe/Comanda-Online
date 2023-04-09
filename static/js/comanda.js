
function difTimmer(startStr, endStr, id) {
    const start = new Date(startStr);
    const end = new Date(endStr);
    const diff = Math.abs(end - start);
    const seconds = Math.floor(diff / 1000) % 60;
    const minutes = Math.floor(diff / 1000 / 60) % 60;
    const hours = Math.floor(diff / 1000 / 60 / 60) % 24;
    const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    $('#tempo-decorrido' + id).html(formattedTime);
}

function setTimmer(startStr, id) {
    const intervalRef = setInterval(() => {
        const start = new Date(startStr);
        const elapsed = new Date() - start;
        const seconds = Math.floor(elapsed / 1000) % 60;
        const minutes = Math.floor(elapsed / 1000 / 60) % 60;
        const hours = Math.floor(elapsed / 1000 / 60 / 60) % 24;
        const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        $('#tempo-decorrido' + id).html(formattedTime);
    }, 1000);

    return intervalRef;
}

function stopTimmer(id) {
    clearInterval(setTimmer.intervalRefs[id]); // interrompe o contador
}

$('.order-id[data-status="Entregue"]').each(function(index, element) {
    const id = $(element).val();
    difTimmer($('#tempo' + id).val(), $('#tempoUpdate' + id).val(), id);
});

$('.order-id[data-status!="Entregue"]').each(function(index, element) {
    const id = $(element).val();
    setTimmer.intervalRefs = setTimmer.intervalRefs || {};
    setTimmer.intervalRefs[id] = setTimmer($('#tempo' + id).val(), id);
});

function sendPedido() {
        // obter os valores dos campos do formulário
        var _idComanda = $('#_idComanda').val();
        var _idCardapio = $('#_idCardapio').val();
        var _idUser = $('#_idUser').val();
        var quantidade = $('#qnt').val();

        // enviar a requisição AJAX
        $.ajax({
            type: 'POST',
            url: '/pedido',
            data: {
                '_idComanda': _idComanda,
                '_idCardapio': _idCardapio,
                '_idUser': _idUser,
                'quantidade': quantidade
            },
            success: function(response) {
                console.log(response);
                  socket.emit("pedido-cliente-solicitado", {
                "_idComanda": _idComanda,
                "_idCardapio": _idCardapio,
                "_idUser": _idUser,
                "quantidade": quantidade,
                "_idPedido":response['_id']
            }, room=_idComanda);

                // atualizar a página
                location.reload();
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    }

function enviarPagamento() {
    // obtém os valores do formulário
    const valor = $('#pagar-valor').val();
    const idComanda = $('input[name="_idComanda"]').val();
    const formaPagamento = $('input[name="btnradio"]:checked').val();

    // cria um objeto com os valores
    const data = {
        valor,
        idComanda,
        formaPagamento
    };

    // envia a requisição para o servidor
    $.ajax({
    url: '/realizar_pagamento',
    method: 'POST',
    data: $('#payment-form').serialize(),
    success: function(response) {
        socket.emit('pedido-cliente-pagamento', {
            "_idComanda": idComanda,
            "valor": valor,
            "formaPagamento": formaPagamento
        });
                 // Redirecionar a página
       window.location.href = response.redirect_url;
    },
    error: function(error) {
        // adicione aqui o código para lidar com o erro da requisição AJAX
    }
});
}
$(document).ready(function(){
    socket.emit('mesa-ocupada', {'_idMesa': $('#_idMesa').val(),'numero_mesa': $('#numero_mesa').val(), '_idUser':$('#_idUser').val() } );

});