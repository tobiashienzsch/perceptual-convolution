import matplotlib.pyplot as plt
import numpy as np


def simplp(x: np.ndarray, xm1: float):
    y = np.zeros_like(x)
    y[0] = x[0] + xm1
    for n in range(1, x.shape[0]):
        y[n] = x[n] + x[n - 1]
    return y, x[-1]


def main():
    fs = 128
    frequency = fs / 4
    t = np.linspace(0.0, 1.0, fs)
    x = np.sin(2.0 * np.pi * frequency * t)
    # y, xm1 = simplp(x, 0)
    # print(np.max(np.abs(y))/np.max(np.abs(x)))

    # plt.plot(t, x, label="In")
    # plt.plot(t, y, label="Out")

    # etl::pow(Float(1) / euler, Float(1) / static_cast<Float>(_sampleRate) / sec);
    plt.plot(t, 20.0*np.log10(np.power(1.0 / np.e, 1.0 / fs / t)), label="Z1")
    plt.plot(t, 20.0*np.log10(np.power(0.5 / np.e, 1.0 / fs / t)), label="Z2")
    plt.plot(t, 20.0*np.log10(np.power(0.1 / np.e, 1.0 / fs / t)), label="Z3")
    plt.legend()
    plt.show()


main()
