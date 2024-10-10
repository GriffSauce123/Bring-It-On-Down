const gameboard = document.querySelector(".game-board")

const player1_segs = document.querySelector(".board-2")
const player2_segs = document.querySelector(".board-1")

for (let seg of player1_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

for (let seg of player2_segs.children) {
    seg.querySelector(".ring").addEventListener("click", () => {changestate(seg.querySelector(".ring"))})
}

function changestate(element) {
    if (!(element.style.bottom == "5.1vw")) {
        element.style.bottom = "5.1vw"
    }
    else if (element.style.bottom == "5.1vw") {
        element.style.bottom = "0"
    }    
}

function make_safe(element) {
    element.style.bottom = "11.6vw"
}

function nextturn() {
    if (gameboard.style.rotate == "180deg") {
        gameboard.style.rotate = "0deg"
    }
    else {
        gameboard.style.rotate = "180deg"
    }
}