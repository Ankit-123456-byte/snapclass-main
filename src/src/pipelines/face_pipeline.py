import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))

    return encodings

def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            sid = student.get('student_id') or student.get('id')
            if sid is None:
                for v in student.values():
                    if isinstance(v, int):
                        sid = v
                        break
            y.append(sid)

    if len(X) == 0:
        return None

    clf = None
    if len(set(y)) >= 2:
        clf = SVC(kernel='linear', probability=True, class_weight='balanced')
        try:
            clf.fit(X, y)
        except ValueError:
            clf = None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    resemblance_threshold = 0.7

    for encoding in encodings:
        distances = [np.linalg.norm(np.array(x) - encoding) for x in X_train]
        best_idx = int(np.argmin(distances))
        best_score = distances[best_idx]
        predicted_id = y_train[best_idx]

        if clf is not None:
            predicted_id = clf.predict([encoding])[0]
            best_score = np.linalg.norm(np.array(X_train[y_train.index(predicted_id)]) - encoding)

        if best_score <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)
