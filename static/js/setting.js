function toggleEditArea(nomeComercialId, editNomeComercialId, iconId, rowId) {
  var nome = document.getElementById(nomeComercialId);
  var editTexto = document.getElementById(editNomeComercialId);
  var icon = document.getElementById(iconId);
  var row = document.getElementById(rowId);

  if (nome.style.display === "none") {
    nome.style.display = "block";
    editTexto.style.display = "none";
    icon.classList.remove("bx-check");
    icon.classList.add("bx-edit-alt");

    row.classList.remove("show");


  } else {
    nome.style.display = "none";
    editTexto.style.display = "block";
    icon.classList.remove("bx-edit-alt");
    icon.classList.add("bx-check");
    row.classList.add("show");
  }
}


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
