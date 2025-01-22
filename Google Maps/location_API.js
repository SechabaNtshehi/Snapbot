const fs = require('fs');
const path = require('path');
const cors = require('cors');

const express = require('express');


const app = express();
app.use(express.json());

const PORT = 8080;
const db_dir = '../DB/locations.json'

app.use(cors());
app.use(express.static(path.join(__dirname, "Public")));

app.get("/", (req, res)=>{
	res.sendFile(path.join(__dirname, "Public", "index.html"))
})

app.get("/coordinates", (req, res)=>{
	getCoordinates().
	then(coordinates =>{
		console.log(coordinates)
		coordinates = {...coordinates, ...{'status' : 'success'}}
		res.send(coordinates);		
	})
	.catch(err =>{
		console.log(err);
		
		res.send({"status" : err})
	});
});

app.get("/image-coordinates", (req, res) =>{
	getImageCoordinates()
	.then(coordinates =>{
		console.log(coordinates)
		coordinates = {...coordinates, ...{'status' : 'success'}}
		res.send(coordinates)
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})

app.get("/get-location:index", (req, res) =>{
	console.log(req.params.index)
	getLocation(req.params.index)
	.then((result) =>{
		console.log(result)
		result = {...result, ...{'status' : 'success'}}
		res.send(result)		
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})

app.get("/get-number-of-locations", (req, res) =>{
	getNumberOfLocations()
	.then((result) =>{
		console.log(result)
		result = {...result, ...{'status' : 'success'}}
		res.send(result)		
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})

app.put("/toggle-location", (req, res)=>{
	const location = req.query.location || "Invalid location"

	console.log(`RRR ${location}`)

	updateDB(location)
	.then((result)=>{
		const response = {"status" : result}
		res.send(response) 
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})

app.post("/add-location", (req, res)=>{
	console.log(req.body)
	addLocation(req.body)
	.then(status =>{
		const result = {"status" : status}
		res.send(result)
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})

app.delete("/remove-location", (req, res)=>{
	console.log(req.query.location)
	deleteLocation(req.query.location)
	.then(status =>{
		const result = {"status" : status}
		res.send(result)
	})
	.catch(err=>{
		console.log(err)
		res.send({"status" : err})
	})
})


app.listen(PORT, () =>{
	console.log("Listening on port ", PORT);
});


function getCoordinates(){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)
		var currLocation;

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject(err);
			}

			const locations = JSON.parse(data);

			currLocation = locations.locations.filter(location => location.current);

			if(currLocation.length > 0){

				fs.writeFile(jsonFilePath, JSON.stringify(locations, null, 4), err =>{
					if(err){
						reject(err);
					}
					else{
						resolve({...currLocation[0].coordinates, ...{"zoom" :currLocation[0].zoom}});
					}
				});
			}
			else{
				reject("no such location");
			}
		});		
	})
}

function getImageCoordinates(){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)
		var currLocation;

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject(err);
			}

			const locations = JSON.parse(data);

			currLocation = locations.locations.filter(location => location.current);

			if(currLocation.length > 0){
				if(err){
					reject(err);
				}
				else{
					resolve(currLocation[0].image_coordinates);
				}
			}
			else{
				reject("no location is current");
			}
		});		
	})
}

function getLocation(index){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject(err);
			}

			const locations = JSON.parse(data);

			if(index < locations.locations.length){ 
				resolve({"name" : locations.locations[index].name});
			}
			else{
				reject("index out of bounds");
			}
		});		
	})	
}

function getNumberOfLocations(){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject(err);
			}

			const locations = JSON.parse(data);
			resolve({"total_locations" : locations.locations.length});
		});		
	})		
}

function updateDB(_location){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)
		var currLocation;

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject("something went wrong while reading data");
			}

			const locations = JSON.parse(data);

			currLocation = locations.locations.filter(location => location.name == _location);
			prevLocation = locations.locations.filter(location => location.current && location.name != _location);

			console.log(currLocation)
			console.log(prevLocation)

			if(currLocation.length > 0){
				currLocation[0].current = true
				if(prevLocation.length > 0){
					prevLocation[0].current = false
				}

				fs.writeFile(jsonFilePath, JSON.stringify(locations, null, 4), err =>{
					if(err){
						reject("something went wrong while updating data");
					}
					else{
						resolve("success");
					}
				});
			}
			else{
				reject("location not found");
			}
		});	
	})
}

function addLocation(_location){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject("something went wrong while reading data");
			}

			const locations = JSON.parse(data);
			locations.locations.push(_location)

			fs.writeFile(jsonFilePath, JSON.stringify(locations, null, 4), err =>{
				if(err){
					reject("something went wrong while updating data");
				}
				else{
					resolve("success");
				}
			});
		});	
	})	
}

function deleteLocation(_location){
	return new Promise((resolve, reject)=> {
		const jsonFilePath = path.join(__dirname, db_dir)

		fs.readFile(jsonFilePath, 'utf-8', (err, data)=>{
			if(err){
				reject("something went wrong while reading data");
			}

			const locations = JSON.parse(data);
			locations.locations = locations.locations.filter(location => location.name != _location);
			if(locations.locations > 0){
				fs.writeFile(jsonFilePath, JSON.stringify(locations, null, 4), err =>{
					if(err){
						reject("something went wrong while updating data");
					}
					else{
						resolve("success");
					}
				});	
			}
			else{
				reject("db is empty or location does not exists")
			}
		});	
	})
}


