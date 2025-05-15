import wave
import numpy as np
import struct
import os

# Define the directory where sound files will be stored
sound_dir = "assets/sounds"
os.makedirs(sound_dir, exist_ok=True)

def create_sound(filename, frequency=440, duration=0.2, volume=0.5, sample_rate=44100):
    """Create a simple sound file with the given parameters."""
    # Calculate the number of samples
    num_samples = int(duration * sample_rate)
    
    # Generate a sine wave
    t = np.linspace(0, duration, num_samples, False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    
    # Apply volume
    sine_wave = sine_wave * volume
    
    # Convert to 16-bit PCM
    sine_wave = sine_wave * 32767
    sine_wave = sine_wave.astype(np.int16)
    
    # Create a wave file
    with wave.open(os.path.join(sound_dir, filename), 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes (16 bits)
        wf.setframerate(sample_rate)
        wf.writeframes(sine_wave.tobytes())
    
    print(f"Created {filename}")

# Create typing sound: higher pitch, short duration
create_sound("typing.wav", frequency=880, duration=0.05, volume=0.3)

# Create correct sound: pleasant ascending tone
create_sound("correct.wav", frequency=660, duration=0.3, volume=0.7)

# Create wrong sound: lower, descending tone
create_sound("wrong.wav", frequency=220, duration=0.4, volume=0.7)

# Create level up sound: cheerful victory sound
create_sound("level_up.wav", frequency=1320, duration=0.5, volume=0.8)

print("All sound files created successfully!")