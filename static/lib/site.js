var site = (function ($) {
// local variables

// Put site specific properties (functions or variables) here.  The property
// p will be accessible outside as site.p.
return {

  set_initial_focus:  function () {
    // TODO: may want to filter disabled fields
    var input = $('form').find('input[type=text],textarea,select').filter(':visible:first');
    input.focus().select();
  }

})(jQuery));
