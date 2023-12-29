import streamlit as st
import contextlib
from functools import wraps
from io import StringIO


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
            st.write(f"Failure while executing: {err}")
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
