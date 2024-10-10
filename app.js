const gameboard = document.querySelector(".game-board")

const player1_segs = document.querySelector(".board-2")
const player2_segs = document.querySelector(".board-1")

var turn = true //true is player 1, false is player 2
var num_turns = 0 //number of turns played

for (let seg of player1_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

for (let seg of player2_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

function changestate(element) {

    if (element.parentElement.parentElement.id == "board-1" && turn) { //which board

        if (!(element.style.bottom == "5.1vw")) {
            element.style.bottom = "5.1vw"
        }
        else if (element.style.bottom == "5.1vw") {
            element.style.bottom = "0"
        }    
    }
}

function make_safe(element) {
    element.style.bottom = "11.6vw"
}

function nextturn() {

    turn ++

    //push up rings to safe space for other players
    for (let seg of player1_segs.children) {
        let ring = seg.querySelector(".ring")
        if (ring.style.bottom == "5.1vw") {
            ring.style.bottom = "11.6vw"
        }
    }

    for (let seg of player2_segs.children) {
        let ring = seg.querySelector(".ring")
        if (ring.style.bottom == "5.1vw") {
            ring.style.bottom = "11.6vw"
        }
    }

    if (gameboard.style.rotate == "180deg") {
        gameboard.style.rotate = "0deg"
    }
    else {
        gameboard.style.rotate = "180deg"
    }
}

function roll_dice() {

    //check if allowed

    document.getElementById("d1").innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
    document.getElementById("d2").innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
}