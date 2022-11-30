var tblventa;

function format(d) {
    console.log(d);
    var html = '<table class="table table-warning">';
    html += '<thead class="table-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html+='<tr>'
        html+='<td>'+value.prod.nombre+'</td>'
        html+='<td>'+value.prod.categoria.nombre+'</td>'
        html+='<td>'+value.precio+'</td>'
        html+='<td>'+value.cantidad+'</td>'
        html+='<td>'+value.subtotal+'</td>'
        html+='</tr>';
    });
    html += '</tbody>';
    return html;
}



$(function () {
    tblventa = $('#lista_ventas').DataTable({
        //responsive: true,
        scrollX: true,
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
            {
                "className":    'details-control',
                "orderable":    false,
                "data":     null,
                "defaultContent": ''
            }, 
            {"data": "cliente.full_name"},
            {"data": "f_registro"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/ventas/eliminar/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="bi bi-trash-fill"></i></a> ';
                    buttons += '<a href="/ventas/actualizar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="bi bi-pencil-square"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="bi bi-search"></i></a> ';
                    buttons += '<a href="/ventas/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="bi bi-filetype-pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });



//LISTAR FACTURAS
    $('#lista_ventas tbody')
        .on('click', 'a[rel="details"]', function(){
            var tr = tblventa.cell($(this).closest('td, li')).index();
            var data = tblventa.row(tr.row).data();
            //console.log(data);
        
            $('#detalle_ventas').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [                     
                    {"data": "prod.nombre"},
                    {"data": "prod.categoria.nombre"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3,],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
        
                }
            });
   
            $('#detalleModal').modal('show');
            
    })

    //TABLA DETALLES
    .on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = tblventa.row(tr);
        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

    
    
});