const express = require("express")
var bodyParser = require('body-parser')
var app = express()

app.use(bodyParser.json());

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
    console.log(req.body)
    res.send(req.body)

    //each game action will be sent here
    //check state in database ( this needs to be done continuously somehow )
    /*
    create sends code to db
    db sends code to user1
    user1 joins
    join sends user1 ip to db
    waiting screen
    user2 joins
    user2 ip to db
    db sends go signal
    user1 turn
    each action updates db
    db updates user2 ( user2 client listening when not turn )
    user1 ends turn
    db validates states on both users
    db sends user2 your turn signal
    repeat
    checks for wins with db board state
    checks for disconnects :(
    sends playerx wins signal
    ends
    */


    //update database
    //push changes to other player
    //gives or removes next turn option
    //if user exits, game is forfeit
})

//starts the app
app.listen(10000, function () {
    console.log("Started application on port %d", 10000)
});