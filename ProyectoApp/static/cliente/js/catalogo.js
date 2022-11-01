var tblCliente;

function getData(){
    tblCliente = $('#dato').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "apellido"},
            {"data": "dni"},
            {"data": "f_nacimiento"},
            {"data": "sexo.nombre"},
            {"data": "id"},
        ], columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="#" rel="edit" class="btn btn-info"><i class="bi bi-pencil-square"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger"><i class="bi bi-trash-fill"></i></a>';
                    return buttons;

                }
            },
        ],
        initComplete: function(settings, json){
            
        }
    });
}

$(function (){

    modal_title =$('.modal-title');

    getData();

//AGREGA CLIENTE
    $('.btnAdd').on('click', function(){
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('bi bi-plus-circle');
        $('input[name="action"]').val('add');
        $('#myModalCliente').modal('show');
    });
    
    //EDITAR CLIENTE
    $('#dato tbody')
    .on('click', 'a[rel="edit"]', function(){
        
        modal_title.find('span').html('Edicion de un cliente');
        modal_title.find('i').removeClass().addClass('bi bi-plus-circle');
        var tr = tblCliente.cell($(this).closest('td, li')).index();
        var data = tblCliente.row( tr.row ).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="apellido"]').val(data.apellido);
        $('input[name="dni"]').val(data.dni);
        $('input[name="f_nacimiento"]').val(data.f_nacimiento);
        $('input[name="direccion"]').val(data.direccion);
        $('select[name="sexo"]').val(data.sexo.id);
        $('#myModalCliente').modal('show');      

    })
    //ELIMINAR CLIENTE
    .on('click', 'a[rel="delete"]', function(){
        
        var tr = tblCliente.cell($(this).closest('td, li')).index();
        var data = tblCliente.row( tr.row ).data();
        var parametros = new FormData();
        parametros.append('action', 'delete')
        parametros.append('id', data.id)
       
        submit_with_ajax(window.location.pathname,'Notificacion', 'Seguro de Eliminar?', parametros, function(){
            
            tblCliente.ajax.reload();
            //getData();
        });      

    });


//MUESTRA EL MODAL
    $('#myModalCliente').on('shown.bs.modal', function(){
        //$('form')[0].reset();
    });






    $('form').on('submit', function (e){
        e.preventDefault();
        //var parametros = $(this).serializeArray();
        var parametros = new FormData(this);
       
        submit_with_ajax(window.location.pathname,'Notificacion', 'Seguro de Realizar la siguiente accion?', parametros, function(){
            $('#myModalCliente').modal('hide');
            tblCliente.ajax.reload();
            //getData();
        });
        
    });
});