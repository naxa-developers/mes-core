(function($) {
    "use strict";
    $(document).ready(function() {
        var map = L.map('map').setView([28.1281, 84.4392], 10.32);

        var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
          maxZoom: 20,
          subdomains:['mt0','mt1','mt2','mt3']
        });
        var googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
          maxZoom: 20,
          subdomains:['mt0','mt1','mt2','mt3']
        });
        var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
          maxZoom: 20,
          subdomains:['mt0','mt1','mt2','mt3']
        });
        var googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
          maxZoom: 20,
          subdomains:['mt0','mt1','mt2','mt3']
        });

        //for changing the layer(layer switcher)
        var baseLayers = {
            "OpenStreetMap": osm,
            "Google Streets": googleStreets,
            "Google Hybrid": googleHybrid,
            "Google Satellite": googleSat,
            "Google Terrain": googleTerrain,
        };

        map.addLayer(osm);
        var layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);

        var beneficiaries = $.ajax({
            url: '/core/get-map-data/',
            type: 'GET',
            data: {},
            dataType: "json",

            success: function(result){
                console.log(result);
                var map_data = result;
            }
        });

        $.when(beneficiaries).done(function(){
            //add geojson file for informal settlements point
                var name = new L.geoJson(beneficiaries.responseJSON, {
                pointToLayer: function(feature,Latlng)
                {
                    var icons=L.icon({
                      iconSize: [20, 22],
                      iconAnchor: [10, 22],
                      popupAnchor:  [2, -24],

                      iconUrl:"https://unpkg.com/leaflet@1.0.3/dist/images/marker-icon.png"
                    });
                    var marker = L.marker(Latlng,{icon:icons});
                    return marker;
                },
                onEachFeature: function (feature, layer) {
                    var popUpContent = "";
                    popUpContent += '<table style="width:100%;" id="CHAL-popup" class="popuptable">';
                    for (var data in layer.feature.properties) {
                        if(data == 'progress'){
                            popUpContent += "<tr>" + "<td>" + data + "</td>" + "<td>" + "  " + layer.feature.properties[data] + '%'  + "</td>" + "</tr>";
                        }
                        else{
                            popUpContent += "<tr>" + "<td>" + data + "</td>" + "<td>" + "  " + layer.feature.properties[data] + "</td>" + "</tr>";
                        }
                    }
                    popUpContent += '</table>';

                    //layer.bindLabel("CHAL");

                    layer.bindPopup(L.popup({
                        closeOnClick: true,
                        closeButton: true,
                        keepInView: true,
                        autoPan: true,
                        maxHeight: 200,
                        minWidth: 250
                    }).setContent(popUpContent));
                }
            }).addTo(map);
        });

            
    
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
          subdomains: 'abcd',
            maxZoom: 19
        }).addTo(map);
    });
})(jQuery);

