
if (typeof jQuery === "undefined") { throw new Error("ode-datatable requires jQuery") }

+function ($) { "use strict";

    var hideTextClass = " text-hide";
    $.fn.dataTableExt.oStdClasses.sPageFirst += hideTextClass;
    $.fn.dataTableExt.oStdClasses.sPagePrevious += hideTextClass;
    $.fn.dataTableExt.oStdClasses.sPageNext += hideTextClass;
    $.fn.dataTableExt.oStdClasses.sPageLast += hideTextClass;

    $('.datatable-listing').each(function() {

        var datatable$ = $(this);

        var ajaxSource = datatable$.attr('data-source');

        datatable$.dataTable({
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": ajaxSource,
            "aaSorting": [[0, "desc"]],
            "bFilter": false,
            "bPaginate": true,
            "sPaginationType": "full_numbers",
            "oLanguage": {
                "sUrl": "/static/dataTables.french.txt"
            }
        });
    });

    $('.datatable-delete-rows').on('click', function(event) {
        event.preventDefault();
        var dataSource = $(this).attr('data-source');

        var idsToDelete = [];

        $(dataSource).find(':checked').each(function() {
            var idToDelete = $(this).attr('data-id');
            idsToDelete.push(
                {'name': 'id_to_delete', 'value': idToDelete});
        });

        var urlToCall = $(this).attr('href');
        var postValues = $.param(idsToDelete);

        $.post(urlToCall, postValues, function(data) {
            // When work is done, reload current page
            // Dont use reload() js function, as this page also contains form.
            // You will have a browser "resend data" alert if you try to
            // delete a source just after having added it
            location.href = window.location.href;
        }).fail(function(data){
            alert("Un problème est apparu lors de la suppression d'une donnée. Contactez l'administrateur pour plus d'informations.");
        });
    });

}(jQuery);