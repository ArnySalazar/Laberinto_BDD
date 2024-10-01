const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Definir colores
const BLACK = '#000';
const WHITE = '#FFF';
const RED = '#F00';
const BLUE = '#00F';
const GREEN = '#0F0';

const blockSize = 20;
let playerPos = { x: blockSize, y: blockSize };

// Definir el laberinto (1 = pared, 0 = camino, 2 = meta)
const maze = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
  [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
  [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
  [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],
  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
];

// Dibujar el laberinto
function drawMaze() {
  for (let row = 0; row < maze.length; row++) {
    for (let col = 0; col < maze[0].length; col++) {
      if (maze[row][col] === 1) {
        ctx.fillStyle = BLUE;
        ctx.fillRect(col * blockSize, row * blockSize, blockSize, blockSize);
      } else if (maze[row][col] === 2) {
        ctx.fillStyle = GREEN;
        ctx.fillRect(col * blockSize, row * blockSize, blockSize, blockSize);
      }
    }
  }
}

// Dibujar al jugador
function drawPlayer() {
  ctx.fillStyle = RED;
  ctx.fillRect(playerPos.x, playerPos.y, blockSize, blockSize);
}

// Verificar movimiento válido
function isValidMove(newX, newY) {
  let row = newY / blockSize;
  let col = newX / blockSize;
  if (maze[row][col] === 0 || maze[row][col] === 2) {
    return true;
  }
  return false;
}

// Controlar el movimiento del jugador
window.addEventListener('keydown', function (e) {
  let newX = playerPos.x;
  let newY = playerPos.y;

  if (e.key === 'ArrowUp') newY -= blockSize;
  if (e.key === 'ArrowDown') newY += blockSize;
  if (e.key === 'ArrowLeft') newX -= blockSize;
  if (e.key === 'ArrowRight') newX += blockSize;

  if (isValidMove(newX, newY)) {
    playerPos.x = newX;
    playerPos.y = newY;
  }
});

// Bucle del juego
function gameLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawMaze();
  drawPlayer();
  requestAnimationFrame(gameLoop);
}

gameLoop();
