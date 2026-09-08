import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
from datetime import datetime
import pyperclip

class JokeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Generator 😂")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#00d4ff"
        self.card_bg = "#16213e"
        self.button_bg = "#0f3460"
        
        self.root.configure(bg=self.bg_color)
        
        # API URLs
        self.joke_api_url = "https://api.jokes.one/joke"
        self.random_joke_url = "https://official-joke-api.appspot.com/random_joke"
        
        self.current_joke = None
        
        # Create UI
        self.create_ui()
        
        # Load first joke
        self.root.after(500, self.get_joke)
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="😂 Joke Generator 😂",
            font=("Segoe UI", 32, "bold"),
            bg=self.accent_color,
            fg="#000000"
        )
        title.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Joke display frame
        self.joke_frame = tk.Frame(
            content_frame,
            bg=self.card_bg,
            relief=tk.FLAT,
            bd=2
        )
        self.joke_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Joke display text
        self.joke_text = tk.Label(
            self.joke_frame,
            text="Loading joke...",
            font=("Segoe UI", 16),
            bg=self.card_bg,
            fg=self.fg_color,
            justify=tk.CENTER,
            wraplength=800,
            padx=30,
            pady=60
        )
        self.joke_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # New Joke Button
        new_btn = tk.Button(
            button_frame,
            text="🎲 New Joke",
            command=self.get_joke,
            bg=self.accent_color,
            fg="#000000",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=12
        )
        new_btn.pack(side=tk.LEFT, padx=10)
        
        # Copy Button
        copy_btn = tk.Button(
            button_frame,
            text="📋 Copy",
            command=self.copy_joke,
            bg=self.button_bg,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=12
        )
        copy_btn.pack(side=tk.LEFT, padx=10)
        
        # Share Button
        share_btn = tk.Button(
            button_frame,
            text="📤 Share",
            command=self.share_joke,
            bg=self.button_bg,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=12
        )
        share_btn.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to laugh!",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.status_label.pack(pady=5)
        
    def get_joke(self):
        """Fetch a random joke"""
        def fetch():
            try:
                self.status_label.config(text="⏳ Loading joke...")
                self.root.update()
                
                # Use official-joke-api
                response = requests.get(self.random_joke_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Format joke
                    setup = data.get('setup', '')
                    punchline = data.get('punchline', '')
                    joke_text = f"{setup}\n\n{punchline}"
                    
                    self.current_joke = joke_text
                    self.joke_text.config(text=joke_text)
                    self.status_label.config(text="✓ Haha! 😂")
                else:
                    self.status_label.config(text="✗ Failed to load joke")
                    messagebox.showerror("Error", "Could not fetch joke")
                    
            except requests.exceptions.Timeout:
                self.status_label.config(text="✗ Connection timeout")
                messagebox.showerror("Error", "Connection timeout. Check internet!")
            except Exception as e:
                self.status_label.config(text="✗ Error occurred")
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()
        
    def copy_joke(self):
        """Copy joke to clipboard"""
        if self.current_joke:
            try:
                pyperclip.copy(self.current_joke)
                messagebox.showinfo("Success", "Joke copied to clipboard! 📋")
                self.status_label.config(text="✓ Copied to clipboard!")
            except:
                messagebox.showinfo("Copy", "Joke: " + self.current_joke)
        else:
            messagebox.showwarning("Warning", "No joke to copy")
            
    def share_joke(self):
        """Share joke"""
        if self.current_joke:
            message = f"😂 Check this joke:\n\n{self.current_joke}\n\nGenerated by Joke Generator"
            messagebox.showinfo("Share", message)
            self.status_label.config(text="✓ Share this with friends!")
        else:
            messagebox.showwarning("Warning", "No joke to share")

def main():
    root = tk.Tk()
    app = JokeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
