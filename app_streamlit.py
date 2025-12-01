# app_streamlit.py — Modern Animated Version
import streamlit as st
import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO
from face_recognition_module import load_known_faces, recognize_faces_in_frame
from database import create_table, insert_worker, get_worker_by_name
import smtplib
from email.message import EmailMessage
import pyttsx3
import threading
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()

# Email setup
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Database init
create_table()

# Paths
KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

# Load YOLO model
MODEL_PATH = "models/ppe.pt"
MODEL_LOADED = False
if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
    MODEL_LOADED = True

# Voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak_async(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()

# ------------------ EMAIL FUNCTION ------------------
def send_email(subject, body):
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        st.error("Email credentials not set in .env")
        return
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Load known faces
known_faces = load_known_faces(KNOWN_FACES_DIR)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI-Based Construction Safety System", layout="wide")

# ------------------ CUSTOM ANIMATED CSS ------------------

st.markdown("""
    <style>
    /* 🌆 Apply background image to full app container */
    [data-testid="stAppViewContainer"] {
        background-image: url("P:\mini project\Construction-PPE-Detection\background.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
    }

    /* 🌫️ Add dark transparent overlay for text visibility */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.65);
        z-index: 0;
    }

    /* 🔮 Make all app content appear above overlay */
    .main, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        position: relative;
        z-index: 1;
    }

    /* 💎 Sidebar glass style */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
        border-right: 2px solid rgba(0,255,255,0.2);
    }

    /* 🧠 Title Glow Animation */
    .animated-title {
        font-size: 36px;
        text-align: center;
        color: #00FFFF;
        animation: glow 2s infinite alternate;
        margin-top: -20px;
        z-index: 2;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00FFFF; }
        to { text-shadow: 0 0 30px #00CED1, 0 0 60px #00FFFF; }
    }

    /* ⚡ Buttons Glow */
    .glow-button {
        background-color: #0E76A8;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        box-shadow: 0 0 10px #00FFFF;
        width: 100%;
    }

    .glow-button:hover {
        background-color: #00FFFF;
        color: #000;
        box-shadow: 0 0 25px #00FFFF;
        transform: scale(1.05);
    }

    /* 🧩 Card Styling */
    .card {
        background-color: rgba(10, 10, 15, 0.7);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        transition: 0.4s ease;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
    }

    hr {
        border: 1px solid #00FFFF33;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# ------------------ HEADER ------------------
st.markdown("<h1 class='animated-title'>AI-Based Construction Safety Monitoring System</h1>", unsafe_allow_html=True)
st.write("### 👷 Smart Vision | Real-Time Detection | Automated Alerts")
st.write("<hr>", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("🧠 Control Panel")
email_interval = st.sidebar.slider("Email Interval (seconds)", 10, 300, 30)
enable_email = st.sidebar.checkbox("Enable Email Alerts", True)
enable_voice = st.sidebar.checkbox("Enable Voice Alerts", True)

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

col1, col2 = st.columns([3, 1])

# ------------------ WORKER MANAGEMENT ------------------
with col2:
    st.markdown("<div class='card'><b>👷 Worker Management</b></div>", unsafe_allow_html=True)
    if st.button("➕ Worker Registration", key="register"):
        with st.form("worker_form", clear_on_submit=True):
            name = st.text_input("Name")
            worker_id = st.text_input("Worker ID")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            st.write("📸 Capture Worker Photo:")
            photo = st.camera_input("Take Photo")
            submit_btn = st.form_submit_button("Register Worker")
            if submit_btn:
                if not (name and worker_id and phone and address and photo):
                    st.error("All fields and photo are required.")
                else:
                    image_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(photo.getvalue())
                    insert_worker(name, worker_id, phone, address, image_path)
                    st.success(f"✅ Worker {name} registered successfully!")
                    known_faces[name] = image_path

# ------------------ MONITORING SECTION ------------------
with col1:
    st.markdown("<div class='card'><b>🎥 Live Detection</b></div>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 Start Monitoring"):
            st.session_state.monitoring = True
    with col_btn2:
        if st.button("🛑 Stop Monitoring"):
            st.session_state.monitoring = False

    frame_placeholder = st.empty()
    details_placeholder = st.empty()

    if st.session_state.monitoring:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Camera not detected.")
        else:
            st.info("Monitoring started... Press Stop to end.")
            last_email_time = 0
            while st.session_state.monitoring:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read from camera.")
                    break

                # YOLO Detection
                unsafe_count = 0
                if MODEL_LOADED:
                    results = model(frame)
                    for box in results[0].boxes:
                        cls = int(box.cls.cpu().numpy())
                        label = results[0].names[cls]
                        conf = float(box.conf.cpu().numpy())
                        xyxy = box.xyxy.cpu().numpy().astype(int)[0]
                        x1, y1, x2, y2 = xyxy
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        if "no" in label.lower():
                            unsafe_count += 1

                # Face Recognition
                faces = recognize_faces_in_frame(frame, known_faces)
                for f in faces:
                    x, y, w, h = f["bbox"]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f["name"], (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB")

                # Real-time Live Details
                names = ", ".join([f["name"] for f in faces]) or "Unknown"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = "SAFE ✅" if unsafe_count == 0 else "UNSAFE ⚠️"
                with details_placeholder:
                    st.markdown(f"""
                        <div class='card'>
                            <b>👷 Worker:</b> {names}<br>
                            <b>🕒 Time:</b> {timestamp}<br>
                            <b>⚠️ Status:</b> {"<span style='color:#00FF7F;'>SAFE ✅</span>" if status == "SAFE ✅" else "<span style='color:#FF4500;'>UNSAFE ⚠️</span>"}
                        </div>
                    """, unsafe_allow_html=True)

                # Alerts
                if unsafe_count > 0 and (time.time() - last_email_time) >= email_interval:
                    subject = f"Safety Alert! {unsafe_count} violation(s)"
                    body = f"Time: {datetime.now()}\nUnsafe count: {unsafe_count}\nDetected workers: {names}"
                    if enable_email:
                        send_email(subject, body)
                    if enable_voice:
                        speak_async(f"Alert! {unsafe_count} unsafe conditions detected.")
                    last_email_time = time.time()

            cap.release()
            st.success("✅ Monitoring stopped.")
