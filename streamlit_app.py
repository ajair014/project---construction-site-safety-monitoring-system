import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile
import time
import os
from dotenv import load_dotenv

# Load environment variables (for email alerts)
load_dotenv()

# Page Config
st.set_page_config(page_title="Construction Safety Monitoring System", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🏗️ CONSTRUCTION SAFETY MONITORING SYSTEM</h1>", unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([2, 1])

# Load YOLO model
model_path = "Model/ppe.pt"
if not os.path.exists(model_path):
    st.error("Model file not found! Place 'ppe.pt' inside the Model folder.")
    st.stop()
model = YOLO(model_path)

# Control variables
start_button = col1.button("▶️ Start Monitoring")
stop_button = col1.button("⏹️ Stop")
frame_placeholder = col1.empty()
person_info = col2.empty()

# Stream capture variable
cap = None

def run_detection():
    global cap
    cap = cv2.VideoCapture(0)
    prev_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera!")
            break

        # Run YOLO detection
        results = model(frame, conf=0.4)
        annotated_frame = results[0].plot()

        # Show live camera feed
        frame_placeholder.image(annotated_frame, channels="BGR")

        # Extract and display detection details
        boxes = results[0].boxes
        detections = []
        for cls_id, conf in zip(boxes.cls, boxes.conf):
            label = model.names[int(cls_id)]
            detections.append(f"{label} ({conf:.2f})")

        if detections:
            details = "<br>".join(detections)
        else:
            details = "No detections yet."

        person_info.markdown(
            f"<div style='background-color:#f4f4f4;padding:10px;border-radius:10px;'>"
            f"<h3>Detected Objects</h3><p>{details}</p></div>",
            unsafe_allow_html=True,
        )

        # Stop button logic
        if st.session_state.get("stop_now", False):
            break

        # Control refresh rate
        time.sleep(0.1)

    cap.release()

# Start / Stop handling
if start_button:
    st.session_state.stop_now = False
    run_detection()

if stop_button:
    st.session_state.stop_now = True
    if cap:
        cap.release()
    st.success("Monitoring stopped.")

# Control buttons section
st.markdown("---")
st.markdown("<h3 style='text-align:center;'>🎮 Control Panel</h3>", unsafe_allow_html=True)
colA, colB, colC = st.columns(3)
colA.button("📸 Capture Frame")
colB.button("📧 Send Alert Email")
colC.button("❌ Exit Application")
