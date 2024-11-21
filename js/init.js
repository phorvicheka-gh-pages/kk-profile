const { OverlayScrollbars, ClickScrollPlugin } = OverlayScrollbarsGlobal;

// optional: use the ClickScrollPlugin to make the option "scrollbars.clickScroll: true" available
OverlayScrollbars.plugin(ClickScrollPlugin);

OverlayScrollbars(document.body, {
    scrollbars: {
        clickScroll: true,
        autoHide: 'scroll',
        autoHideDelay: 1000,
        dragScroll: true,
    },
    scroll: {
        smooth: true,        // Enable smooth scrolling
        smoothTime: 100,     // Duration of the smooth animation in ms
        smoothDistribution: 0.5,  // Distribution of the scroll animation (0 to 1)
    }
});


(function ($) {
    // Loading screen handler
    $(window).on('load', function () {
        // Hide the loading screen when everything is loaded
        const loadingScreen = $('#loading-screen');
        const content = $('#main-content');

        // Hide the loading screen and show the content
        loadingScreen.hide();
    });

    // Initialize Materialize and scroll handlers
    $(document).ready(function () {
        // Initialize Materialize components
        $('.button-collapse').sideNav({
            closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
            draggable: true // Choose whether you can drag to open on touch screens
        });
        $('.collapsible').collapsible();

        // Try to initialize parallax again for safety
        $('.parallax').parallax();

        // Scroll to top functionality
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.scrollToTop').fadeIn();
            } else {
                $('.scrollToTop').fadeOut();
            }
        });

        $('.scrollToTop').click(function () {
            $('html, body').animate({
                scrollTop: 0
            }, 800);
            return false;
        });

        // Initialize typed effects
        var greetingTyped = new Typed('#greeting', {
            strings: ["Hello 👋, I'm <span class='white-text'><b>Vicheka PHOR</b>.</span>"],
            typeSpeed: 30,
            // loop: false,
            showCursor: false,
            // smartBackspace: false
        });

        var professionTyped = new Typed('#profession', {
            strings: ["Researcher &amp; Software Engineering"],
            typeSpeed: 50,
            // loop: false,
            // startDelay: 2000,
            showCursor: false,
            // smartBackspace: false
        });

        // Calculate durations
        $('.label-date').each(function() {
            const text = $(this).text().trim();

            // Skip empty or invalid text
            if (!text || (!text.includes("–") && !text.includes("-"))) {
                return;
            }

            if (!text.includes("·")) {
                const durationText = getDurationText(text);
                if (durationText) {
                    $(this).text(text + ` · (${durationText})`);
                }
            }
        });

        // Tooltips
        const $tooltipContainer = $('.tooltip-container');
        
        $('.tech-item').hover(
            function() { // mouseenter
                const $item = $(this);
                const $tooltip = $item.find('.tech-details');
                
                if ($tooltip.length) {
                    const rect = this.getBoundingClientRect();
                    const $clonedTooltip = $tooltip.clone();
                    
                    $clonedTooltip.css({
                        'top': rect.top + 'px',
                        'left': (rect.left + (rect.width / 2)) + 'px',
                        'transform': 'translate(-50%, -105%)'
                    });
                    
                    $tooltipContainer.empty().append($clonedTooltip);
                }
            },
            function() { // mouseleave
                $tooltipContainer.empty();
            }
        );

        // Initialize PDF modal
        var $modal = $('#pdf-modal');
        var $iframe = $('#pdf-viewer');
        var $closeBtn = $('.pdfModal-close');

        // Function to open the modal
        function openModal(event) {
            event.preventDefault();
            var pdfUrl = $(this).attr('href');
            $iframe.attr('src', pdfUrl);
            $modal.show();
            $('body').addClass('pdfModal-open');
        }

        // Function to close the modal
        function closeModal() {
            $modal.hide();
            $iframe.attr('src', '');
            $('body').removeClass('pdfModal-open');
        }

        // Attach modal event handlers
        $('.pdf-link').on('click', openModal);
        $closeBtn.on('click', closeModal);
        $modal.on('click', function(event) {
            if (event.target === this) {
                closeModal();
            }
        });

        // Initialize Fancybox
        $("a.img-fancy-box, a.img-fancy-box-group").fancybox({
            helpers: {
                title: {
                    type: 'inside'
                },
                overlay: {
                    css: {
                        'background': 'rgba(238,238,238,0.85)'
                    }
                }
            }
        });
    });

    // Helper Functions for Date Calculations
    function getDurationText(dateRange) {
        const [start, end] = dateRange.split(/[–-]/).map(part => part.trim());
        const startDate = parseDate(start);
        const endDate = end === "Present" ? new Date() : parseDate(end);

        if (!startDate || !endDate) {
            return null;
        }

        const { years, months } = calculateDuration(startDate, endDate);

        if (years < 0 || months < 0) {
            return null;
        }

        return formatDuration(years, months);
    }

    function parseDate(dateStr) {
        const [month, year] = dateStr.split(" ");
        const monthIndex = new Date(`${month} 1`).getMonth();
        return isNaN(monthIndex) || isNaN(year) ? null : new Date(year, monthIndex, 1);
    }

    function calculateDuration(start, end) {
        let years = end.getFullYear() - start.getFullYear();
        let months = end.getMonth() - start.getMonth();

        if (months < 0) {
            years -= 1;
            months += 12;
        }

        if (end.getDate() >= start.getDate()) {
            months += 1;
        }

        if (months >= 12) {
            years += 1;
            months -= 12;
        }

        return { years, months };
    }

    function formatDuration(years, months) {
        const yearText = years > 0 ? `${years} yr${years > 1 ? "s" : ""}` : "";
        const monthText = months > 0 ? `${months} mo${months > 1 ? "s" : ""}` : "";
        return [yearText, monthText].filter(Boolean).join(" ");
    }

})(jQuery);
