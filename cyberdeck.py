import streamlit as st
from math import ceil

# Initial setup
st.set_page_config(page_title="CyberDeck UI", layout="wide", initial_sidebar_state="collapsed")

# Default grid configurations
grid_configs = {
    "2x2": (2, 2),
    "3x2": (3, 2),
    "3x3": (3, 3),
    "4x2": (4, 2),
    "4x4": (4, 4),
    "5x2": (5, 2),
    "5x3": (5, 3),
    "5x5": (5, 5),
}

# Custom CSS for Cyberpunk theme
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: cyan;
    }
    .stButton>button {
        width: 100%;
        height: 100%;
        background-color: black;
        border: 2px solid cyan;
        color: cyan;
        border-radius: 10px;
        font-size: 16px;
        font-family: "Courier New", monospace;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: cyan;
        color: black;
    }
    .stTextInput>div>input {
        background-color: black;
        border: 2px solid cyan;
        color: cyan;
        font-family: "Courier New", monospace;
    }
    .stSelectbox>div>div>div>select {
        background-color: black;
        border: 2px solid cyan;
        color: cyan;
        font-family: "Courier New", monospace;
    }
    .stSidebar {
        background-color: black !important;
    }
    .stSidebar h2 {
        color: cyan !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state initialization
if "grid_config" not in st.session_state:
    st.session_state.grid_config = "3x3"
if "buttons" not in st.session_state:
    cols, rows = grid_configs[st.session_state.grid_config]
    st.session_state.buttons = [
        {"id": i, "label": f"Button {i + 1}", "action": "https://example.com"} for i in range(cols * rows)
    ]

# Sidebar Configuration
with st.sidebar:
    st.header("CyberDeck Config")
    
    # Grid Size Selection
    new_config = st.selectbox("Grid Size", list(grid_configs.keys()), index=list(grid_configs.keys()).index(st.session_state.grid_config))
    if new_config != st.session_state.grid_config:
        st.session_state.grid_config = new_config
        cols, rows = grid_configs[new_config]
        st.session_state.buttons = [
            {"id": i, "label": f"Button {i + 1}", "action": "https://example.com"} for i in range(cols * rows)
        ]
    
    # Button Configuration
    button_options = [f"Button {button['id'] + 1}" for button in st.session_state.buttons]
    selected_button_index = st.selectbox("Select Button", range(len(button_options)), format_func=lambda x: button_options[x])
    selected_button = st.session_state.buttons[selected_button_index]
    
    new_label = st.text_input("Button Label", value=selected_button["label"])
    new_action = st.text_input("Button Action (URL)", value=selected_button["action"])
    
    if st.button("Update Button"):
        st.session_state.buttons[selected_button_index] = {
            "id": selected_button_index,
            "label": new_label,
            "action": new_action,
        }
        st.success(f"Button {selected_button_index + 1} updated!")

# Main UI
st.title("CyberDeck")
cols, rows = grid_configs[st.session_state.grid_config]

# Calculate button dimensions for full-screen grid layout
button_height = f"{ceil(100 / rows)}vh"
button_width = f"{ceil(100 / cols)}vw"

# Render grid
for row in range(rows):
    cols_objects = st.columns(cols, gap="small")
    for col_index, col in enumerate(cols_objects):
        button_index = row * cols + col_index
        if button_index < len(st.session_state.buttons):
            button = st.session_state.buttons[button_index]
            with col:
                if st.button(button["label"], key=f"button-{button['id']}"):
                    st.write(f"Opening: {button['action']}")
                    st.experimental_rerun()
