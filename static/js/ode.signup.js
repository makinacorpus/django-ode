
if (typeof jQuery === "undefined") { throw new Error("ode-datatable requires jQuery") }

+function ($) {
    "use strict";

    $('#id_organization_list').change(function() {
	if ($(this).val())
	    $('#organization-details').collapse('hide');
	else
	    $('#organization-details').collapse('show');
    });

}(jQuery);