"""
Advanced Random Password Generator - GUI Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(self.main_frame, text="🔐 Secure Password Generator", 
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        self.create_length_section()
        self.create_character_section()
        self.create_options_section()
        
        self.generate_button = ttk.Button(self.main_frame, text="Generate Password", 
                                         command=self.generate_password)
        self.generate_button.pack(pady=20)
        
        self.create_display_section()
        self.set_defaults()
    
    def create_length_section(self):
        length_frame = ttk.Frame(self.main_frame)
        length_frame.pack(pady=5, fill='x')
        
        ttk.Label(length_frame, text="Password Length:").pack(side='left')
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(length_frame, from_=4, to=32, 
                                     orient='horizontal', 
                                     variable=self.length_var,
                                     command=self.update_length_label)
        self.length_scale.pack(side='left', padx=10, fill='x', expand=True)
        
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side='left', padx=5)
    
    def create_character_section(self):
        char_frame = ttk.LabelFrame(self.main_frame, text="Character Types", padding="10")
        char_frame.pack(pady=10, fill='x')
        
        self.use_letters = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(char_frame, text="Letters (A-Z, a-z)", 
                       variable=self.use_letters).grid(row=0, column=0, sticky='w', pady=2)
        ttk.Checkbutton(char_frame, text="Numbers (0-9)", 
                       variable=self.use_numbers).grid(row=1, column=0, sticky='w', pady=2)
        ttk.Checkbutton(char_frame, text="Symbols (!@#$%^&*)", 
                       variable=self.use_symbols).grid(row=2, column=0, sticky='w', pady=2)
    
    def create_options_section(self):
        options_frame = ttk.LabelFrame(self.main_frame, text="Security Options", padding="10")
        options_frame.pack(pady=10, fill='x')
        
        self.check_strength = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Check password strength", 
                       variable=self.check_strength).pack(anchor='w')
        
        self.auto_copy = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-copy to clipboard", 
                       variable=self.auto_copy).pack(anchor='w')
        
        self.exclude_similar = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Exclude similar characters (i, l, 1, O, 0)", 
                       variable=self.exclude_similar).pack(anchor='w')
    
    def create_display_section(self):
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(pady=10, fill='x')
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(display_frame, textvariable=self.password_var, 
                                       font=('Courier', 14), state='readonly')
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.copy_button = ttk.Button(display_frame, text="📋 Copy", 
                                     command=self.copy_to_clipboard)
        self.copy_button.pack(side='right')
        
        self.strength_label = ttk.Label(self.main_frame, text="", font=('Arial', 10))
        self.strength_label.pack(pady=5)
    
    def set_defaults(self):
        self.update_length_label()
        self.generate_password()
    
    def update_length_label(self, *args):
        self.length_label.config(text=str(int(self.length_var.get())))
    
    def generate_password(self):
        length = int(self.length_var.get())
        use_letters = self.use_letters.get()
        use_numbers = self.use_numbers.get()
        use_symbols = self.use_symbols.get()
        exclude_similar = self.exclude_similar.get()
        
        if not (use_letters or use_numbers or use_symbols):
            messagebox.showwarning("Warning", "Please select at least one character type.")
            return
        
        characters = ""
        if use_letters:
            characters += string.ascii_letters
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation
        
        if exclude_similar:
            similar = "il1Lo0O"
            for char in similar:
                characters = characters.replace(char, "")
        
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        
        if self.check_strength.get():
            self.display_strength(password)
        else:
            self.strength_label.config(text="")
        
        if self.auto_copy.get():
            self.copy_to_clipboard()
    
    def check_password_strength(self, password):
        score = 0
        length = len(password)
        
        if length >= 16:
            score += 2
        elif length >= 12:
            score += 1
        
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        if has_lower and has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        if len(set(password)) >= len(password) * 0.7:
            score += 1
        
        if score >= 5:
            return score, "Strong Password ✓", "green"
        elif score >= 3:
            return score, "Moderate Password", "orange"
        else:
            return score, "Weak Password", "red"
    
    def display_strength(self, password):
        score, strength_text, color = self.check_password_strength(password)
        self.strength_label.config(text=f"Strength: {strength_text}", foreground=color)
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                self.copy_button.config(text="✓ Copied!")
                self.root.after(2000, lambda: self.copy_button.config(text="📋 Copy"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {e}")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()