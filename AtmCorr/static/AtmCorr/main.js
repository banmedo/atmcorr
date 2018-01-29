var app = {}

/*=================== constants =========================*/
app.createConstants = function(){
  app.URL = {
    BASE : '/AtmCorr/',
    GETIMAGES : 'getimagelist'
  }
}


app.createFunctions = function(){
  app.setLoading = function(state){
    console.log("loading", state);
  }
  app.addLeafletCorners = function(){
    var corners = app.map._controlCorners,
        l = 'leaflet-',
        container = app.map._controlContainer;

    function createCorner(vSide, hSide) {
        var className = l + vSide + ' ' + l + hSide;

        corners[vSide + hSide] = L.DomUtil.create('div', className, container);
    }
    //createCorner('verticalcenter', 'left');
    //createCorner('verticalcenter', 'right');
    //createCorner('horizontalcenter','top');
    createCorner('horizontalcenter','bottom');
  }
  app.addDatePicker = function(){
    var DatePicker = L.Control.extend({
        onAdd: function (map) {
            var template = document.createElement('template');
            var html = "<input type=text id=datepicker readonly=true placeholder=Date  />";
            template.innerHTML = html.trim();
            return template.content.firstChild;
        }
    });

    app.datePicker =  new DatePicker({position:'topright'}).addTo(app.map);

    $("#datepicker").datepicker();
  }
  app.addSolarZenithPicker = function(){
    app.solarZenithSlider = L.control.slider(function(value) {
    			//initiae data fetch
			}, {
    		max: 90,
    		value: 75,
    		step:5,
    		size: '250px',
    		orientation:'vertical',
    		id: 'solar-zenith-slider'
		}).addTo(app.map);

  }

  app.addImageScroller = function(){
    var ImageScroller = L.Control.extend({
      onAdd: function(map){
        var template = document.createElement('template');
        var html = "<div class=leaflet-imagescroller>Select a date!</div>";
        template.innerHTML = html.trim();
        return template.content.firstChild;
      }
    });

    app.ImageScroller =  new ImageScroller({position:'horizontalcenterbottom'}).addTo(app.map);
  }

  app.addLayerToMap = function(id){
    app.setLoading(true);
    /*$.ajax({

    });*/
  }
}

app.initialize = function(){
  app.map = L.map('map').setView([28.115593833316762, 84.64141845703126], 8);

  L.tileLayer('https://api.mapbox.com/styles/v1/banmedo/ciiibvf1k0011alki4gp6if1s/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmFubWVkbyIsImEiOiJhSklqeEZzIn0.rzfSxO3cVUhghA2sJN378A').addTo(app.map);

  app.addLeafletCorners();
  app.addImageScroller();
  app.addDatePicker();
  app.addSolarZenithPicker();
}

app.addHandlers = function(){
  $("#datepicker").on('change', function(e){
    var date = $.datepicker.formatDate('yy-mm-dd',new Date(e.target.value));
    var bounds = app.map.getBounds();
    var params = {
      date:date,
      west: bounds.getWest(),
      south: bounds.getSouth(),
      east: bounds.getEast(),
      north: bounds.getNorth(),
      maxZenith: app.solarZenithSlider.slider.value
    }
    app.setLoading(true);
    $.ajax({
        url:app.URL.GETIMAGES,
        data:params,
        success:function(response){
          console.log(response);
          app.origList = response.idList;

          app.setLoading(false);
        }
    });
  });
}

app.createConstants();
app.createFunctions();
app.initialize();
app.addHandlers();
