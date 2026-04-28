import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from ui.base_layout import style_background_dashboard, style_base_layout
from ui.components.header import header_dashboard
from ui.components.footer import footer_home
from PIL import Image
import numpy as np
from pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from pipelines.voice_pipeline import get_voice_embedding, identify_speaker
from db import get_all_students, create_student, get_student_subject, get_student_attendance, unenroll_student_to_subject

from ui.components.dialog_enroll import enroll_dialog
from ui.components.subject_card import subject_card


def _extract_student_id(student_data):
    for key in ('student_id', 'id', 'studentId', 'student_ID'):
        val = student_data.get(key)
        if val is not None:
            return val
    for key, val in student_data.items():
        if isinstance(val, int) and key not in ('face_embedding', 'voice_embedding'):
            return val
    return None


def student_dashboard():
    style_background_dashboard()
    style_base_layout()

    student_data = st.session_state.student_data
    student_id = _extract_student_id(student_data)

    if student_id is None:
        st.error(f"Could not find student ID. Available keys: {list(student_data.keys())}")
        if st.button("Logout"):
            del st.session_state['student_data']
            st.rerun()
        return

    top_left, top_right = st.columns([2, 1])
    with top_left:
        header_dashboard()
    with top_right:
        st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 16px 20px;
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 10px;
">
    <p style="font-size:0.9rem; opacity:0.8; margin:0;">Welcome back</p>
    <p style="font-size:1.4rem; font-weight:700; margin:0;">
        {student_data.get('name', 'Student')}
    </p>
</div>
""", unsafe_allow_html=True)
        if st.button("Logout", type="secondary", width='stretch'):
            del st.session_state['student_data']
            st.rerun()
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()
    st.subheader('Your Enrolled Subjects')
    st.divider()

    with st.spinner('Loading your enrolled subjects...'):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {'total': 0, 'attended': 0})

        def unenroll_button(student_id=student_id, sid=sid, sub=sub):
            if st.button('Unenroll from this course', type='tertiary', width='stretch', key=f'unenroll_{sid}', icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("📅", "Total", stats['total']),
                    ("✅", "Attended", stats['attended']),
                ],
                footer_callback=unenroll_button
            )

    footer_home()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='student_loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    face_tab, voice_tab, register_tab = st.tabs(["FaceID Login", "Voice Login", "Register"])

    with face_tab:
        _face_login_section()

    with voice_tab:
        _voice_login_section()

    with register_tab:
        _register_tab_section()

    footer_home()


def _face_login_section():
    st.header("Login using FaceID")
    st.info("Make sure your face is fully visible and well-lit before taking the photo.")
    photo_source = st.camera_input("Position your face in the center")

    if not photo_source:
        return

    img = np.array(Image.open(photo_source))
    with st.spinner('AI is scanning....'):
        detected, all_ids, num_faces = predict_attendance(img)

    if num_faces == 0:
        st.warning('No face detected — make sure your face fills the frame and is well-lit.')
        return
    if num_faces > 1:
        st.warning('Multiple faces detected — please ensure only you are in the frame.')
        return

    valid_ids = [sid for sid in detected.keys() if sid is not None]

    if valid_ids:
        student_id = valid_ids[0]
        all_students = get_all_students()
        student = next((s for s in all_students if _extract_student_id(s) == student_id), None)

        if student:
            st.session_state.is_logged_in = True
            st.session_state.user_role = 'student'
            st.session_state.student_data = student
            st.toast(f"Welcome Back {student['name']}")
            time.sleep(1)
            st.rerun()
        else:
            st.warning('Face matched internally but student record not found. Please register.')
            _registration_form(photo_source, key_prefix='face_login')
    else:
        st.warning('Face not recognized. If you are new, please register below.')
        _registration_form(photo_source, key_prefix='face_login')


def _voice_login_section():
    st.header("Login using Voice")
    st.info('Record a short phrase to identify yourself')

    audio_data = None
    try:
        audio_data = st.audio_input('Record your voice', key='voice_login_input')
    except Exception:
        st.error('Audio recording not available on this device')
        return

    if audio_data:
        with st.spinner('Identifying voice...'):
            embedding = get_voice_embedding(audio_data.read())
            all_students = get_all_students()

            candidates = {
                _extract_student_id(s): s.get('voice_embedding')
                for s in all_students
                if s.get('voice_embedding') and _extract_student_id(s) is not None
            }

            if not candidates:
                st.warning('No voice profiles enrolled yet.')
                return

            student_id, score = identify_speaker(embedding, candidates)

            if student_id:
                student = next((s for s in all_students if _extract_student_id(s) == student_id), None)
                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student_data = student
                    st.toast(f"Welcome Back {student['name']}")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('Voice not recognized!')


def _register_tab_section():
    st.header("Register using FaceID")
    st.info("Take a photo to register your face for attendance")
    photo_source = st.camera_input("Position your face in the center", key='register_camera')
    if photo_source:
        _registration_form(photo_source, key_prefix='register_tab')


def _registration_form(photo_source, key_prefix='face'):
    with st.container(border=True):
        st.header('Register new Profile')
        new_name = st.text_input('Enter your name', placeholder='E.g. Ankit Bisht', key=f'{key_prefix}_reg_name')

        st.subheader('Optional: Voice Enrollment')
        st.info('Enroll your voice for voice-only attendance')

        audio_data = None
        try:
            audio_data = st.audio_input('Record a short phrase like "I am present, my name is Ankit"', key=f'{key_prefix}_reg_voice_input')
        except Exception:
            st.warning('Audio recording not available')

        if st.button('Create Account', type='primary', key=f'{key_prefix}_reg_submit'):
            if new_name:
                with st.spinner('Creating profile..'):
                    img = np.array(Image.open(photo_source))
                    encodings = get_face_embeddings(img)

                    if encodings:
                        face_emb = encodings[0].tolist()

                        voice_emb = None
                        if audio_data:
                            voice_emb = get_voice_embedding(audio_data.read())

                        response_data = create_student(
                            new_name,
                            face_embedding=face_emb,
                            voice_embedding=voice_emb
                        )

                        if response_data:
                            train_classifier()
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data[0]
                            st.toast(f"Profile Created! Hi {new_name}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Couldn't capture facial features for registration")
                    else:
                        st.error("No face detected in the photo")
            else:
                st.warning('Please enter your name!')
