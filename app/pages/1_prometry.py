import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px

DATADIR = "app/data/"

is_calc = False

st.set_page_config(
        page_title="ra-box",
        page_icon="app/static/ed-icon.png",
        layout="wide",
    )


code_string = "from prometry import pdbloader as pl\n"
code_string += "from prometry import pdbgeometry as pg\n"
code_string += "import pandas as pd\n"
code_string += f"DATADIR = '{DATADIR}'\n"

code_string2 = ""

st.header("PROMETRY")
st.write("#### A library to calculate geometric parameters of protein structures and perform criteria search")

tabDemo,tabHelp,tabCode = st.tabs(["demo","help","code"])

with tabDemo:

    if 'pdbs' not in st.session_state:
        st.session_state['pdbs'] = ""
    if 'geos' not in st.session_state:
        st.session_state['geos'] = ""
    if 'code_df' not in st.session_state:
        st.session_state['code_df'] = ""
        st.session_state['code_df2'] = ""
        st.session_state['code_df3'] = ""

    data_samples = {}
    data_samples["crambin resolution"] = ("1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt",
                                "N:CA CA:C C:O C:N+1",
                                "N:CA","C:O","resolution",
                                "rid","bf_N:CA","pdb_code")

    data_samples["crambin disulfide"] = ("1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt",
                                "SG:{SG@1} SG:N SG:O N:CA",
                                "SG:{SG@1}","info_SG:{SG@1}","pdb_code",
                                "SG:{SG@1}","SG:O","pdb_code")

    data_samples["crambin nearests"] = ("1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt",
                                "N:(N,O) N:(N@1) N:(O@1) N:(N,O@1) N:(N,O@2) N:(N,O&1) N:(N,O&2)",
                                "N:(N,O@1)","info_N:(N,O@1)","pdb_code",
                                "N:(N,O@1)","N:(N,O@2)","N:(O@1)")
                                
    
    data_samples["CA contacts"] = ("5nqo",
                                "CA:{CA@i}[dis|0.5<>10]",
                                "rid","rid2_CA:{CA@i}[dis|0.5<>10]","CA:{CA@i}[dis|0.5<>10]",
                                "rid","rid2_CA:{CA@i}[dis|0.5<>10]","bf_CA:{CA@i}[dis|0.5<>10]")

    data_samples["NO contacts"] = ("5nqo",
                                "N:(O@i)[~aa|HOH,dis|0.5<>10]",
                                "rid","rid2_N:(O@i)[~aa|HOH,dis|0.5<>10]","N:(O@i)[~aa|HOH,dis|0.5<>10]",
                                "rid","rid2_N:(O@i)[~aa|HOH,dis|0.5<>10]","bf_N:(O@i)[~aa|HOH,dis|0.5<>10]")

    data_samples["BRCA1-AF"] = ("AF-Q8CGX5-F1-model_v4",
                                "N:CA:C:N+1 C-1:N:CA:C N:CA CA:C C:O",
                                "rid","bf_N:CA","aa",
                                "C-1:N:CA:C","N:CA:C:N+1","bf_N:CA")

    data_samples["MAST4-AF"] = ("AF-O15021-F1-model_v4",
                                "CA:{CB&1} CA:{CA&1}",
                                "CA:{CA&1}","info_CA:{CA&1}","bf_CA:{CA&1}",
                                "CA:{CB&1}","info_CA:{CB&1}","bf_CA:{CB&1}")

                                
    data_samples["4rek"] = ("4rek",
                                "N:CA:C:N+1 C-1:N:CA:C N:CA CA:C C:O N:N+1 N:CA:C",
                                "N:CA:C:N+1","N:N+1","N:CA:C",
                                "C-1:N:CA:C","N:CA:C:N+1","N:CA:C")
    
    data_samples["glycine"] = ("1AB1 1AHO 1CBN 1DY5 1EJG 1ETL 1ETM 1ETN 1F94 1FN8 1FY4 1FY5 1G4I 1G66 1G6X 4NDS 4NSV 4R5R 4UNU 4UYR 4WKA 4XDX 4XOJ 4Y9W 4YEO 4ZM7 5A71 5AVD 5AVG 5DJ7 5DK1 5DKM 5E7W 5E9N 5HMV 5HQI 5I5B",
                                "N[aa|GLY]:CA:C:N+1 C-1:N:CA:C N:CA CA:C C:O N:N+1 N:CA:C",
                                "N:CA:C:N+1","N:N+1","N:CA:C",
                                "C-1:N:CA:C","N:CA:C:N+1","N:CA:C")

    data_samples["iron"] = ("2d5x 2peg 3vrg 1j41 1j40 3gkv 2r80 2d5z 1thb 2dn2 2dn1 2dn3 2w72 6rp5 2h8f 3d1k 3bom 4esa 5eui 6zmx 6ihx 6ii1 7dy3 7dy4 1uiw 6kah 6kai 6ka9 6kae 6lcx 6lcw 6l5w 6kao 6kaq 6kap 6l5v 1bab 1bz0 1ird 3s66 7jy3",
                                "FE:(N,O) FE:(N,O@1) FE:(N,O@2) FE:(N,O@3)",
                                "FE:(N,O)","FE:(N,O@1)","aa",
                                "FE:(N,O@2)","FE:(N,O@3)","pdb_code")

    data_samples["hydrogen bonds"] = ("1AB1 1AHO 1CBN 1DY5 1EJG 1ETL 1ETM 1ETN 1F94 1FN8 1FY4 1FY5 1G4I 1G66 1G6X 4NDS 4NSV 4R5R 4UNU 4UYR 4WKA 4XDX 4XOJ 4Y9W 4YEO 4ZM7 5A71 5AVD 5AVG 5DJ7 5DK1 5DKM 5E7W 5E9N 5HMV 5HQI 5I5B",
                                "N:(O,N&1)[dis|2.5<>3.0] C:O N:CA:C N:CA",                            
                                "N:(O,N&1)[dis|2.5<>3.0]","info_N:(O,N&1)[dis|2.5<>3.0]","pdb_code",
                                "N:(O,N&1)[dis|2.5<>3.0]","info_N:(O,N&1)[dis|2.5<>3.0]","aa")




    structures = "1ejg 3nir"
    geos = "N:CA:C:N+1 C-1:N:CA:C C:O"
    idx,idy,idz = 0,1,2
    
    st.write("##### 1) Select sample data")
    cols = st.columns([2,1])
    with cols[0]:
        example_set = st.selectbox("Choose a sample set (you can overwrite it)",data_samples.keys())

    structures, geos, idx1,idy1,idz1,idx2,idy2,idz2 = data_samples[example_set]
        

    st.write("---")
    st.write("##### 2) Edit/enter structures and geos")
        
    cols = st.columns([1,1])
    with cols[0]:
        structures = st.text_input("List of structures", value=structures,help="pdb or alphafold codes, space delim")
    with cols[1]:
        geos = st.text_input("List of geometric paramaters",value=geos,help="space delim, 2, 3 or 4 atoms - see help")


    ls_structures = structures.split(" ")
    ls_geos = geos.split(" ")


    df_geos = pd.DataFrame({'A' : []})
    df_atoms = pd.DataFrame({'A' : []})
    if 'data' not in st.session_state:
        st.session_state['data'] = df_geos
        st.session_state['atoms'] = df_atoms
    else:
        if st.session_state['pdbs'] != structures or st.session_state['geos'] != geos:
            st.session_state['data'] = df_geos
            st.session_state['atoms'] = df_atoms
            st.session_state['pdbs'] = structures
            st.session_state['geos'] = geos
        else:
            df_geos = st.session_state['data']
            df_atoms = st.session_state['atoms']

    
    st.write("---")
    st.write("##### 3) Calculate dataframe")
    if st.button("Calculate dataframe"):

        code_string += f"ls_structures = {ls_structures}\n"
        code_string += f"ls_geos = {ls_geos}\n"
        
        pobjs = []
        code_string += f"for pdb in ls_structures:"
        code_string += """    
        if "AF-" in pdb:
            source = "alphafold"
        else:
            source = "ebi"
            pdb = pdb.lower()
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
        po = pla.load_pdb()
        pobjs.append(po)
        """
        
        
        for pdb in ls_structures:        
            if "AF-" in pdb:
                source = "alphafold"
            else:
                source = "ebi"
                pdb = pdb.lower()
            pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
            po = pla.load_pdb()
            pobjs.append(po)
        
        gm = pg.GeometryMaker(pobjs)
        df_geos = gm.calculateGeometry(ls_geos)
        df_atoms = gm.calculateData()

        code_string += "\ngm = pg.GeometryMaker(pobjs)\n"
        code_string += "df_geos = gm.calculateGeometry(ls_geos)\n"
        code_string += "df_atoms = gm.calculateData()\n"
            
        st.session_state['data'] = df_geos
        st.session_state['atoms'] = df_atoms
        st.session_state['code_df'] = code_string
                
    if len(df_geos.index) > 0:
        st.write("---")
        st.write("##### 4) View calculated data")
        with st.expander("Expand geometric dataframe"):
            st.dataframe(df_geos)
            st.download_button("Download geometric promerty file",df_geos.to_csv(),"promerty_geos.csv","text/csv",key='geos-csv')
        
        with st.expander("Expand atomic dataframe"):
            st.dataframe(df_atoms)
            st.download_button("Download atomic promerty file",df_atoms.to_csv(),"promerty_atoms.csv","text/csv",key='atoms-csv')

                
        ax_cols = list(df_geos.columns)
        iidx1,iidy1,iidz1,iidx2,iidy2,iidz2 = 0,0,0,0,0,0
        try:
            iidx1 = ax_cols.index(idx1)
            iidy1 = ax_cols.index(idy1)
            iidz1 = ax_cols.index(idz1)
            iidx2 = ax_cols.index(idx2)
            iidy2 = ax_cols.index(idy2)
            iidz2 = ax_cols.index(idz2)
        except:
            pass

        

        st.write("---")
        st.write("##### 5) Plot geometric data")
        cols = st.columns(6)
        with cols[0]:
            x_ax1 = st.selectbox("x-axis 1", ax_cols,index=iidx1)
        with cols[1]:
            y_ax1 = st.selectbox("y-axis 1",ax_cols,index=iidy1)
        with cols[2]:
            z_ax1 = st.selectbox("z-axis (hue) 1",ax_cols,index=iidz1)
        with cols[3]:
            x_ax2 = st.selectbox("x-axis 2", ax_cols,index=iidx2)
        with cols[4]:
            y_ax2 = st.selectbox("y-axis 2",ax_cols,index=iidy2)
        with cols[5]:
            z_ax2 = st.selectbox("z-axis (hue) 2",ax_cols,index=iidz2)
        
        if st.button("Calculate geo plot"):
            cols = st.columns(2)
            with cols[0]:
                fig = px.scatter(df_geos, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                st.plotly_chart(fig, use_container_width=False)
            with cols[1]:
                fig = px.scatter(df_geos, x=x_ax2, y=y_ax2, color=z_ax2,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                st.plotly_chart(fig, use_container_width=False)
            
            code_string2 = "import plotly.express as px\n"
            code_string2 += f"fig = px.scatter(df_geos, x='{x_ax1}', y='{y_ax1}', color='{z_ax1}',title="",width=500, height=500, opacity=0.7, color_continuous_scale=px.colors.sequential.Viridis))\n"
            code_string2 += "fig.show() #or preferred method, e.g. fig.write_html('path/to/file.html')"
            st.session_state['code_df2'] = code_string2
                                                                           
            
        
        st.write("---")
        st.write("##### 6) Plot spatial data")
        aax_cols = list(df_atoms.columns)
        aiidh1,aiidh2 = 0,0
        try:            
            aiidh1 = aax_cols.index("bfactor")            
            aiidh2 = aax_cols.index("element")
        except:
            pass

        pdbs = list(df_atoms["pdbCode"].unique())
                
        ax_ax1 = "x"        
        ay_ax1 = "y"
        az_ax1 = "z"
        ax_ax2 = "x"        
        ay_ax2 = "y"
        az_ax2 = "z"
                
        cols = st.columns(3)
        with cols[0]:
            pdb = st.selectbox("pdbcode", pdbs,index=0)        
        with cols[1]:
            ah_ax1 = st.selectbox("hue 1",aax_cols,index=aiidh1)        
        with cols[2]:
            ah_ax2 = st.selectbox("hue 2",aax_cols,index=aiidh2)
        if st.button("Calculate atom plot"):
            st.write("Spatial info")
            cols = st.columns(2)
            with cols[0]:                
                fig = px.scatter_3d(df_atoms[df_atoms['pdbCode'] == pdb], x=ax_ax1, y=ay_ax1, z=az_ax1, color=ah_ax1,title="",
                    width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                st.plotly_chart(fig, use_container_width=False)
            with cols[1]:                
                fig = px.scatter_3d(df_atoms[df_atoms['pdbCode'] == pdb], x=ax_ax2, y=ay_ax2, z=az_ax2, color=ah_ax2,title="",
                    width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                st.plotly_chart(fig, use_container_width=False)

            code_string3 = "import plotly.express as px\n"
            code_string3 += f"fig = px.scatter_3d(df_atoms, x='x', y='y', z='z',color='{ah_ax1}',title='',\n"
            code_string3 += "    width=500, height=500, opacity=0.5, color_continuous_scale=px.colors.sequential.Viridis))\n"
            code_string3 += "fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))\n"
            code_string3 += "fig.show() #or preferred method, e.g. fig.write_html('path/to/file.html')\n"
            st.session_state['code_df3'] = code_string3

        

with tabCode:
    st.code(st.session_state['code_df'])
    st.code(st.session_state['code_df2'])
    st.code(st.session_state['code_df3'])
    
with tabHelp:
#with st.expander("Expand for geo and criteria description help"):
    st.code("""
        ---------------------------------------------------------------------       
        Examples
        ---------------------------------------------------------------------  
        Lengths in the backbone: N:CA CA:C C:N+1 C:O  
        Backbone angle tau: N:CA:C  
        Phi and psi : C-1:N:CA:C and N:CA:C:N+1                  
        The carbonyl oxygen and the nearest N to it that is not in the same residue: O:(N&1) 
        The disulfide bonds (or nearest cysteine sulphurs): SG:(SG&1)  
        Any O or N within 2.5-3 of the N but not the same residue: N:{(O),(N)@1}[dis|2.5<>3.0]
        The second nearest O or N: N:(N,O@1)
        The nearest O or N not the same residue: N:{N,O&1}
        Only glycine: N[aa|GLY]:CA
        Never water: N:(O)[~aa|HOH]
        Only glycine TO glycine:  N[aa|GLY]:CA[aa|GLY]
        Contacts CA-CA between 0.5 and 6: CA:{CA@i}[dis|0.5<>6]
        ---------------------------------------------------------------------  
        Description
        ---------------------------------------------------------------------  
        With no brackets or symbols, the simple case is that you are looking for atom types within a residue  
        N:CA - is looking for all atoms of type N and the CA in the same residue, for the distance  
        N:CA:C - is looking for all atoms of types N, CA and C in the same residue and the angle  

        +/- look for neighbouring residues
        C:N+1 - looks for the C in a residue and the N in the next residue  
        C-1:N - as per above but the previous residue to the current   
        ---------------------------------------------------------------------  
        () brackets symbolise element rather than atom type, eg N can mean NZ, NE1 etc, and this starts a 
        nearest lookup if it is not the first item, or a cross product if it is
        (N):N - means any type N, and the N in the same residue - there can be more than 1 per residue
        N:(N) - means all N's in a reside and the nearest type N in the same residue - only 1 per residue
        ---------------------------------------------------------------------  
        {} symbolise distance searchers - the list of atoms is all the candidates
        N:{O,N} is all N's in a residue and the nearest O or N to it - 1 per residue
        ---------------------------------------------------------------------  
        () brackets can be used
        N:{(O),(N)} is all N's in a residue and the nearest O type or N type to it - 1 per residue
        ---------------------------------------------------------------------  
        operators @ or & specify x nearest or at least x away as follows
        N:{O,N@1} means N and the second nearest  O or N to it - 0 indexed
        N:{O,N&2} means N and the nearest O or N as long as it is at least 2 residues away
        CA:{CA@i} i means all CAs so it is CA with all possible CAs.
        ---------------------------------------------------------------------  
        [] after a geo specify a comma delim list of criteria
        aa - amino acid of the residue
        dis - distance from the first atom where
        < less than
        > greater than
        <> between
        >< extremes
        occ - occupancy, with just =, < or >
        ---------------------------------------------------------------------  
    """)