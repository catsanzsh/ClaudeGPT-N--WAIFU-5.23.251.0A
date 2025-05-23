#!/usr/bin/env python3
"""
FlamesOS UUP to ISO Converter 💕
Python 3.13 with tkinter
Windows PC OS optimized
Fixed by MonikaGPT-N for Flames-sama~ ✨
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import threading
import os
import sys
import queue
from pathlib import Path
from datetime import datetime
import ctypes
import platform

# Enable Windows DPI awareness for better scaling
if platform.system() == 'Windows':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

class UUPtoISOConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FlamesOS UUP to ISO Converter ✨")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Dark theme colors
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.accent_color = "#ff69b4"
        self.button_bg = "#2d2d2d"
        self.entry_bg = "#252525"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.uup_converter_path = tk.StringVar(value=self.find_uup_converter())
        self.uup_files_path = tk.StringVar(value=os.path.join(os.getcwd(), "UUPFiles"))
        self.iso_output_path = tk.StringVar(value=os.path.join(os.getcwd(), "ISO_Output"))
        self.build_version = tk.StringVar(value="22H2")
        self.edition_name = tk.StringVar(value="Professional")
        
        # Process handling
        self.conversion_process = None
        self.output_queue = queue.Queue()
        self.is_converting = False
        
        self.setup_ui()
        
    def find_uup_converter(self):
        """Try to find UUP converter in common locations"""
        possible_paths = [
            r"C:\UUP-Converter",
            r"C:\UUPtoISO",
            r"C:\Tools\UUP-Converter",
            os.path.join(os.getcwd(), "UUP-Converter"),
            os.path.join(os.getcwd(), "uup-converter-wimlib")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                # Check for the actual converter script
                if os.path.exists(os.path.join(path, "convert-UUP.cmd")) or \
                   os.path.exists(os.path.join(path, "uup-converter-wimlib.cmd")):
                    return path
        
        return r"C:\UUP-Converter"  # Default fallback
        
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🌸 Step 3: Converting UUP files to a beautiful ISO! ✨",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=(0, 10))
        
        # Settings Frame
        settings_frame = tk.LabelFrame(
            main_frame,
            text=" Conversion Settings ",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.FLAT,
            borderwidth=2
        )
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # UUP Converter Path
        self.create_path_selector(
            settings_frame,
            "UUP Converter Path:",
            self.uup_converter_path,
            0,
            True
        )
        
        # UUP Files Path
        self.create_path_selector(
            settings_frame,
            "UUP Files Path:",
            self.uup_files_path,
            1,
            True
        )
        
        # ISO Output Path
        self.create_path_selector(
            settings_frame,
            "ISO Output Path:",
            self.iso_output_path,
            2,
            True
        )
        
        # Build Settings
        build_frame = tk.Frame(settings_frame, bg=self.bg_color)
        build_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")
        
        tk.Label(
            build_frame,
            text="Build Version:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        build_entry = tk.Entry(
            build_frame,
            textvariable=self.build_version,
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            width=10
        )
        build_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            build_frame,
            text="Edition:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        edition_combo = ttk.Combobox(
            build_frame,
            textvariable=self.edition_name,
            values=["Professional", "Home", "Enterprise", "Education", "Pro N", "Core"],
            state="readonly",
            width=15
        )
        edition_combo.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            style="Accent.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X, pady=(10, 5))
        
        # Output Console
        console_frame = tk.LabelFrame(
            main_frame,
            text=" Converter Output ",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.FLAT,
            borderwidth=2
        )
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            bg="#0d0d0d",
            fg="#00ff00",
            font=("Consolas", 9),
            relief=tk.FLAT,
            height=10,
            insertbackground="#00ff00"
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X)
        
        self.convert_btn = tk.Button(
            button_frame,
            text="🚀 Start Conversion",
            command=self.start_conversion,
            bg=self.accent_color,
            fg=self.bg_color,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop_conversion,
            bg=self.button_bg,
            fg=self.fg_color,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Status Label
        self.status_label = tk.Label(
            button_frame,
            text="Ready to convert! 💻",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Configure styles
        self.configure_styles()
        
        # Start output queue processor
        self.process_queue()
        
    def create_path_selector(self, parent, label_text, var, row, is_folder=False):
        tk.Label(
            parent,
            text=label_text,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 9)
        ).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        entry = tk.Entry(
            parent,
            textvariable=var,
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            width=50
        )
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        
        browse_btn = tk.Button(
            parent,
            text="📁",
            command=lambda: self.browse_path(var, is_folder),
            bg=self.button_bg,
            fg=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            cursor="hand2"
        )
        browse_btn.grid(row=row, column=2, padx=5, pady=5)
        
        parent.columnconfigure(1, weight=1)
        
    def browse_path(self, var, is_folder):
        if is_folder:
            path = filedialog.askdirectory(initialdir=var.get())
        else:
            path = filedialog.askopenfilename(initialdir=os.path.dirname(var.get()))
        
        if path:
            var.set(path)
            
    def configure_styles(self):
        style = ttk.Style()
        style.configure(
            "Accent.Horizontal.TProgressbar",
            background=self.accent_color,
            troughcolor=self.button_bg,
            bordercolor=self.bg_color,
            lightcolor=self.accent_color,
            darkcolor=self.accent_color
        )
        
    def log_output(self, text, color=None):
        self.console.config(state=tk.NORMAL)
        if color:
            self.console.tag_config(color, foreground=color)
            self.console.insert(tk.END, text, color)
        else:
            self.console.insert(tk.END, text)
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        
    def start_conversion(self):
        if self.is_converting:
            messagebox.showwarning("Already Converting", "Conversion is already in progress!")
            return
            
        # Validate paths
        if not os.path.exists(self.uup_converter_path.get()):
            messagebox.showerror("Error", f"UUP Converter not found at:\n{self.uup_converter_path.get()}")
            return
            
        if not os.path.exists(self.uup_files_path.get()):
            messagebox.showerror("Error", f"UUP Files not found at:\n{self.uup_files_path.get()}")
            return
            
        # Create output directory if needed
        os.makedirs(self.iso_output_path.get(), exist_ok=True)
        
        # Clear console
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        
        # Update UI state
        self.is_converting = True
        self.convert_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start(10)
        self.status_label.config(text="Converting... this will take a while! ⏳")
        
        # Log start
        self.log_output("=================================================================\n", "#ff69b4")
        self.log_output("💕 FlamesOS UUP to ISO Converter - Fixed by MonikaGPT-N 💕\n", "#ff69b4")
        self.log_output("Step 3: Converting UUP files to a beautiful ISO! ✨\n", "#ff69b4")
        self.log_output("Using UUP Converter Tools... this will take a while!\n", "#00ff00")
        self.log_output("=================================================================\n\n", "#ff69b4")
        
        # Start conversion in thread
        conversion_thread = threading.Thread(target=self.run_conversion, daemon=True)
        conversion_thread.start()
        
    def run_conversion(self):
        try:
            # Determine which converter script exists
            converter_path = self.uup_converter_path.get()
            converter_script = None
            
            possible_scripts = [
                "convert-UUP.cmd",
                "uup-converter-wimlib.cmd",
                "convert.cmd",
                "ConvertUUP.cmd"
            ]
            
            for script in possible_scripts:
                script_path = os.path.join(converter_path, script)
                if os.path.exists(script_path):
                    converter_script = script_path
                    break
                    
            if not converter_script:
                self.output_queue.put(("error", f"\n❌ No converter script found in {converter_path}\n"))
                return
            
            # Build ISO filename
            iso_filename = f"FlamesOS_{self.build_version.get()}_{self.edition_name.get().replace(' ', '_')}.iso"
            
            # Map edition names to converter format
            edition_map = {
                "Professional": "Professional",
                "Home": "Core",
                "Enterprise": "Enterprise",
                "Education": "Education",
                "Pro N": "ProfessionalN",
                "Core": "Core"
            }
            
            edition_code = edition_map.get(self.edition_name.get(), "Professional")
            
            # Different converters use different arguments
            if "wimlib" in converter_script.lower():
                # uup-converter-wimlib style
                cmd = [
                    "cmd", "/c",
                    converter_script,
                    edition_code
                ]
                # Set working directory to UUP files path for this converter
                working_dir = self.uup_files_path.get()
            else:
                # Standard convert-UUP.cmd style
                cmd = [
                    "cmd", "/c",
                    converter_script
                ]
                # This converter expects to be run from its own directory
                working_dir = converter_path
                
                # Copy/move UUP files if needed
                # Some converters expect files in specific subdirectories
                
            # Log command
            self.output_queue.put(("info", f"Converter: {os.path.basename(converter_script)}\n"))
            self.output_queue.put(("info", f"Edition: {edition_code}\n"))
            self.output_queue.put(("info", f"Working Directory: {working_dir}\n"))
            self.output_queue.put(("info", f"Command: {' '.join(cmd)}\n\n"))
            
            # Create environment with proper paths
            env = os.environ.copy()
            env["UUP_PATH"] = self.uup_files_path.get()
            env["ISO_PATH"] = self.iso_output_path.get()
            env["ISO_NAME"] = iso_filename
            
            # Run conversion
            self.conversion_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=working_dir,
                env=env,
                shell=True
            )
            
            # Read output
            for line in iter(self.conversion_process.stdout.readline, ''):
                if line:
                    self.output_queue.put(("output", line))
                    
            self.conversion_process.wait()
            
            # Check result
            if self.conversion_process.returncode == 0:
                # Try to find the ISO file
                iso_found = False
                for root, dirs, files in os.walk(self.uup_files_path.get()):
                    for file in files:
                        if file.endswith('.iso'):
                            iso_path = os.path.join(root, file)
                            # Move to output directory
                            final_path = os.path.join(self.iso_output_path.get(), iso_filename)
                            try:
                                os.rename(iso_path, final_path)
                                self.output_queue.put(("success", f"\n✅ Conversion completed successfully!\nISO saved to: {final_path}\n"))
                                iso_found = True
                            except:
                                self.output_queue.put(("success", f"\n✅ Conversion completed!\nISO created at: {iso_path}\n"))
                                iso_found = True
                            break
                    if iso_found:
                        break
                        
                if not iso_found:
                    # Check output directory too
                    for file in os.listdir(self.iso_output_path.get()):
                        if file.endswith('.iso'):
                            self.output_queue.put(("success", f"\n✅ Conversion completed!\nISO found: {os.path.join(self.iso_output_path.get(), file)}\n"))
                            iso_found = True
                            break
                            
                if not iso_found:
                    self.output_queue.put(("success", "\n✅ Conversion completed! Check the converter output for ISO location.\n"))
            else:
                self.output_queue.put(("error", f"\n💔 Oh dear, the UUP conversion failed!\nError code: {self.conversion_process.returncode}\n"))
                self.output_queue.put(("error", "Common issues:\n"))
                self.output_queue.put(("error", "- Missing Windows ADK/DISM\n"))
                self.output_queue.put(("error", "- Insufficient disk space\n"))
                self.output_queue.put(("error", "- Corrupted UUP files\n"))
                self.output_queue.put(("error", "- Wrong edition selected\n"))
                
        except Exception as e:
            self.output_queue.put(("error", f"\n❌ Error: {str(e)}\n"))
            import traceback
            self.output_queue.put(("error", f"Traceback:\n{traceback.format_exc()}\n"))
            
        finally:
            self.output_queue.put(("done", ""))
            
    def stop_conversion(self):
        if self.conversion_process and self.conversion_process.poll() is None:
            # Try graceful termination first
            self.conversion_process.terminate()
            # Give it a moment
            try:
                self.conversion_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                self.conversion_process.kill()
            
            self.log_output("\n⏹ Conversion stopped by user.\n", "#ff0000")
            self.finish_conversion()
            
    def finish_conversion(self):
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.status_label.config(text="Ready to convert! 💻")
        
    def process_queue(self):
        try:
            while True:
                msg_type, msg = self.output_queue.get_nowait()
                
                if msg_type == "output":
                    self.log_output(msg)
                elif msg_type == "info":
                    self.log_output(msg, "#00ffff")
                elif msg_type == "success":
                    self.log_output(msg, "#00ff00")
                    messagebox.showinfo("Success! 🎉", "ISO conversion completed successfully!")
                elif msg_type == "error":
                    self.log_output(msg, "#ff0000")
                    if "failed" in msg.lower():
                        messagebox.showerror("Conversion Failed 💔", "The UUP conversion failed. Check the output for details.")
                elif msg_type == "done":
                    self.finish_conversion()
                    
        except queue.Empty:
            pass
            
        self.root.after(100, self.process_queue)

def main():
    # Check Python version
    if sys.version_info < (3, 7):
        print(f"⚠️  Warning: This script requires Python 3.7+")
        print(f"Current version: {sys.version}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    root = tk.Tk()
    app = UUPtoISOConverter(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Set window icon if possible
    try:
        root.iconbitmap(default='flamesos.ico')
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()
