import random
import streamlit as st

# --- CONFIGURATION ---
GRID_SIZE = 10
NUM_MINES = 15

# --- PAGE SETUP ---
st.set_page_config(page_title="Minesweeper by CRYSTAL", page_icon="💣", layout="centered")

# --- HTML/CSS CUSTOMIZATION FOR MOBILE & DESKTOP ---
st.markdown(
    """
    <style>
    /* Make sure the main container expands properly */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* FORCE THE COLUMNS TO STAY IN A ROW ON MOBILE (NO STACKING) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }
    
    /* Adjust Column widths evenly */
    [data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;
        flex: 1 1 0% !important;
    }

    /* Force buttons to be responsive squares */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        height: auto !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 5vw !important; /* Scaled text size relative to screen width */
    }
    
    /* Cap the font size on larger desktop screens so it doesn't get massive */
    @media (min-width: 600px) {
        div.stButton > button {
            font-size: 16px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- GAME LOGIC FUNCTIONS ---
def initialize_game():
    """Sets up a fresh game state inside Streamlit's Session State."""
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.revealed = [
        [False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
    ]
    st.session_state.flags = [
        [False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
    ]

    # Place mines randomly
    mines = set()
    while len(mines) < NUM_MINES:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        mines.add((r, c))
    st.session_state.mines = mines

    # Calculate adjacent numbers
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) in mines:
                board[r][c] = "M"
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < GRID_SIZE and 0 <= c + dc < GRID_SIZE:
                        if (r + dr, c + dc) in mines:
                            count += 1
            board[r][c] = count
    st.session_state.board = board


def handle_cell_click(r, c, mode):
    """Unified handler for clicking cells."""
    if st.session_state.game_over or st.session_state.revealed[r][c]:
        return

    if mode == "Flag Mode 🚩":
        st.session_state.flags[r][c] = not st.session_state.flags[r][c]
    else:
        # Reveal Mode
        if st.session_state.flags[r][c]:
            return

        if (r, c) in st.session_state.mines:
            st.session_state.game_over = True
            for mr, mc in st.session_state.mines:
                st.session_state.revealed[mr][mc] = True
            return

        reveal_loop(r, c)
        check_win_condition()


def reveal_loop(start_r, start_c):
    """Using an iterative queue/stack loop to uncover empty tiles safely."""
    queue = [(start_r, start_c)]
    
    while queue:
        r, c = queue.pop(0)
        if st.session_state.revealed[r][c] or st.session_state.flags[r][c]:
            continue
            
        st.session_state.revealed[r][c] = True
        
        if st.session_state.board[r][c] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if not st.session_state.revealed[nr][nc]:
                            queue.append((nr, nc))


def check_win_condition():
    """Checks if only mines are left unrevealed."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) not in st.session_state.mines and not st.session_state.revealed[r][c]:
                return
    st.session_state.won = True
    st.session_state.game_over = True


# --- INITIALIZE STATE ---
if "board" not in st.session_state:
    initialize_game()


# --- APP INTERFACE UI ---
st.title("💣 Minesweeper by CRYSTAL")

# --- COLLAPSIBLE INSTRUCTIONS ---
with st.expander("📖 Click to see How to Play", expanded=False):
    st.write(
        """
        * **Objective:** Uncover all safe tiles without stepping on any hidden mines!
        * **Numbers:** A number reveals how many mines are touching that exact cell.
        * **Controls:** 1. Choose your tool using the action bar below (**Reveal** or **Flag**).
          2. In **Reveal Mode ⛏️**, click a grid square to clear it.
          3. In **Flag Mode 🚩**, click a square to plant a safety flag.
        """
    )

# --- ON-SCREEN CONTROLS ---
ctrl_col1, ctrl_col2 = st.columns([2, 1])

with ctrl_col1:
    play_mode = st.radio(
        "Select Action Mode:", 
        ["Reveal Mode ⛏️", "Flag Mode 🚩"], 
        horizontal=True,
        label_visibility="collapsed"
    )

with ctrl_col2:
    if st.button("🔄 Restart", use_container_width=True):
        initialize_game()
        st.rerun()

# Win/Loss Status Banners
if st.session_state.won:
    st.success("🎉 You cleared the minefield! Perfect game!")
elif st.session_state.game_over:
    st.error("💥 BOOM! You stepped on a mine. Game Over.")

st.markdown("---")

# --- DISPLAY BOARD GRID ---
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        with cols[c]:
            is_revealed = st.session_state.revealed[r][c]
            is_flagged = st.session_state.flags[r][c]
            cell_value = st.session_state.board[r][c]

            label = " "
            button_type = "secondary"

            if is_revealed:
                if cell_value == "M":
                    label = "💣"
                    button_type = "primary"
                elif cell_value > 0:
                    label = str(cell_value)
                else:
                    label = "•"
            elif is_flagged:
                label = "🚩"

            st.button(
                label,
                key=f"cell_{r}_{c}",
                type=button_type,
                on_click=handle_cell_click,
                args=(r, c, play_mode),
            )
