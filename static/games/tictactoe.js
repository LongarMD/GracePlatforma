let boardWidth = 500;
let boardHeight = 500;
let size = 100;
let raw = "XOX#X#OXO" // v taki obliki dobimo iz baze
let game = [
    ["#", "O", "#"],
    ["#", "X", "#"],
    ["O", "O", "O"]
]

let player = "X" // or O
let nextPlayer = "O"

function setup() {
    createCanvas(boardWidth, boardHeight);
}

function draw() {
    drawLines()
    drawGame(game)
}

function mouseMoved() {
    let [y, x] = detectPostion(mouseX, mouseY)
    fill("yellow")
    console.log(x, y)
    drawBackground(x, y)
}

function mouseClicked() {
     let [y, x] = detectPostion(mouseX, mouseY)
    // if polje že ima X ali O potem nič ne rišemo
    // preverimo, če smo na vrsti
    if (game[x][y] == "#") {
        game[x][y] = player   
    } else {
        console.log("zasedeno!")
    }
}

function detectPostion(x, y) {
    a = Math.floor(x / (boardWidth / 3))
    b = Math.floor(y / (boardHeight / 3))
    return [a, b] // [0, 2]
}

function drawLines() {
    strokeWeight(3) // debelina črte
    stroke(0) // barva črte 0 -> rgb(0, 0, 0)
    line(boardWidth / 3, 0, boardWidth / 3, boardHeight)
    line(2 * boardWidth / 3, 0, 2 * boardWidth / 3, boardHeight)
    line(0, boardHeight / 3, boardWidth, boardHeight / 3)
    line(0, 2 * boardHeight / 3, boardWidth, 2 * boardHeight / 3)
}

function drawX(x, y) {
    line(x - size / 2, y - size / 2, x + size / 2, y + size / 2)
    line(x - size / 2, y + size / 2, x + size / 2, y - size / 2)
}

function drawO(x, y) {
    fill("BLACK")
    ellipse(x, y, size)
}

// želimo da je input takle: [1, 2]
function drawBackground(a, b) {
// iz a in b pridimo do končega x in y
    y = a * boardWidth / 3 + boardWidth / 6
    x = b * boardHeight / 3 + boardHeight / 6
    fill("GREY")
    fill('rgba(0, 0, 0, 0.1)')
    //noStroke()
    strokeWeight(0)
    rectMode(CENTER)
    background("WHITE")
    if (isEmptyField(a, b)) {
        rect(x, y, size * 1.4) // or square    
    }
}

function isEmptyField(a, b) { // a --> 0 or 1 or 2
    if (game[a][b] != "#") {
        return false
    } return true
} // vrne true ali false

function drawGame(game) {
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            if (game[i][j] == "X")
                drawX(j * boardWidth / 3 + boardWidth / 6, i * boardHeight / 3 + boardHeight / 6)
            else if (game[i][j] == "O")
                drawO(j * boardWidth / 3 + boardWidth / 6, i * boardHeight / 3 + boardHeight / 6)
        }
    }
}


async function getTictactoe() {
    let response = await fetch("https://platforma.team-grace.repl.co/game/tictactoe/tictactoe_2")
    console.log(await response.json())
}

getTictactoe()

