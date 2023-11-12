import streamlit as st


st.sidebar.write("Or this 1?")
tabCV, tabAc,TabCom,tabPubs = st.tabs(["Career","Academic","Community","Publications"])
with tabCV:
    st.write("My cv")
    st.sidebar.write("Or this2?")
with tabPubs:
    st.write("My publications")


st.sidebar.write("Or this 3?")