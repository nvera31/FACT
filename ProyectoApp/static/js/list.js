$(function (){
    $('#data').DataTable({
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
            {"data": "desc"},
            {"data": "opc"},
        ], columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/categoria/edit/'+row.id+'/" class="btn btn-info"><i class="bi bi-pencil-square"></i></a> ';
                    buttons += '<a href="/categoria/delete/'+row.id+'/" class="btn btn-danger"><i class="bi bi-trash-fill"></i></a>';
                    return buttons;

                }
            },
        ],
        initComplete: function(settings, json){
            
        }
    });
});