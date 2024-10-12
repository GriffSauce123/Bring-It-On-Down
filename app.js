const startlocal = document.getElementById("startlocal")
const splashpage = document.querySelector(".splashpage")

const gameboard = document.querySelector(".game-board")

const player1_segs = document.querySelector(".board-2")
const player2_segs = document.querySelector(".board-1")

let d1 = document.getElementById("d1")
let d2 = document.getElementById("d2")

let current_moves1 = []
let current_moves2 = []

var turn = true //true is player 1, false is player 2
var num_turns = 0 //number of turns played

startlocal.addEventListener("click", start_local_game)

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

                 //check for win of game
                 let win = true
                 for (let seg of element.parentElement.parentElement.children) {
                     if (!(seg.querySelector(".ring").style.bottom == "5.1vw" || seg.querySelector(".ring").style.bottom == "11.6vw")) {
                         win = false
                         break
                     }
                 }
                 if (win) {  
                    
                    if (turn) { //if player 1 ( blue )
                        document.getElementById("winner").innerHTML = "Player 1 Wins!"
                        possibleColors = ["DodgerBlue", "Blue", "SteelBlue"]
                    }
                    else {
                        document.getElementById("winner").innerHTML = "Player 2 Wins!"
                        possibleColors = ["Red", "Dark Red", "Crimson"]
                    }

                    // Push new confetti objects to `particles[]`
                    // need to check what color and player one to change color of confetti
                    for (var i = 0; i < maxConfettis; i++) {
                        particles.push(new confettiParticle());
                        }
                        
                    // Initialize
                    canvas.width = W;
                    canvas.height = H;
                    Draw();

                    document.querySelector(".win-screen").style.display = "flex"
                    document.getElementById("home-btn").addEventListener("click", exit_game)
                 }

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

function start_local_game() {
    splashpage.style.display = "none"
    document.querySelector(".win-screen").style.display = "none"
}

function exit_game() {
    document.querySelector(".win-screen").style.display = "none";
    
    for (let seg of player1_segs.children) {
        seg.querySelector(".ring").style.bottom = "0vw";
    }
    for (let seg of player2_segs.children) {
        seg.querySelector(".ring").style.bottom = "0vw";
    }
    d1.innerHTML = 0
    d2.innerHTML = 0
    num_turns = 0
    turn = true
    splashpage.style.display = "flex"
}

// win screen confetti
let W = window.innerWidth;
let H = window.innerHeight;
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const maxConfettis = 150;
const particles = [];

var possibleColors = []

function randomFromTo(from, to) {
return Math.floor(Math.random() * (to - from + 1) + from);
}

function confettiParticle() {
this.x = Math.random() * W; // x
this.y = Math.random() * H - H; // y
this.r = randomFromTo(11, 33); // radius
this.d = Math.random() * maxConfettis + 11;
this.color =
    possibleColors[Math.floor(Math.random() * possibleColors.length)];
this.tilt = Math.floor(Math.random() * 33) - 11;
this.tiltAngleIncremental = Math.random() * 0.07 + 0.05;
this.tiltAngle = 0;

this.draw = function() {
    context.beginPath();
    context.lineWidth = this.r / 2;
    context.strokeStyle = this.color;
    context.moveTo(this.x + this.tilt + this.r / 3, this.y);
    context.lineTo(this.x + this.tilt, this.y + this.tilt + this.r / 5);
    return context.stroke();
};
}

function Draw() {
const results = [];

    // Magical recursive functional love
    requestAnimationFrame(Draw);

    context.clearRect(0, 0, W, window.innerHeight);

    for (var i = 0; i < maxConfettis; i++) {
        results.push(particles[i].draw());
    }

    let particle = {};
    let remainingFlakes = 0;
    for (var i = 0; i < maxConfettis; i++) {
        particle = particles[i];

        particle.tiltAngle += particle.tiltAngleIncremental;
        particle.y += (Math.cos(particle.d) + 3 + particle.r / 2) / 2;
        particle.tilt = Math.sin(particle.tiltAngle - i / 3) * 15;

        if (particle.y <= H) remainingFlakes++;

        // If a confetti has fluttered out of view,
        // bring it back to above the viewport and let if re-fall.
        if (particle.x > W + 30 || particle.x < -30 || particle.y > H) {
        particle.x = Math.random() * W;
        particle.y = -30;
        particle.tilt = Math.floor(Math.random() * 10) - 20;
        }
    }

    return results;
}

window.addEventListener(
    "resize",
    function() {
        W = window.innerWidth;
        H = window.innerHeight;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    },
    false
);
