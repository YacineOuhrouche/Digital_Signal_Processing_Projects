# 🎚️ Real-Time Audio Equalizer

This project is a **real-time audio equalizer** application built with **PyQt5** for the graphical user interface (GUI) and **PyAudio** for audio input/output handling.

---

## 🎵 Features

✅ Real-time audio processing  
✅ Adjustable **Low**, **Mid**, and **High** frequency bands  
✅ Horizontal sliders for intuitive gain control  
✅ Instant feedback — audio adjustments are applied **immediately** to the output stream  

---

## 🛠️ Technologies Used

| Library   | Purpose |
|---|---|
| **PyQt5** | Modern, responsive GUI |
| **PyAudio** | Real-time audio input/output |
| **SciPy**  | Digital signal processing (bandpass filtering) |
| **NumPy**  | Efficient numerical processing |

---

## 🔧 How It Works

1. Captures **live audio input** using PyAudio.
2. Splits the audio signal into **three frequency bands**:
   - 🎚️ **Low** frequencies
   - 🎚️ **Mid** frequencies
   - 🎚️ **High** frequencies
3. Applies adjustable **gain** to each band based on slider positions.
4. Recombines the adjusted bands and sends the processed signal to the **audio output** in real time.

---

## 📊 GUI Preview


.![Screenshot 2025-01-30 112112](https://github.com/user-attachments/assets/9524c467-5b82-401d-bd24-072269527cd7)
