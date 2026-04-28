import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from db import create_attendance


def show_attendance_result(df, logs):
    st.write("Please review attendance before confirming.")
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard", width="stretch"):
            st.session_state.pop('voice_attendance_results', None)
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm & Save", width="stretch", type="primary"):
            try:
                create_attendance(logs)
                st.toast("Attendance saved!")
                st.session_state.attendance_images = []
                st.session_state.pop('voice_attendance_results', None)
                st.session_state.pop('attendance_results', None)
                st.session_state.pop('attendance_to_log', None)
                st.rerun()
            except Exception:
                st.error("Sync failed!")


@st.dialog("Attendance Report")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
