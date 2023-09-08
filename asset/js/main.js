/*!
 * App functionalities.
 */

// Global namespace.
var App = App || {};

(function($) {
  App.Init= function() {
    $('.sidenav').sideNav();
    $('.tap-target').tapTarget('open');
    $(".button-collapse").sideNav();
    $('select').material_select('destroy');
  }
})(jQuery);