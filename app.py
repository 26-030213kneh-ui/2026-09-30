import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
    layout="centered",
)


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
    color: white;
    font-family: Arial, "Noto Sans KR", sans-serif;
}

body {
    overflow-x: hidden;
}

#game-wrapper {
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    padding: 8px 0 20px;
}

#player-area {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
}

#playerName {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #475569;
    border-radius: 8px;
    background: #1e293b;
    color: white;
    outline: none;
    font-size: 14px;
}

#playerName:focus {
    border-color: #38bdf8;
}

#info {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
    padding: 10px;
    background: #1e293b;
    border-radius: 12px 12px 0 0;
    text-align: center;
}

.info-item {
    color: #94a3b8;
    font-size: 12px;
    font-weight: bold;
}

.info-value {
    display: block;
    margin-top: 4px;
    color: white;
    font-size: 17px;
}

#gameCanvas {
    display: block;
    width: 100%;
    height: auto;
    background:
        radial-gradient(
            circle at center,
            #172554 0%,
            #020617 75%
        );
    border-left: 2px solid #334155;
    border-right: 2px solid #334155;
    border-bottom: 2px solid #334155;
    touch-action: none;
    user-select: none;
}

#buttons {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

button {
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    color: white;
    font-size: 13px;
    font-weight: bold;
    cursor: pointer;
}

button:active {
    transform: scale(0.96);
}

#startBtn {
    background: #16a34a;
}

#pauseBtn {
    background: #f59e0b;
}

#restartBtn {
    background: #7c3aed;
}

#rankingBtn {
    background: #db2777;
}

#message {
    min-height: 28px;
    margin-top: 9px;
    text-align: center;
    color: #cbd5e1;
    font-size: 14px;
}

#item-help {
    margin-top: 10px;
    padding: 10px;
    background: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #cbd5e1;
    font-size: 12px;
    line-height: 1.7;
    text-align: center;
}

#rankingPanel {
    display: none;
    margin-top: 12px;
    padding: 12px;
    background: #111827;
    border: 1px solid #334155;
    border-radius: 10px;
}

#rankingPanel h3 {
    margin: 0 0 10px;
    color: #facc15;
    text-align: center;
}

.ranking-row {
    display: grid;
    grid-template-columns: 45px 1fr 80px 60px;
    gap: 5px;
    padding: 8px 5px;
    border-bottom: 1px solid #1e293b;
    font-size: 13px;
}

.ranking-row:last-child {
    border-bottom: none;
}

.rank-number {
    color: #facc15;
    font-weight: bold;
}

.rank-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rank-score {
    color: #38bdf8;
    text-align: right;
}

.rank-level {
    color: #a78bfa;
    text-align: right;
}

@media (max-width: 600px) {
    #info {
        padding: 8px 3px;
    }

    .info-item {
        font-size: 10px;
    }

    .info-value {
        font-size: 14px;
    }

    button {
        padding: 9px 10px;
        font-size: 11px;
    }
}
</style>
</head>

<body>

<div id="game-wrapper">

    <div id="player-area">
        <input
            id="playerName"
            maxlength="12"
            autocomplete="off"
            value="Player"
            placeholder="닉네임"
        >
    </div>

    <div id="info">

        <div class="info-item">
            점수
            <span id="score" class="info-value">0</span>
        </div>

        <div class="info-item">
            목숨
            <span id="lives" class="info-value">3</span>
        </div>

        <div class="info-item">
            레벨
            <span id="level" class="info-value">1</span>
        </div>

        <div class="info-item">
            공
            <span id="ballCount" class="info-value">1</span>
        </div>

        <div class="info-item">
            효과
            <span id="effect" class="info-value">-</span>
        </div>

    </div>

    <canvas
        id="gameCanvas"
        width="760"
        height="500">
    </canvas>

    <div id="buttons">
        <button id="startBtn">▶ 게임 시작</button>
        <button id="pauseBtn">⏸ 일시정지</button>
        <button id="restartBtn">🔄 다시 시작</button>
        <button id="rankingBtn">🏆 랭킹</button>
    </div>

    <div id="message">
        닉네임을 입력하고 게임을 시작하세요.
    </div>

    <div id="item-help">
        🎁 <b>아이템</b><br>
        🔵 패들 확대 |
        🟡 공 느려짐 |
        ❤️ 목숨 +1 |
        🟣 멀티볼 |
        ⭐ 보너스 +50
        <br>
        벽돌을 깨면 25% 확률로 아이템이 드롭됩니다.
    </div>

    <div id="rankingPanel">
        <h3>🏆 TOP 10 랭킹</h3>
        <div id="rankingList"></div>
    </div>

</div>


<script>
"use strict";


/* =========================================================
   기본 설정
========================================================= */

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");

const scoreElement =
    document.getElementById("score");

const livesElement =
    document.getElementById("lives");

const levelElement =
    document.getElementById("level");

const ballCountElement =
    document.getElementById("ballCount");

const effectElement =
    document.getElementById("effect");

const playerNameInput =
    document.getElementById("playerName");

const messageElement =
    document.getElementById("message");

const startBtn =
    document.getElementById("startBtn");

const pauseBtn =
    document.getElementById("pauseBtn");

const restartBtn =
    document.getElementById("restartBtn");

const rankingBtn =
    document.getElementById("rankingBtn");

const rankingPanel =
    document.getElementById("rankingPanel");

const rankingList =
    document.getElementById("rankingList");


/* =========================================================
   게임 상태
========================================================= */

let score = 0;
let lives = 3;
let level = 1;

let gameRunning = false;
let paused = false;
let gameOver = false;

let animationId = null;
let lastTime = 0;

let levelTransitioning = false;


/* =========================================================
   입력
========================================================= */

const keys = {
    left: false,
    right: false
};


/* =========================================================
   패들
========================================================= */

const paddle = {
    x: 0,
    y: canvas.height - 35,
    width: 120,
    baseWidth: 120,
    height: 14,
    speed: 520,
    wideTimer: 0
};


/* =========================================================
   공 / 아이템 / 벽돌
========================================================= */

let balls = [];
let items = [];
let bricks = [];


/* =========================================================
   효과
========================================================= */

const effects = {
    slowTimer: 0
};


/* =========================================================
   벽돌 설정
========================================================= */

const BRICK_COLUMNS = 10;
const BRICK_WIDTH = 65;
const BRICK_HEIGHT = 22;
const BRICK_PADDING = 8;
const BRICK_TOP = 50;


/* =========================================================
   색상
========================================================= */

const BRICK_COLORS = [
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#06b6d4",
    "#3b82f6",
    "#8b5cf6"
];


/* =========================================================
   아이템
========================================================= */

const ITEM_TYPES = {
    WIDE: {
        name: "패들 확대",
        icon: "🔵",
        color: "#38bdf8"
    },

    SLOW: {
        name: "공 느려짐",
        icon: "🟡",
        color: "#facc15"
    },

    LIFE: {
        name: "목숨 +1",
        icon: "❤️",
        color: "#fb7185"
    },

    MULTI: {
        name: "멀티볼",
        icon: "🟣",
        color: "#c084fc"
    },

    SCORE: {
        name: "보너스 +50",
        icon: "⭐",
        color: "#fbbf24"
    }
};


const RANKING_KEY =
    "brick_breaker_ranking_v2";


/* =========================================================
   유틸
========================================================= */

function clamp(value, min, max) {
    return Math.max(
        min,
        Math.min(max, value)
    );
}


function randomRange(min, max) {
    return Math.random() *
        (max - min) +
        min;
}


function getBallSpeed() {
    return 260 +
        (level - 1) * 22;
}


function getRemainingBricks() {

    let count = 0;

    for (const brick of bricks) {

        if (brick.alive) {
            count++;
        }
    }

    return count;
}


/* =========================================================
   안전한 localStorage
========================================================= */

function readRankingStorage() {

    try {

        const raw =
            localStorage.getItem(
                RANKING_KEY
            );

        if (!raw) {
            return [];
        }

        const data =
            JSON.parse(raw);

        if (!Array.isArray(data)) {
            return [];
        }

        return data.filter(item =>
            item &&
            typeof item.name === "string" &&
            Number.isFinite(Number(item.score)) &&
            Number.isFinite(Number(item.level))
        );

    } catch (error) {

        console.warn(
            "랭킹을 읽을 수 없습니다.",
            error
        );

        return [];
    }
}


function writeRankingStorage(data) {

    try {

        localStorage.setItem(
            RANKING_KEY,
            JSON.stringify(data)
        );

        return true;

    } catch (error) {

        console.warn(
            "랭킹을 저장할 수 없습니다.",
            error
        );

        return false;
    }
}


/* =========================================================
   벽돌 생성
========================================================= */

function createBricks() {

    bricks = [];

    const rows =
        Math.min(
            4 + level,
            8
        );

    const totalWidth =
        BRICK_COLUMNS * BRICK_WIDTH +
        (BRICK_COLUMNS - 1) *
        BRICK_PADDING;

    const startX =
        (canvas.width - totalWidth) / 2;


    for (
        let row = 0;
        row < rows;
        row++
    ) {

        for (
            let column = 0;
            column < BRICK_COLUMNS;
            column++
        ) {

            bricks.push({

                x:
                    startX +
                    column *
                    (
                        BRICK_WIDTH +
                        BRICK_PADDING
                    ),

                y:
                    BRICK_TOP +
                    row *
                    (
                        BRICK_HEIGHT +
                        BRICK_PADDING
                    ),

                width: BRICK_WIDTH,
                height: BRICK_HEIGHT,

                alive: true,

                color:
                    BRICK_COLORS[
                        row %
                        BRICK_COLORS.length
                    ]
            });
        }
    }
}


/* =========================================================
   공 생성
========================================================= */

function createBall(
    x,
    y,
    angle,
    speed
) {

    return {

        x: x,
        y: y,

        radius: 8,

        dx:
            Math.cos(angle) *
            speed,

        dy:
            Math.sin(angle) *
            speed
    };
}


function createMainBall() {

    const speed =
        getBallSpeed();

    const angle =
        -Math.PI / 2 +
        randomRange(
            -0.45,
            0.45
        );

    return createBall(
        canvas.width / 2,
        canvas.height - 75,
        angle,
        speed
    );
}


function resetBalls() {

    balls = [
        createMainBall()
    ];
}


/* =========================================================
   패들 초기화
========================================================= */

function resetPaddle() {

    paddle.width =
        paddle.baseWidth;

    paddle.x =
        (
            canvas.width -
            paddle.width
        ) / 2;

    paddle.wideTimer = 0;
}


/* =========================================================
   아이템 초기화
========================================================= */

function resetItems() {

    items = [];

    effects.slowTimer = 0;
}


/* =========================================================
   게임 초기화
========================================================= */

function resetGame() {

    stopLoop();

    score = 0;
    lives = 3;
    level = 1;

    gameRunning = false;
    paused = false;
    gameOver = false;

    levelTransitioning = false;

    lastTime = 0;

    keys.left = false;
    keys.right = false;

    createBricks();
    resetBalls();
    resetPaddle();
    resetItems();

    pauseBtn.textContent =
        "⏸ 일시정지";

    messageElement.textContent =
        "▶ 게임 시작 버튼을 눌러주세요.";

    updateUI();
    draw();
}


/* =========================================================
   게임 루프 제어
========================================================= */

function stopLoop() {

    if (animationId !== null) {

        cancelAnimationFrame(
            animationId
        );

        animationId = null;
    }
}


function startLoop() {

    stopLoop();

    lastTime =
        performance.now();

    animationId =
        requestAnimationFrame(
            gameLoop
        );
}


/* =========================================================
   UI
========================================================= */

function updateUI() {

    scoreElement.textContent =
        score.toLocaleString();

    livesElement.textContent =
        lives;

    levelElement.textContent =
        level;

    ballCountElement.textContent =
        balls.length;

    updateEffectText();
}


function updateEffectText() {

    const active = [];

    if (paddle.wideTimer > 0) {

        active.push(
            "🔵 " +
            Math.ceil(
                paddle.wideTimer / 1000
            ) +
            "s"
        );
    }

    if (effects.slowTimer > 0) {

        active.push(
            "🟡 " +
            Math.ceil(
                effects.slowTimer / 1000
            ) +
            "s"
        );
    }

    effectElement.textContent =
        active.length > 0
            ? active.join(" ")
            : "-";
}


/* =========================================================
   게임 시작
========================================================= */

function startGame() {

    if (gameRunning) {

        if (paused) {
            togglePause();
        }

        return;
    }


    if (gameOver) {
        resetGame();
    }


    gameRunning = true;
    paused = false;
    gameOver = false;

    messageElement.textContent =
        "🎮 게임 진행 중!";

    pauseBtn.textContent =
        "⏸ 일시정지";

    startLoop();
}


/* =========================================================
   일시정지
========================================================= */

function togglePause() {

    if (
        !gameRunning ||
        gameOver
    ) {
        return;
    }


    paused = !paused;


    if (paused) {

        stopLoop();

        keys.left = false;
        keys.right = false;

        pauseBtn.textContent =
            "▶ 계속하기";

        messageElement.textContent =
            "⏸ 일시정지되었습니다.";

    } else {

        pauseBtn.textContent =
            "⏸ 일시정지";

        messageElement.textContent =
            "🎮 게임 진행 중!";

        startLoop();
    }
}


/* =========================================================
   다시 시작
========================================================= */

function restartGame() {

    resetGame();

    startGame();
}


/* =========================================================
   패들 이동
========================================================= */

function updatePaddle(dt) {

    if (
        !gameRunning ||
        paused
    ) {
        return;
    }


    if (keys.left) {

        paddle.x -=
            paddle.speed * dt;
    }


    if (keys.right) {

        paddle.x +=
            paddle.speed * dt;
    }


    paddle.x =
        clamp(
            paddle.x,
            0,
            canvas.width -
            paddle.width
        );
}


/* =========================================================
   원-사각형 충돌
========================================================= */

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


/* =========================================================
   벽돌 파괴
========================================================= */

function destroyBrick(brick) {

    if (!brick.alive) {
        return;
    }

    brick.alive = false;

    score += 10;


    /*
     * 벽돌 파괴 시 25% 확률로 아이템 생성
     */

    if (Math.random() < 0.25) {

        createItem(
            brick.x +
            brick.width / 2,

            brick.y +
            brick.height / 2
        );
    }
}


/* =========================================================
   아이템 생성
========================================================= */

function createItem(x, y) {

    const r =
        Math.random();

    let type;

    if (r < 0.35) {

        type = "WIDE";

    } else if (r < 0.60) {

        type = "SLOW";

    } else if (r < 0.75) {

        type = "LIFE";

    } else if (r < 0.90) {

        type = "MULTI";

    } else {

        type = "SCORE";
    }


    items.push({

        x: x,
        y: y,

        width: 28,
        height: 28,

        speed: 110,

        type: type
    });
}


/* =========================================================
   아이템 적용
========================================================= */

function applyItem(type) {

    switch (type) {

        case "WIDE":

            paddle.width =
                Math.min(
                    paddle.baseWidth * 1.7,
                    220
                );

            paddle.wideTimer =
                10000;

            messageElement.textContent =
                "🔵 패들이 10초 동안 커집니다!";

            break;


        case "SLOW":

            effects.slowTimer =
                8000;

            messageElement.textContent =
                "🟡 공이 8초 동안 느려집니다!";

            break;


        case "LIFE":

            lives =
                Math.min(
                    lives + 1,
                    9
                );

            messageElement.textContent =
                "❤️ 목숨 +1!";

            break;


        case "MULTI":

            createMultiBalls();

            messageElement.textContent =
                "🟣 멀티볼!";

            break;


        case "SCORE":

            score += 50;

            messageElement.textContent =
                "⭐ 보너스 +50점!";

            break;
    }


    updateUI();
}


/* =========================================================
   멀티볼
========================================================= */

function createMultiBalls() {

    const MAX_BALLS = 5;

    if (
        balls.length >= MAX_BALLS
    ) {
        return;
    }


    const source =
        balls[
            Math.floor(
                Math.random() *
                balls.length
            )
        ];


    if (!source) {
        return;
    }


    const speed =
        Math.sqrt(
            source.dx * source.dx +
            source.dy * source.dy
        );


    const baseAngle =
        Math.atan2(
            source.dy,
            source.dx
        );


    const angles = [
        baseAngle - 0.35,
        baseAngle + 0.35
    ];


    for (const angle of angles) {

        if (
            balls.length >=
            MAX_BALLS
        ) {
            break;
        }

        balls.push(
            createBall(
                source.x,
                source.y,
                angle,
                speed
            )
        );
    }
}


/* =========================================================
   아이템 업데이트
========================================================= */

function updateItems(dt) {

    for (
        let i = items.length - 1;
        i >= 0;
        i--
    ) {

        const item = items[i];

        item.y +=
            item.speed * dt;


        /*
         * 패들과 충돌
         */

        const hit =
            item.y +
            item.height / 2 >=
            paddle.y &&

            item.y -
            item.height / 2 <=
            paddle.y +
            paddle.height &&

            item.x >=
            paddle.x &&

            item.x <=
            paddle.x +
            paddle.width;


        if (hit) {

            applyItem(
                item.type
            );

            items.splice(
                i,
                1
            );

            continue;
        }


        /*
         * 화면 아래로 나간 아이템 제거
         */

        if (
            item.y >
            canvas.height + 40
        ) {

            items.splice(
                i,
                1
            );
        }
    }
}


/* =========================================================
   벽 충돌
========================================================= */

function checkWallCollision(ball) {

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


/* =========================================================
   패들 충돌
========================================================= */

function checkPaddleCollision(ball) {

    if (ball.dy <= 0) {
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
     * 패들 안쪽으로 파고드는 것을 방지
     */

    ball.y =
        paddle.y -
        ball.radius;


    const center =
        paddle.x +
        paddle.width / 2;


    let position =
        (
            ball.x -
            center
        ) /
        (
            paddle.width / 2
        );


    position =
        clamp(
            position,
            -1,
            1
        );


    const speed =
        Math.sqrt(
            ball.dx * ball.dx +
            ball.dy * ball.dy
        );


    const angle =
        position *
        Math.PI / 3;


    ball.dx =
        speed *
        Math.sin(angle);


    ball.dy =
        -Math.abs(
            speed *
            Math.cos(angle)
        );
}


/* =========================================================
   벽돌 충돌
========================================================= */

function checkBrickCollision(ball) {

    for (const brick of bricks) {

        if (!brick.alive) {
            continue;
        }


        if (
            !circleRectCollision(
                ball,
                brick
            )
        ) {
            continue;
        }


        /*
         * 이미 깨진 벽돌은 다시 처리하지 않습니다.
         */

        destroyBrick(brick);


        const brickCenterX =
            brick.x +
            brick.width / 2;

        const brickCenterY =
            brick.y +
            brick.height / 2;


        const dx =
            ball.x -
            brickCenterX;

        const dy =
            ball.y -
            brickCenterY;


        const overlapX =
            brick.width / 2 +
            ball.radius -
            Math.abs(dx);

        const overlapY =
            brick.height / 2 +
            ball.radius -
            Math.abs(dy);


        if (
            overlapX <
            overlapY
        ) {

            ball.dx =
                -ball.dx;

        } else {

            ball.dy =
                -ball.dy;
        }


        /*
         * 한 이동 단계에서는 한 벽돌만 처리
         */

        return true;
    }


    return false;
}


/* =========================================================
   공 업데이트
========================================================= */

function updateSingleBall(
    ball,
    dt
) {

    let multiplier = 1;

    if (
        effects.slowTimer > 0
    ) {
        multiplier = 0.55;
    }


    const dx =
        ball.dx *
        dt *
        multiplier;

    const dy =
        ball.dy *
        dt *
        multiplier;


    /*
     * 빠른 공의 터널링 방지
     *
     * 이동 거리를 작은 단계로 나눠
     * 각 단계마다 충돌 검사
     */

    const distance =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    const steps =
        Math.max(
            1,
            Math.ceil(
                distance / 4
            )
        );


    const stepX =
        dx / steps;

    const stepY =
        dy / steps;


    for (
        let i = 0;
        i < steps;
        i++
    ) {

        ball.x += stepX;
        ball.y += stepY;


        checkWallCollision(ball);

        checkPaddleCollision(ball);

        checkBrickCollision(ball);


        /*
         * 공이 화면 아래로 완전히 빠졌으면
         * 이 공만 제거
         */

        if (
            ball.y -
            ball.radius >
            canvas.height
        ) {

            return false;
        }
    }


    return true;
}


/* =========================================================
   전체 공 업데이트
========================================================= */

function updateBalls(dt) {

    /*
     * 여기서 중요한 점:
     *
     * 멀티볼에서 공 하나가 빠져도
     * 즉시 목숨을 잃지 않습니다.
     *
     * 모든 공이 사라졌을 때만 목숨 감소.
     */

    for (
        let i = balls.length - 1;
        i >= 0;
        i--
    ) {

        const alive =
            updateSingleBall(
                balls[i],
                dt
            );


        if (!alive) {

            balls.splice(
                i,
                1
            );
        }
    }


    if (
        balls.length === 0
    ) {

        loseLife();
    }
}


/* =========================================================
   목숨 감소
========================================================= */

function loseLife() {

    if (
        !gameRunning ||
        gameOver
    ) {
        return;
    }


    lives--;


    if (lives <= 0) {

        lives = 0;

        updateUI();

        endGame();

        return;
    }


    /*
     * 새 공을 가운데에서 출발
     */

    resetBalls();
    resetPaddle();
    resetItems();


    messageElement.textContent =
        "💥 공을 놓쳤습니다! " +
        "남은 목숨: " +
        lives;


    updateUI();
}


/* =========================================================
   효과 시간
========================================================= */

function updateEffects(dtMs) {

    if (
        paddle.wideTimer > 0
    ) {

        paddle.wideTimer -=
            dtMs;


        if (
            paddle.wideTimer <= 0
        ) {

            paddle.wideTimer = 0;

            paddle.width =
                paddle.baseWidth;


            paddle.x =
                clamp(
                    paddle.x,
                    0,
                    canvas.width -
                    paddle.width
                );
        }
    }


    if (
        effects.slowTimer > 0
    ) {

        effects.slowTimer -=
            dtMs;


        if (
            effects.slowTimer < 0
        ) {

            effects.slowTimer = 0;
        }
    }


    updateEffectText();
}


/* =========================================================
   레벨업
========================================================= */

function nextLevel() {

    if (
        levelTransitioning ||
        gameOver ||
        !gameRunning
    ) {
        return;
    }


    levelTransitioning = true;


    level++;

    score += 100;


    createBricks();

    resetBalls();
    resetPaddle();
    resetItems();


    messageElement.textContent =
        "🎉 레벨 " +
        level +
        "! +100 보너스";


    updateUI();


    /*
     * 다음 프레임부터 정상 게임 진행
     */

    requestAnimationFrame(
        function() {
            levelTransitioning = false;
        }
    );
}


/* =========================================================
   그리기 - 둥근 사각형
========================================================= */

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


/* =========================================================
   그리기 - 벽돌
========================================================= */

function drawBricks() {

    for (const brick of bricks) {

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


/* =========================================================
   그리기 - 패들
========================================================= */

function drawPaddle() {

    const gradient =
        ctx.createLinearGradient(
            paddle.x,
            paddle.y,
            paddle.x +
            paddle.width,
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


/* =========================================================
   그리기 - 공
========================================================= */

function drawBalls() {

    for (const ball of balls) {

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
            "#f8fafc";

        ctx.shadowColor =
            "#ffffff";

        ctx.shadowBlur =
            12;

        ctx.fill();

        ctx.closePath();

        ctx.restore();
    }
}


/* =========================================================
   그리기 - 아이템
========================================================= */

function drawItems() {

    for (const item of items) {

        const data =
            ITEM_TYPES[
                item.type
            ];


        ctx.save();

        ctx.fillStyle =
            data.color;

        ctx.shadowColor =
            data.color;

        ctx.shadowBlur =
            10;


        roundedRect(
            ctx,
            item.x -
            item.width / 2,
            item.y -
            item.height / 2,
            item.width,
            item.height,
            7
        );


        ctx.fill();


        ctx.shadowBlur = 0;


        ctx.fillStyle =
            "#020617";

        ctx.font =
            "16px Arial";

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";


        ctx.fillText(
            data.icon,
            item.x,
            item.y + 1
        );


        ctx.restore();
    }
}


/* =========================================================
   전체 그리기
========================================================= */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    drawBricks();
    drawItems();
    drawBalls();
    drawPaddle();
}


/* =========================================================
   게임 오버
========================================================= */

function endGame() {

    if (gameOver) {
        return;
    }


    gameRunning = false;
    paused = false;
    gameOver = true;


    stopLoop();


    keys.left = false;
    keys.right = false;


    pauseBtn.textContent =
        "⏸ 일시정지";


    messageElement.textContent =
        "💥 GAME OVER! " +
        score.toLocaleString() +
        "점";


    saveRanking();

    showRanking();

    draw();
}


/* =========================================================
   랭킹 저장
========================================================= */

function saveRanking() {

    let name =
        playerNameInput.value
            .trim();


    if (!name) {
        name = "Player";
    }


    name =
        name.substring(
            0,
            12
        );


    const ranking =
        readRankingStorage();


    ranking.push({

        name: name,

        score: score,

        level: level,

        timestamp:
            Date.now()
    });


    ranking.sort(
        function(a, b) {

            if (
                Number(b.score) !==
                Number(a.score)
            ) {

                return (
                    Number(b.score) -
                    Number(a.score)
                );
            }


            if (
                Number(b.level) !==
                Number(a.level)
            ) {

                return (
                    Number(b.level) -
                    Number(a.level)
                );
            }


            return (
                Number(a.timestamp || 0) -
                Number(b.timestamp || 0)
            );
        }
    );


    const top10 =
        ranking.slice(
            0,
            10
        );


    writeRankingStorage(
        top10
    );
}


/* =========================================================
   HTML 이스케이프
========================================================= */

function escapeHtml(text) {

    return String(text)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


/* =========================================================
   랭킹 표시
========================================================= */

function showRanking() {

    const ranking =
        readRankingStorage();


    rankingList.innerHTML = "";


    if (
        ranking.length === 0
    ) {

        rankingList.innerHTML =
            "<div style='text-align:center;color:#94a3b8;padding:10px;'>아직 기록이 없습니다.</div>";

    } else {

        ranking.forEach(
            function(item, index) {

                const row =
                    document.createElement(
                        "div"
                    );


                row.className =
                    "ranking-row";


                row.innerHTML =
                    "<div class='rank-number'>" +
                    (index + 1) +
                    "</div>" +

                    "<div class='rank-name'>" +
                    escapeHtml(
                        item.name
                    ) +
                    "</div>" +

                    "<div class='rank-score'>" +
                    Number(
                        item.score
                    ).toLocaleString() +
                    "점</div>" +

                    "<div class='rank-level'>" +
                    "Lv." +
                    Number(
                        item.level
                    ) +
                    "</div>";


                rankingList.appendChild(
                    row
                );
            }
        );
    }


    rankingPanel.style.display =
        "block";
}


function toggleRanking() {

    if (
        rankingPanel.style.display ===
        "block"
    ) {

        rankingPanel.style.display =
            "none";

    } else {

        showRanking();
    }
}


/* =========================================================
   키보드
========================================================= */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "ArrowLeft"
        ) {

            keys.left = true;

            event.preventDefault();

            return;
        }


        if (
            event.key === "ArrowRight"
        ) {

            keys.right = true;

            event.preventDefault();

            return;
        }


        if (
            event.code === "Space"
        ) {

            /*
             * 입력창에서 Space를 눌렀을 때
             * 게임 일시정지가 실행되지 않게 함
             */

            if (
                document.activeElement ===
                playerNameInput
            ) {
                return;
            }


            togglePause();

            event.preventDefault();

            return;
        }


        if (
            event.key === "Enter"
        ) {

            if (
                document.activeElement ===
                playerNameInput
            ) {

                if (!gameRunning) {
                    startGame();
                }

                return;
            }


            if (!gameRunning) {
                startGame();
            }
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


        if (
            event.key === "ArrowRight"
        ) {

            keys.right = false;
        }
    }
);


/*
 * iframe/브라우저 포커스를 잃었을 때
 * 방향키가 계속 눌린 상태가 되는 문제 방지
 */

window.addEventListener(
    "blur",
    function() {

        keys.left = false;
        keys.right = false;
    }
);


/* =========================================================
   마우스 / 터치
========================================================= */

function movePaddleToClientX(
    clientX
) {

    const rect =
        canvas.getBoundingClientRect();


    const scaleX =
        canvas.width /
        rect.width;


    const x =
        (
            clientX -
            rect.left
        ) *
        scaleX;


    paddle.x =
        x -
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

        movePaddleToClientX(
            event.clientX
        );
    }
);


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


/* =========================================================
   버튼
========================================================= */

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


rankingBtn.addEventListener(
    "click",
    toggleRanking
);


/* =========================================================
   게임 루프
========================================================= */

function gameLoop(timestamp) {

    if (
        !gameRunning ||
        paused
    ) {

        animationId = null;

        return;
    }


    let dt =
        (
            timestamp -
            lastTime
        ) / 1000;


    /*
     * 브라우저가 멈췄다가 돌아왔을 때
     * 공이 순간이동하는 것을 방지
     */

    dt =
        clamp(
            dt,
            0,
            0.033
        );


    lastTime =
        timestamp;


    updatePaddle(dt);

    updateEffects(
        dt * 1000
    );

    updateBalls(dt);

    updateItems(dt);


    /*
     * 목숨을 모두 잃었거나
     * 게임이 종료된 경우
     * 이후 레벨 체크를 하지 않음
     */

    if (
        gameRunning &&
        !gameOver &&
        !levelTransitioning &&
        getRemainingBricks() === 0
    ) {

        nextLevel();
    }


    updateUI();

    draw();


    if (
        gameRunning &&
        !paused &&
        !gameOver
    ) {

        animationId =
            requestAnimationFrame(
                gameLoop
            );
    }
}


/* =========================================================
   초기 실행
========================================================= */

resetGame();

showRanking();

</script>

</body>
</html>
"""


components.html(
    GAME_HTML,
    height=800,
    scrolling=False
)
