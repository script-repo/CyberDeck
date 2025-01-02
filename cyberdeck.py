import streamlit as st

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
    st.title("CyberDeck Config")
    
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

# Render grid
for row in range(rows):
    cols_objects = st.columns(cols)
    for col_index, col in enumerate(cols_objects):
        button_index = row * cols + col_index
        if button_index < len(st.session_state.buttons):
            button = st.session_state.buttons[button_index]
            if col.button(button["label"]):
                st.write(f"Opening: {button['action']}")
                st.experimental_rerun()
