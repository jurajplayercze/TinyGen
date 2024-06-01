import tkinter as tk
import pyperclip
import time
import keyboard
import threading
import datetime

shortcut = "F2"

# Funkce pro převod normálního textu na tiny 
def to_tiny_text(text):
    tiny_text_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ",
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ"
    )
    return text.translate(tiny_text_map)

# Funkce pro zavření okna a vypnutí programu
def on_closing(event=None):
    root.destroy()

# Funkce, která se zavolá při stisknutí klávesové zkratky
def on_shortcut():
    old_clipboard = pyperclip.paste()
    time.sleep(0.1)  # Pauza pro zajištění správného zkopírování aktuálního obsahu schránky
    # Sudo copy
    keyboard.send("ctrl+c")
    time.sleep(0.1)  # Pauza pro zajištění, že text je vložen do schránky
    selected_text = pyperclip.paste()
    tiny_text = to_tiny_text(selected_text)
    time.sleep(0.1)
    pyperclip.copy(tiny_text)
    # Sudo paste
    keyboard.send("ctrl+v")
    
    time.sleep(0.1)
    pyperclip.copy(old_clipboard)

    # Přidání převedeného textu do textového widgetu (konzole)
    local_time = datetime.datetime.now().strftime("%H:%M:%S")
    console_text.insert(tk.END, f"{local_time}: {tiny_text}\n")
    console_text.see(tk.END)  # Posunutí textového widgetu na konec pro zobrazení posledního textu

# Funkce pro aktualizaci klávesové zkratky
def update_shortcut():
    global shortcut
    new_shortcut = shortcut_entry.get()
    if new_shortcut:
        try:
            keyboard.remove_hotkey(shortcut)
        except KeyError:
            pass  # Pokud klávesová zkratka nebyla ještě nastavena
        shortcut = new_shortcut
        keyboard.add_hotkey(shortcut, on_shortcut)
        console_text.insert(tk.END, f"{datetime.datetime.now().strftime("%H:%M:%S")}: Aktualizace klávesové zkratky {new_shortcut}\n")
        console_text.see(tk.END)  # Posunutí textového widgetu na konec pro zobrazení posledního textu
        shortcut_label.config(text=f"Použijte klávesovou zkratku {shortcut} pro konverzi textu na tiny text")

# Vytvoření hlavního okna
root = tk.Tk()
root.title("Tiny Text Converter")
root.geometry("400x400")
root.configure(bg="#6A6A6A")

# Vytvoření a umístění popisku s instrukcí pro klávesovou zkratku
shortcut_label = tk.Label(root, text="Použijte klávesovou zkratku " + shortcut + " pro konverzi textu na tiny text", fg="white", bg="#6A6A6A")
shortcut_label.pack(pady=10)

# Vytvoření vstupního pole pro zadání vlastní klávesové zkratky
shortcut_entry = tk.Entry(root)
shortcut_entry.pack(pady=10)

# Tlačítko pro potvrzení nové klávesové zkratky
set_shortcut_button = tk.Button(root, text="Potvrdit novou klávesovou zkratku", command=update_shortcut)
set_shortcut_button.pack(pady=10)

# Vytvoření textového widgetu (konzole) pro zobrazení převedených textů
console_text = tk.Text(root, wrap=tk.WORD, height=10, fg="white", bg="#1e1e1e", insertbackground="white")
console_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Listeners
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Escape>", on_closing)

# Spuštění naslouchání klávesové zkratky v novém vlákně
thread = threading.Thread(target=lambda: keyboard.add_hotkey(shortcut, on_shortcut))
thread.start()

root.mainloop()
