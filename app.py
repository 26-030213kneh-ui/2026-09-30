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
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: #020617;
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
    margin-bottom: 8px;
}

#playerName {
    width: 100%;
    padding: 11px 13px;
    background: #1e293b;
    color: white;
    border: 1px solid #475569;
    border-radius: 9px;
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
    font-size: 11px;
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
            #020617 78%
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
    padding: 10px 14px;
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
    min-height: 30px;
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
    border-radius: 9px;
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
    grid-template-columns: 42px 1fr 85px 55px;
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
        font-size: 9px;
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
        height="500"
    ></canvas>

    <div id="buttons">

        <button id="startBtn">
            ▶ 게임 시작
        </button>

        <button id="pauseBtn">
            ⏸ 일시정지
        </button>

        <button id="restartBtn">
            🔄 다시 시작
        </button>

        <button id="rankingBtn">
            🏆 랭킹
        </button>

    </div>

    <div id="message">
        ▶ 게임 시작 버튼을 눌러주세요.
    </div>

    <div id="item-help">

        🎁 <b>아이템</b><br>

        🔵 패들 확대 |
        🟡 슬로우 |
        ❤️ 목숨 +1 |
        🟣 멀티볼 |
        ⭐ 보너스 +50

        <br>

        벽돌을 깨면
        <b>25% 확률</b>로 아이템이 드롭됩니다.

        <br>

        🟡 슬로우:
        현재 레벨에서만 공 속도 15% 감소

        <br>

        레벨이 올라가면
        공 속도는 다시 <b>700</b>으로 초기화됩니다.

        <br>

        ← → 이동 / 마우스 / 터치 |
        Space 일시정지

    </div>

    <div id="rankingPanel">

        <h3>🏆 TOP 10</h3>

        <div id="rankingList"></div>

    </div>

</div>


<script>
"use strict";


/* =========================================================
   DOM
========================================================= */

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const livesEl = document.getElementById("lives");
const levelEl = document.getElementById("level");
const ballCountEl = document.getElementById("ballCount");
const effectEl = document.getElementById("effect");

const playerNameEl = document.getElementById("playerName");

const messageEl = document.getElementById("message");

const startBtn = document.getElementById("startBtn");
const pauseBtn = document.getElementById("pauseBtn");
const restartBtn = document.getElementById("restartBtn");
const rankingBtn = document.getElementById("rankingBtn");

const rankingPanel = document.getElementById("rankingPanel");
const rankingList = document.getElementById("rankingList");


/* =========================================================
   상수
========================================================= */

const W = canvas.width;
const H = canvas.height;


/*
    ⭐ 기본 공 속도

    모든 레벨에서 700
*/
const BASE_SPEED = 700;


/*
    슬로우 아이템은 15% 감소

    700 × 0.85 = 595
*/
const SLOW_RATE = 0.85;


/*
    아이템 드롭 확률
*/
const ITEM_CHANCE = 0.25;


/*
    멀티볼 최대 개수
*/
const MAX_BALLS = 5;


/*
    랭킹 저장 키
*/
const RANKING_KEY = "brick_breaker_ranking_v7";


/* =========================================================
   게임 상태
========================================================= */

let score = 0;
let lives = 3;
let level = 1;

let running = false;
let paused = false;
let gameOver = false;

let balls = [];
let bricks = [];
let items = [];

let animationFrame = null;
let lastTime = 0;


/*
    현재 레벨의 슬로우 상태.

    타이머가 없음.
    현재 레벨 동안 유지.
*/
let slowActive = false;


/* =========================================================
   키
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
    y: H - 35,
    width: 120,
    baseWidth: 120,
    height: 14,
    speed: 700,
    wideTimer: 0
};


/* =========================================================
   벽돌
========================================================= */

const COLS = 10;
const BRICK_WIDTH = 65;
const BRICK_HEIGHT = 22;
const BRICK_GAP = 8;
const BRICK_TOP = 50;

const COLORS = [
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

const ITEM_DATA = {

    WIDE: {
        icon: "🔵",
        color: "#38bdf8"
    },

    SLOW: {
        icon: "🟡",
        color: "#facc15"
    },

    LIFE: {
        icon: "❤️",
        color: "#fb7185"
    },

    MULTI: {
        icon: "🟣",
        color: "#c084fc"
    },

    SCORE: {
        icon: "⭐",
        color: "#fbbf24"
    }
};


/* =========================================================
   유틸
========================================================= */

function clamp(value, min, max) {

    return Math.max(
        min,
        Math.min(max, value)
    );

}


function random(min, max) {

    return Math.random() * (max - min) + min;

}


/*
    현재 공 속도.

    레벨과 관계없이 700.
*/
function getCurrentSpeed() {

    return slowActive
        ? BASE_SPEED * SLOW_RATE
        : BASE_SPEED;

}


/* =========================================================
   UI
========================================================= */

function updateUI() {

    scoreEl.textContent =
        score.toLocaleString();

    livesEl.textContent =
        lives;

    levelEl.textContent =
        level;

    ballCountEl.textContent =
        balls.length;

    const effects = [];

    if (paddle.wideTimer > 0) {

        effects.push(
            "🔵 " +
            Math.ceil(paddle.wideTimer / 1000) +
            "s"
        );

    }

    if (slowActive) {

        effects.push("🟡");

    }

    effectEl.textContent =
        effects.length
            ? effects.join(" ")
            : "-";
}


/* =========================================================
   랭킹
========================================================= */

function loadRanking() {

    try {

        const data =
            localStorage.getItem(RANKING_KEY);

        if (!data) {
            return [];
        }

        const parsed =
            JSON.parse(data);

        if (!Array.isArray(parsed)) {
            return [];
        }

        return parsed.filter(item => {

            return (
                item &&
                typeof item.name === "string" &&
                Number.isFinite(Number(item.score)) &&
                Number.isFinite(Number(item.level))
            );

        });

    } catch (error) {

        console.warn(
            "랭킹 불러오기 실패",
            error
        );

        return [];
    }
}


function saveRanking() {

    try {

        let ranking =
            loadRanking();

        let name =
            playerNameEl.value.trim();

        if (!name) {
            name = "Player";
        }

        name =
            name.substring(0, 12);

        ranking.push({

            name: name,

            score: score,

            level: level,

            time: Date.now()

        });


        ranking.sort((a, b) => {

            if (
                Number(b.score) !==
                Number(a.score)
            ) {

                return (
                    Number(b.score) -
                    Number(a.score)
                );

            }

            return (
                Number(b.level) -
                Number(a.level)
            );

        });


        ranking =
            ranking.slice(0, 10);


        localStorage.setItem(
            RANKING_KEY,
            JSON.stringify(ranking)
        );

    } catch (error) {

        console.warn(
            "랭킹 저장 실패",
            error
        );

    }

}


function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


function renderRanking() {

    const ranking =
        loadRanking();

    rankingList.innerHTML = "";


    if (ranking.length === 0) {

        rankingList.innerHTML =
            "<div style='text-align:center;color:#94a3b8;padding:10px'>" +
            "아직 랭킹 기록이 없습니다." +
            "</div>";

        return;
    }


    ranking.forEach((item, index) => {

        const row =
            document.createElement("div");

        row.className =
            "ranking-row";

        row.innerHTML =
            "<div class='rank-number'>" +
            (index + 1) +
            "</div>" +

            "<div class='rank-name'>" +
            escapeHTML(item.name) +
            "</div>" +

            "<div class='rank-score'>" +
            Number(item.score).toLocaleString() +
            "점</div>" +

            "<div class='rank-level'>" +
            "Lv." +
            Number(item.level) +
            "</div>";

        rankingList.appendChild(row);

    });

}


function toggleRanking() {

    if (
        rankingPanel.style.display === "block"
    ) {

        rankingPanel.style.display = "none";

    } else {

        renderRanking();

        rankingPanel.style.display = "block";

    }

}


/* =========================================================
   벽돌 생성
========================================================= */

function createBricks() {

    bricks = [];

    const rows =
        Math.min(4 + level, 8);

    const totalWidth =
        COLS * BRICK_WIDTH +
        (COLS - 1) * BRICK_GAP;

    const startX =
        (W - totalWidth) / 2;


    for (let row = 0; row < rows; row++) {

        for (
            let col = 0;
            col < COLS;
            col++
        ) {

            bricks.push({

                x:
                    startX +
                    col *
                    (BRICK_WIDTH + BRICK_GAP),

                y:
                    BRICK_TOP +
                    row *
                    (BRICK_HEIGHT + BRICK_GAP),

                width:
                    BRICK_WIDTH,

                height:
                    BRICK_HEIGHT,

                alive:
                    true,

                color:
                    COLORS[row % COLORS.length]

            });

        }

    }

}


/* =========================================================
   공
========================================================= */

function makeBall(
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
            Math.cos(angle) * speed,

        dy:
            Math.sin(angle) * speed

    };

}


function createBall() {

    const speed =
        getCurrentSpeed();

    /*
        시작 방향을 위쪽으로 제한.
    */

    const angle =
        -Math.PI / 2 +
        random(-0.45, 0.45);

    return makeBall(
        W / 2,
        H - 75,
        angle,
        speed
    );

}


function resetBalls() {

    balls = [
        createBall()
    ];

}


/* =========================================================
   패들
========================================================= */

function resetPaddle() {

    paddle.width =
        paddle.baseWidth;

    paddle.x =
        (W - paddle.width) / 2;

    paddle.wideTimer = 0;

}


/* =========================================================
   충돌
========================================================= */

function circleRectCollision(ball, rect) {

    const closestX =
        clamp(
            ball.x,
            rect.x,
            rect.x + rect.width
        );

    const closestY =
        clamp(
            ball.y,
            rect.y,
            rect.y + rect.height
        );

    const dx =
        ball.x - closestX;

    const dy =
        ball.y - closestY;

    return (
        dx * dx +
        dy * dy <=
        ball.radius * ball.radius
    );

}


/* =========================================================
   공과 벽
========================================================= */

function wallCollision(ball) {

    if (
        ball.x - ball.radius <= 0
    ) {

        ball.x =
            ball.radius;

        ball.dx =
            Math.abs(ball.dx);

    }


    if (
        ball.x + ball.radius >= W
    ) {

        ball.x =
            W - ball.radius;

        ball.dx =
            -Math.abs(ball.dx);

    }


    if (
        ball.y - ball.radius <= 0
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

function paddleCollision(ball) {

    /*
        공이 내려오는 경우에만 충돌.
    */

    if (ball.dy <= 0) {
        return;
    }


    if (
        !circleRectCollision(ball, paddle)
    ) {

        return;
    }


    /*
        공이 패들 위에 정확히 올라오도록
        위치를 보정.
    */

    ball.y =
        paddle.y - ball.radius;


    const center =
        paddle.x +
        paddle.width / 2;


    let relative =
        (ball.x - center) /
        (paddle.width / 2);


    relative =
        clamp(relative, -1, 1);


    /*
        현재 공의 실제 속도를 유지.
    */

    const speed =
        Math.sqrt(
            ball.dx * ball.dx +
            ball.dy * ball.dy
        );


    /*
        패들 중앙에서 맞으면 거의 수직.
        양 끝으로 갈수록 더 대각선.
    */

    const angle =
        relative * (Math.PI / 3);


    ball.dx =
        speed * Math.sin(angle);

    ball.dy =
        -Math.abs(
            speed * Math.cos(angle)
        );

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

        speed: 120,

        type: type

    });

}


/* =========================================================
   벽돌 충돌
========================================================= */

function brickCollision(ball) {

    for (
        let i = 0;
        i < bricks.length;
        i++
    ) {

        const brick =
            bricks[i];


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
            벽돌 제거
        */

        brick.alive =
            false;


        score += 10;


        /*
            아이템 드롭
        */

        if (
            Math.random() <
            ITEM_CHANCE
        ) {

            createItem(
                brick.x + brick.width / 2,
                brick.y + brick.height / 2
            );

        }


        /*
            충돌 방향 계산
        */

        const centerX =
            brick.x +
            brick.width / 2;

        const centerY =
            brick.y +
            brick.height / 2;

        const dx =
            ball.x - centerX;

        const dy =
            ball.y - centerY;


        if (
            Math.abs(dx) / brick.width >
            Math.abs(dy) / brick.height
        ) {

            ball.dx =
                -ball.dx;

        } else {

            ball.dy =
                -ball.dy;

        }


        return true;

    }

    return false;

}


/* =========================================================
   아이템 적용
========================================================= */

function applyItem(type) {

    if (type === "WIDE") {

        paddle.width =
            Math.min(
                paddle.baseWidth * 1.7,
                220
            );

        paddle.wideTimer =
            10000;

        paddle.x =
            clamp(
                paddle.x,
                0,
                W - paddle.width
            );

        messageEl.textContent =
            "🔵 패들이 10초 동안 커졌습니다!";

    }


    else if (type === "SLOW") {

        /*
            ⭐ 현재 레벨 동안 유지.

            다음 레벨에서 resetLevel()을
            호출하면 자동으로 해제.
        */

        slowActive =
            true;

        messageEl.textContent =
            "🟡 슬로우! 현재 레벨 동안 공이 느려집니다.";

    }


    else if (type === "LIFE") {

        lives =
            Math.min(
                lives + 1,
                9
            );

        messageEl.textContent =
            "❤️ 목숨 +1!";

    }


    else if (type === "MULTI") {

        addMultiBalls();

        messageEl.textContent =
            "🟣 멀티볼!";

    }


    else if (type === "SCORE") {

        score += 50;

        messageEl.textContent =
            "⭐ 보너스 +50점!";

    }


    updateUI();

}


/* =========================================================
   멀티볼
========================================================= */

function addMultiBalls() {

    if (
        balls.length >= MAX_BALLS
    ) {

        return;
    }


    const source =
        balls[0];


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
        baseAngle - 0.45,
        baseAngle + 0.45
    ];


    for (
        const angle of angles
    ) {

        if (
            balls.length >= MAX_BALLS
        ) {

            break;
        }


        balls.push(
            makeBall(
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

        const item =
            items[i];


        item.y +=
            item.speed * dt;


        const hit =

            item.y + item.height / 2 >=
                paddle.y &&

            item.y - item.height / 2 <=
                paddle.y + paddle.height &&

            item.x >=
                paddle.x &&

            item.x <=
                paddle.x + paddle.width;


        if (hit) {

            applyItem(
                item.type
            );

            items.splice(i, 1);

            continue;

        }


        if (
            item.y -
            item.height / 2 >
            H
        ) {

            items.splice(i, 1);

        }

    }

}


/* =========================================================
   패들 업데이트
========================================================= */

function updatePaddle(dt) {

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
            W - paddle.width
        );


    /*
        패들 확대 시간
    */

    if (
        paddle.wideTimer > 0
    ) {

        paddle.wideTimer -=
            dt * 1000;


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
                    W - paddle.width
                );

        }

    }

}


/* =========================================================
   공 하나 업데이트
========================================================= */

function updateBall(ball, dt) {

    /*
        현재 속도.

        일반 = 700
        슬로우 = 595
    */

    const speed =
        getCurrentSpeed();


    /*
        현재 dx/dy의 방향을 유지하면서
        속도를 정확하게 맞춘다.

        이렇게 하면 레벨이나 아이템 때문에
        속도가 이상하게 누적되는 것을 방지한다.
    */

    const currentMagnitude =
        Math.sqrt(
            ball.dx * ball.dx +
            ball.dy * ball.dy
        );


    if (
        currentMagnitude > 0
    ) {

        const ratio =
            speed / currentMagnitude;

        ball.dx *= ratio;
        ball.dy *= ratio;

    }


    const moveX =
        ball.dx * dt;

    const moveY =
        ball.dy * dt;


    /*
        ⭐ 빠른 공 충돌 보정.

        이동 거리를 최대 3px 정도로
        나눠서 처리한다.
    */

    const distance =
        Math.sqrt(
            moveX * moveX +
            moveY * moveY
        );


    const steps =
        Math.max(
            1,
            Math.ceil(distance / 3)
        );


    const stepX =
        moveX / steps;

    const stepY =
        moveY / steps;


    for (
        let i = 0;
        i < steps;
        i++
    ) {

        ball.x += stepX;
        ball.y += stepY;


        wallCollision(ball);

        paddleCollision(ball);

        brickCollision(ball);


        /*
            공이 아래로 떨어졌다면
            이 공은 제거.
        */

        if (
            ball.y - ball.radius > H
        ) {

            return false;

        }

    }


    return true;

}


/* =========================================================
   모든 공 업데이트
========================================================= */

function updateBalls(dt) {

    /*
        뒤에서부터 제거.
    */

    for (
        let i = balls.length - 1;
        i >= 0;
        i--
    ) {

        const alive =
            updateBall(
                balls[i],
                dt
            );


        if (!alive) {

            balls.splice(i, 1);

        }

    }


    /*
        ⭐ 모든 공이 사라졌을 때만
        목숨을 하나 감소.
    */

    if (
        balls.length === 0
    ) {

        loseLife();

    }

}


/* =========================================================
   목숨 잃음
========================================================= */

function loseLife() {

    if (
        !running ||
        gameOver
    ) {

        return;
    }


    lives--;


    if (
        lives <= 0
    ) {

        lives = 0;

        updateUI();

        endGame();

        return;

    }


    /*
        현재 레벨 유지.

        ⭐ slowActive를 건드리지 않는다.

        따라서 같은 레벨에서는
        슬로우가 계속 유지된다.
    */

    resetBalls();

    resetPaddle();

    items = [];


    messageEl.textContent =
        "💥 공을 놓쳤습니다! 남은 목숨: " +
        lives;


    updateUI();

}


/* =========================================================
   레벨 클리어
========================================================= */

function checkLevelClear() {

    if (gameOver) {
        return;
    }


    const remaining =
        bricks.some(
            brick => brick.alive
        );


    if (remaining) {
        return;
    }


    /*
        다음 레벨
    */

    level++;

    score += 100;


    /*
        ⭐ 레벨업하면 슬로우 초기화.

        새 레벨에서는 무조건 700.
    */

    slowActive = false;


    createBricks();

    resetBalls();

    resetPaddle();

    items = [];


    messageEl.textContent =
        "🎉 레벨 " +
        level +
        " 시작! +100점";


    updateUI();

}


/* =========================================================
   게임 루프
========================================================= */

function gameLoop(timestamp) {

    /*
        실행 중이 아니거나
        일시정지 상태라면
        프레임을 예약하지 않는다.
    */

    if (
        !running ||
        paused ||
        gameOver
    ) {

        animationFrame = null;

        return;
    }


    /*
        첫 프레임에서 dt 폭발 방지.
    */

    if (!lastTime) {

        lastTime =
            timestamp;

    }


    let dt =
        (timestamp - lastTime) / 1000;


    lastTime =
        timestamp;


    /*
        브라우저 탭을 오래 떠났을 때
        공이 순간이동하는 것을 방지.
    */

    dt =
        Math.min(
            dt,
            0.025
        );


    updatePaddle(dt);

    updateItems(dt);

    updateBalls(dt);

    checkLevelClear();

    updateUI();

    draw();


    /*
        ⭐ 여기서 단 한 번만
        다음 프레임을 예약.
    */

    animationFrame =
        requestAnimationFrame(
            gameLoop
        );

}


/* =========================================================
   루프 시작
========================================================= */

function startLoop() {

    /*
        이미 루프가 있다면
        중복 실행하지 않는다.
    */

    if (
        animationFrame !== null
    ) {

        return;
    }


    lastTime = 0;


    animationFrame =
        requestAnimationFrame(
            gameLoop
        );

}


/* =========================================================
   루프 정지
========================================================= */

function stopLoop() {

    if (
        animationFrame !== null
    ) {

        cancelAnimationFrame(
            animationFrame
        );

        animationFrame =
            null;

    }

}


/* =========================================================
   게임 시작
========================================================= */

function startGame() {

    /*
        게임 오버 상태에서 시작 버튼을 누르면
        새 게임으로 초기화.
    */

    if (gameOver) {

        newGame();

    }


    running = true;
    paused = false;
    gameOver = false;


    pauseBtn.textContent =
        "⏸ 일시정지";


    messageEl.textContent =
        "🎮 게임 진행 중!";


    startLoop();

}


/* =========================================================
   일시정지
========================================================= */

function togglePause() {

    if (
        !running ||
        gameOver
    ) {

        return;
    }


    if (!paused) {

        paused = true;

        stopLoop();


        keys.left = false;
        keys.right = false;


        pauseBtn.textContent =
            "▶ 계속하기";


        messageEl.textContent =
            "⏸ 일시정지";

    } else {

        paused = false;


        pauseBtn.textContent =
            "⏸ 일시정지";


        messageEl.textContent =
            "🎮 게임 진행 중!";


        startLoop();

    }

}


/* =========================================================
   새 게임
========================================================= */

function newGame() {

    stopLoop();


    score = 0;
    lives = 3;
    level = 1;


    running = false;
    paused = false;
    gameOver = false;


    slowActive = false;


    balls = [];
    bricks = [];
    items = [];


    keys.left = false;
    keys.right = false;


    createBricks();

    resetPaddle();

    resetBalls();


    pauseBtn.textContent =
        "⏸ 일시정지";


    messageEl.textContent =
        "▶ 게임 시작 버튼을 눌러주세요.";


    updateUI();

    draw();

}


/* =========================================================
   다시 시작
========================================================= */

function restartGame() {

    newGame();

    startGame();

}


/* =========================================================
   게임 오버
========================================================= */

function endGame() {

    if (gameOver) {
        return;
    }


    gameOver = true;
    running = false;
    paused = false;


    stopLoop();


    keys.left = false;
    keys.right = false;


    messageEl.textContent =
        "💥 GAME OVER! " +
        score.toLocaleString() +
        "점";


    saveRanking();

    renderRanking();

    rankingPanel.style.display =
        "block";


    updateUI();

    draw();

}


/* =========================================================
   그리기
========================================================= */

function roundedRect(
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


    ctx.beginPath();

    ctx.moveTo(
        x + r,
        y
    );

    ctx.lineTo(
        x + width - r,
        y
    );

    ctx.quadraticCurveTo(
        x + width,
        y,
        x + width,
        y + r
    );

    ctx.lineTo(
        x + width,
        y + height - r
    );

    ctx.quadraticCurveTo(
        x + width,
        y + height,
        x + width - r,
        y + height
    );

    ctx.lineTo(
        x + r,
        y + height
    );

    ctx.quadraticCurveTo(
        x,
        y + height,
        x,
        y + height - r
    );

    ctx.lineTo(
        x,
        y + r
    );

    ctx.quadraticCurveTo(
        x,
        y,
        x + r,
        y
    );

    ctx.closePath();

}


/* =========================================================
   벽돌 그리기
========================================================= */

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
                brick.y + brick.height
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
            brick.x,
            brick.y,
            brick.width,
            brick.height,
            5
        );


        ctx.fill();


        ctx.strokeStyle =
            "rgba(255,255,255,0.18)";


        ctx.stroke();

    }

}


/* =========================================================
   패들 그리기
========================================================= */

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
   공 그리기
========================================================= */

function drawBalls() {

    for (
        const ball of balls
    ) {

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
   아이템 그리기
========================================================= */

function drawItems() {

    for (
        const item of items
    ) {

        const data =
            ITEM_DATA[item.type];


        ctx.save();


        ctx.fillStyle =
            data.color;


        ctx.shadowColor =
            data.color;

        ctx.shadowBlur =
            10;


        roundedRect(
            item.x - item.width / 2,
            item.y - item.height / 2,
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
            item.y
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
        W,
        H
    );


    drawBricks();

    drawItems();

    drawBalls();

    drawPaddle();

}


/* =========================================================
   키보드
========================================================= */

document.addEventListener(
    "keydown",
    function(event) {

        /*
            입력창에서 방향키나 스페이스를 누른 경우
            게임 조작으로 처리하지 않는다.
        */

        if (
            document.activeElement === playerNameEl
        ) {

            if (
                event.code === "Space"
            ) {

                return;

            }

        }


        if (
            event.key === "ArrowLeft"
        ) {

            keys.left = true;

            event.preventDefault();

        }


        if (
            event.key === "ArrowRight"
        ) {

            keys.right = true;

            event.preventDefault();

        }


        if (
            event.code === "Space"
        ) {

            togglePause();

            event.preventDefault();

        }


        if (
            event.key === "Enter"
        ) {

            if (!running) {

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


/* =========================================================
   창 포커스 잃었을 때
========================================================= */

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

function movePaddle(clientX) {

    const rect =
        canvas.getBoundingClientRect();


    if (
        rect.width <= 0
    ) {

        return;
    }


    const scale =
        W / rect.width;


    const x =
        (clientX - rect.left) * scale;


    paddle.x =
        x - paddle.width / 2;


    paddle.x =
        clamp(
            paddle.x,
            0,
            W - paddle.width
        );

}


canvas.addEventListener(
    "mousemove",
    function(event) {

        movePaddle(
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

            movePaddle(
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

            movePaddle(
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
   버튼 이벤트
========================================================= */

/*
    ⭐ addEventListener를 사용하고
    함수 자체를 정확하게 연결한다.
*/

startBtn.addEventListener(
    "click",
    function() {
        startGame();
    }
);


pauseBtn.addEventListener(
    "click",
    function() {
        togglePause();
    }
);


restartBtn.addEventListener(
    "click",
    function() {
        restartGame();
    }
);


rankingBtn.addEventListener(
    "click",
    function() {
        toggleRanking();
    }
);


/* =========================================================
   초기 실행
========================================================= */

newGame();

renderRanking();

</script>

</body>
</html>
"""


components.html(
    GAME_HTML,
    height=800,
    scrolling=False,
)
