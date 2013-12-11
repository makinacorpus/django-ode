
if (typeof jQuery === "undefined") { throw new Error("ode-datatable requires jQuery") }

+function ($) {
    "use strict";

    moment.lang('fr');

    var locale = {
	applyLabel: 'Accepter',
        cancelLabel: 'Annuler',
        fromLabel: 'Du',
        toLabel: 'Au',
        weekLabel: 'S',
        customRangeLabel: 'Période personnalisée',
        daysOfWeek: moment()._lang._weekdaysMin.slice(),
        monthNames: moment()._lang._monthsShort.slice(),
        firstDay: 1
    };

    $('#daterange').daterangepicker(
	{
	    format: 'DD/MM/YYYY',
	    showDropdowns: false,
	    timePicker: true,
	    timePickerIncrement: 15,
	    timePicker12Hour: false,
	    locale: locale
	},
	function(start, end) {
	    $('#start_time').val(start.toISOString());
	    $('#end_time').val(end.toISOString());
	}
    );

    $('#daterange_publication').daterangepicker(
	{
	    format: 'DD/MM/YYYY',
	    showDropdowns: false,
	    timePicker: true,
	    timePickerIncrement: 15,
	    timePicker12Hour: false,
	    locale: locale
	},
	function(start, end) {
	    $('#publication_start').val(start.toISOString());
	    $('#publication_end').val(end.toISOString());
	}
    );

}(jQuery);