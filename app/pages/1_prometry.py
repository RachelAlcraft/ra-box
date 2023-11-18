import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px

DATADIR = "app/static/"

is_calc = False

st.set_page_config(
        page_title="ra-box",
        page_icon="app/static/ed-icon.png",
        layout="wide",
    )


st.header("prometry")
st.write("#### A library to calculate geometric parameters of protein structures and perform criteria search")

data_samples = {}
data_samples["crambin"] = ("1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt",
                            "CA:C:N+1 N:O N:CA:C:N+1 C:O N:CA N:CA:C",
                            "N:CA","resolution","pdb_code",
                            "rid","bf_N:CA","pdb_code")

data_samples["brca1"] = ("AF-Q8CGX5-F1-model_v4",
                            "N:CA:C:N+1 C-1:N:CA:C N:CA CA:C C:O",
                            "rid","bf_N:CA","aa",
                            "C-1:N:CA:C","N:CA:C:N+1","bf_N:CA")

data_samples["4rek"] = ("4rek",
                            "N:CA:C:N+1 C-1:N:CA:C N:CA CA:C C:O N:N+1 N:CA:C",
                            "N:CA:C:N+1","N:N+1","N:CA:C",
                            "C-1:N:CA:C","N:CA:C:N+1","N:CA:C")

data_samples["iron"] = ("5d8v 4u9h 5jsk 6rk0",
                            "FE:{(N),(O)} FE:{(N),(O)@2} FE:{(N),(O)&2} (FE):(O,N)+1",
                            "FE:{(N),(O)}","FE:{(N),(O)@2}","aa",
                            "FE:{(N),(O)&2}","(FE):(O,N)+1","pdb_code")

data_samples["sulphur contacts"] = ("1AB1 1AHO 1CBN 1DY5 1EJG 1ETL 1ETM 1ETN 1F94 1FN8 1FY4 1FY5 1G4I 1G66 1G6X 4NDS 4NSV 4R5R 4UNU 4UYR 4WKA 4XDX 4XOJ 4Y9W 4YEO 4ZM7 5A71 5AVD 5AVG 5DJ7 5DK1 5DKM 5E7W 5E9N 5HMV 5HQI 5I5B",
                            #"SG:{SG@1} SG:{(N),(O)}[dis|<3] SG:{(N),(O)}:{SG@1}",
                            "SG:{SG@1} SG:{(N),(O)} SG:{(N),(O)}:{SG@1}",
                            "SG:{SG@1}","SG:{(N),(O)}","SG:{(N),(O)}:{SG@1}",
                            "SG:{(N),(O)}:{SG@1}","SG:{SG@1}","SG:{(N),(O)}")

data_samples["hydrogen bonds"] = ("1AB1 1AHO 1CBN 1DY5 1EJG 1ETL 1ETM 1ETN 1F94 1FN8 1FY4 1FY5 1G4I 1G66 1G6X 4NDS 4NSV 4R5R 4UNU 4UYR 4WKA 4XDX 4XOJ 4Y9W 4YEO 4ZM7 5A71 5AVD 5AVG 5DJ7 5DK1 5DKM 5E7W 5E9N 5HMV 5HQI 5I5B",
                            "O:{(N)}[dis|2.0<>3.00] C:O N:CA:C N:CA",                            
                            "O:{(N)}[dis|2.0<>3.00]","info_O:{(N)}[dis|2.0<>3.00]","C:O",
                            "O:{(N)}[dis|2.0<>3.00]","C:O","N:CA:C")




structures = "1ejg 3nir"
geos = "N:CA:C:N+1 C-1:N:CA:C C:O"
idx,idy,idz = 0,1,2

cols = st.columns([1,3])
with cols[0]:
    example_set = st.selectbox("Choose a sample set - you can overwrite it",data_samples.keys())

structures, geos, idx1,idy1,idz1,idx2,idy2,idz2 = data_samples[example_set]
    

st.write("---")
    
cols = st.columns([1,1])
with cols[0]:
    structures = st.text_input("Enter a list of structures", value=structures)
with cols[1]:
    geos = st.text_input("Enter a list of geometric paramaters",value=geos)


ls_structures = structures.split(" ")
ls_geos = geos.split(" ")


df = pd.DataFrame({'A' : []})
if 'data' not in st.session_state:
    st.session_state['data'] = df
else:
    df = st.session_state['data']

#if len(df.index) > 0:
#    st.dataframe(df)

if st.button("Calulate dataframe"):
    
    pobjs = []
    for pdb in ls_structures:
        source = "ebi"
        if "AF-" in pdb:
            source = "alphafold"
        if source == "ebi":
            pdb = pdb.lower()
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)

    #st.dataframe(df)
    st.session_state['data'] = df
    


if len(df.index) > 0:
    st.dataframe(df)
    ax_cols = list(df.columns)
    iidx1 = ax_cols.index(idx1)
    iidy1 = ax_cols.index(idy1)
    iidz1 = ax_cols.index(idz1)
    iidx2 = ax_cols.index(idx2)
    iidy2 = ax_cols.index(idy2)
    iidz2 = ax_cols.index(idz2)
     

    cols = st.columns(6)
    with cols[0]:
        x_ax1 = st.selectbox("Choose x-axis 1", ax_cols,index=iidx1)
    with cols[1]:
        y_ax1 = st.selectbox("Choose y-axis 1",ax_cols,index=iidy1)
    with cols[2]:
        z_ax1 = st.selectbox("Choose z-axis (hue) 1",ax_cols,index=iidz1)
    with cols[3]:
        x_ax2 = st.selectbox("Choose x-axis 2", ax_cols,index=iidx2)
    with cols[4]:
        y_ax2 = st.selectbox("Choose y-axis 2",ax_cols,index=iidy2)
    with cols[5]:
        z_ax2 = st.selectbox("Choose z-axis (hue) 2",ax_cols,index=iidz2)

    if st.button("Calulate plot"):
        cols = st.columns(2)
        with cols[0]:
            fig = px.scatter(df, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=600, height=600, opacity=0.7)
            st.plotly_chart(fig, use_container_width=False)
        with cols[1]:
            fig = px.scatter(df, x=x_ax2, y=y_ax2, color=z_ax2,title="",width=600, height=600, opacity=0.7)
            st.plotly_chart(fig, use_container_width=False)

    


    



