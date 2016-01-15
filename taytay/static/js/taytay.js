/* globals jQuery */
(function ($) {
    'use strict';

    function bindPagination() {
        $('.pagination a').on('click', function (e) {
            e.preventDefault();
            var link = $(this),
                wrapper = link.parent('.pagination');
            $.get(link.attr('href')).done(function (html) {
                link.fadeOut(400, function () {
                    wrapper.before(html);
                    wrapper.remove();
                    bindPagination();
                });
            });
        });
    }

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
        bindPagination();
    });
})(jQuery);
