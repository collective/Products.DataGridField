/**
 * DataGridField checking of required columns
 * Columns with the HTML 5 attribute "data-required" must be filled
 */

if (!jQuery.DataGridField) {
	jQuery.DataGridField = {};
	
	(function($) {
		$(document).ready(function() {
			$('form[name=edit_form]').submit(function(event) {
				$("div.dataGridError").remove();
				var $form = $(this);
				var firstEmpyField = null;
				$('td[data-required]', $form).each(function() {
					var $cell = $(this);
					var $input = $(':input', $cell);
					if (!$input.val() && !firstEmpyField) {
						firstEmpyField = $input
						event.preventDefault();
						$('<div tabindex="-1" class="dataGridError error">ABCD</div>').prependTo($cell).focus();
					}
				});
			});
		});
	})(jQuery);
}


