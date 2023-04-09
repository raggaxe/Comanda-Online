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