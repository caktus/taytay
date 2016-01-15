/* globals jQuery */
(function ($) {
    'use strict';

    $(document).ready(function(){
        $('.parallax').parallax();
        $('select').material_select();
        $('#create-button').click(function(e){
            e.preventDefault();
            var button = $(this),
                form = button.next('form');
            button.fadeOut(200, function(){
                form.fadeIn(400);
            });
        });
    });
})(jQuery);
