import numpy as np
import scipy.io.wavfile as wavfile


def sine(frequency, samplerate):
    t = np.linspace(0.0, 1.0, samplerate)
    return np.sin(2.0 * np.pi * frequency * t)


def impulse(samplerate):
    t = np.zeros(samplerate)
    t[0] = 1.0
    return t


def main():
    frequency = 440
    samplerate = 44100
    wave = sine(frequency, samplerate)
    # wave = impulse(samplerate)
    stereo = np.stack((wave, wave), axis=1)

    print(wave.flags)
    print(stereo.flags)
    wavfile.write("example.wav", samplerate, stereo.astype(np.float32))


main()
