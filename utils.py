import streamlit as st
from streamlit.components.v1.components import CustomComponent
import contextlib
from functools import wraps
from io import StringIO
from code_editor import code_editor
from functools import partial


def get_customized_code_editor() -> CustomComponent:
    """
    https://code-editor-documentation.streamlit.app/Advanced_usage
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

    return partial(
        code_editor, shortcuts=keyboard_binding, height=[15, 30], buttons=buttons
    )


def capture_output_streamlit(func):
    """
    Capture output from running a function and write using Streamlit.
    https://github.com/streamlit/streamlit/issues/268
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Redirect output to string buffers
        stdout, stderr = StringIO(), StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                return func(*args, **kwargs)
        except Exception as err:
            st.error(f"Failure while executing: {err}")
        finally:
            if _stdout := stdout.getvalue():
                st.write("Execution stdout:")
                st.code(_stdout)
            if _stderr := stderr.getvalue():
                st.write("Execution stderr:")
                st.code(_stderr)

    return wrapper


def capture_output(func):
    """
    Capture output from running a function
    https://github.com/streamlit/streamlit/issues/268
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Redirect output to string buffers
        stdout, stderr = StringIO(), StringIO()
        error = None
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                return func(*args, **kwargs)
        except Exception as err:
            error = err
        finally:
            return {
                "stdout": stdout.getvalue(),
                "stderr": stderr.getvalue(),
                "error": error,
            }

    return wrapper


def code_interpreter_stdout(code: str) -> str:
    """
    Run code and return stdout
    """
    return capture_output(exec)(code)


# TODO: code interpreter that can get the latest variable or output


if __name__ == "__main__":
    return_value = code_interpreter_stdout("print('hello')")
    print(return_value)
