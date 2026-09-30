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

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>벽돌깨기</title>

<style>

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    background: #020617;

    color: white;

    font-family:
        Arial,
        "Noto Sans KR",
        sans-serif;
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


/* ================================
   닉네임
================================ */

#player-area {

    display: flex;

    margin-bottom: 8px;
}

#playerName {

    width: 100%;

    padding: 11px 13px;

    background: #1e293b;

    border: 1px solid #475569;

    border-radius: 9px;

    color: white;

    outline: none;

    font-size: 14px;
}

#playerName:focus {

    border-color: #38bdf8;
}


/* ================================
   정보
================================ */

#info {

    display: grid;

    grid-template-columns:
        repeat(5, 1fr);

    gap: 4px;

    padding: 10px;

    background: #1e293b;

    border-radius:
        12px 12px 0 0;

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


/* ================================
   Canvas
================================ */

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

    border-left:
        2px solid #334155;

    border-right:
        2px solid #334155;

    border-bottom:
        2px solid #334155;

    touch-action: none;

    user-select: none;
}


/* ================================
   버튼
================================ */

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


/* ================================
   메시지
================================ */

#message {

    min-height: 30px;

    margin-top: 9px;

    text-align: center;

    color: #cbd5e1;

    font-size: 14px;
}


/* ================================
   아이템 설명
================================ */

#item-help {

    margin-top: 10px;

    padding: 10px;

    background: #111827;

    border:
        1px solid #334155;

    border-radius: 9px;

    color: #cbd5e1;

    font-size: 12px;

    line-height: 1.7;

    text-align: center;
}


/* ================================
   랭킹
================================ */

#rankingPanel {

    display: none;

    margin-top: 12px;

    padding: 12px;

    background: #111827;

    border:
        1px solid #334155;

    border-radius: 10px;
}

#rankingPanel h3 {

    margin:
        0 0 10px;

    color: #facc15;

    text-align: center;
}

.ranking-row {

    display: grid;

    grid-template-columns:
        42px 1fr 85px 55px;

    gap: 5px;

    padding: 8px 5px;

    border-bottom:
        1px solid #1e293b;

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


/* ================================
   모바일
================================ */

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

        padding:
            9px 10px;

        font-size: 11px;
    }

}

</style>

</head>


<body>

<div id="game-wrapper">


<!-- 닉네임 -->

<div id="player-area">

    <input
        id="playerName"
        maxlength="12"
        autocomplete="off"
        value="Player"
        placeholder="닉네임"
    >

</div>


<!-- 게임 정보 -->

<div id="info">

    <div class="info-item">

        점수

        <span
            id="score"
            class="info-value"
        >
            0
        </span>

    </div>


    <div class="info-item">

        목숨

        <span
            id="lives"
            class="info-value"
        >
            3
        </span>

    </div>


    <div class="info-item">

        레벨

        <span
            id="level"
            class="info-value"
        >
            1
        </span>

    </div>


    <div class="info-item">

        공

        <span
            id="ballCount"
            class="info-value"
        >
            1
        </span>

    </div>


    <div class="info-item">

        효과

        <span
            id="effect"
            class="info-value"
        >
            -
        </span>

    </div>

</div>


<!-- 게임 화면 -->

<canvas
    id="gameCanvas"
    width="760"
    height="500"
></canvas>


<!-- 버튼 -->

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
    닉네임을 입력하고 게임을 시작하세요.
</div>


<!-- 아이템 설명 -->

<div id="item-help">

    🎁 <b>아이템</b><br>

    🔵 패들 확대 |
    🟡 슬로우 |
    ❤️ 목숨 +1 |
    🟣 멀티볼 |
    ⭐ 보너스 +50

    <br>

    벽돌을 깨면
    <b>25% 확률</b>로 아이템이 떨어집니다.

    <br>

    🟡 슬로우는 현재 레벨에서
    공 속도를 <b>15%</b> 감소시킵니다.

    <br>

    레벨업하면 슬로우가 해제되고
    공 속도는 다시 <b>700</b>으로 돌아옵니다.

    <br>

    ← → 이동 |
    Space 일시정지

</div>


<!-- 랭킹 -->

<div id="rankingPanel">

    <h3>
        🏆 TOP 10
    </h3>

    <div id="rankingList"></div>

</div>


</div>


<script>

"use strict";


/* ============================================================
   DOM
============================================================ */

const canvas =
    document.getElementById(
        "gameCanvas"
    );

const ctx =
    canvas.getContext("2d");


const scoreElement =
    document.getElementById(
        "score"
    );

const livesElement =
    document.getElementById(
        "lives"
    );

const levelElement =
    document.getElementById(
        "level"
    );

const ballCountElement =
    document.getElementById(
        "ballCount"
    );

const effectElement =
    document.getElementById(
        "effect"
    );

const playerNameInput =
    document.getElementById(
        "playerName"
    );

const messageElement =
    document.getElementById(
        "message"
    );

const startBtn =
    document.getElementById(
        "startBtn"
    );

const pauseBtn =
    document.getElementById(
        "pauseBtn"
    );

const restartBtn =
    document.getElementById(
        "restartBtn"
    );

const rankingBtn =
    document.getElementById(
        "rankingBtn"
    );

const rankingPanel =
    document.getElementById(
        "rankingPanel"
    );

const rankingList =
    document.getElementById(
        "rankingList"
    );


/* ============================================================
   게임 상수
============================================================ */

const CANVAS_WIDTH =
    canvas.width;

const CANVAS_HEIGHT =
    canvas.height;


/*
 * ============================================================
 *
 * ⭐ 공 기본 속도
 *
 * 이번 버전:
 *
 * 700
 *
 * ============================================================
 */

const BASE_BALL_SPEED =
    700;


/*
 * ============================================================
 *
 * ⭐ 슬로우 배율
 *
 * 700 × 0.85 = 595
 *
 * ============================================================
 */

const SLOW_MULTIPLIER =
    0.85;


const MAX_BALLS =
    5;


const ITEM_DROP_CHANCE =
    0.25;


const RANKING_KEY =
    "brick_breaker_ranking_v6";


/* ============================================================
   게임 상태
============================================================ */

let score = 0;

let lives = 3;

let level = 1;

let gameRunning = false;

let paused = false;

let gameOver = false;

let levelTransitioning = false;

let animationId = null;

let lastTime = 0;

let balls = [];

let items = [];

let bricks = [];


/* ============================================================
   키 상태
============================================================ */

const keys = {

    left: false,

    right: false

};


/* ============================================================
   효과
============================================================ */

const effects = {

    /*
     * 현재 레벨 동안 유지.
     *
     * 다음 레벨에서 false.
     */

    slowActive: false

};


/* ============================================================
   패들
============================================================ */

const paddle = {

    x: 0,

    y:
        CANVAS_HEIGHT - 35,

    width: 120,

    baseWidth: 120,

    height: 14,

    speed: 650,

    wideTimer: 0

};


/* ============================================================
   벽돌
============================================================ */

const BRICK_COLUMNS =
    10;

const BRICK_WIDTH =
    65;

const BRICK_HEIGHT =
    22;

const BRICK_PADDING =
    8;

const BRICK_TOP =
    50;


const BRICK_COLORS = [

    "#ef4444",

    "#f97316",

    "#eab308",

    "#22c55e",

    "#06b6d4",

    "#3b82f6",

    "#8b5cf6"

];


/* ============================================================
   아이템
============================================================ */

const ITEM_TYPES = {

    WIDE: {

        name: "패들 확대",

        icon: "🔵",

        color: "#38bdf8"

    },

    SLOW: {

        name: "슬로우",

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


/* ============================================================
   유틸
============================================================ */

function clamp(
    value,
    min,
    max
) {

    return Math.max(
        min,
        Math.min(
            max,
            value
        )
    );

}


function randomRange(
    min,
    max
) {

    return (

        Math.random() *
        (max - min) +
        min

    );

}


/*
 * ⭐ 모든 레벨에서 700.
 */

function getBallSpeed() {

    return BASE_BALL_SPEED;

}


/* ============================================================
   랭킹
============================================================ */

function readRanking() {

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


        if (
            !Array.isArray(data)
        ) {

            return [];

        }


        return data.filter(
            item =>

                item &&

                typeof item.name ===
                "string" &&

                Number.isFinite(
                    Number(item.score)
                ) &&

                Number.isFinite(
                    Number(item.level)
                )
        );

    } catch (error) {

        console.warn(
            "랭킹 읽기 실패:",
            error
        );

        return [];

    }

}


function saveRankingData(
    data
) {

    try {

        localStorage.setItem(
            RANKING_KEY,
            JSON.stringify(data)
        );

    } catch (error) {

        console.warn(
            "랭킹 저장 실패:",
            error
        );

    }

}


/* ============================================================
   벽돌 생성
============================================================ */

function createBricks() {

    bricks = [];


    /*
     * 레벨 1 → 5줄
     * 레벨 2 → 6줄
     * ...
     * 최대 8줄
     */

    const rows =
        Math.min(
            4 + level,
            8
        );


    const totalWidth =

        BRICK_COLUMNS *
        BRICK_WIDTH +

        (
            BRICK_COLUMNS - 1
        ) *
        BRICK_PADDING;


    const startX =

        (
            CANVAS_WIDTH -
            totalWidth
        ) / 2;


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

                width:
                    BRICK_WIDTH,

                height:
                    BRICK_HEIGHT,

                alive:
                    true,

                color:

                    BRICK_COLORS[
                        row %
                        BRICK_COLORS.length
                    ]

            });

        }

    }

}


/* ============================================================
   공 생성
============================================================ */

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


    /*
     * 공이 너무 수평으로
     * 시작하지 않도록 합니다.
     */

    const angle =

        -Math.PI / 2 +

        randomRange(
            -0.45,
            0.45
        );


    return createBall(

        CANVAS_WIDTH / 2,

        CANVAS_HEIGHT - 75,

        angle,

        speed

    );

}


function resetBalls() {

    balls = [

        createMainBall()

    ];

}


/* ============================================================
   패들 초기화
============================================================ */

function resetPaddle() {

    paddle.width =
        paddle.baseWidth;


    paddle.x =

        (
            CANVAS_WIDTH -
            paddle.width
        ) / 2;


    paddle.wideTimer =
        0;

}


/* ============================================================
   아이템 초기화
============================================================ */

function resetItems() {

    items = [];


    /*
     * ⭐ 레벨이 변경될 때 호출.
     *
     * 슬로우 해제.
     */

    effects.slowActive =
        false;

}


/* ============================================================
   전체 초기화
============================================================ */

function resetGame() {

    stopGameLoop();


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


/* ============================================================
   벽돌 개수
============================================================ */

function getRemainingBricks() {

    let count = 0;


    for (
        const brick of bricks
    ) {

        if (
            brick.alive
        ) {

            count++;

        }

    }


    return count;

}


/* ============================================================
   UI
============================================================ */

function updateUI() {

    scoreElement.textContent =
        score.toLocaleString();


    livesElement.textContent =
        lives;


    levelElement.textContent =
        level;


    ballCountElement.textContent =
        balls.length;


    updateEffectUI();

}


function updateEffectUI() {

    const active = [];


    if (
        paddle.wideTimer > 0
    ) {

        active.push(

            "🔵 " +

            Math.ceil(
                paddle.wideTimer / 1000
            ) +

            "s"

        );

    }


    if (
        effects.slowActive
    ) {

        active.push(
            "🟡 Lv." + level
        );

    }


    effectElement.textContent =

        active.length > 0

            ? active.join(" ")

            : "-";

}


/* ============================================================
   게임 루프
============================================================ */

function stopGameLoop() {

    if (
        animationId !== null
    ) {

        cancelAnimationFrame(
            animationId
        );

        animationId =
            null;

    }

}


function startGameLoop() {

    stopGameLoop();


    lastTime =
        performance.now();


    animationId =
        requestAnimationFrame(
            gameLoop
        );

}


/* ============================================================
   게임 시작
============================================================ */

function startGame() {

    if (
        gameRunning &&
        !paused
    ) {

        return;

    }


    if (
        gameOver
    ) {

        resetGame();

    }


    gameRunning =
        true;


    paused =
        false;


    gameOver =
        false;


    pauseBtn.textContent =
        "⏸ 일시정지";


    messageElement.textContent =
        "🎮 게임 진행 중!";


    startGameLoop();

}


/* ============================================================
   일시정지
============================================================ */

function togglePause() {

    if (
        !gameRunning ||
        gameOver
    ) {

        return;

    }


    paused =
        !paused;


    if (
        paused
    ) {

        stopGameLoop();


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


        startGameLoop();

    }

}


/* ============================================================
   다시 시작
============================================================ */

function restartGame() {

    resetGame();

    startGame();

}


/* ============================================================
   패들 이동
============================================================ */

function updatePaddle(
    dt
) {

    if (
        !gameRunning ||
        paused
    ) {

        return;

    }


    if (
        keys.left
    ) {

        paddle.x -=

            paddle.speed *
            dt;

    }


    if (
        keys.right
    ) {

        paddle.x +=

            paddle.speed *
            dt;

    }


    paddle.x =

        clamp(

            paddle.x,

            0,

            CANVAS_WIDTH -
            paddle.width

        );

}


/* ============================================================
   원/사각형 충돌
============================================================ */

function circleRectCollision(
    circle,
    rect
) {

    const closestX =

        clamp(

            circle.x,

            rect.x,

            rect.x +
            rect.width

        );


    const closestY =

        clamp(

            circle.y,

            rect.y,

            rect.y +
            rect.height

        );


    const dx =
        circle.x -
        closestX;


    const dy =
        circle.y -
        closestY;


    return (

        dx * dx +
        dy * dy

        <=

        circle.radius *
        circle.radius

    );

}


/* ============================================================
   벽돌 파괴
============================================================ */

function destroyBrick(
    brick
) {

    if (
        !brick.alive
    ) {

        return false;

    }


    brick.alive =
        false;


    score +=
        10;


    /*
     * 25% 확률로 아이템.
     */

    if (
        Math.random() <
        ITEM_DROP_CHANCE
    ) {

        createItem(

            brick.x +
            brick.width / 2,

            brick.y +
            brick.height / 2

        );

    }


    return true;

}


/* ============================================================
   아이템 생성
============================================================ */

function createItem(
    x,
    y
) {

    const random =
        Math.random();


    let type;


    if (
        random < 0.35
    ) {

        type =
            "WIDE";

    } else if (
        random < 0.60
    ) {

        type =
            "SLOW";

    } else if (
        random < 0.75
    ) {

        type =
            "LIFE";

    } else if (
        random < 0.90
    ) {

        type =
            "MULTI";

    } else {

        type =
            "SCORE";

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


/* ============================================================
   아이템 적용
============================================================ */

function applyItem(
    type
) {

    switch (
        type
    ) {


        /* 패들 확대 */

        case "WIDE":

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

                    CANVAS_WIDTH -
                    paddle.width

                );


            messageElement.textContent =
                "🔵 패들이 10초 동안 커집니다!";

            break;


        /* 슬로우 */

        case "SLOW":

            /*
             * ⭐ 중요:
             *
             * 타이머 없음.
             *
             * 현재 레벨 동안 유지.
             */

            effects.slowActive =
                true;


            messageElement.textContent =
                "🟡 현재 레벨 동안 공이 15% 느려집니다!";

            break;


        /* 목숨 */

        case "LIFE":

            lives =

                Math.min(
                    lives + 1,
                    9
                );


            messageElement.textContent =
                "❤️ 목숨 +1!";

            break;


        /* 멀티볼 */

        case "MULTI":

            createMultiBalls();


            messageElement.textContent =
                "🟣 멀티볼!";

            break;


        /* 보너스 */

        case "SCORE":

            score +=
                50;


            messageElement.textContent =
                "⭐ 보너스 +50점!";

            break;

    }


    updateUI();

}


/* ============================================================
   멀티볼
============================================================ */

function createMultiBalls() {

    if (
        balls.length >=
        MAX_BALLS
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

            source.dx *
            source.dx +

            source.dy *
            source.dy

        );


    const baseAngle =

        Math.atan2(

            source.dy,

            source.dx

        );


    const angles = [

        baseAngle - 0.40,

        baseAngle + 0.40

    ];


    for (
        const angle of angles
    ) {

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


/* ============================================================
   아이템 업데이트
============================================================ */

function updateItems(
    dt
) {

    for (
        let i = items.length - 1;
        i >= 0;
        i--
    ) {

        const item =
            items[i];


        item.y +=

            item.speed *
            dt;


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


        if (
            hit
        ) {

            applyItem(
                item.type
            );


            items.splice(
                i,
                1
            );


            continue;

        }


        if (
            item.y -
            item.height / 2 >
            CANVAS_HEIGHT
        ) {

            items.splice(
                i,
                1
            );

        }

    }

}


/* ============================================================
   벽 충돌
============================================================ */

function checkWallCollision(
    ball
) {

    if (
        ball.x -
        ball.radius <=
        0
    ) {

        ball.x =
            ball.radius;

        ball.dx =
            Math.abs(
                ball.dx
            );

    }


    if (
        ball.x +
        ball.radius >=
        CANVAS_WIDTH
    ) {

        ball.x =

            CANVAS_WIDTH -
            ball.radius;

        ball.dx =
            -Math.abs(
                ball.dx
            );

    }


    if (
        ball.y -
        ball.radius <=
        0
    ) {

        ball.y =
            ball.radius;

        ball.dy =
            Math.abs(
                ball.dy
            );

    }

}


/* ============================================================
   패들 충돌
============================================================ */

function checkPaddleCollision(
    ball
) {

    /*
     * 내려오는 공만 처리.
     */

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


    ball.y =

        paddle.y -
        ball.radius;


    const paddleCenter =

        paddle.x +
        paddle.width / 2;


    let relative =

        (
            ball.x -
            paddleCenter
        ) /

        (
            paddle.width / 2
        );


    relative =

        clamp(
            relative,
            -1,
            1
        );


    const speed =

        Math.sqrt(

            ball.dx *
            ball.dx +

            ball.dy *
            ball.dy

        );


    const angle =

        relative *
        (
            Math.PI / 3
        );


    ball.dx =

        speed *
        Math.sin(angle);


    ball.dy =

        -Math.abs(

            speed *
            Math.cos(angle)

        );

}


/* ============================================================
   벽돌 충돌
============================================================ */

function checkBrickCollision(
    ball
) {

    for (
        const brick of bricks
    ) {

        if (
            !brick.alive
        ) {

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


        if (
            !destroyBrick(
                brick
            )
        ) {

            continue;

        }


        /*
         * 공의 중심과 벽돌 중심.
         */

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


        /*
         * 충돌 방향을 추정합니다.
         */

        if (
            Math.abs(dx) /
            brick.width >

            Math.abs(dy) /
            brick.height
        ) {

            ball.dx =
                -ball.dx;

        } else {

            ball.dy =
                -ball.dy;

        }


        /*
         * 공이 벽돌 안에
         * 계속 들어가는 것을 방지.
         */

        if (
            ball.dy > 0
        ) {

            ball.y =

                Math.min(

                    ball.y,

                    brick.y -
                    ball.radius

                );

        } else {

            ball.y =

                Math.max(

                    ball.y,

                    brick.y +
                    brick.height +
                    ball.radius

                );

        }


        return true;

    }


    return false;

}


/* ============================================================
   공 업데이트
============================================================ */

function updateSingleBall(
    ball,
    dt
) {

    /*
     * 슬로우가 켜지면
     *
     * 700 × 0.85 = 595
     */

    const speedMultiplier =

        effects.slowActive

            ? SLOW_MULTIPLIER

            : 1;


    const moveX =

        ball.dx *
        dt *
        speedMultiplier;


    const moveY =

        ball.dy *
        dt *
        speedMultiplier;


    /*
     * ⭐ 빠른 공 충돌 보정.
     *
     * 700 속도에서는 한 프레임에
     * 상당히 많이 이동할 수 있기 때문에
     * 3~4픽셀 단위로 나눠서 이동합니다.
     */

    const distance =

        Math.sqrt(

            moveX * moveX +
            moveY * moveY

        );


    const steps =

        Math.max(

            1,

            Math.ceil(
                distance / 3
            )

        );


    const stepX =
        moveX / steps;


    const stepY =
        moveY / steps;


    for (
        let step = 0;
        step < steps;
        step++
    ) {

        ball.x +=
            stepX;

        ball.y +=
            stepY;


        /*
         * 벽
         */

        checkWallCollision(
            ball
        );


        /*
         * 패들
         */

        checkPaddleCollision(
            ball
        );


        /*
         * 벽돌
         */

        checkBrickCollision(
            ball
        );


        /*
         * 아래로 떨어짐
         */

        if (
            ball.y -
            ball.radius >
            CANVAS_HEIGHT
        ) {

            return false;

        }

    }


    return true;

}


/* ============================================================
   공 업데이트
============================================================ */

function updateBalls(
    dt
) {

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


        if (
            !alive
        ) {

            balls.splice(
                i,
                1
            );

        }

    }


    /*
     * ⭐ 공이 모두 떨어졌을 때만
     * 목숨을 감소시킵니다.
     *
     * 멀티볼 중 공 하나가 떨어져도
     * 목숨이 감소하지 않습니다.
     */

    if (
        balls.length === 0
    ) {

        loseLife();

    }

}


/* ============================================================
   목숨 감소
============================================================ */

function loseLife() {

    if (
        !gameRunning ||
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
     * 같은 레벨에서 재시작.
     *
     * ⭐ resetItems()를 호출하지 않습니다.
     *
     * 따라서 슬로우가 켜져 있었다면
     * 같은 레벨에서 계속 유지됩니다.
     */

    resetBalls();

    resetPaddle();


    /*
     * 떨어진 아이템은 제거.
     */

    items = [];


    messageElement.textContent =

        "💥 공을 놓쳤습니다! " +
        "남은 목숨: " +
        lives;


    updateUI();

}


/* ============================================================
   효과 업데이트
============================================================ */

function updateEffects(
    dtMs
) {

    /*
     * 패들 확대 효과
     */

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

                    CANVAS_WIDTH -
                    paddle.width

                );

        }

    }


    /*
     * 슬로우에는 타이머가 없습니다.
     *
     * 현재 레벨 전체 동안 유지됩니다.
     */

    updateEffectUI();

}


/* ============================================================
   다음 레벨
============================================================ */

function nextLevel() {

    if (
        levelTransitioning ||
        gameOver ||
        !gameRunning
    ) {

        return;

    }


    levelTransitioning =
        true;


    level++;


    /*
     * 레벨 클리어 보너스.
     */

    score +=
        100;


    /*
     * 새로운 벽돌.
     */

    createBricks();


    /*
     * ⭐ 새로운 공 생성.
     *
     * 항상 700.
     */

    resetBalls();


    /*
     * 패들 초기화.
     */

    resetPaddle();


    /*
     * ⭐ 슬로우 초기화.
     *
     * 다음 레벨에서는 다시 700.
     */

    resetItems();


    messageElement.textContent =

        "🎉 레벨 " +
        level +
        "! +100점";


    updateUI();


    requestAnimationFrame(
        () => {

            levelTransitioning =
                false;

        }
    );

}


/* ============================================================
   게임 오버
============================================================ */

function endGame() {

    if (
        gameOver
    ) {

        return;

    }


    gameOver =
        true;


    gameRunning =
        false;


    paused =
        false;


    stopGameLoop();


    keys.left = false;

    keys.right = false;


    pauseBtn.textContent =
        "⏸ 일시정지";


    messageElement.textContent =

        "💥 GAME OVER! " +
        score.toLocaleString() +
        "점";


    saveCurrentScore();

    showRanking();

    draw();

}


/* ============================================================
   랭킹 저장
============================================================ */

function saveCurrentScore() {

    let name =
        playerNameInput.value.trim();


    if (
        name.length === 0
    ) {

        name =
            "Player";

    }


    name =
        name.substring(
            0,
            12
        );


    let ranking =
        readRanking();


    ranking.push({

        name: name,

        score: score,

        level: level,

        timestamp: Date.now()

    });


    ranking.sort(
        (a, b) => {

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


    ranking =
        ranking.slice(
            0,
            10
        );


    saveRankingData(
        ranking
    );

}


/* ============================================================
   HTML 보안 처리
============================================================ */

function escapeHtml(
    value
) {

    return String(value)

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


/* ============================================================
   랭킹 표시
============================================================ */

function showRanking() {

    const ranking =
        readRanking();


    rankingList.innerHTML =
        "";


    if (
        ranking.length === 0
    ) {

        rankingList.innerHTML =

            "<div style='" +
            "text-align:center;" +
            "color:#94a3b8;" +
            "padding:10px;" +
            "'>" +

            "아직 기록이 없습니다." +

            "</div>";

    } else {

        ranking.forEach(
            (item, index) => {

                const row =
                    document.createElement(
                        "div"
                    );


                row.className =
                    "ranking-row";


                row.innerHTML =

                    "<div class='rank-number'>" +

                    (
                        index + 1
                    ) +

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


/* ============================================================
   둥근 사각형
============================================================ */

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


/* ============================================================
   벽돌 그리기
============================================================ */

function drawBricks() {

    for (
        const brick of bricks
    ) {

        if (
            !brick.alive
        ) {

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
            "rgba(255,255,255,0.18)";


        ctx.stroke();

    }

}


/* ============================================================
   패들 그리기
============================================================ */

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


/* ============================================================
   공 그리기
============================================================ */

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


/* ============================================================
   아이템 그리기
============================================================ */

function drawItems() {

    for (
        const item of items
    ) {

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


        ctx.shadowBlur =
            0;


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


/* ============================================================
   그리기
============================================================ */

function draw() {

    ctx.clearRect(

        0,

        0,

        CANVAS_WIDTH,

        CANVAS_HEIGHT

    );


    drawBricks();

    drawItems();

    drawBalls();

    drawPaddle();

}


/* ============================================================
   키보드
============================================================ */

document.addEventListener(
    "keydown",
    event => {

        if (
            event.key ===
            "ArrowLeft"
        ) {

            keys.left =
                true;

            event.preventDefault();

            return;

        }


        if (
            event.key ===
            "ArrowRight"
        ) {

            keys.right =
                true;

            event.preventDefault();

            return;

        }


        if (
            event.code ===
            "Space"
        ) {

            if (
                document.activeElement !==
                playerNameInput
            ) {

                togglePause();

                event.preventDefault();

            }

            return;

        }


        if (
            event.key ===
            "Enter"
        ) {

            if (
                !gameRunning
            ) {

                startGame();

            }

        }

    }
);


document.addEventListener(
    "keyup",
    event => {

        if (
            event.key ===
            "ArrowLeft"
        ) {

            keys.left =
                false;

        }


        if (
            event.key ===
            "ArrowRight"
        ) {

            keys.right =
                false;

        }

    }
);


/*
 * 브라우저 창을 벗어나면
 * 이동키를 초기화.
 */

window.addEventListener(
    "blur",
    () => {

        keys.left =
            false;

        keys.right =
            false;

    }
);


/* ============================================================
   마우스
============================================================ */

function movePaddleToClientX(
    clientX
) {

    const rect =
        canvas.getBoundingClientRect();


    if (
        rect.width <= 0
    ) {

        return;

    }


    const scaleX =

        CANVAS_WIDTH /
        rect.width;


    const canvasX =

        (
            clientX -
            rect.left
        ) *
        scaleX;


    paddle.x =

        canvasX -
        paddle.width / 2;


    paddle.x =

        clamp(

            paddle.x,

            0,

            CANVAS_WIDTH -
            paddle.width

        );

}


canvas.addEventListener(
    "mousemove",
    event => {

        movePaddleToClientX(
            event.clientX
        );

    }
);


/* ============================================================
   터치
============================================================ */

canvas.addEventListener(
    "touchstart",
    event => {

        if (
            event.touches.length > 0
        ) {

            movePaddleToClientX(

                event.touches[0]
                    .clientX

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
    event => {

        if (
            event.touches.length > 0
        ) {

            movePaddleToClientX(

                event.touches[0]
                    .clientX

            );

        }


        event.preventDefault();

    },
    {
        passive: false
    }
);


/* ============================================================
   버튼
============================================================ */

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


/* ============================================================
   게임 시작
============================================================ */

resetGame();

showRanking();

</script>

</body>

</html>
"""


components.html(
    GAME_HTML,
    height=800,
    scrolling=False,
)
