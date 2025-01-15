
import streamlit as st
import pandas as pd
import numpy as np

# Title of the app
st.title("Namaste Streamlit!")

# To display a simple text
st.write("This is a demonstration for streamlit.")

# To create a Dataframe
df = pd.DataFrame({
    '1st column' : [1,2,3,4,5],
    '2nd column' : ['a','b','c','d', 'e']
})

# To display a Dataframe
st.write("This is a dataframe.")
st.write(df)

# To create and display a line chart
chart_data = pd.DataFrame(
    np.random.randn(20,3), 
    columns = ['a','b','c']
)
st.line_chart(chart_data)