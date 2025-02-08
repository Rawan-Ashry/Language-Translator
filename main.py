from tkinter import *
from tkinter import ttk, messagebox
import googletrans
import asyncio
from googletrans import Translator

# -----------------------------
# Setup and styling configuration
# -----------------------------
root = Tk()
root.title("Language Translator")
root.geometry("1000x600")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # light gray background

# Use a modern theme for ttk widgets
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="white", background="white", padding=5)

# Create language mappings (capitalize names for display)
languages = googletrans.LANGUAGES  # e.g., {'en': 'english', 'fr': 'french', ...}
language_list = [v.capitalize() for k, v in languages.items()]
lang_codes = {v.capitalize(): k for k, v in languages.items()}

# -----------------------------
# Functions
# -----------------------------
def label_change():
    """Update the labels above the text areas to reflect the selected languages."""
    src_lang = combo_1.get()
    dest_lang = combo_2.get()
    input_label.config(text=f"{src_lang} Text")
    output_label.config(text=f"{dest_lang} Text")
    root.after(1000, label_change)

def translate_text():
    """Translate the text from the source language to the destination language."""
    original_text = text_1.get(1.0, END).strip()
    if not original_text:
        messagebox.showinfo("Info", "Please enter some text to translate.")
        return

    src_name = combo_1.get()
    dest_name = combo_2.get()
    src_code = lang_codes.get(src_name)
    dest_code = lang_codes.get(dest_name)

    if not src_code or not dest_code:
        messagebox.showerror("Error", "Invalid language selection!")
        return

    translator = Translator()
    try:
        # Use an asyncio event loop to run the async translation coroutine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        translation = loop.run_until_complete(
            translator.translate(original_text, src=src_code, dest=dest_code)
        )
        loop.close()
        translated_text = translation.text
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")
        return

    text_2.delete(1.0, END)
    text_2.insert(END, translated_text)

# -----------------------------
# Layout using grid
# -----------------------------

# Configure grid weights for proper resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)

# Title Label
title_label = Label(root, text="Language Translator", font=("Roboto", 32, "bold"),
                    bg="#f0f0f0", fg="#333")
title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

# Language Selection Frame
lang_frame = Frame(root, bg="#f0f0f0")
lang_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20))

# Source language selection (left)
src_frame = Frame(lang_frame, bg="#f0f0f0")
src_frame.grid(row=0, column=0, padx=20)
src_title = Label(src_frame, text="From", font=("Roboto", 14, "bold"),
                  bg="#f0f0f0", fg="#333")
src_title.pack(pady=(0, 5))
combo_1 = ttk.Combobox(src_frame, values=language_list, font=("Roboto", 14),
                       state="readonly", width=15)
combo_1.pack(pady=(0, 5))
combo_1.set("English")  # default selection

# Destination language selection (right)
dest_frame = Frame(lang_frame, bg="#f0f0f0")
dest_frame.grid(row=0, column=1, padx=20)
dest_title = Label(dest_frame, text="To", font=("Roboto", 14, "bold"),
                   bg="#f0f0f0", fg="#333")
dest_title.pack(pady=(0, 5))
combo_2 = ttk.Combobox(dest_frame, values=language_list, font=("Roboto", 14),
                       state="readonly", width=15)
combo_2.pack(pady=(0, 5))
combo_2.set("Select Language")

# Text Areas Frame
text_frame = Frame(root, bg="#f0f0f0")
text_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
text_frame.grid_columnconfigure(0, weight=1)
text_frame.grid_columnconfigure(2, weight=1)
text_frame.grid_rowconfigure(1, weight=1)

# Left Side: Input Text
input_label = Label(text_frame, text="English Text", font=("Roboto", 16, "bold"),
                    bg="#f0f0f0", fg="#333")
input_label.grid(row=0, column=0, pady=(0, 5))
frame_input = Frame(text_frame, bg="white", bd=2, relief=GROOVE)
frame_input.grid(row=1, column=0, padx=(10, 5), sticky="nsew")
text_1 = Text(frame_input, font=("Roboto", 14), bg="white", wrap=WORD, bd=0)
text_1.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
scroll_bar1 = Scrollbar(frame_input)
scroll_bar1.pack(side=RIGHT, fill=Y)
text_1.config(yscrollcommand=scroll_bar1.set)

# Right Side: Translated Text
output_label = Label(text_frame, text="Select Language Text", font=("Roboto", 16, "bold"),
                     bg="#f0f0f0", fg="#333")
output_label.grid(row=0, column=2, pady=(0, 5))
frame_output = Frame(text_frame, bg="white", bd=2, relief=GROOVE)
frame_output.grid(row=1, column=2, padx=(5, 10), sticky="nsew")
text_2 = Text(frame_output, font=("Roboto", 14), bg="white", wrap=WORD, bd=0)
text_2.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
scroll_bar2 = Scrollbar(frame_output)
scroll_bar2.pack(side=RIGHT, fill=Y)
text_2.config(yscrollcommand=scroll_bar2.set)

# Center: Translate Button
translate_btn = Button(text_frame, text="Translate", font=("Roboto", 16, "bold"),
                       bg="#4a7abc", fg="white", cursor="hand2", relief=GROOVE,
                       command=translate_text, padx=20, pady=10)
translate_btn.grid(row=1, column=1, padx=10, pady=10)

# Start the periodic label update
label_change()

root.mainloop()
