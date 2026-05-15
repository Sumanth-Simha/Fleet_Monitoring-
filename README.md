# AutoSentinel: Fleet Risk Intelligence Platform
### AI-Powered Driver Fatigue Detection & Fleet Monitoring System

> A real-time computer vision based fleet safety platform that detects driver fatigue, classifies driver alertness, and provides centralized fleet intelligence through a cloud-connected monitoring dashboard. Because apparently humans decided sleep deprivation and heavy vehicles should coexist on highways. Brilliant species design.

---

## 📌 Project Overview

AutoSentinel is an AI-powered fleet intelligence and driver monitoring platform designed to reduce fatigue-related road accidents in commercial transportation systems. The project continuously monitors drivers using a cabin-mounted camera and applies computer vision techniques to detect drowsiness and unresponsiveness in real time.

The system combines:

- Real-time facial landmark detection
- Eye behavior analysis
- Fatigue metric computation
- Cloud-based monitoring
- Centralized fleet dashboarding
- Intelligent alert generation

The platform uses **MediaPipe FaceMesh**, **OpenCV**, **NumPy**, **Supabase**, and **Streamlit** to create a scalable and low-cost fleet safety ecosystem suitable for logistics companies, public transportation systems, and commercial vehicle operators.

---

## 🚨 Problem Statement

Driver fatigue remains one of the leading causes of commercial road accidents. Existing solutions such as dashcams, lane departure systems, and manual rest-hour monitoring are largely reactive and fail to identify fatigue before an accident occurs.

AutoSentinel addresses this problem by:

- Monitoring driver eye behavior continuously
- Detecting fatigue indicators in real time
- Triggering in-cabin alerts
- Uploading fatigue events to the cloud
- Providing centralized fleet-level visibility

---

## 🎯 Objectives

- Real-time driver monitoring using a cabin-mounted camera
- Facial landmark extraction using MediaPipe FaceMesh
- Computation of fatigue metrics: Eye Aspect Ratio (EAR), PERCLOS, Blink Rate, Eye Closure Duration
- Driver state classification: Normal, Drowsy, Unresponsive
- Cloud synchronization of driver metrics
- Fleet monitoring through a centralized dashboard
- Scalable modular architecture for future integrations

---

## 🧠 Core Features

### 👁️ Real-Time Driver Monitoring
- Continuous webcam-based face tracking
- Facial landmark extraction at 15–30 FPS
- Low-latency fatigue analysis

### 😴 Fatigue Detection Engine

The system computes multiple fatigue indicators simultaneously:

| Metric | Description |
|---|---|
| EAR | Measures eye openness |
| PERCLOS | Percentage of eye closure over time |
| Blink Rate | Blinks per minute |
| Eye Closure Duration | Detects prolonged closures |
| Fatigue Score | Weighted combined fatigue metric |

### 🚦 Driver State Classification

| Driver State | EAR | PERCLOS | System Action |
|---|---|---|---|
| Normal | > 0.20 | < 0.35 | No alert |
| Drowsy | 0.10–0.20 | 0.35–0.70 | Audio alert + cloud upload |
| Unresponsive | < 0.10 | > 0.70 | Continuous alarm + emergency flag |

### ☁️ Cloud-Based Fleet Monitoring

The platform uploads driver metrics, fatigue events, timestamps, and captured frames to a **Supabase** backend, enabling fleet managers to monitor drivers remotely through a live dashboard.

### 📊 Fleet Dashboard

The Streamlit dashboard provides:
- Live driver feed
- Fatigue score monitoring
- Historical alert logs
- Driver-wise analysis
- Real-time status badges
- Multi-driver overview grid

---

## 🏗️ System Architecture

```
Webcam
   ↓
OpenCV Frame Capture
   ↓
MediaPipe FaceMesh
   ↓
Fatigue Analysis Engine
   ↓
Decision Engine
   ↓
Supabase Cloud Backend
   ↓
Streamlit Fleet Dashboard
```

---

## ⚙️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Computer Vision | OpenCV, MediaPipe FaceMesh |
| Numerical Computation | NumPy, SciPy |
| Backend & Cloud | Supabase, PostgreSQL, Supabase Storage |
| Frontend Dashboard | Streamlit |
| Simulation & Research | CARLA Autonomous Driving Simulator |

---

## 🧪 Working Principle

**Step 1 — Webcam Input**

Frames are captured using OpenCV and preprocessed using RGB conversion, CLAHE enhancement, and timestamping.

**Step 2 — Facial Landmark Detection**

MediaPipe FaceMesh extracts 468 facial landmarks per frame.

**Step 3 — Eye Landmark Extraction**

Eye-specific landmarks are isolated for EAR calculation.

**Step 4 — EAR Calculation**

$$EAR = \frac{\|p_1 - p_4\|}{2(\|p_2 - p_6\| + \|p_3 - p_5\|)}$$

Where vertical eye distances determine openness and horizontal eye distance normalizes the metric.

Typical EAR ranges:
- Open Eye: `0.25–0.30`
- Drowsy: `0.15–0.20`
- Closed Eye: `0.00–0.10`

**Step 5 — PERCLOS Calculation**

$$PERCLOS = \frac{\text{Frames where } EAR < \theta_{close}}{\text{Total Frames in Window}}$$

PERCLOS measures the percentage of time the driver's eyes remain closed over a rolling window — widely regarded as one of the most reliable fatigue indicators.

**Step 6 — Composite Fatigue Score**

$$\text{Fatigue Score} = w_1 \cdot EAR_d + w_2 \cdot PERCLOS + w_3 \cdot BR_d + w_4 \cdot ECD_d$$

Combines multiple metrics into a normalized 0–100 score.

---

## 📁 Project Modules

| Module | Description |
|---|---|
| Vision Input Module | Captures webcam frames |
| Facial Landmark Module | Detects 468 facial landmarks |
| Fatigue Analysis Module | Computes fatigue metrics |
| Decision Engine | Classifies driver state |
| Database Module | Uploads cloud data |
| Fleet Dashboard | Displays live fleet analytics |

---

## 🖥️ Dashboard Features

- **Overview Page** — All active drivers with color-coded fatigue states
- **Driver Detail Page** — Live metrics, EAR charts, historical trends
- **Alert History Page** — Captured fatigue events, thumbnails, timestamp logs
- **Settings Page** — Threshold customization, fleet-level configurations

---

## 📈 Results

The system successfully classified all three driver states across multiple test conditions:

| State | EAR | PERCLOS | Blink Rate | Fatigue Score |
|---|---|---|---|---|
| Normal | 0.26 | 0.23 | 16 BPM | 18 |
| Drowsy | 0.14 | 0.86 | 9 BPM | 74 |
| Unresponsive | 0.00 | 1.00 | 0 BPM | 98 |

Key observations:
- EAR decreases significantly during fatigue
- PERCLOS rises sharply during drowsiness
- Blink rate drops under fatigue conditions
- Composite fatigue score provides interpretable risk assessment

---

## ✅ Advantages

- Non-intrusive monitoring
- Real-time fatigue detection
- Centralized fleet supervision
- Cloud accessibility
- Cost-effective deployment
- Modular and scalable design
- Historical audit capability

---

## ⚠️ Limitations

- Performance degradation under poor lighting
- Requires visible frontal face orientation
- Internet required for real-time cloud synchronization
- Eye-based metrics alone cannot detect all cognitive fatigue
- EAR thresholds may vary across users

> Humans insist on sunglasses, weird seating positions, and driving at 2 AM after four cups of tea and no sleep. Computer vision can only negotiate with biology up to a point.

---

## 🔮 Future Scope

- Raspberry Pi / Jetson Nano hardware deployment
- IR camera integration
- GPS-based fleet tracking
- Neural network fatigue classification
- Mobile alert application
- Driver analytics engine
- Automated safe parking integration
- Offline location tracking using cellular signals

---

## 🧰 Requirements

### Software

| Package | Version |
|---|---|
| Python | 3.10+ |
| OpenCV | 4.8+ |
| MediaPipe | 0.10+ |
| NumPy | 1.24+ |
| SciPy | 1.11+ |
| Streamlit | 1.30+ |
| Supabase SDK | 2.x |

### Hardware

| Component | Requirement |
|---|---|
| CPU | Intel i5 / Ryzen 5 or higher |
| RAM | Minimum 16 GB |
| GPU | NVIDIA GTX 1060 or better |
| Camera | 1080p Webcam |
| Storage | SSD Recommended |

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd AutoSentinel
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

**Run the face_detection**
```bash
python main.py
```

**Run the Streamlit dashboard**
```bash
streamlit run Final_Dashboard/app.py
```

> Because every engineering project eventually becomes: camera feed not working, environment variables broken, Supabase yelling about invalid API keys at 2:13 AM, and someone saying "it worked yesterday" with total confidence. Ancient academic ritual.

---

## 📚 Research References

1. [MediaPipe: A Framework for Building Perception Pipelines](https://arxiv.org/abs/1906.08172)
2. [Real-Time Eye Blink Detection Using Facial Landmarks](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
3. [PERCLOS: A Valid Psychophysiological Measure of Alertness](https://www.fhwa.dot.gov/publications/research/safety/96108/96108.pdf)
4. [CARLA Autonomous Driving Simulator](https://carla.org/)
5. [OpenCV Documentation](https://docs.opencv.org/)
6. [Supabase Documentation](https://supabase.com/docs)
7. [Streamlit Documentation](https://docs.streamlit.io/)

---

## 👨‍💻 Team Members

- Rohan Sudhan
- R Sumanth Simha
- Pranav K
- Rida Arshad

---

## 📌 Academic Relevance

This project demonstrates practical implementation of Computer Vision, Artificial Intelligence, Real-Time Systems, Human State Monitoring, Edge AI, Cloud Integration, Fleet Analytics, Human-Machine Interaction, and Autonomous Safety Systems.

Suitable for: Final Year Major Projects · AI/ML Research Demonstrations · Intelligent Transportation Research · Computer Vision Applications · Fleet Safety Research
