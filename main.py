import tkinter as tk
from tkinter import ttk, font, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.geometry("400x400")
        # Spawn window in the center of the screen
        self.eval("tk::PlaceWindow . center")

        # Create main content frame
        self.mainframe = Mainframe(self)
        self.mainframe.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

        # Enable main frame auto-resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class Mainframe(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.initial_time_limit = 10 # How long the test runs for

        # Initialize tracking variables
        self.CPM_var = tk.IntVar(self, value=0)
        self.WPM_var = tk.IntVar(self, value=0)
        self.time_var = tk.IntVar(self, value=self.initial_time_limit)

        self._countdown_id = None
        self._is_countdown_running = False

        # Create fonts
        self.text_box_font = font.Font(family="Times New Roman", size=20)
        self.typing_field_font = font.Font(family="Arial", size=14)

        # Enable content auto-resizing
        for col in range(0, 6):
            self.columnconfigure(col, weight=1)

        self.rowconfigure(1, weight=1)


        # Create menu bar elements
        self.CPM_desc_label = ttk.Label(self, text="Corrected CPM: ")
        self.CPM_desc_label.grid(column=0, row=0)
        self.CPM_count_label = ttk.Label(self, textvariable=self.CPM_var)
        self.CPM_count_label.grid(column=1, row=0)

        self.WPM_desc_label = ttk.Label(self, text="WPM: ")
        self.WPM_desc_label.grid(column=2, row=0)
        self.WPM_count_label = ttk.Label(self, textvariable=self.WPM_var)
        self.WPM_count_label.grid(column=3, row=0)

        self.time_desc_label = ttk.Label(self, text="Time Left: ")
        self.time_desc_label.grid(column=4, row=0)
        self.time_count_label = ttk.Label(self, textvariable=self.time_var)
        self.time_count_label.grid(column=5, row=0)

        self.restart_btn = ttk.Button(self, text="Restart", command=self.restart)
        self.restart_btn.grid(column=6, row=0)

        # Create text box
        self.text_box = tk.Text(self, width=50, height=10)
        self.text_box.grid(column=0, row=1, columnspan=7, sticky="nsew", pady=10)
        self.text_box.config(font=self.text_box_font)
        self.text_box["wrap"] = "word"
        self.text_box["state"] = "disabled"

        # Populate text box
        self.generate_words()

        # Create the typing field
        self.typing_field = tk.Text(self, width=50, height=1)
        self.typing_field.grid(column=0, row=2, columnspan=7, sticky="ew")
        self.typing_field.config(font=self.typing_field_font)
        self.typing_field["wrap"] = "word"

        # Event bindings
        self.typing_field.bind("<KeyPress>", self.countdown)

        # Disable placeholder elements
        self.CPM_desc_label["state"] = "disabled"
        self.CPM_count_label["state"] = "disabled"
        self.WPM_desc_label["state"] = "disabled"
        self.WPM_count_label["state"] = "disabled"


    def restart(self):
        # Stop countdown
        self.after_cancel(self._countdown_id)
        self._is_countdown_running = False

        # Clear text box and regenerate words
        self.text_box["state"] = "normal"
        self.text_box.delete("1.0", tk.END)
        self.generate_words()

        # Enable and clear typing field
        self.typing_field["state"] = "normal"
        self.typing_field.delete("1.0", tk.END)

        # Reset tk variables
        self.CPM_var.set(0)
        self.WPM_var.set(0)
        self.time_var.set(self.initial_time_limit)


    def generate_words(self, *args, **kwargs):
        # Convert txt file into list of words
        with open("random_word_list.txt", "r") as file:
            words = [line.strip() for line in file]

        # Insert words into text_box
        self.text_box["state"] = "normal"
        self.text_box.insert("1.0", " ".join(words))
        self.text_box["state"] = "disabled"


    def countdown(self, *args, **kwargs):
        # Stop multiple countdown timers from being queued
        if self._is_countdown_running:
            return

        count = self.time_var.get()

        # Only proceed if there's time left
        if count > 0:
            self._is_countdown_running = True
            self._countdown_id = self.after(0, self._decrement_count)

    def _decrement_count(self):
        count = self.time_var.get()
        if count > 0:
            count -=1
            self.time_var.set(count)
            self._countdown_id = self.after(1000, self._decrement_count)
        else:
            self._is_countdown_running = False # Stop the countdown when it reaches 0
            self.end_test()


    def end_test(self):
        # Disable typing field
        self.typing_field["state"] = "disabled"

        # Get list of words typed by the user
        user_string = self.typing_field.get("1.0", tk.END)
        user_words = user_string.split()

        # Get list of words generated in the text_box
        generated_string = self.text_box.get("1.0", tk.END)
        generated_words = generated_string.split()

        correct_characters = 0

        # Compare user's typed words with test words and obtain correct character count
        for i in range(len(user_words)):
            if user_words[i] == generated_words[i]:
                correct_characters += len(user_words[i])

        # Calculate cpm and wpm stats, then display results
        cpm = int(correct_characters * (60 / self.initial_time_limit))
        wpm = int(cpm // 5)
        messagebox.showinfo(title="Results", message=f"CPM: {cpm}\nWPM: {wpm}")


    # todo Improve program to achieve greater parity to online example
        # todo Get list of random words from web and populate text file with them
        # todo Choose a random selection of words from the list
        # todo Track progress in realtime
        # todo Scroll textbox and typing field when line complete
        # todo High score feature


if __name__ == '__main__':
    app = App()
    app.mainloop()
