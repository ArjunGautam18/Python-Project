import tkinter as tk
import random
from time import time

# list of texts
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am.",
    "The only thing we have to fear is fear itself.",
    "That's one small step for man, one giant leap for mankind.",
    "In the middle of difficulty lies opportunity.",
]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        self.text_to_type = random.choice(texts)
        self.start_time = None

        # display text
        self.label = tk.Label(
            root, text=self.text_to_type, wraplength=400, font=("Helvetica", 14)
        )
        self.label.pack(pady=20)

        # typing area
        self.text_area = tk.Text(root, height=5, width=50, font=("Helvetica", 14))
        self.text_area.pack(pady=10)
        self.text_area.bind("<KeyPress>", self.start_timer)

        # submit button
        self.submit_button = tk.Button(root, text="Check Result", command=self.check_result)
        self.submit_button.pack(pady=10)

        # result label
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

        # reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_test)
        self.reset_button.pack(pady=10)

    def start_timer(self, event):
        if self.start_time is None:
            self.start_time = time()

    def check_result(self):
        if self.start_time is None:
            return

        end_time = time()
        elapsed_time = end_time - self.start_time

        typed_text = self.text_area.get("1.0", tk.END).strip()

        # calculate WPM
        words_typed = len(typed_text.split())
        wpm = (words_typed / elapsed_time) * 60 if elapsed_time > 0 else 0

        # calculate accuracy
        correct_chars = sum(
            1 for i, c in enumerate(typed_text)
            if i < len(self.text_to_type) and c == self.text_to_type[i]
        )
        total_chars = len(self.text_to_type)
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

        self.result_label.config(
            text=f"Speed: {wpm:.2f} WPM\nAccuracy: {accuracy:.2f}%"
        )

    def reset_test(self):
        self.text_to_type = random.choice(texts)
        self.label.config(text=self.text_to_type)
        self.text_area.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.start_time = None


# run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
