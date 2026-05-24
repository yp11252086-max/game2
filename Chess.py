import streamlit as st
import streamlit.components.v1 as components

# Set page title and layout
st.set_page_config(page_title="Chess Game by CRYSTAL", layout="centered")

# Custom CSS injected directly into Streamlit to style the page container in pastel pink
st.markdown("""
    <style>
        /* Target the main background app container */
        .stApp {
            background-color: #FFDEE9;
            background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Style the headline */
        .main-headline {
            color: #4A4A4A;
            font-family: 'Courier New', Courier, monospace;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Style the instructions card using light yellow */
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
        
        /* Center container for the embedded game */
        .game-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# 1. Headline
st.markdown('<h1 class="main-headline">Chess Game by CRYSTAL</h1>', unsafe_allow_html=True)

# 2. Instructions (placed exactly below the headline)
st.markdown("""
    <div class="instructions-box">
        <div class="instructions-title">How to Play</div>
        <p style="color: #555; margin: 0; font-size: 0.95rem; line-height: 1.5;">
            Welcome to Crystal's Chess Lounge! 🌸 <br>
            • Click on a piece to highlight it, then click on a valid destination square to move.<br>
            • The game follows standard chess rules. White always moves first.<br>
            • Use the <b>Reset Game</b> button below the board to clear the board and start fresh at any time.
        </p>
    </div>
""", unsafe_allow_html=True)


# 3. HTML & JavaScript Code for the Interactive Chess Game
# Uses standard unicode chess symbols and styles the board with light blue and light yellow squares.
html_chess_game = """
<!DOCTYPE html>
<html>
<head>
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
        }
        
        .game-container {
            background-color: #E0F7FA; /* Soft light blue container */
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            border: 3px solid #B2EBF2;
            display: flex;
            flex-direction: column;
            align-items: center;
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
            grid-template-columns: repeat(8, 55px);
            grid-template-rows: repeat(8, 55px);
            border: 4px solid #006064;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .square {
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.2s;
        }
        
        /* Light squares: Light Yellow */
        .light {
            background-color: #FFFDE7;
        }
        
        /* Dark squares: Light Blue */
        .dark {
            background-color: #B2EBF2;
        }
        
        /* Highlight selected piece */
        .selected {
            background-color: #FF8A80 !important;
        }
        
        .btn-reset {
            margin-top: 15px;
            background-color: #FFB74D;
            color: white;
            border: none;
            padding: 8px 20px;
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
    // Initial standard board setup representation using unicode characters
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
    let turn = 'white'; // 'white' or 'black'
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
                square.dataset.row = r;
                square.dataset.col = c;
                square.innerHTML = boardState[r][c];
                
                // Color formatting logic for piece styles
                if (whitePieces.includes(boardState[r][c])) {
                    square.style.color = "#37474F"; // Distinct dark dark-grey for white pieces
                } else if (blackPieces.includes(boardState[r][c])) {
                    square.style.color = "#000000"; // Pure black for black pieces
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
            // If clicking the same square, deselect it
            if (selectedSquare.row === r && selectedSquare.col === c) {
                selectedSquare = null;
                renderBoard();
                return;
            }
            
            // Execute Move
            boardState[r][c] = boardState[selectedSquare.row][selectedSquare.col];
            boardState[selectedSquare.row][selectedSquare.col] = '';
            selectedSquare = null;
            turn = (turn === 'white') ? 'black' : 'white';
            renderBoard();
        } else {
            // Select a piece matching current player's turn
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

    // Launch the game initially
    renderBoard();
</script>

</body>
</html>
"""

# Render the game inside Streamlit using the components feature
st.markdown('<div class="game-wrapper">', unsafe_allow_html=True)
components.html(html_chess_game, height=520, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)
