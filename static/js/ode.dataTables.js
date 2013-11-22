
if (typeof jQuery === "undefined") { throw new Error("ode-datatable requires jQuery") }

+function ($) { "use strict";

	var hideTextClass = " text-hide";
	$.fn.dataTableExt.oStdClasses.sPageFirst += hideTextClass;
	$.fn.dataTableExt.oStdClasses.sPagePrevious += hideTextClass;
	$.fn.dataTableExt.oStdClasses.sPageNext += hideTextClass;
	$.fn.dataTableExt.oStdClasses.sPageLast += hideTextClass;

	$(document).find('.datatable-listing').each(function() {

		var datatable$ = $(this);
	    
	    var ajaxSource = datatable$.attr('data-source');
	    
	    datatable$.dataTable({
	        "bProcessing": true,
	        "bServerSide": true,
	        "sAjaxSource": ajaxSource,
	        "aaSorting": [[0, "desc"]],
	        "bFilter": false,
			"sPaginationType": "full_numbers",
			"oLanguage": {
				"sUrl": "/static/dataTables.french.txt"
			}
	    });
	});

}(jQuery);