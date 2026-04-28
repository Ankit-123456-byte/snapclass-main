import streamlit as st

def header_home():
    logo_url="[img]https://i.ibb.co/dsnWCpVP/Generated-Image-April-19-2026-10-02-PM.png[/img]"

    st.markdown(f"""
          <div style="display:flex; align-items:center; justify-content:center;gap:10px; margin-bottom:30px margin-top:30px">
                <img src='{logo_url}' style='height:85px;'/>
                <h1 style='text-align:center; color:#E0E3FF'>SNAP<b/r>CLASS</h1>
           </div>
             """, unsafe_allow_html=True )

def header_dashboard():
    logo_url="[img]https://i.ibb.co/dsnWCpVP/Generated-Image-April-19-2026-10-02-PM.png[/img]"

    st.markdown(f"""
          <div style="display:flex; align-items:center;justify-content:center; gap:10px; margin-top:30px;">
                <img src='{logo_url}' style='height:60px;'/>
                <h2 style='color:#5865F2'>SNAP<br/>CLASS</h2>
           </div>
             """, unsafe_allow_html=True )
