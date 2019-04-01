(function($) {
    "use strict";
    $(document).ready(function() {
        var mymap = L.map('map').setView([27.608421548604188, 85.3887634444982], 11);
        //  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        //     subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(mymap);

        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(mymap);
                
        // L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //   attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        //   subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(mymap);
    });
})(jQuery);

