import tkinter as tk
from PIL import Image, ImageTk
import psutil
import base64
import io


class BandwidthMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bandwidth Monitor")
        self.root.geometry("396x128")
        self.root.configure(bg="#2f2f2f")  

        self.main_frame = tk.Frame(root, bg="#2f2f2f", bd=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.main_frame, width=96, bg="#2f2f2f")
        self.image_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.load_image()

        self.text_frame = tk.Frame(self.main_frame, bg="#2f2f2f")
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create frames for "Up" and "Down" labels and values
        self.sent_frame = tk.Frame(self.text_frame, bg="#2f2f2f")
        self.sent_frame.pack(pady=5, padx=10, fill=tk.X)

        self.recv_frame = tk.Frame(self.text_frame, bg="#2f2f2f")
        self.recv_frame.pack(pady=5, padx=10, fill=tk.X)

        # Labels for "Up" and "Down" text
        self.label_sent_text = tk.Label(self.sent_frame, text=" Up ", font=("Courier New", 16), fg="lightblue", bg="#2f2f2f")
        self.label_sent_text.pack(side=tk.LEFT, anchor="w", pady=(8, 0))

        self.label_recv_text = tk.Label(self.recv_frame, text=" Down ", font=("Courier New", 16), fg="lightblue", bg="#2f2f2f")
        self.label_recv_text.pack(side=tk.LEFT, anchor="w", pady=(8, 0))

        self.label_sent_value = tk.Label(self.sent_frame, text="000.000 B/s", font=("Courier New", 16), fg="lightblue", bg="#2f2f2f")
        self.label_sent_value.pack(side=tk.LEFT, pady=(8, 0), padx=(29, 0))

        self.label_recv_value = tk.Label(self.recv_frame, text="000.000 B/s", font=("Courier New", 16), fg="lightblue", bg="#2f2f2f")
        self.label_recv_value.pack(side=tk.LEFT, pady=(8, 0), padx=(5, 0))

        # Initialize previous network I/O counters
        self.prev_net_io = psutil.net_io_counters()
        self.update_display()

    def load_image(self):
        try:
            image = Image.open(load_image_from_string(icon))
            image = image.resize((96, 96), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(image)
            self.img_label = tk.Label(self.image_frame, image=self.img, bg="#2f2f2f")
            self.img_label.pack(fill=tk.Y)
        except Exception as e:
            print(f"Error loading image: {e}")

    def format_bytes(self, bytes):
        if bytes < 1024:
            formatted = f"{bytes:.3f} By"
        elif bytes < 1024**2:
            formatted = f"{bytes / 1024:.3f} KB"
        elif bytes < 1024**3:
            formatted = f"{bytes / 1024**2:.3f} MB"
        else:
            formatted = f"{bytes / 1024**3:.3f} GB"

        # Ensure the formatted string has leading zeros and always 3 decimal places
        parts = formatted.split()
        number = parts[0].zfill(7)  # Ensure at least 7 characters with leading zeros
        unit = parts[1]

        return f"{number} {unit}/s"

    def calculate_bandwidth(self, prev, curr, interval):
        bytes_sent = curr.bytes_sent - prev.bytes_sent
        bytes_recv = curr.bytes_recv - prev.bytes_recv

        # Convert to bandwidth per second
        bandwidth_sent_per_sec = bytes_sent / interval
        bandwidth_recv_per_sec = bytes_recv / interval

        return bandwidth_sent_per_sec, bandwidth_recv_per_sec

    def update_display(self):
        interval = 0.5  

        curr_net_io = psutil.net_io_counters()

        bandwidth_sent_per_sec, bandwidth_recv_per_sec = self.calculate_bandwidth(self.prev_net_io, curr_net_io, interval)

        self.label_sent_value.config(text=self.format_bytes(bandwidth_sent_per_sec))
        self.label_recv_value.config(text=self.format_bytes(bandwidth_recv_per_sec))

        self.prev_net_io = curr_net_io

        self.root.after(int(interval * 1000), self.update_display)


icon = "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"


def load_image_from_string(image_string):
    image_data = base64.b64decode(image_string)
    return io.BytesIO(image_data)



if __name__ == "__main__":
    root = tk.Tk()
    app = BandwidthMonitorApp(root)
    root.mainloop()
