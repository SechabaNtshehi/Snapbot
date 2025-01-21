let map;

const url = "http://localhost:8080/coordinates";
var lat
var lng 
var zoom_

var index = 0

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: parseFloat(lat), lng:    parseFloat(lng)},
    zoom: zoom_,
  });

  const trafficLayer = new google.maps.TrafficLayer();

  trafficLayer.setMap(map);
}


// function loadMap(){
//   console.log(document.getElementById("lat").value);
//   initMap();  
// }


loadMap()

function loadMap(){
  fetch(url)
  .then(response => response.json())
  .then(data =>{
    console.log(data);
    lat = data.lat;
    lng = data.long
    zoom_ = data.zoom
    initMap();
  })
  .catch(err =>{
    console.log(err);
  })
}


document.getElementById("next_map").addEventListener("click", ()=>{
  // console.log("clicked next map")
  fetch(`http://localhost:8080/get-location${index}`)
  .then(response => response.json())
  .then(data =>{
    console.log(data.name);
    // document.getElementById("name").textContent = data.name
    fetch(`http://localhost:8080/toggle-location?location=${data.name}`, {
      method: "PUT"
    })
    .then(res => res.json())
    .then(json_data =>{
      if (json_data.status == "success"){
        loadMap()
        fetch(`http://localhost:8080/get-number-of-locations`)
        .then(num_res => num_res.json())
        .then(num_json =>{
          index = (index + 1) % num_json.total_locations
        })
      }
    })
  })
  .catch(err =>{
    console.log(err);
  })   
}); 

document.getElementById("prev_map").addEventListener("click", ()=>{
  // console.log("clicked next map")
  fetch(`http://localhost:8080/get-location${index}`)
  .then(response => response.json())
  .then(data =>{
    console.log(data.name);
    fetch(`http://localhost:8080/toggle-location?location=${data.name}`, {
      method: "PUT"
    })
    .then(res => res.json())
    .then(json_data =>{
      if (json_data.status == "success"){
        loadMap()
        fetch(`http://localhost:8080/get-number-of-locations`)
        .then(num_res => num_res.json())
        .then(num_json =>{
          index = (((index - 1) % num_json.total_locations) + num_json.total_locations) % num_json.total_locations
        })
      }
    })
  })
  .catch(err =>{
    console.log(err);
  })   
}); 

// loadMap()
