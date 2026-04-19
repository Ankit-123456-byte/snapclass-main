import streamlit as st

def style_background_home():
    st.markdown(""" 
        <style>
                .stApp{
                    background:#5865F2 !important;
                }

                .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;
            }
                
                
                
        </style>
    
    
""",unsafe_allow_html=True)
    

def style_background_dashboard():
    st.markdown(""" 
        <style>
                .stApp{
                    background:#E0E3FF
                }
                
        </style>
    
    
""",unsafe_allow_html=True)
    

def style_base_layout():
    st.markdown(""" 
        <style>
                
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');


        /* Hide Top Bar of Streamlit */
                
            #MainMenu,footer,header{
                visibility:hidden;
                }
            .block-container {
                padding-top:1.5rem;
                }    
            h1{
               font-family: 'Climate Crisis',sans-serif !important;
               font-Size: 3.5rem  !important;
               line-height:1.1 !important;
               margin-bottom: 0rem !important;
               color: #E0E3FF;

            }

             h2{
               font-family: 'Climate Crisis',sans-serif !important;
               font-Size: 2rem  !important;
               line-height:0.9 !important;
               margin-bottom: 0rem !important;
               color: #E0E3FF;
                


            }       
            h3,h4,p{
                font-family: 'Outfit',sans-serif;
            }
                

            .stButton button {
                border-radius: 1.5rem !important;
                background: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            .stButton button:hover {
                background: #c73584 !important;
                transform: scale(1.03) !important;
                }                



                    
                
        </style>
    
    
""",unsafe_allow_html=True)