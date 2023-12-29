import streamlit as st
import utils
from dotenv import load_dotenv

load_dotenv()

code = """
print("Hello")
"""

code_editor = utils.get_customized_code_editor()
return_value = code_editor(code)
st.write(return_value)

if return_value.get("type") == "submit":
    # https://realpython.com/python-exec/
    utils.capture_output_streamlit(exec)(return_value.get("text"))
    output = utils.capture_output(exec)(return_value.get("text"))
    st.write(output)
