# ✍️ On-Screen Drawing using Index Finger (with Color Selection) | OpenCV + MediaPipe

A creative and intuitive project that lets you **draw on-screen using just your index finger** and a webcam! Built using **OpenCV** and **MediaPipe**, this project also includes a **color palette** to choose brush colors with a simple fingertip hover gesture.

---

## 🎯 Features

- 🖐️ Hand tracking with **MediaPipe Hands**
- 🖊️ Draw in real-time using only your **index finger**
- 🎨 Color palette overlay to **change brush color**
- 🎭 Smooth drawing canvas blended with webcam feed
- 🔁 Press **'C' to clear**, **ESC to exit**
- 🧠 Detects finger state to avoid accidental drawing

---

## 🛠 Tech Stack

- **Python 3.x**
- **OpenCV** – For computer vision and GUI rendering
- **MediaPipe** – For fast and accurate hand landmark detection
- **NumPy** – For canvas operations

---

## 🧠 How It Works

- **MediaPipe** detects 21 landmarks of the hand.
- If only the **index finger** is raised, it activates draw mode.
- Tracks fingertip coordinates frame-by-frame and draws lines on a canvas.
- A **color selection box** on the top right lets you choose different brush colors.

---

## 📁 Project Structure

```bash
finger-drawing/
├── writing.py     # Main Python script
├── README.md      # Project documentation
```
---
## 🚀 How to Run
1. Clone the Repository
```bash
git clone https://github.com/AlienMinus/finger-drawing.git
cd finger-drawing
```
2. Install Dependencies
```bash
pip install opencv-python mediapipe numpy
```
3. Run the Application
```bash
python writing.py
```

## 🎨 Controls
- 🖊️ Raise only the index finger to draw
- 🎨 Touch a color box with your fingertip to change brush color
- 🧽 Press C to clear the canvas
- ❌ Press ESC to exit the application

## 🌟 Potential Extensions
- Add Eraser Tool using gestures
- Add Stroke Size Control
- Export drawing as image file
- Gesture-based menu toggling (save, load, undo)

👨‍💻 Author
Manas Ranjan Das
B.Tech in ECE | Embedded Systems & AI Enthusiast | Full-Stack Developer
📧 dasmanasranjan2005@gmail.com