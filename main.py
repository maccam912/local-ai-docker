from typing import List
import openai
import streamlit as st

def reset():
    st.session_state["content"] = ["Once upon a time..."]
    st.session_state["turn"] = 0
    st.session_state["messages"] = [{"role": "system", "content": "You are a children's story writing assistant. Given prompts to direct the story, write a three part adventure story fun for a 3-year-old full if whimsy and wonder."}]

if "content" not in st.session_state:
    reset()

def set_api_key():
    openai.api_key = st.session_state["api_key"]

def get_suggestions() -> List[str]:
    suggestions = []
    tries = 0
    suggestions_str = ""
    while len(suggestions) != 5 and tries < 3:
        prompt = "Suggest five sentences to continue the story. Write them out one phrase per line, no extra text before or after."
        st.session_state["messages"] += [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"],
        )

        suggestions_str = response.choices[0].message.content
        suggestions = suggestions_str.split("\n")
        tries += 1
    if tries >= 3:
        suggestions = ["The End 1", "The End 2", "The End 3"]
    st.session_state["messages"] += [{"role": "assistant", "content": suggestions_str}]
    return suggestions

def add_text(text: str):
    turn = st.session_state["turn"]
    if turn == 0:
        st.session_state["messages"] += [{"role": "user", "content": f"Please write the first third of the story, incorporating the following suggestion: {text}"}]
    elif turn == 1:
        st.session_state["messages"] += [{"role": "user", "content": f"Please continue the story, incorporating the following suggestion: {text}"}]
    elif turn == 2:
        st.session_state["messages"] += [{"role": "user", "content": f"Please complete the story with a satisfying ending, incorporating the following suggestion: {text}"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"],
    )
    suggestions_str = response.choices[0].message.content
    st.session_state["content"] += [suggestions_str]
    print(st.session_state.content)
    st.session_state["messages"] += [{"role": "assistant", "content": suggestions_str}]
    st.session_state["turn"] += 1

with st.sidebar:
    st.text_input("OpenAI API Key", key="api_key", on_change=set_api_key)

st.title("Adventure Genie")

if st.session_state["api_key"] == "":
    st.write("Please enter your OpenAI API Key to begin.")
else:
    for c in st.session_state.content:
        st.write(c)

    if st.session_state["turn"] < 3:
        ss = get_suggestions()
        cols = st.columns(len(ss))
        for i in range(len(ss)):
            cols[i].button(ss[i], key=ss[i], on_click=lambda: add_text(ss[i]))

    st.write("---")
    st.button("Reset", on_click=reset)