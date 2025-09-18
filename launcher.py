# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import subprocess
import atexit

# Try to import PIL for image handling, but continue without it if not available
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL/Pillow not installed. Image display will be limited.")

class YugiohLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Yu-Gi-Oh! ONLINE 2 Launcher")
        
        # Configuration file path
        self.config_file = "launcher_config.json"
        
        # Set up proper exit handling
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        atexit.register(self.cleanup)
        
        # Set window icon for main window
        self.set_window_icon(self.root)
        
        # Set fixed window size to 500x500 and center it
        window_width = 500
        window_height = 500
        self.root.geometry(f"{window_width}x{window_height}")
        self.center_window(self.root)
        self.root.resizable(False, False)
        
        # Load or create default configuration
        self.load_config()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header image or text
        self.setup_header(main_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Launch button
        self.launch_btn = ttk.Button(button_frame, text="Launch Game", 
                                    command=self.launch_game, width=20)
        self.launch_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Options button
        self.options_btn = ttk.Button(button_frame, text="Options", 
                                     command=self.show_options, width=20)
        self.options_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Exit button
        self.exit_btn = ttk.Button(button_frame, text="Exit", 
                                  command=self.exit_app, width=20)
        self.exit_btn.grid(row=2, column=0, padx=10, pady=10)
        
        # Available options
        self.resolutions = ["640x480", "800x600", "1024x768", "1280x960", "1600x1200"]
        self.languages = ["English", "German", "French", "Italian"]
        
        # Initially hide options
        self.options_visible = False
        
        # Track if we're exiting
        self.exiting = False
        
    def center_window(self, window):
        """Center the window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"+{x}+{y}")
        
    def load_config(self):
        """Load configuration from JSON file or create default"""
        default_config = {
            "resolution": "800x600",
            "fullscreen": False,
            "language": "English",
            "last_launch": None
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                # Ensure all required keys exist
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = default_config
            
        # Set variables from config
        self.resolution_var = tk.StringVar(value=self.config["resolution"])
        self.fullscreen_var = tk.BooleanVar(value=self.config["fullscreen"])
        self.language_var = tk.StringVar(value=self.config["language"])
        
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            # Update config with current values
            self.config.update({
                "resolution": self.resolution_var.get(),
                "fullscreen": self.fullscreen_var.get(),
                "language": self.language_var.get(),
                "last_launch": self.get_current_timestamp()
            })
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
                
        except Exception as e:
            print(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Could not save configuration: {e}")
    
    def get_current_timestamp(self):
        """Get current timestamp for last launch"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def set_window_icon(self, window):
        """Set the window icon with error handling"""
        icon_paths = [
            os.path.join("export", "data", "yo2.ico"),
            os.path.join("data", "yo2.ico"),
            "yo2.ico",
            # Fallback paths if the above don't exist
            os.path.join("export", "data", "icon.ico"),
            os.path.join("data", "icon.ico"),
            "icon.ico"
        ]
        
        icon_set = False
        for icon_path in icon_paths:
            try:
                if os.path.exists(icon_path):
                    window.iconbitmap(icon_path)
                    icon_set = True
                    print(f"Icon set from: {icon_path}")
                    break
            except Exception as e:
                print(f"Could not set icon from {icon_path}: {e}")
                continue
        
        if not icon_set:
            print("Warning: No suitable icon file found")
    
    def setup_header(self, parent_frame):
        """Setup the header image or text with error handling"""
        try:
            # Try multiple possible image paths
            image_paths = [
                os.path.join("export", "data", "title", "title_title_01_e.png"),
                os.path.join("data", "title", "title_title_01_e.png"),
                os.path.join("title_title_01_e.png")
            ]
            
            image_found = False
            for image_path in image_paths:
                if os.path.exists(image_path) and HAS_PIL:
                    img = Image.open(image_path)
                    # Resize to fit the window (smaller for 500x500 window)
                    target_width = 400  # Reduced from 450 to fit better
                    width_percent = target_width / float(img.size[0])
                    target_height = int(float(img.size[1]) * float(width_percent))
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    self.header_img = ImageTk.PhotoImage(img)
                    
                    header_label = ttk.Label(parent_frame, image=self.header_img)
                    header_label.pack(pady=(0, 15))  # Reduced padding
                    image_found = True
                    break
            
            if not image_found:
                # Fallback to text
                header_label = ttk.Label(parent_frame, text="YU-GI-OH! ONLINE 2", 
                                        font=('Arial', 18, 'bold'))  # Smaller font
                header_label.pack(pady=(15, 15))
                
        except Exception as e:
            print(f"Error setting up header: {e}")
            # Fallback to text
            header_label = ttk.Label(parent_frame, text="YU-GI-OH! ONLINE 2", 
                                    font=('Arial', 18, 'bold'))  # Smaller font
            header_label.pack(pady=(15, 15))
    
    def launch_game(self):
        """Launch the game executable with configured settings"""
        try:
            # Save configuration before launch
            self.save_config()
            
            # Prepare game arguments based on configuration
            game_args = []
            
            # Add resolution argument if configured
            if self.resolution_var.get() != "800x600":  # Default
                resolution = self.resolution_var.get()
                game_args.extend(["--resolution", resolution])
            
            # Add fullscreen argument if configured
            if self.fullscreen_var.get():
                game_args.append("--fullscreen")
            
            # Add language argument if configured
            if self.language_var.get() != "English":  # Default
                language = self.language_var.get().lower()
                game_args.extend(["--language", language])
            
            # Try multiple possible game executable paths
            game_paths = [
                os.path.join("game.exe"),
                os.path.join("yu-gi-oh.exe"),
                os.path.join("bin", "game.exe")
            ]
            
            game_found = False
            for game_path in game_paths:
                if os.path.exists(game_path):
                    # Launch the game with arguments
                    full_command = [game_path] + game_args
                    print(f"Launching: {' '.join(full_command)}")
                    subprocess.Popen(full_command)
                    game_found = True
                    break
            
            if not game_found:
                messagebox.showinfo("Launch", "Game executable not found. Please make sure the game is installed.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch game: {e}")
    
    def show_options(self):
        """Show the options dialog"""
        if self.options_visible:
            self.hide_options()
            return
            
        self.options_visible = True
        
        # Create a top-level window for options
        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Options")
        self.options_window.geometry("300x280")
        self.options_window.resizable(False, False)
        self.options_window.transient(self.root)
        self.options_window.grab_set()
        
        # Set icon for options window
        self.set_window_icon(self.options_window)
        
        # Center the options window
        self.center_window(self.options_window)
        
        # Options frame
        options_frame = ttk.Frame(self.options_window, padding="20")
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Resolution selection
        ttk.Label(options_frame, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=5)
        resolution_combo = ttk.Combobox(options_frame, textvariable=self.resolution_var, 
                                       values=self.resolutions, state="readonly", width=15)
        resolution_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Fullscreen option
        fullscreen_check = ttk.Checkbutton(options_frame, text="Fullscreen", 
                                          variable=self.fullscreen_var)
        fullscreen_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Language selection
        ttk.Label(options_frame, text="Language:").grid(row=2, column=0, sticky=tk.W, pady=5)
        language_combo = ttk.Combobox(options_frame, textvariable=self.language_var, 
                                     values=self.languages, state="readonly", width=15)
        language_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(options_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Save and Cancel buttons
        ttk.Button(button_frame, text="Save", command=self.save_options).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.hide_options).pack(side=tk.LEFT, padx=10)
        
        # Handle window close
        self.options_window.protocol("WM_DELETE_WINDOW", self.hide_options)
        
    def hide_options(self):
        """Hide the options dialog"""
        self.options_visible = False
        if hasattr(self, 'options_window'):
            self.options_window.destroy()
        
    def save_options(self):
        """Save the selected options"""
        self.save_config()
        messagebox.showinfo("Options Saved", 
                           f"Settings saved:\n"
                           f"Resolution: {self.resolution_var.get()}\n"
                           f"Fullscreen: {self.fullscreen_var.get()}\n"
                           f"Language: {self.language_var.get()}")
        self.hide_options()
    
    def cleanup(self):
        """Cleanup function to ensure proper exit"""
        if not self.exiting:
            self.exiting = True
            try:
                if hasattr(self, 'options_window') and self.options_window:
                    self.options_window.destroy()
            except:
                pass
                
    def exit_app(self):
        """Exit the application"""
        if not self.exiting:
            self.exiting = True
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.cleanup()
                self.root.quit()
                self.root.destroy()
                sys.exit(0)

def main():
    """Main function"""
    root = tk.Tk()
    app = YugiohLauncher(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.cleanup()
        sys.exit(0)
    finally:
        # Force exit to prevent reopening
        os._exit(0)

if __name__ == "__main__":
    main()