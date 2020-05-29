export default function takeAlgorithm(boardData) {
    let rx, ry;
    do {
        [rx, ry] = getRandomPos(boardData.length, boardData[0] ? boardData[0].length : 0);
    } while (boardData[rx][ry] != '');
    return [rx, ry];

}

function getRandomPos(x, y) {
    let rand = max => parseInt(Math.random() * max);
    return [rand(x), rand(y)];
}
// function alphaBeta(n, a, b, role = 0) {
//     if (n == 0) return evaluate();
//     for (let move of getAllMoves()) {
//         take(move, role);
//         let v = -alphaBeta(n - 1, -b, -a, 1 - role);
//         untake(move, role);
//         if (v >= b) return b;
//         if (v > a) a = v;
//     }
// }

// function evaluate() {

// }

// function getAllMoves() {

// }

// function take(move, role) {
    
// }

// function untake(move, role) {
    
// }