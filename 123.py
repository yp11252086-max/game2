import streamlit as str

# 1. Page Configuration & Setup
str.set_page_config(page_title="Crystal Refiner Tycoon", page_icon="💎", layout="centered")

# 2. Advanced Sci-Fi UI Layout (HTML Injection)
str.markdown(
    """
    <style>
    .game-header {
        text-align: center;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .hud-container {
        background-color: #0d1117;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0,242,254,0.15);
        margin-bottom: 25px;
    }
    .resource-title {
        color: #8b949e;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .resource-value {
        font-family: 'Courier New', monospace;
        font-size: 2.2rem;
        font-weight: bold;
    }
    .crystal-text { color: #00f2fe; }
    .shard-text { color: #a370f7; }
    
    .status-card {
        background: #161b22;
        border-left: 4px solid #4facfe;
        padding: 10px 15px;
        border-radius: 4px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Game Engine State Tracking
if "raw_crystals" not in str.session_state:
    str.session_state.raw_crystals = 0
if "pure_shards" not in str.session_state:
    str.session_state.pure_shards = 0
if "drill_level" not in str.session_state:
    str.session_state.drill_level = 1
if "refiner_level" not in str.session_state:
    str.session_state.refiner_level = 0

# Dynamic Upgrade Math
drill_cost = 15 + (str.session_state.drill_level * 12)
refiner_cost = 25 + (str.session_state.refiner_level * 30)

# 4. Core Game Mechanics (Python Logic)
def mine_crystals():
    # Mining power scales with your Drill Level
    str.session_state.raw_crystals += str.session_state.drill_level

def upgrade_drill():
    global drill_cost
    if str.session_state.raw_crystals >= drill_cost:
        str.session_state.raw_crystals -= drill_cost
        str.session_state.drill_level += 1

def refine_shards():
    # Converts up to 10 Raw Crystals into Pure Shards per cycle
    # Scaling factor depends on your Refiner Level
    if str.session_state.raw_crystals >= 10:
        yield_multiplier = 1 + (str.session_state.refiner_level * 0.5)
        str.session_state.raw_crystals -= 10
        str.session_state.pure_shards += int(5 * yield_multiplier)
    else:
        str.sidebar.warning("Not enough Raw Crystals to initiate refinement! Need at least 10.")

def upgrade_refiner():
    global refiner_cost
    if str.session_state.pure_shards >= refiner_cost:
        str.session_state.pure_shards -= refiner_cost
        str.session_state.refiner_level += 1

# 5. Rendering the UI Elements
str.markdown("<h1 class='game-header'>💎 CRYSTAL REFINER TYCOON</h1>", unsafe_allow_html=True)
str.write("<p style='text-align:center; color:#8b949e;'>Extract quantum subterranean crystals and process them into high-yield energy shards.</p>", unsafe_allow_html=True)

# Resource Heads-Up Display (Custom HTML Grid)
str.markdown(
    f"""
    <div class="hud-container">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div class="resource-title">Raw Crystals</div>
                <div class="resource-value crystal-text">💎 {str.session_state.raw_crystals}</div>
            </div>
            <div style="border-left: 1px solid #30363d; height: 50px; margin-top: 5px;"></div>
            <div>
                <div class="resource-title">Pure Shards</div>
                <div class="resource-value shard-text">✨ {str.session_state.pure_shards}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. Interactive Game Panels
col1, col2 = str.columns(2)

with col1:
    str.markdown("### ⛏️ Extraction Deck")
    str.button(
        f"Activate Sonic Drill (+{str.session_state.drill_level} Crystal)",
        on_click=mine_crystals,
        use_container_width=True,
        type="primary"
    )
    
    str.write("---")
    str.write(f"⚙️ **Drill Optimization** (MK {str.session_state.drill_level})")
    str.write(f"Cost: `{drill_cost}` Crystals")
    str.button(
        "Upgrade Drill Power",
        on_click=upgrade_drill,
        disabled=(str.session_state.raw_crystals < drill_cost),
        use_container_width=True
    )

with col2:
    str.markdown("### 🧪 Processing Core")
    str.button(
        "Refine Crystals (Convert 10 Crystals ➡️ Shards)",
        on_click=refine_shards,
        disabled=(str.session_state.raw_crystals < 10),
        use_container_width=True
    )
    
    str.write("---")
    str.write(f"🔮 **Quantum Resonance Matrix** (Tier {str.session_state.refiner_level})")
    str.write(f"Cost: `{refiner_cost}` Pure Shards")
    str.button(
        "Upgrade Refiner Efficiency (+50% yield)",
        on_click=upgrade_refiner,
        disabled=(str.session_state.pure_shards < refiner_cost),
        use_container_width=True
    )

# 7. Dynamic Narrative Sandbox (HTML Status Alert)
str.markdown("<br>", unsafe_allow_html=True)
if str.session_state.pure_shards >= 100:
    str.balloons()
    str.markdown(
        """
        <div class="status-card" style="border-left-color: #00ff66;">
            <b style="color:#00ff66;">🛰️ Deep Space Signal:</b> Your massive inventory of Pure Shards has attracted interstellar trade ships! You've successfully conquered the local sector economy.
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    str.markdown(
        f"""
        <div class="status-card">
            <b>System Telemetry:</b> Current mining speed is operational. Drills pulling <b>{str.session_state.drill_level}</b> payload items per sequence.
        </div>
        """, 
        unsafe_allow_html=True
    )
