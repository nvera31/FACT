//IMPRIME LOS ERRORES QUE SURGAN AL GUARDAR UNA NUEVA CATEGORIA
function errores(obj){
    var html = '';
    if (typeof (obj) === 'object'){
        html = '<ul>';
        $.each(obj, function (key, value){
            html+='<li>'+key+': '+value+'</li>';
        
        })
        html+='</ul>';
    }
    else{
        html = '<p>'+obj+'</p>';
    }
    alert(html)
}

//FUNCION PARA ALERTAS JQUERY
function submit_with_ajax(url,parametros,callback){
    $.confirm({
        theme: 'bootstrap',
        title: 'Confirmación',
        icon: 'bi bi-info-circle',
        content: 'Seguro de seguir?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        //TRABAJA CON LA VISTA ACTUAL
                         url: url,// window.location.pathname,
                         type: 'POST',
                         data: parametros,
                         dataType: 'json'
                     }).done(function (data) {
                        console.log(data);
                         if(!data.hasOwnProperty('error')){
                            callback();
                            return false;
                         }
                         errores(data.error);
    
                     }).fail(function (jqXHR, textStatus, errorThrown) {
                         alert(textStatus+':'+errorThrown);
                     }).always(function (data) {
    
                     });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    
                }
            },
        }
    })
}