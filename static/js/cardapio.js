function changeEstoque(_this){
    if(_this.checked){
        $('#estoque').prop("disabled", true);
        $('#estoque').val('');
    }
    else{
     $('#estoque').prop("disabled", false);
     $('#estoque').val(0);
    }
}

function changeEstoque_edit(_this){
    if(_this.checked){
        $('#estoque_edit').prop("disabled", true);
        $('#estoque_edit').val('');
    }

    else{
     $('#estoque_edit').prop("disabled", false);
     $('#estoque_edit').val(0);
    }
}




const $table = $('#item_data');


const exampleModal = document.getElementById('cardapio-modal')
exampleModal.addEventListener('show.bs.modal', event => {
  // Button that triggered the modal
  const button = event.relatedTarget
  // Extract info from data-bs-* attributes
  const _bs__idCardapio = button.getAttribute('data-bs-cardapio')
  const _bs_nome = button.getAttribute('data-bs-nome')
  const _bs_categoria = button.getAttribute('data-bs-categoria')
  const _bs_filename = button.getAttribute('data-bs-filename')
  const _bs_tempo = button.getAttribute('data-bs-tempo')
  const _bs_valor = button.getAttribute('data-bs-valor')
  const _bs_estoque = button.getAttribute('data-bs-estoque')
  const _bs_status = button.getAttribute('data-bs-status')
  // If necessary, you could initiate an Ajax request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  const nome_inserrt = exampleModal.querySelector('.modal-body #nome_produto_edit')
  const _idCardapio = exampleModal.querySelector('#produto_remove')
  const produto_status_id = exampleModal.querySelector('#produto_status_id')

  const categoria = exampleModal.querySelector('.modal-body #categoria_edit')
  const filename = exampleModal.querySelector('.modal-body #filename_edit')
  const tempo = exampleModal.querySelector('.modal-body #tempo_edit')
  const valor = exampleModal.querySelector('.modal-body #valor_edit')
  const estoque = exampleModal.querySelector('.modal-body #estoque_edit')
  const status = exampleModal.querySelector('#ativo_edit')
  const ativo = exampleModal.querySelector('#ativo')
  const no_stock_edit = exampleModal.querySelector('.modal-body #no_stock_edit')

    nome_inserrt.value = _bs_nome
    _idCardapio.value = _bs__idCardapio
    produto_status_id.value = _bs__idCardapio
    categoria.value = _bs_categoria
//    filename
    tempo.value = _bs_tempo
    valor.value = _bs_valor
    console.log(_bs_tempo)

    filename.src = '/static/uploads/'+ _bs_filename

    if(_bs_estoque !== "False"){
        estoque.value = _bs_estoque
    }
    else{
     $('#estoque_edit').prop("disabled", true);
      $('#estoque_edit').val('');
        no_stock_edit.checked = true;
    }
     if(_bs_categoria === "False"){
        categoria.value = 'Escolha a categoria'
    }
     if(_bs_status === "True"){
        status.checked = true;
        ativo.value = true
    }
    else{
        status.checked = false;
        ativo.value = false
    }


})

const alerta = $('.alerta-container');

function ShowAlerta(msg, categoria) {
  var html = '<div class="alert ' + categoria + '" role="alert" id="alerta">' + msg + '</div>';
  alerta.html(html);

  setTimeout(function() {
    alerta.fadeOut('slow', function() {
      $(this).empty().show();
    });
  }, 3000);
}


function EnviarFormulario(_id) {
    if(_id){
         // Obter o formulário pelo ID
      var form = document.getElementById('editItem');

      // Criar um objeto FormData
      var formData = new FormData(form);

      // Enviar os dados do formulário via AJAX
      $.ajax({
        url: '/cardapio',
        method: 'POST',
        data: formData,
        processData: false, // Não processar dados do formulário
        contentType: false, // Não definir o tipo de conteúdo
        success: function(response) {
            if(!response.erro){
                $table.bootstrapTable('refresh')
                OffcanvasEdit.click();
                ShowAlerta(response.msg, response.categoria)
            }
            else{
                ShowAlerta(response.erro, response.categoria)
            }
        },
        error: function(xhr, status, error) {
         ShowAlerta(response.msg, response.categoria)
          // Resto do código de erro aqui
        }
      });
    }
    else{
      // Obter o formulário pelo ID
      var form = document.getElementById('criarItem');

      // Criar um objeto FormData
      var formData = new FormData(form);

      // Enviar os dados do formulário via AJAX
      $.ajax({
        url: '/cardapio',
        method: 'POST',
        data: formData,
        processData: false, // Não processar dados do formulário
        contentType: false, // Não definir o tipo de conteúdo
        success: function(response) {

            if(!response.erro){
                ShowAlerta(response.msg, response.categoria)
                $table.bootstrapTable('refresh')
                $('.lista_items').show();$('.add_items').hide()
            }
            else{
                ShowAlerta(response.erro, response.categoria)
            }

        },
        error: function(xhr, status, error) {
         ShowAlerta(response.msg, response.categoria)
          // Resto do código de erro aqui
        }
      });
    }

}






function image(value) {
    return '<img src="/uploads/' + value + '" align="middle"/>';
}

const OffcanvasEdit = $('#offcanvasEdit')

$table.bootstrapTable({
  onDblClickRow: function (row, $element, field) {
   $.ajax({
    url: '/get-items',
    method:'POST',
    data:{_id: row._id},
    success: function(data) {
       $('#editItemModal').html(data);
       OffcanvasEdit.click()
    },
    error: function(xhr, status, error) {
      console.log('Erro na requisição AJAX');
      console.log('Status:', status);
      console.log('Erro:', error);
    }
  });
  }
})




function deleteItem(_id) {

    if (confirm('Tem certeza que deseja excluir o item?')) {
    $.ajax({
    url: '/delete_cardapio',
    method: 'POST',
    data: {_id:_id},
    success: function(response) {
        if(!response.erro){
            OffcanvasEdit.click();
            $table.bootstrapTable('refresh');
            ShowAlerta(response.msg, response.categoria)
        }
        else{
            ShowAlerta(response.erro, response.categoria)
        }

    },
    error: function(xhr, status, error) {
     ShowAlerta(response.msg, response.categoria)
      // Resto do código de erro aqui
    }
  });
  } else {
    // Código para executar caso a opção "Não" seja selecionada
    console.log('Exclusão cancelada');
  }
  // Enviar os dados do formulário via AJAX

}








$(document).ready(function() {
  // Seletor CSS para o campo de entrada
  var valorInput = $("#valor");

  // Aplica a máscara de dinheiro usando o plugin inputmask
  valorInput.inputmask("currency", {
    prefix: "R$ ",
    radixPoint: ",",
    groupSeparator: ".",
    allowMinus: false,
    autoGroup: true,
    digits: 2,
    digitsOptional: false,
    rightAlign: false,
    unmaskAsNumber: true  // Permite obter o valor sem a formatação
  });

  // Evento keyup para capturar o valor sem a formatação
  valorInput.on("keyup", function(event) {
    var valorSemFormatacao = valorInput.inputmask("unmaskedvalue");
    console.log(valorSemFormatacao);
    // Faça o que quiser com o valor sem formatação
  });
});



function destque(value){
    return '<span style="font-weight:600">'+value+'</span>'
}




//const tabPaneEl = document.querySelector('#disabled-tab');
//
//
//tabPaneEl.addEventListener('shown.bs.tab', event => {
//  console.log('Pane aberta');
//
//  $.ajax({
//    url: '/get-items',
//    success: function(data) {
//    console.log(data)
//      $table.bootstrapTable('load', data);
//    },
//    error: function(xhr, status, error) {
//      console.log('Erro na requisição AJAX');
//      console.log('Status:', status);
//      console.log('Erro:', error);
//    }
//  });
//
//});


//
//$('#criarItem').on('submit', function(e) {
//  e.preventDefault(); // Evitar o comportamento padrão do envio do formulário
//  EnviarFormulario(); // Chamar função para enviar o formulário via AJAX
//});






//const nome_produto = $('#nome_produto')
//const insert_nome_produto = $('#insert_nome_produto')
//
//nome_produto.on('keyup',function(){
//    if($(this).val() == ''){
//        insert_nome_produto.addClass('opacity-25')
//        insert_nome_produto.html("Descrição completa do produto.");
//    }
//    else{
//        insert_nome_produto.removeClass('opacity-25')
//        insert_nome_produto.html($(this).val());
//    }
//})
//
//const descricao = $('#descricao')
//const insert_descricao = $('#insert_descricao')
//descricao.on('keyup',function(){
//    if($(this).val() == ''){
//        insert_descricao.addClass('opacity-25')
//        insert_descricao.html("Insira um título para seu produto");
//    }
//    else{
//        insert_descricao.removeClass('opacity-25')
//        insert_descricao.html($(this).val());
//    }
//})
//
//const categoria = $('#categoria');
//const insert_categoria = $('#insert_categoria');
//
//categoria.on('change', function() {
//    if ($(this).val() == '') {
//        insert_categoria.addClass('opacity-25');
//        insert_categoria.html("Categorias");
//    } else {
//        insert_categoria.removeClass('opacity-25');
//        insert_categoria.html($('option:selected', this).text());
//    }
//});
//
//
//
//








function previewImage2(event) {
  const input = event.target;
  const img = document.getElementById('previewImage');

  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function(e) {
      img.setAttribute('src', e.target.result);
      img.style.display = 'block';
      $('#preview-title').hide()
    }

    reader.readAsDataURL(input.files[0]);
  } else {
    img.setAttribute('src', '');
    img.style.display = 'none';
  }
}


function previewImage3(event) {
  const input = event.target;
  const img = document.getElementById('previewImage2');

  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function(e) {
      img.setAttribute('src', e.target.result);
      img.style.display = 'block';
      $('#preview-title').hide()
    }

    reader.readAsDataURL(input.files[0]);
  } else {
    img.setAttribute('src', '');
    img.style.display = 'none';
  }
}
//
//
//
//// Aplicar máscara de dinheiro no campo de entrada
//  Inputmask("currency", {
//    radixPoint: ",",
//    groupSeparator: ".",
//    allowMinus: false,
//    prefix: "R$ ",
//    placeholder: "0",
//    autoGroup: true,
//    rightAlign: false,
//    clearMaskOnLostFocus: true
//  }).mask("#valor");
//
//
//const valor = $('#valor');
//const insert_valor = $('#insert_valor');
//
//valor.on('keyup', function() {
//console.log($(this).val())
//    if ($(this).val() == '') {
//        insert_valor.addClass('opacity-25');
//        insert_valor.html("R$ 0,00");
//    } else {
//        insert_valor.removeClass('opacity-25');
//        insert_valor.html($(this).val());
//    }
//});



