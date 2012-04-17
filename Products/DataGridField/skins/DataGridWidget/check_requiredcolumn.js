/**
 * DataGridField checking of required columns
 * Columns with the HTML 5 attribute "data-required" must be filled
 */

if (!jQuery.DataGridField) {
	jQuery.DataGridField = {};
	(function($) {
		$(document).ready(function() {
			$('form[name=edit_form]').submit(function(event) {
				$('.dataGridError').removeClass('dataGridError');
				var $form = $(this);
				var firstEmpyField = null;
				$('td[data-required]', $form).each(function() {
					var $cell = $(this);
					var $input = $(':input', $cell);
					if (!$input.val() && !firstEmpyField) {
						firstEmpyField = $input
						event.preventDefault();
						$input.addClass('dataGridError')
							.val($('.dataGridRequiredFieldMessage:first').text()).focus();
						$('input[type="submit"]', $form).addClass('allowMultiSubmit');
					}
				});
			});
		});
	})(jQuery);
}


