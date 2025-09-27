import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import threading
import os
import time
from urllib.parse import urlparse
import math
from datetime import datetime, timedelta
import shutil

class ModernDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast File Downloader Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#2c3e50')
        
        self.downloading = False
        self.current_download = None
        self.start_time = None
        self.downloaded_size = 0
        self.total_size = 0
        self.current_file = None
        
        self.setup_modern_ui()
        
    def setup_modern_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, text="FAST DOWNLOADER PRO", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#34495e')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Version info
        version_label = tk.Label(header_frame, text="v2.1", 
                               font=('Arial', 10), fg='#bdc3c7', bg='#34495e')
        version_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Download Section
        download_section = self.create_download_section(main_container)
        download_section.pack(fill=tk.X, pady=(0, 15))
        
        # Progress Section
        progress_section = self.create_progress_section(main_container)
        progress_section.pack(fill=tk.X, pady=(0, 15))
        
        # Stats Section
        stats_section = self.create_stats_section(main_container)
        stats_section.pack(fill=tk.X, pady=(0, 15))
        
        # Control Buttons
        control_section = self.create_control_section(main_container)
        control_section.pack(fill=tk.X, pady=(0, 15))
        
        # History Section
        history_section = self.create_history_section(main_container)
        history_section.pack(fill=tk.BOTH, expand=True)
        
        # Set default download directory
        self.dest_entry.insert(0, os.path.expanduser("~/Downloads"))
        
    def create_download_section(self, parent):
        frame = tk.LabelFrame(parent, text="DOWNLOAD DETAILS", font=('Arial', 10, 'bold'),
                             fg='#ecf0f1', bg='#34495e', bd=2, relief=tk.GROOVE)
        
        # URL Input
        url_frame = tk.Frame(frame, bg='#34495e')
        url_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(url_frame, text="Download URL:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.url_entry = tk.Entry(url_frame, font=('Arial', 9), width=60, bd=2, relief=tk.SOLID)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Destination
        dest_frame = tk.Frame(frame, bg='#34495e')
        dest_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(dest_frame, text="Save to:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.dest_entry = tk.Entry(dest_frame, font=('Arial', 9), bd=2, relief=tk.SOLID)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        
        self.browse_btn = tk.Button(dest_frame, text="📁 Browse", font=('Arial', 9),
                                   command=self.browse_directory, bg='#3498db', fg='white',
                                   relief=tk.RAISED, bd=2)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Filename
        filename_frame = tk.Frame(frame, bg='#34495e')
        filename_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(filename_frame, text="Filename:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.filename_entry = tk.Entry(filename_frame, font=('Arial', 9), bd=2, relief=tk.SOLID)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        return frame
    
    def create_progress_section(self, parent):
        frame = tk.LabelFrame(parent, text="DOWNLOAD PROGRESS", font=('Arial', 10, 'bold'),
                             fg='#ecf0f1', bg='#34495e', bd=2, relief=tk.GROOVE)
        
        # Progress bar with percentage
        self.progress_bar = ttk.Progressbar(frame, mode='determinate', length=800)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=15)
        
        # Progress text
        self.progress_label = tk.Label(frame, text="Ready to download", font=('Arial', 10),
                                      fg='#ecf0f1', bg='#34495e')
        self.progress_label.pack(pady=(0, 10))
        
        return frame
    
    def create_stats_section(self, parent):
        frame = tk.LabelFrame(parent, text="DOWNLOAD STATISTICS", font=('Arial', 10, 'bold'),
                             fg='#ecf0f1', bg='#34495e', bd=2, relief=tk.GROOVE)
        
        stats_grid = tk.Frame(frame, bg='#34495e')
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Speed
        tk.Label(stats_grid, text="Download Speed:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        self.speed_label = tk.Label(stats_grid, text="0 MB/s", font=('Arial', 9),
                                   fg='#2ecc71', bg='#34495e')
        self.speed_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 40))
        
        # Time remaining
        tk.Label(stats_grid, text="Time Remaining:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        self.time_label = tk.Label(stats_grid, text="Calculating...", font=('Arial', 9),
                                  fg='#e74c3c', bg='#34495e')
        self.time_label.grid(row=0, column=3, sticky=tk.W, padx=(0, 40))
        
        # Downloaded size
        tk.Label(stats_grid, text="Downloaded:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        self.downloaded_label = tk.Label(stats_grid, text="0 MB", font=('Arial', 9),
                                       fg='#3498db', bg='#34495e')
        self.downloaded_label.grid(row=1, column=1, sticky=tk.W, padx=(0, 40))
        
        # Total size
        tk.Label(stats_grid, text="Total Size:", font=('Arial', 9, 'bold'),
                fg='#ecf0f1', bg='#34495e').grid(row=1, column=2, sticky=tk.W, padx=(0, 20))
        self.total_label = tk.Label(stats_grid, text="0 MB", font=('Arial', 9),
                                  fg='#f39c12', bg='#34495e')
        self.total_label.grid(row=1, column=3, sticky=tk.W)
        
        return frame
    
    def create_control_section(self, parent):
        frame = tk.Frame(parent, bg='#2c3e50')
        
        button_style = {'font': ('Arial', 10, 'bold'), 'width': 12, 'height': 2, 
                       'relief': tk.RAISED, 'bd': 3}
        
        self.download_btn = tk.Button(frame, text="🚀 START", command=self.start_download,
                                     bg='#27ae60', fg='white', **button_style)
        self.download_btn.pack(side=tk.LEFT, padx=10)
        
        self.pause_btn = tk.Button(frame, text="⏸️ PAUSE", command=self.pause_download,
                                  bg='#f39c12', fg='white', state=tk.DISABLED, **button_style)
        self.pause_btn.pack(side=tk.LEFT, padx=10)
        
        self.cancel_btn = tk.Button(frame, text="❌ CANCEL", command=self.cancel_download,
                                   bg='#e74c3c', fg='white', **button_style)
        self.cancel_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = tk.Button(frame, text="🧹 CLEAR", command=self.clear_history,
                                  bg='#95a5a6', fg='white', **button_style)
        self.clear_btn.pack(side=tk.RIGHT, padx=10)
        
        return frame
    
    def create_history_section(self, parent):
        frame = tk.LabelFrame(parent, text="DOWNLOAD HISTORY", font=('Arial', 10, 'bold'),
                             fg='#ecf0f1', bg='#34495e', bd=2, relief=tk.GROOVE)
        
        # Create a text widget with scrollbar for history
        text_frame = tk.Frame(frame, bg='#34495e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(text_frame, height=8, width=80,
                                                     font=('Consolas', 9), bg='#2c3e50',
                                                     fg='#ecf0f1', insertbackground='white')
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Add welcome message to history
        welcome_msg = f"{'='*50}\n"
        welcome_msg += "FAST DOWNLOADER PRO - Download History\n"
        welcome_msg += f"{'='*50}\n"
        welcome_msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Application started\n\n"
        self.history_text.insert(tk.END, welcome_msg)
        self.history_text.config(state=tk.DISABLED)
        
        return frame
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, directory)
    
    def get_filename_from_url(self, url):
        parsed = urlparse(url)
        path = parsed.path
        filename = os.path.basename(path)
        return filename if filename else "downloaded_file"
    
    def validate_inputs(self):
        url = self.url_entry.get().strip()
        destination = self.dest_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a download URL")
            return False
        
        if not destination:
            messagebox.showerror("Error", "Please select a destination directory")
            return False
        
        # Fix path separator issue
        destination = destination.replace('/', '\\')
        
        if not os.path.exists(destination):
            try:
                os.makedirs(destination)
            except OSError:
                messagebox.showerror("Error", "Cannot create destination directory")
                return False
        
        return True
    
    def safe_file_rename(self, src, dst, max_retries=5, delay=1):
        """Safely rename file with retry mechanism"""
        for attempt in range(max_retries):
            try:
                # First try direct rename
                os.rename(src, dst)
                return True
            except PermissionError:
                # If rename fails, try copy + delete
                try:
                    shutil.copy2(src, dst)
                    os.remove(src)
                    return True
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
            except OSError as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay)
        return False
    
    def calculate_time_remaining(self, downloaded, total, speed):
        if speed <= 0 or total <= 0:
            return "Calculating..."
        
        remaining_bytes = total - downloaded
        seconds_remaining = remaining_bytes / speed
        
        if seconds_remaining < 60:
            return f"{int(seconds_remaining)} seconds"
        elif seconds_remaining < 3600:
            return f"{int(seconds_remaining // 60)} min {int(seconds_remaining % 60)} sec"
        else:
            hours = int(seconds_remaining // 3600)
            minutes = int((seconds_remaining % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def format_speed(self, bytes_per_sec):
        if bytes_per_sec == 0:
            return "0 B/s"
        size_names = ["B/s", "KB/s", "MB/s", "GB/s"]
        i = int(math.floor(math.log(bytes_per_sec, 1024)))
        p = math.pow(1024, i)
        s = round(bytes_per_sec / p, 2)
        return f"{s} {size_names[i]}"
    
    def start_download(self):
        if not self.validate_inputs():
            return
            
        if self.downloading:
            messagebox.showwarning("Warning", "A download is already in progress")
            return
        
        self.downloading = True
        self.start_time = time.time()
        self.downloaded_size = 0
        
        self.download_btn.config(state=tk.DISABLED, bg='#7f8c8d')
        self.pause_btn.config(state=tk.NORMAL, bg='#e67e22')
        
        # Reset progress
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Starting download...")
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_file)
        thread.daemon = True
        thread.start()
    
    def pause_download(self):
        if self.downloading:
            self.downloading = False
            self.pause_btn.config(text="▶️ RESUME", bg='#27ae60')
            self.progress_label.config(text="Download paused")
            # Close the file handle if it's open
            if hasattr(self, 'current_file') and self.current_file:
                try:
                    self.current_file.close()
                except:
                    pass
        else:
            self.downloading = True
            self.pause_btn.config(text="⏸️ PAUSE", bg='#e67e22')
            self.start_time = time.time() - (self.downloaded_size / max(self.get_current_speed(), 1))
            thread = threading.Thread(target=self.download_file)
            thread.daemon = True
            thread.start()
    
    def get_current_speed(self):
        if self.start_time and self.downloaded_size > 0:
            elapsed = time.time() - self.start_time
            return self.downloaded_size / elapsed if elapsed > 0 else 0
        return 0
    
    def cancel_download(self):
        self.downloading = False
        self.current_download = None
        
        # Close file handle if open
        if hasattr(self, 'current_file') and self.current_file:
            try:
                self.current_file.close()
            except:
                pass
        
        self.download_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ PAUSE", bg='#f39c12')
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Download cancelled")
        self.speed_label.config(text="0 B/s")
        self.time_label.config(text="--")
        self.downloaded_label.config(text="0 B")
        self.total_label.config(text="0 B")
    
    def clear_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] History cleared\n")
        self.history_text.config(state=tk.DISABLED)
    
    def download_file(self):
        file_handle = None
        try:
            url = self.url_entry.get().strip()
            destination = self.dest_entry.get().strip().replace('/', '\\')
            custom_filename = self.filename_entry.get().strip()
            
            # Get filename
            if custom_filename:
                filename = custom_filename
            else:
                filename = self.get_filename_from_url(url)
            
            filepath = os.path.join(destination, filename)
            temp_filepath = filepath + '.part'
            
            # Check if file already exists
            if os.path.exists(filepath):
                response = messagebox.askyesno("File exists", 
                                             f"File '{filename}' already exists. Overwrite?")
                if not response:
                    self.root.after(0, self.cancel_download)
                    return
            
            # Start download
            headers = {}
            start_byte = 0
            
            # Check for partial download
            if os.path.exists(temp_filepath):
                start_byte = os.path.getsize(temp_filepath)
                headers = {'Range': f'bytes={start_byte}-'}
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            self.total_size = int(response.headers.get('content-length', 0)) + start_byte
            mode = 'ab' if start_byte > 0 else 'wb'
            
            # Open file with explicit closing
            file_handle = open(temp_filepath, mode)
            self.current_file = file_handle
            
            self.current_download = response
            self.downloaded_size = start_byte
            self.start_time = time.time()
            last_update = self.start_time
            
            for chunk in response.iter_content(chunk_size=8192):
                if not self.downloading:
                    break
                    
                if chunk:
                    file_handle.write(chunk)
                    file_handle.flush()  # Ensure data is written to disk
                    self.downloaded_size += len(chunk)
                    
                    current_time = time.time()
                    if current_time - last_update >= 0.1:  # Update UI every 100ms
                        # Calculate progress and statistics
                        progress = (self.downloaded_size / self.total_size * 100) if self.total_size > 0 else 0
                        elapsed_time = current_time - self.start_time
                        download_speed = self.downloaded_size / elapsed_time if elapsed_time > 0 else 0
                        time_remaining = self.calculate_time_remaining(
                            self.downloaded_size, self.total_size, download_speed
                        )
                        
                        # Update UI in main thread
                        self.root.after(0, self.update_progress, progress, 
                                      self.downloaded_size, self.total_size, 
                                      download_speed, time_remaining)
                        last_update = current_time
            
            # Close file handle before renaming
            if file_handle:
                file_handle.close()
                self.current_file = None
            
            if self.downloading and self.downloaded_size == self.total_size:
                # Download completed successfully - use safe rename
                if self.safe_file_rename(temp_filepath, filepath):
                    self.root.after(0, self.download_completed, filepath, self.downloaded_size)
                else:
                    self.root.after(0, self.download_error, "Failed to rename file after download")
            else:
                # Download was paused or cancelled
                if self.downloading:  # If paused, keep the partial file
                    self.root.after(0, self.download_paused)
                else:  # If cancelled, delete partial file
                    if os.path.exists(temp_filepath):
                        try:
                            os.remove(temp_filepath)
                        except:
                            pass
                    self.root.after(0, self.cancel_download)
                    
        except Exception as e:
            # Ensure file handle is closed on error
            if file_handle:
                try:
                    file_handle.close()
                    self.current_file = None
                except:
                    pass
            self.root.after(0, self.download_error, str(e))
    
    def update_progress(self, progress, downloaded, total, speed, time_remaining):
        self.progress_bar['value'] = progress
        
        # Update progress text
        if total > 0:
            percent = f"{progress:.1f}%"
            size_info = f"{self.format_size(downloaded)} / {self.format_size(total)}"
            self.progress_label.config(text=f"Downloading... {percent} - {size_info}")
        else:
            self.progress_label.config(text=f"Downloading... {self.format_size(downloaded)}")
        
        # Update statistics
        self.speed_label.config(text=self.format_speed(speed))
        self.time_label.config(text=time_remaining)
        self.downloaded_label.config(text=self.format_size(downloaded))
        self.total_label.config(text=self.format_size(total))
    
    def download_completed(self, filepath, size):
        self.downloading = False
        self.current_download = None
        self.current_file = None
        
        self.download_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ PAUSE", bg='#f39c12')
        self.progress_bar['value'] = 100
        self.progress_label.config(text="✅ Download completed successfully!")
        
        # Update final statistics
        elapsed = time.time() - self.start_time
        avg_speed = size / elapsed if elapsed > 0 else 0
        self.speed_label.config(text=f"{self.format_speed(avg_speed)} (avg)")
        self.time_label.config(text="Completed!")
        self.downloaded_label.config(text=self.format_size(size))
        
        # Add to history
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.history_text.config(state=tk.NORMAL)
        history_entry = f"[{timestamp}] ✅ {filename} ({self.format_size(size)}) - {self.format_speed(avg_speed)} avg\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        messagebox.showinfo("Success", 
                          f"✅ Download completed!\n\n"
                          f"File: {filename}\n"
                          f"Size: {self.format_size(size)}\n"
                          f"Time: {timedelta(seconds=int(elapsed))}\n"
                          f"Avg Speed: {self.format_speed(avg_speed)}")
    
    def download_paused(self):
        self.progress_label.config(text="⏸️ Download paused")
        self.time_label.config(text="Paused")
    
    def download_error(self, error_msg):
        self.downloading = False
        self.current_download = None
        self.current_file = None
        
        self.download_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ PAUSE", bg='#f39c12')
        self.progress_bar['value'] = 0
        self.progress_label.config(text="❌ Download failed")
        
        # Add error to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"[{timestamp}] ❌ Download failed: {error_msg}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        messagebox.showerror("Download Error", f"❌ Download failed:\n{error_msg}")

def main():
    try:
        root = tk.Tk()
        app = ModernDownloader(root)
        
        # Set window to bring to front
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        
        root.mainloop()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()