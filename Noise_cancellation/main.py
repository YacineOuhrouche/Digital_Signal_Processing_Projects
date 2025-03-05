import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import numpy as np
import scipy.fftpack
from scipy.io.wavfile import read, write
import os
import io
import soundfile as sf

# Function to apply spectral subtraction
def spectral_subtraction(noisy_signal, noise_estimate, window_size=1024, overlap=512):
    noisy_signal_fft = scipy.fftpack.fft(noisy_signal)
    noise_fft = scipy.fftpack.fft(noise_estimate)

    magnitude = np.abs(noisy_signal_fft) - np.abs(noise_fft)
    magnitude[magnitude < 0] = 0  # Avoid negative magnitudes

    phase = np.angle(noisy_signal_fft)
    cleaned_signal_fft = magnitude * np.exp(1j * phase)

    cleaned_signal = np.real(scipy.fftpack.ifft(cleaned_signal_fft))

    return cleaned_signal

# Function to estimate noise using silent segments
def estimate_noise(signal, silence_threshold=500):
    # Create a simple noise estimate by looking for silent segments in the audio.
    silence = np.where(np.abs(signal) < silence_threshold)[0]
    noise_estimate = signal[silence][:len(signal)]  # Basic estimate by copying the silent part
    return noise_estimate

# Function to load audio file and convert to a numpy array
def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
    if file_path:
        try:
            # Use pydub to handle multiple formats
            audio = AudioSegment.from_file(file_path)
            app.audio = audio
            app.sample_rate = audio.frame_rate

            # Convert audio to numpy array
            samples = np.array(audio.get_array_of_samples())
            app.noisy_signal = samples

            app.filename = os.path.basename(file_path)
            app.label_file.config(text=f"Loaded: {app.filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to apply noise cancellation
def apply_noise_cancellation():
    if hasattr(app, 'noisy_signal'):
        try:
            # Estimate the noise from silent parts of the audio
            noise_estimate = estimate_noise(app.noisy_signal)
            cleaned_signal = spectral_subtraction(app.noisy_signal, noise_estimate)

            # Normalize the cleaned signal
            cleaned_signal = np.int16(cleaned_signal / np.max(np.abs(cleaned_signal)) * 32767)
            app.cleaned_signal = cleaned_signal

            messagebox.showinfo("Success", "Noise cancellation applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply noise cancellation: {e}")
    else:
        messagebox.showwarning("No File", "Please load an audio file first.")

# Function to preview the cleaned audio
def preview_cleaned_audio():
    if hasattr(app, 'cleaned_signal'):
        try:
            # Convert cleaned signal back to audio segment for playback
            cleaned_audio = AudioSegment(
                app.cleaned_signal.tobytes(), 
                frame_rate=app.sample_rate, 
                sample_width=2, 
                channels=1, 
                length=len(app.cleaned_signal) // app.sample_rate
            )
            cleaned_audio.export("temp_cleaned.wav", format="wav")
            os.system("start temp_cleaned.wav")  # Play the cleaned audio file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview audio: {e}")
    else:
        messagebox.showwarning("No Cleaned Audio", "Please apply noise cancellation first.")

# Function to save the cleaned audio
def save_cleaned_audio():
    if hasattr(app, 'cleaned_signal'):
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3")])
        if save_path:
            try:
                write(save_path, app.sample_rate, app.cleaned_signal)
                messagebox.showinfo("Success", f"Cleaned audio saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    else:
        messagebox.showwarning("No Cleaned Audio", "Please apply noise cancellation first.")

# Create the GUI application
class NoiseCancellationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noise Cancellation Tool")

        # Layout
        self.label_file = tk.Label(root, text="No file loaded", font=("Arial", 14))
        self.label_file.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Audio File", command=load_audio_file, width=20)
        self.load_button.pack(pady=5)

        self.cancel_button = tk.Button(root, text="Apply Noise Cancellation", command=apply_noise_cancellation, width=20)
        self.cancel_button.pack(pady=5)

        self.preview_button = tk.Button(root, text="Preview Cleaned Audio", command=preview_cleaned_audio, width=20)
        self.preview_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Cleaned Audio", command=save_cleaned_audio, width=20)
        self.save_button.pack(pady=5)

# Create the root window and run the application
root = tk.Tk()
app = NoiseCancellationApp(root)
root.mainloop()
