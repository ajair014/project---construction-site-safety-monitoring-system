🏗️ AI-Based Construction Safety Monitoring System
🔥 Real-Time PPE Detection | Face Recognition | Voice & Email Alerts | Streamlit Dashboard

This project is an AI-powered safety monitoring system designed for construction sites.
It uses YOLO-based object detection, facial recognition, email notifications, and voice alerts to detect worker safety violations and instantly notify supervisors.

🌟 Key Features
🟡 1. Real-Time PPE Detection

Detects construction PPE violations using YOLO:

No-Helmet

No-Safety Vest

No-Mask

Worker Detection

🟢 2. Worker Face Recognition

Identifies each worker using a photo captured during registration.

🔔 3. Instant Alerts

Email Alerts (every fixed interval)

Voice Alerts (continuous until violation stops)

🗄️ 4. MySQL Database Integration

Stores:

Worker details

Photo

ID

Phone number

Address

🎥 5. Live Monitoring Dashboard

Beautiful Streamlit UI with:

Live video feed

Live worker status

Real-time violation updates

Stylish animated background UI

🛠️ Tech Stack
Component	Technology
Programming Language	Python
Object Detection	YOLO (Ultralytics)
Facial Recognition	OpenCV + Custom Face Encoder
Frontend/UI	Streamlit
Database	MySQL
Alerts	SMTP Email, pyttsx3 Voice Engine
Environment Storage	.env
📂 Project Structure
Construction-Safety-Monitoring/
│── app_streamlit.py
│── database.py
│── face_recognition_module.py
│── models/
│     └── ppe.pt
│── known_faces/
│── background.jpg
│── .env
│── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/yourusername/Construction-Safety-Monitoring.git
cd Construction-Safety-Monitoring

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup .env File

Create a .env file:

SENDER_EMAIL=yourmail@gmail.com
SENDER_PASSWORD=yourpassword
RECEIVER_EMAIL=supervisormail@gmail.com

4️⃣ Start Streamlit App
streamlit run app_streamlit.py

📸 Live Monitoring Output

✔ Real-time PPE Detection
✔ Worker Face Recognition
✔ Unsafe Condition Alerts
✔ Status Panel UI


🚀 Future Enhancements

Mobile app integration

Cloud storage for detection logs

Daily/weekly report generation

Integration with IoT sensors

Tracking worker attendance using face recognition

🤝 Contributions

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to improve.
