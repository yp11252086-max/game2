import streamlit as st

# 1. Base Configurations
st.set_page_config(page_title="Crystal Alchemist Matrix", page_icon="🔮", layout="wide")

# Inject Custom Cyberpunk UI CSS
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

GRID_SIZE = 6

# 2. Session State Initialization
if "matrix" not in st.session_state:
    st.session_state.matrix = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # Place target nodes/collectors to harvest energy
    st.session_state.matrix[1][4] = "🎯"
    st.session_state.matrix[4][5] = "🎯"
    
if "laser_y" not in st.session_state:
    st.session_state.laser_y = 2
if "score" not in st.session_state:
    st.session_state.score = 0

# 3. Callback Functions (Fixes the input lag bug by running BEFORE page render)
def handle_install():
    # Fetch values directly from the widget keys to prevent stale state bugs
    t_row = st.session_state.sel_row
    t_col = st.session_state.sel_col
    c_choice = st.session_state.sel_crystal
    
    icon_map = {
        "🔺 Prism (Upward Mirror)": "🔺",
        "🔻 Prism (Downward Mirror)": "🔻",
        "🔷 Focus Lens (Rightward Mirror)": "🔷",
        "🧹 Dissolve Node": "."
    }
    
    # Block overwriting target nodes accidentally
    if st.session_state.matrix[t_row][t_col] != "🎯":
        st.session_state.matrix[t_row][t_col] = icon_map[c_choice]

# 4. Game Simulation Core Engine (Pathfinding Algorithm)
def calculate_beam_path():
    path = []
    curr_x, curr_y = 0, st.session_state.laser_y
    dir_x, dir_y = 1, 0  # Default: Heading Right
    
    steps = 0
    targets_hit = 0
    
    while 0 <= curr_x < GRID_SIZE and 0 <= curr_y < GRID_SIZE and steps < 30:
        path.append((curr_x, curr_y))
        cell = st.session_state.matrix[curr_y][curr_x]
        
        if cell == "🎯":
            targets_hit += 1
            
        # Reflector Node Processing
        elif cell == "🔺":    # Deflect UP
            dir_x, dir_y = 0, -1
        elif cell == "🔻":    # Deflect DOWN
            dir_x, dir_y = 0, 1
        elif cell == "🔷":    # Deflect RIGHT
            dir_x, dir_y = 1, 0
            
        curr_x += dir_x
        curr_y += dir_y
        steps += 1
        
    return path, targets_hit

# Run calculations immediately after any state updates
beam_coords, current_hits = calculate_beam_path()
st.session_state.score = current_hits * 500

# 5. Building the UI Architecture
st.markdown("<h1 class='main-header'>🔮 CRYSTAL MATRIX ALCHEMIST</h1>", unsafe_allow_html=True)

col_controls, col_board = st.columns([1, 2])

with col_controls:
    st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
    st.write("### 🎛️ Emitter Core Controls")
    
    # Moving the slider instantly recalculates the path
    st.slider("Laser Injector Row Y-Axis", 0, GRID_SIZE-1, key="laser_y")
    
    st.write("---")
    st.write("### 🎒 Component Inventory")
    st.radio(
        "Select Crystal Node Type to Deploy:", 
        ["🔺 Prism (Upward Mirror)", "🔻 Prism (Downward Mirror)", "🔷 Focus Lens (Rightward Mirror)", "🧹 Dissolve Node"],
        key="sel_crystal"
    )
    
    st.write("### 📍 Targeting Coordinates")
    st.selectbox("Select Target Row (Y)", range(GRID_SIZE), key="sel_row")
    st.selectbox("Select Target Column (X)", range(GRID_SIZE), key="sel_col")
    
    # Pressing this fires the fixed callback immediately
    st.button("🔧 Install Crystal Node", on_click=handle_install, use_container_width=True)
            
    st.write("---")
    st.markdown(f"**Matrix Energy Yield:** <span class='hud-metric'>{st.session_state.score} GW</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_board:
    st.write("### 🔬 Real-time Refraction Grid")
    
    # Generate interactive visual HTML matrix
    html_grid = "<div style='display: grid; grid-template-columns: repeat(6, 70px); gap: 8px; background: #090d16; padding: 20px; border-radius:10px; width: fit-content; border: 2px dashed #00ffcc;'>"
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_item = st.session_state.matrix[y][x]
            
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
    st.markdown(html_grid, unsafe_allow_html=True)

# 6. Win Conditions / Info Alerts
st.markdown("---")
if st.session_state.score >= 1000:
    st.balloons()
    st.success("🌟 **Matrix Overload Success!** You perfectly linked and routed beams into all Target Collectors simultaneously!")
else:
    st.info("💡 **Mission:** Reposition the Laser Injector slider and plant Crystal mirrors on specific coordinate paths to target both 🎯 nodes simultaneously.")
