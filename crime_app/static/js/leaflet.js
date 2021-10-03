// This code is used to generate the leaflet map.

// Function to determine the circle color.
function circleColor(qty)  {
    switch (true) {
    case (qty >= 10000):
        return "#ff0000";
    case (qty > 5000):
        return "#ff8000";
    case (qty > 2000):
        return "#ffbf00";
    case (qty > 1000):
        return "#ffff00";
    case (qty > 500):
        return "#bfff00";
    case (qty > 200):
        return "#66ff8c";
    case (qty > 0):
        return "#CDFFD9";
    
    }

}

// Function to determine the legend color.
function legendColor(d) {
    return d > 10000 ? '#ff0000' :
           d > 5000 ?  '#ff8000' :
           d > 2000  ? '#ffbf00' :
           d > 1000  ? '#ffff00' :
           d > 500  ? '#bfff00':
           d > 200  ? '#66ff8c':
                    '#CDFFD9';

}

// Reading in the map route and then building the maps.
d3.json("/map_2021").then(function(data) {

    // Creating an outdoor layer.
    var outdoorLayer =L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 12,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: "pk.eyJ1IjoibWpqb2huc29uOTQiLCJhIjoiY2tzcGx5eTI0MDRrMjJvcTR5dXJvYW9lbSJ9._mU94YuzAPKe6OVDEhkzKg"
      });
    
    //   Creating a satallite layer.
    var satelliteLayer = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/satellite-v9",
        accessToken: "pk.eyJ1IjoibWpqb2huc29uOTQiLCJhIjoiY2tzcGx5eTI0MDRrMjJvcTR5dXJvYW9lbSJ9._mU94YuzAPKe6OVDEhkzKg"
        });
    

    // Creating the circle markers and popup box for 2021.
    var incidents = new L.LayerGroup();
    for (var i = 0; i < data.length; i++) {
            L.circle([data[i].latitude, data[i].longitude], { 
            weight: 0.4,
            color: "black",
            fillColor: circleColor(data[i].incidents),
            fillOpacity: 0.7,
            radius: 800, 
            }).bindPopup("<strong>" + "Year 2021: " +  data[i].suburb + "</strong>" +
            "<br>"+"No. of incidents: " + data[i].incidents).addTo(incidents);}

            
    // Reading in the 2020 route and creating the circle markers and popup box for 2020.
    var incidents2020 = new L.LayerGroup();
    d3.json("/map_2020").then(function(data) {

    
    for (var i = 0; i < data.length; i++) {
            L.circle([data[i].latitude, data[i].longitude], { 
            weight: 0.4,
            color: "black",
            fillColor: circleColor(data[i].incidents),
            fillOpacity: 0.7,
            radius: 800, 
            }).bindPopup("<strong>" + "Year 2020: " +  data[i].suburb + "</strong>" +
            "<br>"+"No. of incidents: " + data[i].incidents).addTo(incidents2020);}

        })

    // Reading in the 2015 route and creating the circle markers and popup box for 2015.
    

    // Creating the basemaps.
    var baseMaps = {
        "Outdoors": outdoorLayer,
        "Satellite": satelliteLayer
        }

    // Creating the overlaymaps.
    var overlayMaps = {
        "2021 Incidents": incidents,
        "2020 Incidents": incidents2020
        };

    
    // Creating the intial map.
    var myMap = L.map("map", {
            center: [-37.840935, 144.946457],
            zoom: 10,
            layers:[outdoorLayer, incidents]
          });


    // Adding the control layers.
    L.control.layers(baseMaps).addTo(myMap);

    // Adding the overlays as another control layer - more practical to be able to toggle between years rather than overlay. It creates a better visualisation.
    L.control.layers(overlayMaps,null,{collapsed:false}).addTo(myMap);

    // Creating the legend.
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        
        var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 200, 500, 1000, 2000, 5000, 10000],
        labels = [];
        
            for (var i = 0; i < grades.length; i++) {
                div.innerHTML += 
                    '<div><i style="background:' + legendColor(grades[i] + 1) + '"></i> ' + 
                    grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+' +'</div>');
        }
        
        return div;
        };
        
    // Adding the legend to the map.
      legend.addTo(myMap);
      

})



