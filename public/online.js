
const gameboard = document.querySelector(".game-board")

const player1_segs = document.getElementById("yourboard")
const player2_segs = document.getElementById("opponentboard")

const game_code = document.getElementById("game-code")

let code = document.URL.slice(-6)
    code = Number(code)
    if (code >= 100000) {
        game_code.value = code;
        var game_login_code = code; 
    }
    else {
        var game_login_code = Number(game_code.value);
    }

game_code.addEventListener("input", () => {game_login_code = Number(game_code.value);})

const join_button = document.getElementById("join-coop")

let d1 = document.getElementById("d1")
let d2 = document.getElementById("d2")

let current_moves1 = []
let current_moves2 = []


//these needs to be assigned by server to determine when your turn is
//player == turn HAS to be true for you to be able to go
var player = true //true plays when turn is true ( even number ) false plays when turn is false ( odd number )
var turn = true //true is player 1, false is player 2
var num_turns = 0 //total number of turns played

for (let seg of player1_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

for (let seg of player2_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

function changestate(element) {
    //checking if dice allow the move
    
    let temp = [element.parentElement.id]

    if (element.parentElement.id.includes(d1.innerHTML) || //if first die
        element.parentElement.id.includes(d2.innerHTML) || //if second die
        element.parentElement.id.includes(Math.round(d1.innerHTML) + Math.round(d2.innerHTML))) //if sum of dice
    {
        //check if it is either your piece, or opponent in up position
        if (element.parentElement.parentElement.id == "yourboard" && turn == player && element.style.bottom != "5.1vw" ||    //if your board, not up position
            element.parentElement.parentElement.id == "opponentboard" && turn == player && element.style.bottom == "5.1vw")  //if it is the opponents board, but up position         //if opp board, up position 
            {
                if (!(element.style.bottom == "5.1vw")) {
                    element.style.bottom = "5.1vw"
                }
                else if (element.style.bottom == "5.1vw") {
                    element.style.bottom = "0"
                }
                
                temp.push(element.style.bottom)
                if (element.parentElement.parentElement.id == "board-1") {current_moves1.push(temp)}
                else if (element.parentElement.parentElement.id == "board-2") {current_moves2.push(temp)}

                 //check for win of game
                 let win = true
                 for (let seg of element.parentElement.parentElement.children) {
                     if (!(seg.querySelector(".ring").style.bottom == "5.1vw" || seg.querySelector(".ring").style.bottom == "11.6vw")) {
                         win = false
                         break
                     }
                 }
                 if (win) {
                     //do the winning things
                     //check which team won
                     //coneftti or something
                     //show number of moves, number of rolls, etc
                     //timer?
                 }

                //resetting the dice
                if (element.parentElement.id.includes(Math.round(d1.innerHTML) + Math.round(d2.innerHTML))) {d1.innerHTML = 0; d2.innerHTML = 0}
                else if (element.parentElement.id.includes(d1.innerHTML)) {d1.innerHTML = 0}
                else if (element.parentElement.id.includes(d2.innerHTML)) {d2.innerHTML = 0}
                //send reset dice to db
                //send move to db
            }
    }
    
}

function nextturn() {

    //if it is not your turn, you may not end it.
    if (player != turn) {
        return
    }

    d1.innerHTML = 0
    d2.innerHTML = 0

    turn = !turn
    num_turns ++

    //push up rings to safe space for other players
    //only once they have sat for an opponent turn
    if (num_turns % 2 == 1) {
        for (let seg of player1_segs.children) {
            let ring = seg.querySelector(".ring")
            if (ring.style.bottom == "5.1vw") {
                ring.style.bottom = "11.6vw"
                let safe = true
                for (let move of current_moves2) {
                    if (move.includes(ring.parentElement.id)) {
                        safe = false
                        break
                    }
                }
                if (safe) {ring.style.bottom = "11.6vw"}
            }
        }
    }

    //get make safe pushes from server

    current_moves1 = []
    current_moves2 = []

    //send moves and nextturn to db

}

function roll_dice() {

    if (player != turn) {
        return
    }

    if (d1.innerHTML == 0 && d2.innerHTML == 0) {
        d1.innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
        d2.innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
        //send dice values to db
    }
}

async function pushdata(args) {
    const response = await fetch("/join", {
        method: "POST",
        body: JSON.stringify(args),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
          },
    });
    let temp =  await response.json()   
    //do the things here     
}

join_button.addEventListener("click", () => {pushdata({id:game_login_code});const socket = io();})


//if get request, skip join splashpage