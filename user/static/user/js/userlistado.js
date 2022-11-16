$(function (){
    $('#tbluser').DataTable({
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
            {"data": "full_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "imagen"},
            {"data": "groups"},
            {"data": "id"},
        ], columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return '<img src="'+row.imagen+'" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';

                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var html = '';
                    $.each(row.groups, function (key, value){
                        html+='<span class="badge bg-success">'+value.name+'</span> '
                    })
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/usuarios/editar/'+row.id+'/" class="btn btn-info"><i class="bi bi-pencil-square"></i></a> ';
                    buttons += '<a href="/usuarios/eliminar/'+row.id+'/" class="btn btn-danger"><i class="bi bi-trash-fill"></i></a>';
                    return buttons;

                }
            },
            
            
        ],
        initComplete: function(settings, json){
            
        }
    });

    
});