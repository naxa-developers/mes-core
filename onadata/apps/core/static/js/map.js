(function($) {
    "use strict";
    $(document).ready(function() {
        // var mymap = L.map('map').setView([27.608421548604188, 85.3887634444982], 11);
        //  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        //     subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(mymap);

        // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        //     subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(mymap);
        
        // var LeafIcon = L.Icon.extend({
        //     options: {
        //         shadowUrl: 'leaf-shadow.png',
        //         iconSize:     [38, 95],
        //         shadowSize:   [50, 64],
        //         iconAnchor:   [22, 94],
        //         shadowAnchor: [4, 62],
        //         popupAnchor:  [-3, -76]
        //     }
        // });
        // var greenIcon = new LeafIcon({iconUrl: 'leaf-green.png'}),
        // redIcon = new LeafIcon({iconUrl: 'leaf-red.png'}),
        // orangeIcon = new LeafIcon({iconUrl: 'leaf-orange.png'});

        // L.icon = function (options) {
        //     return new L.Icon(options);
        // };

        

        // var planes = [
        //     ["7C6B07",27.67658, 85.31417],
        //     ["7C6B38",27.67988, 85.27544],
        //     ["7C6CA1",27.62979, 85.52138],
        //     ["7C6CA2",-40.98585,174.50659],
        //     ["C81D9D",-40.93163,173.81726],
        //     ["C82009",-41.5183,174.78081],
        //     ["C82081",-41.42079,173.5783],
        //     ["C820AB",-42.08414,173.96632],
        //     ["C820B6",-41.51285,173.53274]
        //     ];
        var Gorkha = L.marker([28.28998, 84.68975]).bindPopup('<ul><li><label>Name :</label><span>House Construction</span></li> <li><label>Progress :</label><span>50%</span></li><li><label>Type :</label><span>Marginalized</span></li></ul>'),
            Dhading    = L.marker([27.86667, 84.91667]).bindPopup('<ul><li><label>Name :</label><span>Verification & Listing</span></li> <li><label>Progress :</label><span>40%</span></li><li><label>Type :</label><span>Marginalized</span></li></ul>'),
            Banepa    = L.marker([27.62979, 85.52138]).bindPopup('<ul><li><label>Name :</label><span>Husehold awareness & creation</span></li> <li><label>Progress :</label><span>20%</span></li><li><label>Type :</label><span>Marginalized</span></li></ul>'),
            Butwal    = L.marker([27.704004, 83.457504]).bindPopup('<ul><li><label>Name :</label><span>Finaliztion of house design</span></li> <li><label>Progress :</label><span>80%</span></li><li><label>Type :</label><span>Marginalized</span></li></ul>');

        var cities = L.layerGroup([Gorkha, Dhading, Banepa, Butwal]);
        
            // var mymap = L.map('map').setView([28.3973623 , 84.12576], 11);
           

            var map = L.map('map', {
                center: [28.3973623, 84.12576],
                zoom: 7,
                layers: [cities]
            });

            // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            //     subdomains: 'abcd',
            //     maxZoom: 19
            // }).addTo(map);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            // var baseMaps = {
            //     "Grayscale": grayscale,
            //     "Streets": streets
            // };
            
            var overlayMaps = {
                "Cities": cities
            };
            L.control.layers(overlayMaps).addTo(map);
            
    
        // L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //   attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        //   subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(mymap);
    });
})(jQuery);

