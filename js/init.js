(function ($) {
    $.browser = {};
    $(function () {

        $('.button-collapse').sideNav();
        $('.parallax').parallax();
        $('.collapsible').collapsible();
        $('.drag-target').next().hide();
        $('.hiddendiv').prev().hide();

        jQuery.browser.msie = false;
        jQuery.browser.version = 0;
        if (navigator.userAgent.match(/MSIE ([0-9]+)\./)) {
            jQuery.browser.msie = true;
            jQuery.browser.version = RegExp.$1;
        }

        $("a.img-fancy-box, a.img-fancy-box-group").fancybox({
            helpers : {
                title : {
                    type : 'inside'
                },
                overlay : {
                    css : {
                        'background' : 'rgba(238,238,238,0.85)'
                    }
                }
            },
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space