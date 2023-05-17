var bsOffcanvas = document.getElementById('clickCart')
function addItem(_id){
    $.ajax({
        url: "/pedido/"+_id,
        type: "POST",
        success: function(response) {
            // handle successful response here
            console.log(response);
        },
        error: function(xhr, status, error) {
            // handle error response here
            console.log(xhr.responseText);
        }
    });

    bsOffcanvas.click()
}

