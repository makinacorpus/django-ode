
if (typeof jQuery === "undefined") { throw new Error("ode-datatable requires jQuery") }

+function ($) { "use strict";

	$(document).find('.datatable-listing').each(function() {

		var datatable$ = $(this);
	    
	    var ajaxSource = datatable$.attr('data-source');
	    
	    datatable$.dataTable({
	        // ...
	        "bProcessing": true,
	        "bServerSide": true,
	        "sAjaxSource": ajaxSource,
	        "aaSorting": [[0, "desc"]],
	    });
	});

}(jQuery);