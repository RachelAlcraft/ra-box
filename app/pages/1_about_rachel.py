import streamlit as st


tabCV, tabAc,TabCom,tabPubs = st.tabs(["Career","Academic","Community","Publications"])
with tabCV:
    st.write("My cv")
with tabPubs:
    st.write("My publications")


