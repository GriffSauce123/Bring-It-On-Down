const express = require("express")
var app = express()

app.use(express.static('public'))

// Homepage
app.get('/', (req, res) => {
   res.sendFile(__dirname + '/index.html')
})

//creating a lobby page
app.get('/create', (req, res) => {
    res.sendFile(__dirname + '/create.html')
})

app.post('/create', (req, res) => {
    console.log(Math.round(Math.random()*100000,0))
    res.send(`${Math.round(Math.random()*100000,0)}`)
})

app.get('/join', (req, res) => {
    res.sendFile(__dirname + '/join.html')
})



//starts the app
app.listen(10000, function () {
    console.log("Started application on port %d", 10000)
});