var tblCliente;
var tProductos;
var ventas ={
    items : {
        cliente: '',
        f_registro : '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        productos : []
    },
    calcular_factura: function(){
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.productos, function(pos, dict){
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal+=dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacal"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function(item){
        this.items.productos.push(item);
        this.list();
    },

    list: function (){
        this.calcular_factura();
        tProductos = $('#tblProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "categoria.nombre"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},

            ], columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row){                        
                        return '<a rel="remove" class="btn btn-danger"><i class="bi bi-trash-fill"></i></a>';
                        
    
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row){                        
                        return '$'+parseFloat(data).toFixed(2);
                        
    
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row){                        
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cantidad+'">';
                        
    
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row){                        
                        return '$'+parseFloat(data).toFixed(2);
                        
    
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max:100000000000,
                    step: 1
                });
            },
            initComplete: function(settings, json){
                
            }
        });
    },

};

//DATABLE PRODUCTOS
// $(function (){
//     tblCliente = $('#tblProductos').DataTable({
//         responsive: true,
//         autoWidth: false,
//     });
// });

//ALERTA VACIAR
function alert_action(title,content,callback){
    $.confirm({
        theme: 'bootstrap',
        title: title,
        icon: 'bi bi-info-circle',
        content: content,
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
                    callback();
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


//BUSCAR PRODUCTOS
$(function (){
    $( 'input[name="search"]' ).autocomplete({
        source: function(request, response){
            $.ajax({
                //TRABAJA CON LA VISTA ACTUAL
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_productos',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus+':'+errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function( event, ui){
            event.preventDefault();
            console.clear();
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.00;            
            console.log(ventas.items);

            ventas.add(ui.item);

            $(this).val('');
        }
        });

//VACIA LA TABLA
        $('.btnRemove').on('click', function(){
            if(ventas.items.productos.length === 0) return false;
            alert_action('Notificacion', 'Seguro de Vaciar la lista?', function(){
                ventas.items.productos = []
                ventas.list();
            });
            
        });

//EVENTO CANTIDAD, CALCULA LOS SUBTOTAL
    $('#tblProductos tbody')
        .on('click', 'a[rel="remove"]', function(){
            var tr = tProductos.cell($(this).closest('td, li')).index();
            alert_action('Notificacion', 'Seguro de Eliminar el producto de la lista?', function(){
                ventas.items.productos.splice(tr.row, 1)
                ventas.list();
            });
        })
        .on('change', 'input[name="cant"]', function(){
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tProductos.cell($(this).closest('td, li')).index();
        ventas.items.productos[tr.row].cantidad = cant;
        ventas.calcular_factura();
        $('td:eq(5)',tProductos.row(tr.row).node()).html('$'+ventas.items.productos[tr.row].subtotal.toFixed(2));
        
   
    });

});


