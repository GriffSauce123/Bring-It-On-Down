const gameboard = document.querySelector(".game-board")

const player1_segs = document.querySelector(".board-2")
const player2_segs = document.querySelector(".board-1")

let d1 = document.getElementById("d1")
let d2 = document.getElementById("d2")

let current_moves1 = []
let current_moves2 = []

var turn = true //true is player 1, false is player 2
var num_turns = 0 //number of turns played

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
        if (element.parentElement.parentElement.id == "board-1" && turn && element.style.bottom != "5.1vw" ||  //if it is your board and not up position
            element.parentElement.parentElement.id == "board-2" && !turn && element.style.bottom != "5.1vw" ||
            element.parentElement.parentElement.id == "board-1" && !turn && element.style.bottom == "5.1vw" || //if it is the opponents board, but up position
            element.parentElement.parentElement.id == "board-2" && turn && element.style.bottom == "5.1vw")
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

                //resetting the dice
                if (element.parentElement.id.includes(Math.round(d1.innerHTML) + Math.round(d2.innerHTML))) {d1.innerHTML = 0; d2.innerHTML = 0}
                else if (element.parentElement.id.includes(d1.innerHTML)) {d1.innerHTML = 0}
                else if (element.parentElement.id.includes(d2.innerHTML)) {d2.innerHTML = 0}
            }
    }
    
}

function make_safe(element) {
    element.style.bottom = "11.6vw"
}

function nextturn() {

    d1.innerHTML = 0
    d2.innerHTML = 0

    console.log(current_moves1)
    console.log(current_moves2)

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

    if ((num_turns) % 2 == 0) {
        for (let seg of player2_segs.children) {
            let ring = seg.querySelector(".ring")
            if (ring.style.bottom == "5.1vw") {
                safe = true
                for (let move of current_moves1) {
                    if (move.includes(ring.parentElement.id)) {
                        safe = false
                        break
                    }
                }
                if (safe) {ring.style.bottom = "11.6vw"}
            }
        }
    }

    if (gameboard.style.rotate == "180deg") {
        gameboard.style.rotate = "0deg"
    }
    else {
        gameboard.style.rotate = "180deg"
    }

    current_moves1 = []
    current_moves2 = []
}

function roll_dice() {

    if (d1.innerHTML == 0 && d2.innerHTML == 0) {
        d1.innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
        d2.innerHTML = Math.floor(Math.random() * (7 - 1) ) + 1
    }
}