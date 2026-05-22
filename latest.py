import random
import streamlit as st

# --- CONFIGURATION ---
GRID_SIZE = 10
NUM_MINES = 15

# --- PAGE SETUP ---
st.set_page_config(page_title="Streamlit Minesweeper", page_icon="💣", layout="centered")

# --- HTML/CSS CUSTOMIZATION ---
# Inject custom CSS to make the grid compact and style the buttons nicely
st.markdown(
    """
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    /* Style for revealed safe empty cells */
    div.stButton > button[disabled] {
        background-color: #f0f2f6 !important;
        color: #333333 !important;
        opacity: 1 !important;
    }
    </style>
    """,
    unsafe_allow_code=True,
)


# --- GAME LOGIC FUNCTIONS ---
def initialize_game():
    """Sets up a fresh game state."""
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.revealed = [
        [False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
    ]
    st.session_state.flags = [
        [False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
    ]

    # Place mines
    mines = set()
    while len(mines) < NUM_MINES:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        mines.add((r, c))
    st.session_state.mines = mines

    # Calculate neighboring numbers
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) in mines:
                board[r][c] = "M"
                continue
            # Count surrounding mines
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < GRID_SIZE and 0 <= c + dc < GRID_SIZE:
                        if (r + dr, c + dc) in mines:
                            count += 1
            board[r][c] = count
    st.session_state.board = board


def reveal_cell(r, c):
    """Handles cell clicks, including cascade revealing for zeroes."""
    if (
        st.session_state.game_over
        or st.session_state.revealed[r][c]
        or st.session_state.flags[r][c]
    ):
        return

    # Hit a mine
    if (r, c) in st.session_state.mines:
        st.session_state.game_over = True
        # Reveal all mines
        for mr, mc in st.session_state.mines:
            st.session_state.revealed[mr][mc] = True
        return

    # Safe cell reveal
    st.session_state.revealed[r][c] = True

    # Cascade reveal if it's a 0
    if st.session_state.board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if not st.session_state.revealed[nr][nc]:
                        reveal_cell(nr, nc)

    check_win_condition()


def toggle_flag(r, c):
    """Flags/unflags a cell."""
    if not st.session_state.revealed[r][c] and not st.session_state
