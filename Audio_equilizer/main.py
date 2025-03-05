import numpy as np
import pyaudio
import scipy.signal as signal
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys

# Audio settings
RATE = 44100  # Sampling rate
CHUNK = 1024  # Buffer size

# Filter settings
FREQ_BANDS = {
    "Low": (20, 250),
    "Mid": (250, 4000),
    "High": (4000, 20000)
}

class Equalizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.gains = {"Low": 0, "Mid": 0, "High": 0}
        self.stream = None
        self.p = None
        self.start_audio()
    
    def initUI(self):
        layout = QVBoxLayout()
        self.sliders = {}
        
        for band in FREQ_BANDS:
            label = QLabel(f"{band} Gain: 0 dB")
            layout.addWidget(label)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-20)
            slider.setMaximum(20)
            slider.setValue(0)
            slider.valueChanged.connect(lambda value, b=band, l=label: self.update_gain(value, b, l))
            layout.addWidget(slider)
            self.sliders[band] = slider
        
        self.reset_button = QPushButton("Reset EQ")
        self.reset_button.clicked.connect(self.reset_eq)
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Real-Time Audio Equalizer")
    
    def update_gain(self, value, band, label):
        self.gains[band] = value
        label.setText(f"{band} Gain: {value} dB")
    
    def reset_eq(self):
        for band in self.gains:
            self.gains[band] = 0
            self.sliders[band].setValue(0)
    
    def apply_eq(self, audio_data):
        processed_audio = np.zeros_like(audio_data, dtype=np.float32)
        for band, (low, high) in FREQ_BANDS.items():
            sos = signal.butter(4, [low, high], btype='band', fs=RATE, output='sos')
            filtered = signal.sosfilt(sos, audio_data)
            gain = 10 ** (self.gains[band] / 20)
            processed_audio += filtered * gain
        return np.clip(processed_audio, -1, 1)
    
    def callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        processed_audio = self.apply_eq(audio_data)
        processed_audio = (processed_audio * 32768).astype(np.int16)
        return (processed_audio.tobytes(), pyaudio.paContinue)
    
    def start_audio(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback
        )
        self.stream.start_stream()
    
    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    eq = Equalizer()
    eq.show()
    sys.exit(app.exec_())
