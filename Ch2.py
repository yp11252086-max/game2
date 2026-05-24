import streamlit as st
import streamlit.components.v1 as components

# 設定頁面標題與佈局
st.set_page_config(page_title="Chess Game by CRYSTAL", layout="centered")

# 注入自訂 CSS，調整 Streamlit 背景與外觀為粉色系
st.markdown("""
    <style>
        /* 調整主要背景 app 容器 */
        .stApp {
            background-color: #FFDEE9;
            background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* 標題樣式 */
        .main-headline {
            color: #4A4A4A;
            font-family: 'Courier New', Courier, monospace;
            font-size: 2.8rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* 淺黃色說明欄 */
        .instructions-box {
            background-color: #FFFDE7;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #FFF59D;
            margin-bottom: 25px;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        }
        
        .instructions-title {
            color: #D4AF37;
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 8px;
        }
        
        /* 置中對齊包裹器 */
        .game-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 1. 標題
st.markdown('<h1 class="main-headline">Chess Game by CRYSTAL</h1>', unsafe_allow_html=True)

# 2. 遊戲說明 (精確位於標題下方)
st.markdown("""
    <div class="instructions-box">
        <div class="instructions-title">How to Play / 遊戲玩法</div>
        <p style="color: #555; margin: 0; font-size: 0.95rem; line-height: 1.5;">
            歡迎來到 Crystal 的 CHESS Page！<br>
            • 點擊棋子可以選取它（會變紅色背景），接著點擊目標格子即可移動。<br>
            • 遊戲遵循標準國際象棋規則，由<b>白方先動</b>。<br>
            • 如果想重新開始，點擊棋盤下方的 <b>Reset Game</b> 按鈕即可。
        </p>
    </div>
""", unsafe_allow_html=True)


# 3. 修正後的 HTML / CSS / JavaScript 程式碼 (完美防遮擋、標準 8x8 棋盤)
html_chess_game = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: transparent;
            margin: 0;
            padding: 0;
            overflow: hidden; /* 防止內部出現不需要的滾動條 */
        }
        
        .game-container {
            background-color: #E0F7FA; /* 淺藍色外框 */
            padding: 15px;
            border-radius: 16px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            border: 3px solid #B2EBF2;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 90%;
            max-width: 440px; /* 限制最大寬度，防止在大螢幕上過度拉伸 */
            box-sizing: border-box;
        }
        
        .status-panel {
            font-size: 1.1rem;
            font-weight: bold;
            color: #006064;
            margin-bottom: 12px;
            background: #ffffff;
            padding: 6px 16px;
            border-radius: 20px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .chessboard {
            display: grid;
            grid-template-columns: repeat(8, 1fr); /* 平分 8 個等寬欄位 */
            grid-template-rows: repeat(8, 1fr);    /* 平分 8 個等高列 */
            width: 100%;
            aspect-ratio: 1 / 1; /* 彈性維持 1:1 正方形 */
            border: 4px solid #006064;
            border-radius: 4px;
            overflow: hidden;
            box-sizing: border-box;
        }
        
        .square {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: min(7vw, 34px); /* 根據螢幕寬度自動縮放棋子大小，最大 34px */
            cursor: pointer;
            user-select: none;
            transition: background-color 0.2s;
            box-sizing: border-box;
        }
        
        /* 淺色格：淺黃色 */
        .light {
            background-color: #FFFDE7;
        }
        
        /* 深色格：淺藍色 */
        .dark {
            background-color: #B2EBF2;
        }
        
        /* 選取時的棋格特效 */
        .selected {
            background-color: #FF8A80 !important;
        }
        
        .btn-reset {
            margin-top: 15px;
            background-color: #FFB74D;
            color: white;
            border: none;
            padding: 8px 24px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.1s, background-color 0.2s;
        }
        
        .btn-reset:hover {
            background-color: #FFA726;
        }
        
        .btn-reset:active {
            transform: scale(0.96);
        }
    </style>
</head>
<body>

<div class="game-container">
    <div class="status-panel" id="status">White's Turn</div>
    <div class="chessboard" id="board"></div>
    <button class="btn-reset" onclick="resetGame()">Reset Game</button>
</div>

<script>
    // 修正後的完整標準 8x8 棋盤陣列 (最外側補上了 ♜ ♖ 車)
    const initialBoard = [
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ];

    let boardState = JSON.parse(JSON.stringify(initialBoard));
    let turn = 'white'; 
    let selectedSquare = null;

    const whitePieces = ['♙', '♖', '♘', '♗', '♕', '♔'];
    const blackPieces = ['♟', '♜', '♞', '♝', '♛', '♚'];

    function renderBoard() {
        const boardEl = document.getElementById('board');
        boardEl.innerHTML = '';
        
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const square = document.createElement('div');
                const isLight = (r + c) % 2 === 0;
                square.className = `square ${isLight ? 'light' : 'dark'}`;
                square.innerHTML = boardState[r][c];
                
                // 渲染棋子顏色
                if (whitePieces.includes(boardState[r][c])) {
                    square.style.color = "#37474F"; // 質感深灰色(代表白棋)
                } else if (blackPieces.includes(boardState[r][c])) {
                    square.style.color = "#000000"; // 純黑色(代表黑棋)
                }

                if (selectedSquare && selectedSquare.row === r && selectedSquare.col === c) {
                    square.classList.add('selected');
                }

                square.addEventListener('click', () => handleSquareClick(r, c));
                boardEl.appendChild(square);
            }
        }
        document.getElementById('status').innerText = `${turn.charAt(0).toUpperCase() + turn.slice(1)}'s Turn`;
    }

    function handleSquareClick(r, c) {
        const piece = boardState[r][c];
        
        if (selectedSquare) {
            if (selectedSquare.row === r && selectedSquare.col === c) {
                selectedSquare = null;
                renderBoard();
                return;
            }
            
            // 執行移動
            boardState[r][c] = boardState[selectedSquare.row][selectedSquare.col];
            boardState[selectedSquare.row][selectedSquare.col] = '';
            selectedSquare = null;
            turn = (turn === 'white') ? 'black' : 'white';
            renderBoard();
        } else {
            if (piece !== '') {
                if ((turn === 'white' && whitePieces.includes(piece)) || 
                    (turn === 'black' && blackPieces.includes(piece))) {
                    selectedSquare = { row: r, col: c };
                    renderBoard();
                }
            }
        }
    }

    function resetGame() {
        boardState = JSON.parse(JSON.stringify(initialBoard));
        turn = 'white';
        selectedSquare = null;
        renderBoard();
    }

    renderBoard();
</script>

</body>
</html>
"""

# 渲染內嵌的 HTML 遊戲，將高度微調為 540，保證下方 Reset 按鈕不會被切掉
st.markdown('<div class="game-wrapper">', unsafe_allow_html=True)
components.html(html_chess_game, height=540, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)
