jQuery.fn.filterByText = function(textbox, selectSingleMatch) {
  return this.each(function() {
    var select = this;
    var options = [];
    $(select).find('option').each(function() {
      options.push({value: $(this).val(), text: $(this).text()});
    });
    $(select).data('options', options);
    $(textbox).bind('change', function() {
      var options = $(select).empty().scrollTop(0).data('options');
      var search = $.trim($(this).val());
      var regex = new RegExp(search,'gi');

      $.each(options, function(i) {
        var option = options[i];
        if(option.value.match(regex) !== null) {
          $(select).append(
             $('<option>').text(option.text).val(option.value)
          );
        }
      });
      if (selectSingleMatch === true &&
          $(select).children().length === 1) {
        $(select).children().get(0).selected = true;
      }
    });
  });
};

jQuery.fn.facetedFilterDeactivated = function() {
  return this.each(function() {
    var select = this;
    var content = $(select).html();
    $(Faceted.Events).bind(Faceted.Events.FORM_DO_QUERY, function(evt, data) {
      if ($(select).attr('id') !== data.wid) {
        $(select).html(content);
      }
    });

    $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function() {
      $(select).find('option[disabled="disabled"]').remove();
    });
  });
};


jQuery(document).ready(function($) {
  var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
  if (isSafari === true) {
    $('select.faceted_select').facetedFilterDeactivated();
  }

  $('select#form-widgets-category').filterByText($('select#form-widgets-fbk_formation'), true);
  $('select#form-widgets-fbk_formation').trigger('change');

});
