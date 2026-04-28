import streamlit as st

from src.src.home_screen import Home_screen
from src.src.teacher_screen import teacher_screen
from src.src.student_screen import student_screen
from src.src.ui.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SnapClass-Making Attendance faster using AI',
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
            if join_code and st.session_state.get('is_logged_in'):
                auto_enroll_dialog(join_code)

        case None:
            Home_screen()

main()
