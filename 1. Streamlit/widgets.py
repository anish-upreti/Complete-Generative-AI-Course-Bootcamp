import streamlit as st
import pandas as pd

st.title("Streamlit Text input")

name = st.text_input("Enter your name: ")

if name:
    st.write(f'Hello, {name}')

age = st.slider("Select your age: ")

st.write("Your age is ",age)

options = ["rock", "metal", "pop", "classic", "hiphop"]
choice = st.selectbox("Choose your music genre ", options)

st.write("You chose ",choice)

upload_file = st.file_uploader("Choose a csv file", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.write(df)
