import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ui.components.header import header_home
from ui.components.footer import footer_home
from ui.base_layout import style_base_layout,style_background_home
from teacher_screen import teacher_screen
from student_screen import student_screen

def Home_screen():
    
    header_home()
    style_background_home()

    style_base_layout()

    col1, col2 = st.columns(2,gap="large")

    with col1:
        st.header("I'm Student")
        if st.button('Student Portal', type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()
       
    with col2:
        st.header("I'm Teacher")
        if st.button('Teacher Portal', type='primary' ,icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

login_type = st.session_state.get('login_type', None)

if login_type == 'student':
    student_screen()
elif login_type == 'teacher':
    teacher_screen()    
else:
    Home_screen()

footer_home()    
