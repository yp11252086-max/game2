import streamlit as st

# 1. Base Configurations
st.set_page_config(page_title="Crystal Alchemist Matrix", page_icon="🔮", layout="wide")

# Inject Custom Cyberpunk / Alchemy UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.6);
        margin-bottom: 20px;
    }
    .control-panel {
        background: #11141a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
    .hud-metric {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        color: #ff007f;
        text-shadow: 0 0 8px rgba(255, 0, 127, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Game Data Architecture
GRID_SIZE = 6

if "matrix" not in st.session_state:
    # Build a blank 6x6 grid matrix array
    st.session_state.matrix = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # Place target nodes/collectors to harvest energy
    st.session_state.matrix[1][4] = "🎯"
    st.session_state.matrix[4][5] = "🎯"
    
if "laser_y" not in st.session_state:
    st.session_state.laser_y = 2 # Starting Row index for the laser beam
if "score" not in st.session_state:
    st.session_state.score = 0

# 3. Game Simulation Core Engine (The Python Magic)
def calculate_beam_path():
    """Traces the physics path of the laser beam interacting with placed crystals"""
    path = []
    curr_x, curr_y = 0, st.session_state.laser_y
    dir_x, dir_y = 1, 0  # Traveling Right originally
    
    steps = 0
    targets_hit = 0
    
    while 0 <= curr_x < GRID_SIZE and 0 <= curr_y < GRID_SIZE and steps < 30:
        path.append((curr_x, curr_y))
        cell = st.session_state.matrix[curr_y][curr_x]
        
        if cell == "🎯":
            targets_hit += 1
            
        # Reflectors processing
        elif cell == "🔺": # Deflects beam UP
            dir_x, dir_y = 0, -1
        elif cell == "🔻": # Deflects beam DOWN
            dir_x, dir_y = 0, 1
        elif cell == "🔷": # Deflects beam RIGHT
            dir_x, dir_y = 1, 0
            
        curr_x += dir_x
        curr_y += dir_y
        steps += 1
        
    return path, targets_hit

# Calculate current real-time beam frame coordinates
beam_coords, current_hits = calculate_beam_path()
st.session_state.score = current_hits * 500

# 4. Building the Layout Architecture
st.markdown("<h1 class='main-header'>🔮 CRYSTAL MATRIX ALCHEMIST</h1>", unsafe_allow_html=True)

col_controls, col_board = st.columns([1, 2])

with col_controls:
    st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
    st.write("### 🎛️ Emitter Core Controls")
    
    # Adjust Emitter positioning directly mutating state
    st.session_state.laser_y = st.slider("Laser Injector Row Y-Axis", 0, GRID_SIZE-1, st.session_state.laser_y)
    
    st.write("---")
    st.write("### 🎒 Component Inventory")
    crystal_type = st.radio("Select Crystal Node Type to Deploy:", ["🔺 Prism (Upward Mirror)", "🔻 Prism (Downward Mirror)", "🔷 Focus Lens (Rightward Mirror)", "🧹 Dissolve Node"])
    
    st.write("### 📍 Targeting Target Location")
    target_row = st.selectbox("Select Target Row (Y)", range(GRID_SIZE))
    target_col = st.selectbox("Select Target Column (X)", range(GRID_SIZE))
    
    if st.button("🔧 Install Crystal Node", use_container_width=True):
        icon_map = {
            "🔺 Prism (Upward Mirror)": "🔺",
            "🔻 Prism (Downward Mirror)": "🔻",
            "🔷 Focus Lens (Rightward Mirror)": "🔷",
            "🧹 Dissolve Node": "."
        }
        # Safeguard preventing wiping target zones accidentally
        if st.session_state.matrix[target_row][target_col] != "🎯":
            st.session_state.matrix[target_row][target_col] = icon_map[crystal_type]
            st.rerun()
            
    st.write("---")
    st.markdown(f"**Matrix Energy Yield:** <span class='hud-metric'>{st.session_state.score} GW</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_board:
    st.write("### 🔬 Real-time Refraction Grid")
    
    # Generating an interactive visual matrix directly outputting native styled HTML
    html_grid = "<div style='display: grid; grid-template-columns: repeat(6, 70px); gap: 8px; background: #090d16; padding: 20px; border-radius:10px; width: fit-content; border: 2px dashed #00ffcc;'>"
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_item = st.session_state.matrix[y][x]
            
            # Determine color background modifications
            is_laser_origin = (x == 0 and y == st.session_state.laser_y)
            is_beam_path = (x, y) in beam_coords
            
            bg_color = "#161f30"
            border_style = "1px solid #2d3d5a"
            
            if is_beam_path:
                bg_color = "rgba(255, 0, 127, 0.25)"
                border_style = "1px solid #ff007f"
            if is_laser_origin:
                bg_color = "#ff007f"
                cell_item = "⚡"
                
            html_grid += f"""
            <div style='
                height: 70px; 
                width: 70px; 
                background-color: {bg_color}; 
                border: {border_style};
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                box-shadow: { '0 0 10px #ff007f' if is_beam_path else 'none' };
            '>
                {cell_item if cell_item != '.' else ''}
            </div>
            """
    html_grid += "</div>"
    
    # Render pure layout directly to screen surface
    st.markdown(html_grid, unsafe_allow_html=True)

# 5. Reward / Puzzle UI updates
st.markdown("---")
if st.session_state.score >= 1000:
    st.balloons()
    st.success("🌟 **Matrix Overload Success!** You perfectly linked and routed beams into all Target Collectors simultaneously!")
else:
    st.info("💡 **Mission:** Reposition the Laser Injector slider and plant Crystal mirrors on specific coordinate paths to target both 🎯 nodes simultaneously.")
