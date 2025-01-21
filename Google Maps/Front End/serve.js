const express = require('express')
const path = require('path')
const cors = require('cors')

const app = express()
const PORT = 5555

app.use(cors())
app.use(express.static(path.join(__dirname, "Public")));

app.get("/", (req, res)=>{
	res.sendFile(path.join(__dirname, "Public", "index.html"))
})

app.listen(PORT, ()=>{
	console.log("Listening on", PORT)
})