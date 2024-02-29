import tkinter as tk
from tkinter import messagebox
import random
from tkinter import font
import math


class HammingCode(object):

    @classmethod
    def get_parity_bit_positions(cls, n):
        return [2 ** i - 1 for i in range(n)]

    @classmethod
    def is_parity_bit(cls, pos):
        return (pos + 1) & pos == 0

    @classmethod
    def encode(cls, data):
        n = len(data)  # Długość danych wejściowych
        k = math.ceil(math.log2(n + 1))  # Liczba bitów parzystości

        data = list(reversed(data))

        encoded_data = [None] * (n + k)
        j = 0  # Indeks danych wejściowych

        # pozycje bitów parzystości
        parity_bit_pos = cls.get_parity_bit_positions(k)

        # Wstawiamy bity danych wejściowych w odpowiednie pozycje w zakodowanych danych
        for i in range(n + k):
            if not cls.is_parity_bit(i):
                encoded_data[i] = data[j]
                j += 1

        xor_result = 0
        for i in range(n + k):
            if encoded_data[i] == 1:
                xor_result ^= i + 1

        xor_str = cls.to_bin_str(xor_result, len(parity_bit_pos))
        for i, position in enumerate(parity_bit_pos):
            encoded_data[position] = int(xor_str[i])

        return list(reversed(encoded_data))

    @classmethod
    def to_bin_str(cls, value, length):
        return list(reversed(str(bin(value)[2:]).rjust(length, '0')))

    @classmethod
    def detect_error(cls, encoded_data):
        encoded_data = list(reversed(encoded_data))

        xor_result = 0
        for i in range(len(encoded_data)):
            if encoded_data[i] == 1:
                pos = i + 1
                xor_result ^= pos

        return xor_result

    @classmethod
    def correct_error(cls, encoded_data, error_position):
        # Korekcja błędu
        encoded_data[len(encoded_data) - error_position] ^= 1
        return encoded_data

    @classmethod
    def randomize_error(cls, encoded_data):
        # Generacja błędu
        error_position = random.randint(0, len(encoded_data) - 1)
        if not encoded_data[error_position]:
            return cls.randomize_error(encoded_data)

        encoded_data[error_position] ^= 1
        return len(encoded_data) - error_position

    @classmethod
    def decode(cls, encoded_data):
        encoded_data = list(reversed(encoded_data))

        k = int(math.log2(len(encoded_data) + 1))  # Liczba bitów parzystości
        n = len(encoded_data) - k  # Długość danych wejściowych

        # pozycje bitów parzystości
        # parity_bit_pos = cls.get_parity_bit_positions(k)

        decoded_data = []
        for i in range(n + k):
            # if i in parity_bit_pos:
            if cls.is_parity_bit(i):
                continue
            decoded_data.append(encoded_data[i])

        return list(reversed(decoded_data))


def printHamming():
    data = entry.get()

    if (len(data) != 0):
        if (len(data) % 4 == 0):
            try:
                data = [int(c) for c in data]
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid binary number.")
                return
        else:
            messagebox.showerror("Error", "Invalid input. The lenght must be the multipy of 4.")
    else:
        messagebox.showerror("Error", "No input.")

    result_text = f"Data: {data}\n"

    encoded_data = HammingCode.encode(data)
    result_text += f"Encoded data: {encoded_data}\n"

    error_position = HammingCode.detect_error(encoded_data)
    if error_position:
        result_text += f"Error on position: {error_position}\n"

    error_position = HammingCode.randomize_error(encoded_data)
    # Reverse the error position before displaying
    # error_position = len(encoded_data) - error_position + 1
    result_text += f"Randomized error position: {error_position} <--\n"
    result_text += f"Encoded data with error: {encoded_data}\n"

    detected_error_position = HammingCode.detect_error(encoded_data)
    # Reverse the detected error position before displaying
    # detected_error_position = len(encoded_data) - detected_error_position + 1
    result_text += f"Detected error on position: {detected_error_position} <--\n"

    corrected_data = HammingCode.correct_error(encoded_data, detected_error_position)
    result_text += f"Corrected data: {corrected_data}\n"

    decoded_data = HammingCode.decode(corrected_data)
    result_text += f"Decoded data: {decoded_data}\n"

    messagebox.showinfo("Result", result_text)


# Create the main window
window = tk.Tk()
window.title("Hamming Code Encoder/Decoder")

# Set the window dimensions and center it on the screen
window_width = 400
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Change the button color to sage
window.tk_setPalette(background='#d3e4c5')

# Create the input label and entry
input_label = tk.Label(window, text="Enter binary data:", font=("Arial", 12))
input_label.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
entry.focus()

# Create the button to trigger the encoding/decoding process
button = tk.Button(window, text="Encode/Decode", command=printHamming, font=("Arial", 12), bg="#9dc183")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Configure column and row weights
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

# Start the main event loop
window.mainloop()
