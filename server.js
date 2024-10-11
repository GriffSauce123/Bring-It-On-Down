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

//server creating the code and sending to client
app.post('/create', (req, res) => {
    let code = (Math.random() + 'a').slice(2,8);
    res.send(code)
})

app.get('/join', (req, res) => {
    //get id from get request in url and check database
    res.sendFile(__dirname + '/join.html')
})

app.post('/join', (req, res) => {
    //each game action will be sent here
    //check state in database ( this needs to be done continuously somehow )
    //update database
    //push changes to other player
    //gives or removes next turn option
    //if user exits, game is forfeit
})

//starts the app
app.listen(10000, function () {
    console.log("Started application on port %d", 10000)
});