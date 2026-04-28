import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from db import create_subject
import time


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_code = st.text_input("Subject Code", placeholder='CS101')
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject", type="primary", width="stretch"):
        if not sub_code or not sub_name or not sub_section:
            st.warning("All fields are required.")
        else:
            result = create_subject(sub_code, sub_name, sub_section, teacher_id)
            if result:
                st.success("Subject created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Subject code already exists or an error occurred.")
