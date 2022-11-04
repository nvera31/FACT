var tblCliente;

$(function (){
    tblCliente = $('#dataPro').DataTable({
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
            {"data": "categoria.nombre"},
            {"data": "imagen"},
            {"data": "pvp"},
            {"data": "id"},
        ], columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(2);
                }
            },            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/cliente/actualizar/'+row.id+'/"  class="btn btn-info"><i class="bi bi-pencil-square"></i></a> ';
                    buttons += '<a href="/cliente/eliminar/'+row.id+'/"  class="btn btn-danger"><i class="bi bi-trash-fill"></i></a>';
                    return buttons;

                }
            },
            
        ],
        initComplete: function(settings, json){
            
        }
    });
});
