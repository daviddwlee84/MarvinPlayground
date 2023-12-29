import streamlit as st
import utils
import os
from glob import glob


curr_dir = os.path.dirname(os.path.abspath(__file__))

with st.sidebar:
    client = utils.generate_api_and_language_model_selection_and_get_model()

# st.write(client)
#
# if client is not None:
#     chat_completion = client.chat.completions.create(
#         model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
#     )
#     st.write(chat_completion)


code_path = st.selectbox(
    "Example code",
    # glob(os.path.join(curr_dir, "../examples/ai_functions/*.py")),
    glob(os.path.join(curr_dir, "../examples/*/*.py")),
    format_func=os.path.basename,
)

with open(code_path, "r") as fp:
    code = fp.read()

code_editor = utils.get_customized_code_editor()
return_value = code_editor(code)

if return_value.get("type") == "submit":
    # https://realpython.com/python-exec/
    # BUG: OSError('could not get source code')
    output = utils.capture_output(exec)(return_value.get("text"), {"client": client})
    st.write(output)


st.divider()

from marvin import ai_fn


@ai_fn(client=client)
def sentiment(text: str) -> float:
    """Given `text`, returns a number between 1 (positive) and -1 (negative) indicating its sentiment score."""


# BUG: NotFoundError: Error code: 404 - {'error': {'message': 'Unrecognized request argument supplied: tools', 'type': 'invalid_request_error', 'param': None, 'code': None}}

print(sentiment("I love working with Marvin!"))  # 0.8
print(sentiment("These examples could use some work..."))  # -0.2
