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
  app.addDatePicker = function(){
    var DatePicker = L.Control.extend({
        options: {
            // Default control position
            position: 'topright'
        },
        onAdd: function (map) {
            // Create a container with classname and return it
            var template = document.createElement('template');
            var html = "<input type=text id=datepicker readonly=true placeholder=Date style='width:90px;padding:2px;text-align:center;box-shadow:0px 1px 5px rgba(0, 0, 0, 0.4);border-radius:4px;border:1px solid #ccc;' />";
            template.innerHTML = html.trim();
            return template.content.firstChild;
        },
        setContent: function (content) {
            // Set the innerHTML of the container
            this.getContainer().innerHTML = content;
        }
    });

    app.datePicker =  new DatePicker().addTo(app.map);

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
  app.addLayerToMap = function(id){
    app.setLoading(true);
    /*$.ajax({

    });*/
  }
}

app.initialize = function(){
  app.map = L.map('map').setView([28.115593833316762, 84.64141845703126], 8);

  L.tileLayer('https://api.mapbox.com/styles/v1/banmedo/ciiibvf1k0011alki4gp6if1s/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmFubWVkbyIsImEiOiJhSklqeEZzIn0.rzfSxO3cVUhghA2sJN378A').addTo(app.map);

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
