import express from "express"
import { createClient } from "@libsql/client";
import "dotenv/config.js";
import bodyParser from "body-parser"
var app = express()

/**
 * SOCKET.IO to manage current games, only use db for saved information lol.
 * socket id instead of ip addr
 * authoritative server functions
 * 
 * 
 * 
 * 
 * 
 * 
 */




app.use(bodyParser.json());
app.use(express.static('public'))

import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url)) + "\\public";

//DATABASE THINGS
const turso = createClient({
               url: process.env.TURSO_DATABASE_URL,
    authToken: process.env.TURSO_AUTH_TOKEN,
  });
  
/*
//getting all current games
let data = await turso.execute("SELECT * FROM current_games")
console.log(data)*/

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
    let player1ip = req.socket.remoteAddress;
    console.log(player1ip)
    turso.execute(`INSERT INTO current_games ("code", "player1ip") VALUES (${code}, "${player1ip}");`)
    res.send(code)
})

app.get('/join', (req, res) => {
    //make sure there is a valid get request

    //check that this is not the one who created the match (set to player2ip)
    turso.execute(`UPDATE current_games SET player2ip=${req.socket.remoteAddress} WHERE code=${req.query.id}`)

    res.sendFile(__dirname + '/join.html') // add little thing telling user which team they are on, which color
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