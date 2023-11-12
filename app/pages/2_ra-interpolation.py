import streamlit as st
import ra_interp.interpolation as pol

st.set_page_config(
        page_title="ra-box",
        page_icon="app/static/ed-icon.png",
        layout="wide",
    )

st.header("Multidimensional interpolation")
st.write("### Using my library ra-interpolation")

tab1d,tab2d = st.tabs(["1d","2d"])
with tab1d:
    st.write("Interpolating a line of values at even interval")
    input_data = "1,3,7,11,13,14,16"
    inpit_data = st.text_input("Enter input points", input_data)
    degree=3
    degree = st.number_input("Enter degree",value=degree)
    extra = 2
    extra = st.number_input("Enter extra points between data",extra)
    st.write(f"Calling ra-interp, {pol.hello()}")


