import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered",
)

st.title("🧱 벽돌깨기")
st.caption("← → 방향키, 마우스 또는 터치로 패들을 움직이세요.")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    background: #0f172a;
    font-family: Arial, sans-serif;
}

body {
    overflow: hidden;
}

#game-container {
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    color: white;
}

#info {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;

    padding: 11px 15px;

    background: #1e293b;

    border-radius: 12px 12px 0 0;

    font-size: 15px;
    font-weight: bold;
}

#gameCanvas {
    display: block;

    width: 100%;
    max-width: 760px;

    background:
        radial-gradient(
            circle at center,
            #172554 0%,
            #020617 70%
        );

    border: 2px solid #334155;
    border-top: none;

    touch-action: none;
    user-select: none;
}

#buttons {
    display: flex;
    justify-content: center;
    gap: 8px;

    margin-top: 10px;
}

button {
    border: none;
    border-radius: 8px;

    padding: 10px 16px;

    background: #2563eb;
    color: white;

    font-size: 14px;
    font-weight: bold;

    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

button:active {
    transform: scale(0.97);
}

#startBtn {
    background: #16a34a;
}

#startBtn:hover {
    background: #15803d;
}

#restartBtn {
    background: #7c3aed;
}

#restartBtn:hover {
    background: #6d28d9;
}

#message {
    min-height: 24px;

    margin-top: 8px;

    text-align: center;

    color: #cbd5e1;

    font-size: 14px;
}

@media (max-width: 600px) {

    #info {
        font-size: 13px;
        padding: 9px;
    }

    button {
        padding: 9px 11px;
        font-size: 12px;
    }
}
</style>
</head>

<body>

<div id="game-container">

    <div id="info">
        <span>
            점수:
            <span id="score">0</span>
        </span>

        <span>
            목숨:
            <span id="lives">3</span>
        </span>

        <span>
            레벨:
            <span id="level">1</span>
        </span>
    </div>

    <canvas
        id="gameCanvas"
        width="760"
        height="500">
    </canvas>

    <div id="buttons">

        <button id="startBtn">
            게임 시작
        </button>

        <button id="pauseBtn">
            일시정지
        </button>

        <button id="restartBtn">
            다시 시작
        </button>

    </div>

    <div id="message">
        게임 시작 버튼을 눌러주세요.
    </div>

</div>


<script>
"use strict";

/* =====================================================
   Canvas
===================================================== */

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");


/* =====================================================
   UI
===================================================== */

const scoreElement =
    document.getElementById("score");

const livesElement =
    document.getElementById("lives");

const levelElement =
    document.getElementById("level");

const messageElement =
    document.getElementById("message");

const startBtn =
    document.getElementById("startBtn");

const pauseBtn =
    document.getElementById("pauseBtn");

const restartBtn =
    document.getElementById("restartBtn");


/* =====================================================
   게임 상태
===================================================== */

let score = 0;
let lives = 3;
let level = 1;

let gameRunning = false;
let paused = false;
let gameOver = false;

let animationId = null;


/* =====================================================
   키보드 상태
===================================================== */

const keys = {
    left: false,
    right: false
};


/* =====================================================
   공
===================================================== */

const ball = {

    x: canvas.width / 2,

    y: canvas.height - 80,

    radius: 8,

    dx: 4,

    dy: -4,

    color: "#f8fafc"
};


/* =====================================================
   패들
===================================================== */

const paddle = {

    width: 120,

    height: 14,

    x: 0,

    y: canvas.height - 35,

    speed: 8
};


/* =====================================================
   벽돌 설정
===================================================== */

const brickSettings = {

    columns: 10,

    width: 65,

    height: 22,

    padding: 8,

    offsetTop: 50
};


let bricks = [];


/* =====================================================
   벽돌 색상
===================================================== */

const brickColors = [

    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#06b6d4",
    "#3b82f6",
    "#8b5cf6"

];


/* =====================================================
   유틸리티
===================================================== */

function clamp(value, min, max) {

    return Math.max(
        min,
        Math.min(max, value)
    );
}


/* =====================================================
   둥근 사각형
   roundRect 미지원 브라우저 대비
===================================================== */

function roundedRect(
    context,
    x,
    y,
    width,
    height,
    radius
) {

    const r =
        Math.min(
            radius,
            width / 2,
            height / 2
        );

    context.beginPath();

    context.moveTo(
        x + r,
        y
    );

    context.lineTo(
        x + width - r,
        y
    );

    context.quadraticCurveTo(
        x + width,
        y,
        x + width,
        y + r
    );

    context.lineTo(
        x + width,
        y + height - r
    );

    context.quadraticCurveTo(
        x + width,
        y + height,
        x + width - r,
        y + height
    );

    context.lineTo(
        x + r,
        y + height
    );

    context.quadraticCurveTo(
        x,
        y + height,
        x,
        y + height - r
    );

    context.lineTo(
        x,
        y + r
    );

    context.quadraticCurveTo(
        x,
        y,
        x + r,
        y
    );

    context.closePath();
}


/* =====================================================
   벽돌 생성
===================================================== */

function createBricks() {

    bricks = [];

    const rows =
        Math.min(
            4 + level,
            8
        );

    const totalWidth =
        brickSettings.columns *
        brickSettings.width
        +
        (brickSettings.columns - 1) *
        brickSettings.padding;

    const startX =
        (canvas.width - totalWidth) / 2;

    for (
        let row = 0;
        row < rows;
        row++
    ) {

        for (
            let column = 0;
            column < brickSettings.columns;
            column++
        ) {

            bricks.push({

                x:
                    startX +
                    column *
                    (
                        brickSettings.width +
                        brickSettings.padding
                    ),

                y:
                    brickSettings.offsetTop +
                    row *
                    (
                        brickSettings.height +
                        brickSettings.padding
                    ),

                width:
                    brickSettings.width,

                height:
                    brickSettings.height,

                alive: true,

                color:
                    brickColors[
                        row %
                        brickColors.length
                    ]

            });
        }
    }
}


/* =====================================================
   공 속도
===================================================== */

function getBallSpeed() {

    return 4.2 + (level - 1) * 0.35;
}


/* =====================================================
   공 초기화
===================================================== */

function resetBall() {

    const speed =
        getBallSpeed();

    ball.x =
        canvas.width / 2;

    ball.y =
        canvas.height - 75;

    const direction =
        Math.random() < 0.5
            ? -1
            : 1;

    ball.dx =
        direction * speed * 0.75;

    ball.dy =
        -speed;

}


/* =====================================================
   패들 초기화
===================================================== */

function resetPaddle() {

    paddle.x =
        (
            canvas.width -
            paddle.width
        ) / 2;
}


/* =====================================================
   게임 전체 초기화
===================================================== */

function resetGame() {

    cancelAnimationFrame(
        animationId
    );

    animationId = null;

    score = 0;
    lives = 3;
    level = 1;

    gameRunning = false;
    paused = false;
    gameOver = false;

    keys.left = false;
    keys.right = false;

    pauseBtn.textContent =
        "일시정지";

    scoreElement.textContent =
        score;

    livesElement.textContent =
        lives;

    levelElement.textContent =
        level;

    createBricks();

    resetBall();
    resetPaddle();

    messageElement.textContent =
        "게임 시작 버튼을 눌러주세요.";

    draw();
}


/* =====================================================
   게임 시작
===================================================== */

function startGame() {

    if (gameOver) {

        resetGame();
    }

    if (gameRunning) {
        return;
    }

    gameRunning = true;
    paused = false;
    gameOver = false;

    messageElement.textContent =
        "게임 진행 중!";

    pauseBtn.textContent =
        "일시정지";

    startGameLoop();
}


/* =====================================================
   게임 루프 시작
===================================================== */

function startGameLoop() {

    cancelAnimationFrame(
        animationId
    );

    animationId =
        requestAnimationFrame(
            gameLoop
        );
}


/* =====================================================
   일시정지
===================================================== */

function togglePause() {

    if (
        !gameRunning ||
        gameOver
    ) {
        return;
    }

    paused = !paused;

    if (paused) {

        pauseBtn.textContent =
            "계속하기";

        messageElement.textContent =
            "⏸ 게임이 일시정지되었습니다.";

        cancelAnimationFrame(
            animationId
        );

        animationId = null;

    } else {

        pauseBtn.textContent =
            "일시정지";

        messageElement.textContent =
            "게임 진행 중!";

        startGameLoop();
    }
}


/* =====================================================
   게임 재시작
===================================================== */

function restartGame() {

    resetGame();

    startGame();
}


/* =====================================================
   공 그리기
===================================================== */

function drawBall() {

    ctx.save();

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        ball.color;

    ctx.shadowColor =
        "#ffffff";

    ctx.shadowBlur =
        12;

    ctx.fill();

    ctx.closePath();

    ctx.restore();
}


/* =====================================================
   패들 그리기
===================================================== */

function drawPaddle() {

    const gradient =
        ctx.createLinearGradient(
            paddle.x,
            paddle.y,
            paddle.x + paddle.width,
            paddle.y
        );

    gradient.addColorStop(
        0,
        "#0284c7"
    );

    gradient.addColorStop(
        0.5,
        "#38bdf8"
    );

    gradient.addColorStop(
        1,
        "#0ea5e9"
    );

    ctx.fillStyle =
        gradient;

    roundedRect(
        ctx,
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.fill();

    ctx.strokeStyle =
        "rgba(255,255,255,0.3)";

    ctx.stroke();
}


/* =====================================================
   벽돌 그리기
===================================================== */

function drawBricks() {

    for (
        const brick of bricks
    ) {

        if (!brick.alive) {
            continue;
        }

        const gradient =
            ctx.createLinearGradient(
                brick.x,
                brick.y,
                brick.x,
                brick.y +
                brick.height
            );

        gradient.addColorStop(
            0,
            brick.color
        );

        gradient.addColorStop(
            1,
            "#0f172a"
        );

        ctx.fillStyle =
            gradient;

        roundedRect(
            ctx,
            brick.x,
            brick.y,
            brick.width,
            brick.height,
            5
        );

        ctx.fill();

        ctx.strokeStyle =
            "rgba(255,255,255,0.2)";

        ctx.stroke();
    }
}


/* =====================================================
   전체 그리기
===================================================== */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();
}


/* =====================================================
   패들 이동
===================================================== */

function updatePaddle() {

    if (!gameRunning || paused) {
        return;
    }

    if (keys.left) {

        paddle.x -=
            paddle.speed;
    }

    if (keys.right) {

        paddle.x +=
            paddle.speed;
    }

    paddle.x =
        clamp(
            paddle.x,
            0,
            canvas.width -
            paddle.width
        );
}


/* =====================================================
   사각형 충돌 검사
===================================================== */

function circleRectCollision(
    circle,
    rect
) {

    const closestX =
        clamp(
            circle.x,
            rect.x,
            rect.x + rect.width
        );

    const closestY =
        clamp(
            circle.y,
            rect.y,
            rect.y + rect.height
        );

    const dx =
        circle.x - closestX;

    const dy =
        circle.y - closestY;

    return (
        dx * dx +
        dy * dy
        <=
        circle.radius *
        circle.radius
    );
}


/* =====================================================
   벽돌 충돌 처리
===================================================== */

function checkBrickCollision() {

    for (
        const brick of bricks
    ) {

        if (!brick.alive) {
            continue;
        }

        if (
            circleRectCollision(
                ball,
                brick
            )
        ) {

            brick.alive = false;

            score += 10;

            scoreElement.textContent =
                score;

            /*
             * 공이 벽돌 내부에 남아 있는 것을
             * 방지하기 위해 충돌 방향을 결정합니다.
             */

            const ballCenterX =
                ball.x;

            const ballCenterY =
                ball.y;

            const brickCenterX =
                brick.x +
                brick.width / 2;

            const brickCenterY =
                brick.y +
                brick.height / 2;

            const dx =
                ballCenterX -
                brickCenterX;

            const dy =
                ballCenterY -
                brickCenterY;

            const overlapX =
                (
                    brick.width / 2 +
                    ball.radius
                )
                -
                Math.abs(dx);

            const overlapY =
                (
                    brick.height / 2 +
                    ball.radius
                )
                -
                Math.abs(dy);

            if (
                overlapX <
                overlapY
            ) {

                ball.dx =
                    -ball.dx;

                if (dx > 0) {

                    ball.x =
                        brick.x +
                        brick.width +
                        ball.radius;

                } else {

                    ball.x =
                        brick.x -
                        ball.radius;
                }

            } else {

                ball.dy =
                    -ball.dy;

                if (dy > 0) {

                    ball.y =
                        brick.y +
                        brick.height +
                        ball.radius;

                } else {

                    ball.y =
                        brick.y -
                        ball.radius;
                }
            }

            return true;
        }
    }

    return false;
}


/* =====================================================
   패들 충돌
===================================================== */

function checkPaddleCollision() {

    if (
        ball.dy <= 0
    ) {
        return;
    }

    if (
        !circleRectCollision(
            ball,
            paddle
        )
    ) {
        return;
    }

    /*
     * 공을 패들 위쪽으로 강제로 이동시켜
     * 패들 내부에 끼는 현상을 방지합니다.
     */

    ball.y =
        paddle.y -
        ball.radius;

    const paddleCenter =
        paddle.x +
        paddle.width / 2;

    let hitPosition =
        (
            ball.x -
            paddleCenter
        )
        /
        (
            paddle.width / 2
        );

    hitPosition =
        clamp(
            hitPosition,
            -1,
            1
        );

    const currentSpeed =
        Math.sqrt(
            ball.dx * ball.dx +
            ball.dy * ball.dy
        );

    /*
     * 패들 중앙에 맞으면 위로,
     * 가장자리에 맞으면 대각선으로 튕깁니다.
     */

    const angle =
        hitPosition *
        (Math.PI / 3);

    ball.dx =
        currentSpeed *
        Math.sin(angle);

    ball.dy =
        -Math.abs(
            currentSpeed *
            Math.cos(angle)
        );
}


/* =====================================================
   벽 충돌
===================================================== */

function checkWallCollision() {

    if (
        ball.x -
        ball.radius <= 0
    ) {

        ball.x =
            ball.radius;

        ball.dx =
            Math.abs(ball.dx);
    }

    if (
        ball.x +
        ball.radius >=
        canvas.width
    ) {

        ball.x =
            canvas.width -
            ball.radius;

        ball.dx =
            -Math.abs(ball.dx);
    }

    if (
        ball.y -
        ball.radius <= 0
    ) {

        ball.y =
            ball.radius;

        ball.dy =
            Math.abs(ball.dy);
    }
}


/* =====================================================
   공 이동
===================================================== */

function updateBall() {

    if (
        !gameRunning ||
        paused
    ) {
        return;
    }

    /*
     * 빠른 공이 벽돌을 통과하는 문제를 줄이기 위해
     * 한 프레임을 여러 개의 작은 단계로 나눕니다.
     */

    const speed =
        Math.sqrt(
            ball.dx * ball.dx +
            ball.dy * ball.dy
        );

    const steps =
        Math.max(
            1,
            Math.ceil(speed / 4)
        );

    const stepX =
        ball.dx / steps;

    const stepY =
        ball.dy / steps;

    for (
        let i = 0;
        i < steps;
        i++
    ) {

        ball.x += stepX;
        ball.y += stepY;

        checkWallCollision();

        checkPaddleCollision();

        checkBrickCollision();

        /*
         * 공이 바닥 아래로 완전히 내려가면
         * 즉시 목숨을 처리합니다.
         */

        if (
            ball.y -
            ball.radius >
            canvas.height
        ) {

            loseLife();

            return;
        }
    }
}


/* =====================================================
   남은 벽돌 확인
===================================================== */

function getRemainingBricks() {

    let count = 0;

    for (
        const brick of bricks
    ) {

        if (brick.alive) {
            count++;
        }
    }

    return count;
}


/* =====================================================
   다음 레벨
===================================================== */

function nextLevel() {

    level++;

    levelElement.textContent =
        level;

    createBricks();

    resetBall();
    resetPaddle();

    messageElement.textContent =
        "🎉 레벨 " +
        level +
        " 시작!";
}


/* =====================================================
   목숨 감소
===================================================== */

function loseLife() {

    if (!gameRunning) {
        return;
    }

    lives--;

    livesElement.textContent =
        lives;

    if (lives <= 0) {

        endGame();

        return;
    }

    resetBall();
    resetPaddle();

    messageElement.textContent =
        "💥 공을 놓쳤습니다! " +
        "남은 목숨: " +
        lives;
}


/* =====================================================
   게임 종료
===================================================== */

function endGame() {

    gameRunning = false;
    paused = false;
    gameOver = true;

    cancelAnimationFrame(
        animationId
    );

    animationId = null;

    keys.left = false;
    keys.right = false;

    pauseBtn.textContent =
        "일시정지";

    messageElement.textContent =
        "💥 게임 오버! 최종 점수: " +
        score +
        "점";

    draw();
}


/* =====================================================
   키보드
===================================================== */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "ArrowLeft"
        ) {

            keys.left = true;

            event.preventDefault();
        }

        else if (
            event.key === "ArrowRight"
        ) {

            keys.right = true;

            event.preventDefault();
        }

        else if (
            event.code === "Space"
        ) {

            togglePause();

            event.preventDefault();
        }
    }
);


document.addEventListener(
    "keyup",
    function(event) {

        if (
            event.key === "ArrowLeft"
        ) {

            keys.left = false;
        }

        else if (
            event.key === "ArrowRight"
        ) {

            keys.right = false;
        }
    }
);


/* =====================================================
   마우스
===================================================== */

function movePaddleToClientX(
    clientX
) {

    const rect =
        canvas.getBoundingClientRect();

    const scaleX =
        canvas.width /
        rect.width;

    const mouseX =
        (
            clientX -
            rect.left
        ) *
        scaleX;

    paddle.x =
        mouseX -
        paddle.width / 2;

    paddle.x =
        clamp(
            paddle.x,
            0,
            canvas.width -
            paddle.width
        );
}


canvas.addEventListener(
    "mousemove",
    function(event) {

        if (!gameOver) {

            movePaddleToClientX(
                event.clientX
            );
        }
    }
);


/* =====================================================
   터치
===================================================== */

canvas.addEventListener(
    "touchstart",
    function(event) {

        if (
            event.touches.length > 0
        ) {

            movePaddleToClientX(
                event.touches[0].clientX
            );
        }

        event.preventDefault();

    },
    {
        passive: false
    }
);


canvas.addEventListener(
    "touchmove",
    function(event) {

        if (
            event.touches.length > 0
        ) {

            movePaddleToClientX(
                event.touches[0].clientX
            );
        }

        event.preventDefault();

    },
    {
        passive: false
    }
);


/* =====================================================
   게임 루프
===================================================== */

function gameLoop() {

    if (
        !gameRunning ||
        paused
    ) {

        animationId = null;

        return;
    }

    updatePaddle();

    updateBall();

    /*
     * 모든 벽돌을 제거했다면
     * 다음 레벨로 이동합니다.
     */

    if (
        gameRunning &&
        getRemainingBricks() === 0
    ) {

        nextLevel();
    }

    draw();

    animationId =
        requestAnimationFrame(
            gameLoop
        );
}


/* =====================================================
   버튼 이벤트
===================================================== */

startBtn.addEventListener(
    "click",
    startGame
);

pauseBtn.addEventListener(
    "click",
    togglePause
);

restartBtn.addEventListener(
    "click",
    restartGame
);


/* =====================================================
   초기화
===================================================== */

resetGame();

</script>

</body>
</html>
"""


components.html(
    GAME_HTML,
    height=650,
    scrolling=False
)
