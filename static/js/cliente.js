var socket = io.connect('http://' + document.domain + ':' + location.port) ;

socket.on('connect', function() {
  console.log('Conectado ao servidor!');
});

 $(document).ready(function() {
    socket.emit('join-room', {'_idComanda': $('#_idComanda').val(), '_idUser':$('#_idUser').val() });
  });
socket.on('pedido-aceito-confirmacao', function(data) {
  const idPedido = data._idPedido;
  const status = data.status;

  if (status === 'Aceito') {
    $('#status' + idPedido).removeClass('pending').addClass('process');
    $('#status' + idPedido).html(status);

    // Verifica se já existe um intervalo de tempo criado para o pedido
    if (setTimmer.intervalRefs && setTimmer.intervalRefs[idPedido]) {
      stopTimmer(idPedido); // Limpa o intervalo existente
    }

    // Cria um novo intervalo de tempo para o pedido
    setTimmer.intervalRefs = setTimmer.intervalRefs || {};
    setTimmer.intervalRefs[idPedido] = setTimmer($('#tempo' + idPedido).val(), idPedido);
  }

  if (status === 'Entregue') {
    $('#status' + idPedido).removeClass('process').addClass('completed');
    $('#status' + idPedido).html(status);

    // Limpa o intervalo de tempo quando o status do pedido muda para 'Entregue'
    stopTimmer(idPedido);
  }
});

function addToPedido(_this, quantidade){

    $('#pedido').modal('show')
    $('#title_modal').html($(_this).attr('data-bs-nome'))
    $('#descricao_modal').html('show')
    $('#tempo_espera').html($(_this).attr('data-bs-tempo')+'min')
    $('#qnt_modal').html(quantidade)
    $('#valor_unid').html(parseFloat($(_this).attr('data-bs-valor')).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) )
    $('#sub_total').html( (parseFloat($(_this).attr('data-bs-valor')) * parseInt(quantidade)).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    $('#qnt').val(quantidade)
    $('#_idCardapio').val($(_this).attr('data-bs-cardapio'))


}


$('.valor').inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});



var totalConta = 0
$('.subValor').each(function(i,e){
 var valorFloat = parseFloat($(e).html().replace(/[^\d.,]/g, "").replace(",", "."));
 totalConta = totalConta + valorFloat
 })
$('#total').html(totalConta)

$('#total-pagamento').html(totalConta).inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});
$('#total-subtotal').html(totalConta).inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});



$('#total').inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});

$('#taxa-serviço').html((totalConta * 0.1)).inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});
$('#total-pagamento-final').html(totalConta + (totalConta * 0.1)).inputmask("currency",{
prefix: "R$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,rightAlign: false


});
$('#pagar-valor').val(totalConta + (totalConta * 0.1))
$('.date').html(function(){
const dataStr = $(this).html();
const data = new Date(dataStr);

const dia = data.getDate().toString().padStart(2, "0");
const mes = (data.getMonth() + 1).toString().padStart(2, "0");
const ano = data.getFullYear().toString().slice(-2);
const hora = data.getHours().toString().padStart(2, "0");
const minuto = data.getMinutes().toString().padStart(2, "0");
const segundo = data.getSeconds().toString().padStart(2, "0");

const dataFormatada = `${dia}/${mes}/${ano} ${hora}:${minuto}:${segundo}`;
return dataFormatada;


})


