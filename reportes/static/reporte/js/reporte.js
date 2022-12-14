var date_ranger = null;
var date_now = new moment().format('YYYY-MM-DD')

function generar_reporte(){
    var parametros = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,

    };

    if(date_ranger !== null){
        parametros['start_date']= date_ranger.startDate.format('YYYY-MM-DD');
        parametros['end_date']= date_ranger.endDate.format('YYYY-MM-DD');
    }


    $('#tblreporte').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parametros,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="bi bi-file-earmark-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="bi bi-file-earmark-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','20%','15%','15%','15%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creaci??n: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['p??gina ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columnDefs: [
            {
                targets: [-1,-2,-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return '$'+parseFloat(data).toFixed(2)

                }
            },
        ],
        initComplete: function(settings, json){
            
        }
    });
    
}




$(function () {
    $('input[name="date_ranger"]').daterangepicker({
        locale : {
            format: 'YYYY-MM-DD',
            applyLabel: 'Aplicar',
            cancelLabel: 'Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker){
        date_ranger = picker;
        generar_reporte();
    }).on('cancel.daterangepicker', function (ev, picker){
        $(this).data('daterangepicker').setStartDate(date_now)
        $(this).data('daterangepicker').setEndDate(date_now)
        date_ranger = picker;
        generar_reporte();
        
    })
    
    generar_reporte();
});


