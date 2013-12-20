
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

    function toIsoString(moment) {
        var utc_timestamp = Date.UTC(
            moment.year(),
            moment.month(),
            moment.date(),
            moment.hours(),
            moment.minutes(),
            moment.seconds()
        );
        return new Date(utc_timestamp).toISOString();
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
	    $('#start_time').val(toIsoString(start));
	    $('#end_time').val(toIsoString(end));
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
	    $('#publication_start').val(toIsoString(start));
	    $('#publication_end').val(toIsoString(end));
	}
    );

}(jQuery);
