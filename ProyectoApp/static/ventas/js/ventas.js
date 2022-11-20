var tblCliente;
var tProductos;
var tblBuscarPro;
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
        var fsubtotal = 0.00;
        var fiva = $('input[name="iva"]').val();
        $.each(this.items.productos, function(pos, dict){
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            fsubtotal+=dict.subtotal;
        });
        this.items.subtotal = fsubtotal;
        this.items.iva = this.items.subtotal * fiva;
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

//BUSQUEDA CON IMAGEN
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        '<b>Categoría:</b> ' + repo.categoria.nombre + '<br>' +
        '<b>PVP:</b> <span class="badge text-bg-warning">$'+repo.pvp+'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}



//DATABLE PRODUCTOS
// $(function (){
//     tblCliente = $('#tblProductos').DataTable({
//         responsive: true,
//         autoWidth: false,
//     });
// });

//ALERTA VACIAR
function alert_action(title,content,callback, cancel){
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
                    cancel();
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
    
//BUSQUEDA CLIENTES
    $('select[name="cliente"]').select2({
        allowClear: true,
        ajax:{
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params){
                var query = {
                    term: params.term,
                    action: 'search_clientes'
                }
                return query;
            },
            processResults: function (data){
                return {
                    results: data
                }
            },

        },
        placeholder: 'busqueda',
        minimumInputLength: 1,
    })

//AGREGAR CLIENTE
    $('.btnAddCliente').on('click', function (){
        $('#ModalCliente').modal('show');
    });

    //LIMPIAR MODAL
    $('#ModalCliente').on('hidden.bs.modal', function(e){
        $('#frmCliente').trigger('reset');
    });
    

    $('#frmCliente').on('submit', function (e){
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'create_cliente');

        submit_with_ajax(window.location.pathname,'Notificacion', 'Seguro de crear cliente?', parametros, function (response) {
            //console.log(response)
            var newOption = new Option(response.full_name, response.id, false, true);
            $('select[name="cliente"]').append(newOption).trigger('change');
            $('#ModalCliente').modal('hide');
            
        });  
    
    });   


//VACIA LA TABLA
        $('.btnRemove').on('click', function(){
            if(ventas.items.productos.length === 0) return false;
            alert_action('Notificacion', 'Seguro de Vaciar la lista?', function(){
                ventas.items.productos = []
                ventas.list();
            }, function(){

            });
            
        });

//EVENTO CANTIDAD, CALCULA LOS SUBTOTAL
    $('#tblProductos tbody')
        .on('click', 'a[rel="remove"]', function(){
            var tr = tProductos.cell($(this).closest('td, li')).index();
            alert_action('Notificacion', 'Seguro de Eliminar el producto de la lista?', function(){
                ventas.items.productos.splice(tr.row, 1)
                ventas.list();
            }, function(){

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

    $('.btnLimpiar').on('click', function(){
        $('input[name="search"]').val('').focus();
    });

    //MODAL DE BUSQUEDA DE PRODUCTOS
    $('.btnBuscarPro').on('click', function(){
        tblBuscarPro = $('#tblBuscarProd').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_productos',
                    'term': $('input[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
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
                        return '<a rel="add" class="btn btn-success"><i class="bi bi-plus-circle-fill"></i></a> ';
    
                    }
                },
                
            ],
            initComplete: function(settings, json){
                
            }
        });
        $('#ModalProducto').modal('show');

    });


    //AGREGAR DEL MODAL PRODUCTO A LA LISTA
    $('#tblBuscarProd tbody')
        .on('click', 'a[rel="add"]', function(){
            console.clear();
            var tr = tblBuscarPro.cell($(this).closest('td, li')).index();
            var producto = tblBuscarPro.row(tr.row).data();
            producto.cantidad = 1;
            producto.subtotal = 0.00; 
            ventas.add(producto);
            
   
    });

//EVENTO SUBMIT AGREGAR VENTAS
    $('frmVenta').on('submit', function (e){
        e.preventDefault();

        if(ventas.items.productos.length === 0){
            errores('Debe tener items en Detalle');
            return false;
        }

        ventas.items.f_registro = $('input[name="f_registro"]').val();
        ventas.items.cliente = $('select[name="cliente"]').val();

        var parametros = new FormData();
        parametros.append('action', $('input[name="action"]').val());
        parametros.append('ventas', JSON.stringify(ventas.items));

        submit_with_ajax(window.location.pathname,'Notificacion', 'Seguro de Realizar la siguiente accion?', parametros, function (response) {
            
            alert_action('Notificacion', 'Desea imprimir factura?', function(){
                window.open('/ventas/factura/pdf/'+ response.id + '/', '_blank');
                location.href = '/ventas/listar/';
            }, function(){
                location.href = '/ventas/listar/';
            });
            
            
        });  
    
    });   

    
    
    // $('select[name="search"]').select2({
    //     language: 'es',
    //     allowClear: true,
    //     ajax:{
    //         delay: 250,
    //         type: 'POST',
    //         url: window.location.pathname,
    //         data: function (params){
    //             var query = {
    //                 term: params.term,
    //                 action: 'search_productos'
    //             }
    //             return query;
    //         },
    //         processResults: function (data){
    //             return {
    //                 results: data
    //             }
    //         },

    //     },
    //     placeholder: 'Ingrese Descripcion',
    //     minimumInputLength: 1,
    //     templateResult: formatRepo,
    // }).on('select2:select', function(e){
    //     var data = e.params.data;
    //     data.cantidad = 1;
    //     data.subtotal = 0.00;            
    //     ventas.add(data);
    //     $(this).val('').trigger('change.select2');
    
    // });
    
     ventas.list();

});


