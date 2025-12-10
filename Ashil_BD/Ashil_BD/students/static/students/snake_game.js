// Основные переменные
let canvas = document.getElementById('gameCanvas');
let ctx = canvas.getContext('2d');
let gridSize = 20;
let tileCount = canvas.width / gridSize;

let snake = [
    {x: 10, y: 10} // Начальная позиция головы
];
let direction = {x: 0, y: 0};
let food = {x: 15, y: 15};
let score = 0;
let gameSpeed = 10; // Скорость игры (FPS)
let tailLength = 1; // Начальная длина змейки (только голова)

// Генерация еды в случайном месте
function generateFood() {
    food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
    };
    
    // Проверяем, не сгенерировалась ли еда на змейке
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            generateFood(); // Рекурсивно ищем свободное место
            break;
        }
    }
}

// Отрисовка игры
function draw() {
    // Очистка canvas
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Отрисовка змейки
    ctx.fillStyle = 'lime';
    for (let i = 0; i < snake.length; i++) {
        ctx.fillRect(snake[i].x * gridSize, snake[i].y * gridSize, gridSize - 2, gridSize - 2);
    }
    
    // Отрисовка еды (яблока)
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(
        food.x * gridSize + gridSize/2, 
        food.y * gridSize + gridSize/2, 
        gridSize/2 - 2, 
        0, 
        2 * Math.PI
    );
    ctx.fill();
    
    // Отрисовка счета
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText('Счет: ' + score, 10, 25);
    ctx.fillText('Длина: ' + snake.length, 10, 50);
}

// Обновление игры
function update() {
    // Двигаем голову змейки
    let head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};
    
    // Проверка на выход за границы
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        gameOver();
        return;
    }
    
    // Проверка на столкновение с собой
    for (let i = 0; i < snake.length; i++) {
        if (snake[i].x === head.x && snake[i].y === head.y) {
            gameOver();
            return;
        }
    }
    
    // Добавляем новую голову
    snake.unshift(head);
    
    // Проверка съедания еды
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        
        // Увеличиваем длину змейки (НЕ удаляем хвост в этом кадре)
        generateFood();
        
        // Можно увеличить скорость при достижении определенного счета
        if (score % 50 === 0 && gameSpeed < 20) {
            gameSpeed += 1;
        }
    } else {
        // Если не съели еду - удаляем хвост, чтобы сохранить длину
        snake.pop();
    }
}

// Конец игры
function gameOver() {
    alert('Игра окончена! Ваш счет: ' + score + '\nДлина змейки: ' + snake.length);
    
    // Сброс игры
    snake = [{x: 10, y: 10}];
    direction = {x: 0, y: 0};
    score = 0;
    tailLength = 1;
    gameSpeed = 10;
    generateFood();
}

// Управление с клавиатуры
document.addEventListener('keydown', (event) => {
    // Стрелка вверх
    if (event.key === 'ArrowUp' && direction.y !== 1) {
        direction = {x: 0, y: -1};
    }
    // Стрелка вниз
    if (event.key === 'ArrowDown' && direction.y !== -1) {
        direction = {x: 0, y: 1};
    }
    // Стрелка влево
    if (event.key === 'ArrowLeft' && direction.x !== 1) {
        direction = {x: -1, y: 0};
    }
    // Стрелка вправо
    if (event.key === 'ArrowRight' && direction.x !== -1) {
        direction = {x: 1, y: 0};
    }
    
    // Пробел для паузы/старта
    if (event.key === ' ') {
        if (gameLoop) {
            clearInterval(gameLoop);
            gameLoop = null;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'black';
            ctx.font = '30px Arial';
            ctx.fillText('ПАУЗА', canvas.width/2 - 60, canvas.height/2);
        } else {
            gameLoop = setInterval(game, 1000 / gameSpeed);
        }
    }
});

// Основной игровой цикл
function game() {
    update();
    draw();
}

// Запуск игры
generateFood();
let gameLoop = setInterval(game, 1000 / gameSpeed);

// Добавляем кнопки управления для мобильных устройств
document.addEventListener('DOMContentLoaded', () => {
    const controlsDiv = document.createElement('div');
    controlsDiv.style.cssText = `
        margin-top: 20px;
        text-align: center;
    `;
    
    const buttonStyle = `
        padding: 15px;
        margin: 5px;
        font-size: 20px;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    `;
    
    const buttonsHTML = `
        <div style="margin-bottom: 10px;">
            <button id="upBtn" style="${buttonStyle}">↑</button>
        </div>
        <div>
            <button id="leftBtn" style="${buttonStyle}">←</button>
            <button id="downBtn" style="${buttonStyle}">↓</button>
            <button id="rightBtn" style="${buttonStyle}">→</button>
        </div>
        <div style="margin-top: 10px;">
            <button id="pauseBtn" style="${buttonStyle}">Пауза</button>
        </div>
    `;
    
    controlsDiv.innerHTML = buttonsHTML;
    document.querySelector('.game-container').appendChild(controlsDiv);
    
    // Назначаем обработчики для кнопок
    document.getElementById('upBtn').addEventListener('click', () => {
        if (direction.y !== 1) direction = {x: 0, y: -1};
    });
    document.getElementById('downBtn').addEventListener('click', () => {
        if (direction.y !== -1) direction = {x: 0, y: 1};
    });
    document.getElementById('leftBtn').addEventListener('click', () => {
        if (direction.x !== 1) direction = {x: -1, y: 0};
    });
    document.getElementById('rightBtn').addEventListener('click', () => {
        if (direction.x !== -1) direction = {x: 1, y: 0};
    });
    document.getElementById('pauseBtn').addEventListener('click', () => {
        if (gameLoop) {
            clearInterval(gameLoop);
            gameLoop = null;
            document.getElementById('pauseBtn').textContent = 'Продолжить';
        } else {
            gameLoop = setInterval(game, 1000 / gameSpeed);
            document.getElementById('pauseBtn').textContent = 'Пауза';
        }
    });
});