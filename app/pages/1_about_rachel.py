import streamlit as st

st.set_page_config(
        page_title="ra-box",
        page_icon="app/static/ed-icon.png",
        layout="wide",
    )


tabCV, tabAc,TabCom,tabPubs = st.tabs(["Career","Academic","Community","Publications"])
with tabCV:
    st.write("My cv")
with tabPubs:
    st.write("My publications")


