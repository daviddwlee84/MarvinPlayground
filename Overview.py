import streamlit as st
from code_editor import code_editor
from utils import capture_output_streamlit
import redirect

code = """
print("Hello")
"""

keyboard_binding = st.selectbox("Keyboard Binding", ["vim", "vscode"])

buttons = [
    {
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll"],
        "style": {"top": "0.46rem", "right": "0.4rem"},
    },
    {
        "name": "Shortcuts",
        "feather": "Type",
        "class": "shortcuts-button",
        "hasText": True,
        "commands": ["toggleKeyboardShortcuts"],
        "style": {"bottom": "calc(50% + 1.75rem)", "right": "0.4rem"},
    },
    # {
    #     "name": "Collapse",
    #     "feather": "Minimize2",
    #     "hasText": True,
    #     "commands": [
    #         "selectall",
    #         "toggleSplitSelectionIntoLines",
    #         "gotolinestart",
    #         "gotolinestart",
    #         "backspace",
    #     ],
    #     "style": {"bottom": "calc(50% - 1.25rem)", "right": "0.4rem"},
    # },
    # {
    #     "name": "Save",
    #     "feather": "Save",
    #     "hasText": True,
    #     "commands": ["save-state", ["response", "saved"]],
    #     "response": "saved",
    #     "style": {"bottom": "calc(50% - 4.25rem)", "right": "0.4rem"},
    # },
    {
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    },
    {
        "name": "Command",
        "feather": "Terminal",
        "primary": True,
        "hasText": True,
        "commands": ["openCommandPallete"],
        "style": {"bottom": "3.5rem", "right": "0.4rem"},
    },
]

return_value = code_editor(
    code, shortcuts=keyboard_binding, height=[15, 30], buttons=buttons
)

st.write(return_value)

if return_value.get("type") == "submit":
    # https://realpython.com/python-exec/
    capture_output_streamlit(exec)(return_value.get("text"))

    # This is not work as expected
    with redirect.stdout, redirect.stderr(format="markdown", to=st.sidebar):
        exec(return_value.get("text"))
