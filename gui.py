import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime

class SmartGlassGUI:
    def __init__(self, width=800, height=480):
        """Initialize GUI"""
        self.root = tk.Tk()
        self.root.title("Smart Glass - Live Captions")
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg='#1e1e1e')
        
        self.caption_history = []
        self.trigger_callback = None
        
        self._setup_ui()
        print("[GUI] Initialized")
    
    def _setup_ui(self):
        """Setup UI components"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2d2d2d', height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        title_label = tk.Label(
            header_frame,
            text="🎧 Smart Glass Live Captions",
            font=("Arial", 18, "bold"),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="● LISTENING",
            font=("Arial", 10),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.status_label.pack()
        
        # Current caption (large display)
        caption_frame = tk.Frame(self.root, bg='#1e1e1e')
        caption_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            caption_frame,
            text="Current Caption:",
            font=("Arial", 12),
            bg='#1e1e1e',
            fg='#888888'
        ).pack(anchor=tk.W)
        
        self.current_caption_text = tk.Text(
            caption_frame,
            font=("Arial", 16, "bold"),
            bg='#2d2d2d',
            fg='#ffffff',
            height=4,
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.current_caption_text.pack(fill=tk.BOTH, expand=True)
        
        # Caption history
        history_frame = tk.Frame(self.root, bg='#1e1e1e')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            history_frame,
            text="Caption History:",
            font=("Arial", 10),
            bg='#1e1e1e',
            fg='#888888'
        ).pack(anchor=tk.W)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=("Arial", 11),
            bg='#252525',
            fg='#cccccc',
            height=10,
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Alert log
        alert_frame = tk.Frame(self.root, bg='#1e1e1e')
        alert_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            alert_frame,
            text="🚨 Trigger Alerts:",
            font=("Arial", 10, "bold"),
            bg='#1e1e1e',
            fg='#ff6b6b'
        ).pack(anchor=tk.W)
        
        self.alert_text = tk.Text(
            alert_frame,
            font=("Arial", 10),
            bg='#2d2d2d',
            fg='#ff6b6b',
            height=3,
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.alert_text.pack(fill=tk.X)
    
    def update_caption(self, caption):
        """Update current caption display"""
        self.current_caption_text.delete(1.0, tk.END)
        self.current_caption_text.insert(1.0, caption)
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {caption}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        self.caption_history.append(caption)
    
    def show_alert(self, trigger_words):
        """Display alert when trigger detected"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        alert_msg = f"[{timestamp}] ALERT: Detected {', '.join(trigger_words)}\n"
        self.alert_text.insert(tk.END, alert_msg)
        self.alert_text.see(tk.END)
        
        # Flash status
        self.status_label.config(text="● ALERT!", fg='#ff0000')
        self.root.after(2000, lambda: self.status_label.config(
            text="● LISTENING", fg='#00ff00'
        ))
    
    def run(self):
        """Start GUI main loop"""
        self.root.mainloop()
    
    def update(self):
        """Process pending GUI updates (call periodically)"""
        self.root.update()
    
    def close(self):
        """Close GUI window"""
        self.root.destroy()
