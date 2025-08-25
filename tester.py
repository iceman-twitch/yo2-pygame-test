import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
import sys

class TestScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Test Script Launcher")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        # Get all Python files in the current directory
        self.python_files = self.find_python_files()
        
        if not self.python_files:
            self.show_no_scripts_message()
            return
            
        self.setup_ui()
        
    def find_python_files(self):
        """Find all Python files in the current directory"""
        python_files = []
        for file in os.listdir('.'):
            if file.endswith('.py') and file != os.path.basename(__file__):
                python_files.append(file)
        return sorted(python_files)
    
    def show_no_scripts_message(self):
        """Display message when no Python scripts are found"""
        message_frame = tk.Frame(self.root, bg="#f0f0f0")
        message_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        label = tk.Label(
            message_frame, 
            text="No Python scripts found in the current directory!",
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="#ff0000"
        )
        label.pack(pady=20)
        
        instruction = tk.Label(
            message_frame,
            text="Please place your Python scripts (e.g., main.py, mouse.py) in the same directory as this launcher.",
            font=("Arial", 12),
            bg="#f0f0f0",
            wraplength=500
        )
        instruction.pack(pady=10)
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Python Script Launcher", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Script selection frame
        selection_frame = tk.Frame(main_frame, bg="#f0f0f0")
        selection_frame.pack(fill='x', pady=(0, 15))
        
        script_label = tk.Label(
            selection_frame, 
            text="Select Script:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        script_label.pack(side='left', padx=(0, 10))
        
        # Combobox for script selection
        self.script_var = tk.StringVar()
        self.script_combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.script_var,
            values=self.python_files,
            state="readonly",
            width=30,
            height=15
        )
        self.script_combo.pack(side='left', fill='x', expand=True)
        self.script_combo.current(0)  # Set default selection
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill='x', pady=15)
        
        # Start button
        self.start_button = tk.Button(
            button_frame, 
            text="Launch Script",
            command=self.start_selected_script,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat"
        )
        self.start_button.pack(pady=5)
        
        # Output area
        output_label = tk.Label(
            main_frame, 
            text="Output:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        output_label.pack(anchor='w', pady=(10, 5))
        
        # Text widget for output with border
        output_frame = tk.Frame(main_frame, bg="#cccccc", padx=1, pady=1)
        output_frame.pack(expand=True, fill='both')
        
        self.output_text = tk.Text(
            output_frame, 
            height=15, 
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#333333",
            fg="#00ff00",
            insertbackground="white",
            selectbackground="#555555"
        )
        self.output_text.pack(expand=True, fill='both')
        
        # Scrollbar for output text
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#e0e0e0",
            fg="#333333",
            font=("Arial", 10)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure button hover effects
        self.setup_button_hover()
    
    def setup_button_hover(self):
        # Configure button hover effects
        self.start_button.bind("<Enter>", lambda e: self.start_button.configure(bg="#45a049"))
        self.start_button.bind("<Leave>", lambda e: self.start_button.configure(bg="#4CAF50"))
    
    def start_selected_script(self):
        """Start the selected test script in a separate thread"""
        selected_script = self.script_combo.get()
        
        if not selected_script:
            self.append_output("Error: No script selected!")
            return
        
        # Disable button during execution
        self.start_button.config(state=tk.DISABLED, bg="#cccccc")
        self.status_var.set(f"Running {selected_script}...")
        
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        
        # Run script in separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_script, args=(selected_script,))
        thread.daemon = True
        thread.start()
    
    def run_script(self, script_file):
        """Execute the test script and capture output"""
        try:
            # Check if script file exists
            if not os.path.exists(script_file):
                self.append_output(f"Error: Script file '{script_file}' not found!")
                self.update_button_state(True)
                self.status_var.set("Error: Script file not found")
                return
            
            # Execute the script
            self.append_output(f"Starting {script_file}...\n")
            self.append_output("=" * 60 + "\n")
            
            # Set up the process with real-time output capture
            process = subprocess.Popen(
                [sys.executable, script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output in real-time
            for line in iter(process.stdout.readline, ''):
                self.append_output(line)
            
            # Wait for process to complete and get return code
            return_code = process.wait()
            
            self.append_output("\n" + "=" * 60 + "\n")
            if return_code == 0:
                self.append_output(f"\n{script_file} completed successfully!")
                self.status_var.set(f"{script_file} completed successfully")
            else:
                self.append_output(f"\n{script_file} exited with code {return_code}")
                self.status_var.set(f"{script_file} exited with code {return_code}")
                
        except Exception as e:
            self.append_output(f"Error executing script: {str(e)}")
            self.status_var.set("Execution error")
        finally:
            self.update_button_state(True)
    
    def append_output(self, text):
        """Append text to the output area (thread-safe)"""
        def update_text():
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, text)
            self.output_text.see(tk.END)  # Auto-scroll to bottom
            self.output_text.config(state=tk.NORMAL)
        
        # Use thread-safe GUI update
        self.root.after(0, update_text)
    
    def update_button_state(self, enabled):
        """Update button state (thread-safe)"""
        def update_state():
            if enabled:
                self.start_button.config(state=tk.NORMAL, bg="#4CAF50")
            else:
                self.start_button.config(state=tk.DISABLED, bg="#cccccc")
        
        self.root.after(0, update_state)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestScriptLauncher(root)
    root.mainloop()