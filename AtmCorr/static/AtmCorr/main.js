var app = {}

/*=================== constants =========================*/
app.createConstants = function(){
  app.URL = {
    BASE : '/AtmCorr/',
    GETIMAGES : 'getimagelist',
    GETMAPID : 'getmapid',
    GETCORRECTEDMAPID : 'getcorrectedmapid',
    EXPORT : 'exportimage'
  }
}

app.defineVariables = function(){
  app.map, app.datePicker, app.solarZenithSlider, app.showCorrected, app.origTileLayer, app.correctedTileLayer, app.mapSplit;
  app.imageIdList = [];
  app.__mapURLcache, app.__correctedURLcache = {};
  app.showCorrected = false;
}


app.createFunctions = function(){
  app.setLoading = function(state, message){
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
      },
      updateImageList: function(list){
        this.imgIndex = 0
        this.imgCount = list.length;
        if (!this.imgCount){
          $('.leaflet-imagescroller').html("No images for current Date!");
        }else{
          var html = "<button class='leaflet-imagescroller-btn leaflet-imagescroller-prev'> < </button> ";
          html += "<span class='leaflet-imagescroller-current'> 1 </span> / "+this.imgCount;
          html += " <button class='leaflet-imagescroller-btn leaflet-imagescroller-next'> > </button>";
          $('.leaflet-imagescroller').html(html);
          var curObj = this;
          $('.leaflet-imagescroller-next').on('click',function(e){
            if(curObj.imgIndex < (curObj.imgCount-1)){
              curObj.imgIndex ++;
              $(".leaflet-imagescroller-current").html(curObj.imgIndex+1);
              app.updateActiveImage();
            }
          });
          $('.leaflet-imagescroller-prev').on('click',function(e){
            if(curObj.imgIndex > 0){
              curObj.imgIndex --;
              $(".leaflet-imagescroller-current").html(curObj.imgIndex+1);
              app.updateActiveImage();
            }
          });
        }
      }
    });
    app.imageScroller =  new ImageScroller({position:'horizontalcenterbottom'}).addTo(app.map);
  }
  app.addShowCorrectedToggle = function(){
    var LeafletShowCorrected = L.Control.extend({
        onAdd: function (map) {
            var template = document.createElement('template');
            var html = "<button class='leaflet-showcorrected' > Show Corrected Image!</button>";
            template.innerHTML = html.trim();
            return template.content.firstChild;
        }
    });
    app.showCorrected = new LeafletShowCorrected({position:'bottomright'}).addTo(app.map);
    app.showCorrected.state = false;
  }
  app.addExportButton = function(){
    var LeafletExport = L.Control.extend({
        onAdd: function (map) {
            var template = document.createElement('template');
            var html = "<button class='leaflet-exportimage' disabled> <img src='https://png.icons8.com/metro/50/000000/download.png'> </button>";
            template.innerHTML = html.trim();
            return template.content.firstChild;
        }
    });
    new LeafletExport({position:'topleft'}).addTo(app.map);
  }
  app.updateActiveImage = function(){
    app._clearMap();
    if(app.__mapURLcache[app.imageScroller.imgIndex]){
      L.tileLayer(app.__mapURLcache[app.imageScroller.imgIndex]).addTo(app.map);
    }else{
      app.setLoading(true);
      var data = {id: app.imageIdList[app.imageScroller.imgIndex]};
      $.ajax({
        url:app.URL.GETMAPID,
        data:data,
        success: function(response){
          console.log(response);
          var tempURL = app._getMapURL(response.mapid, response.token);
          app.__mapURLcache[app.imageScroller.imgIndex] = tempURL;
          app.origTileLayer = L.tileLayer(tempURL);
          app.origTileLayer.addTo(app.map);
          app.setLoading(false);
          app.showCorrectedImage();
        }
      });
    }
  }
  app.showCorrectedImage = function(){
    if (app.showCorrected.state){
      if (app.imageIdList.length < 1) return;
      if(app.__correctedURLcache[app.imageScroller.imgIndex]){
        app.correctedTileLayer = L.tileLayer(app.__correctedURLcache[app.imageScroller.imgIndex]);
        app.correctedTileLayer.addTo(app.map);
        app.mapSplit = L.control.sideBySide(app.origTileLayer, app.correctedTileLayer);
        app.mapSplit.addTo(app.map);
      }
      else{
        app.setLoading(true);
        var data = {id: app.imageIdList[app.imageScroller.imgIndex]};
        $.ajax({
          url:app.URL.GETCORRECTEDMAPID,
          data:data,
          success: function(response){
            console.log(response);
            var tempURL = app._getMapURL(response.mapid, response.token);
            app.__correctedURLcache[app.imageScroller.imgIndex] = tempURL;
            app.correctedTileLayer = L.tileLayer(tempURL);
            app.correctedTileLayer.addTo(app.map);
            app.mapSplit = L.control.sideBySide(app.origTileLayer, app.correctedTileLayer);
            app.mapSplit.addTo(app.map);
            app.setLoading(false);
          }
        });
      }
    }else app._removeSplit();
  }
  app._getMapURL = function(mapId, token){
      var baseUrl = 'https://earthengine.googleapis.com/map';
      var url = [baseUrl, mapId, "{z}", "{x}", "{y}"].join('/');
      url += '?token=' + token;
      return url;
  }
  app._clearMap = function(){
    app.map.eachLayer(function(layer){
      app.map.removeLayer(layer);
    });
    L.tileLayer('https://api.mapbox.com/styles/v1/banmedo/ciiibvf1k0011alki4gp6if1s/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmFubWVkbyIsImEiOiJhSklqeEZzIn0.rzfSxO3cVUhghA2sJN378A').addTo(app.map);
  }
  app._removeSplit = function(){
    if (app.mapSplit){
      app.map.removeControl(app.mapSplit);
      app.map.removeLayer(app.correctedTileLayer);
      delete(app.mapSplit);app.mapSplit;
    }
  }
}

app.initialize = function(){
  app.map = L.map('map').setView([28.115593833316762, 84.64141845703126], 8);
  app._clearMap();

  app.addLeafletCorners();
  app.addImageScroller();
  app.addDatePicker();
  app.addSolarZenithPicker();
  app.addShowCorrectedToggle();
  app.addExportButton()
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
          app.__mapURLcache = {};
          app.imageIdList = response.idlist;
          app.imageScroller.updateImageList(app.imageIdList);
          app.setLoading(false);
          app.updateActiveImage(app.imageIdList[0]);
        }
    });
  });

  $(".leaflet-showCorrected").on('click',function(e){
    $(".leaflet-exportimage").prop("disabled",app.showCorrected.state)
    app.showCorrected.state = !app.showCorrected.state;
    if (app.showCorrected.state){
      $(".leaflet-showCorrected").css("background","#A3F7B5");
    }else{
      $(".leaflet-showCorrected").css("background","#FFFFFF");
    }
    app.showCorrectedImage();
  });

  $(".leaflet-exportimage").on('click',function(e){
    console.log('exportimage');
  });

}

app.createConstants();
app.defineVariables();
app.createFunctions();
app.initialize();
app.addHandlers();
