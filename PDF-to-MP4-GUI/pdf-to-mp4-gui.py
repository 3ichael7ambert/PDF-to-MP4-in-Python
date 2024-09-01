import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from moviepy.editor import ImageSequenceClip
from PIL import Image

def select_pdf():
    pdf_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, pdf_path)

def select_output():
    output_path = filedialog.asksaveasfilename(
        title="Select Output MP4 File",
        defaultextension=".mp4",
        filetypes=[("MP4 Files", "*.mp4")])
    if output_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

def pdf_to_images(pdf_path, dpi):
    images = convert_from_path(pdf_path, dpi=dpi)
    return images

def create_video(images, output_path, duration, resolution):
    image_files = []
    for i, img in enumerate(images):
        img_path = f"page_{i+1}.png"
        img = img.resize(resolution, Image.ANTIALIAS)
        img.save(img_path)
        image_files.append(img_path)

    clip = ImageSequenceClip(image_files, fps=1/duration)
    clip.write_videofile(output_path, codec='libx264', fps=24)

def pdf_to_video():
    pdf_path = pdf_entry.get()
    output_path = output_entry.get()
    duration = int(duration_entry.get())
    resolution = (int(width_entry.get()), int(height_entry.get()))
    dpi = 200  # You can adjust the DPI as needed

    if not pdf_path or not output_path:
        messagebox.showerror("Error", "Please select both a PDF file and an output destination.")
        return

    images = pdf_to_images(pdf_path, dpi)
    create_video(images, output_path, duration, resolution)
    messagebox.showinfo("Success", "MP4 video has been created successfully!")

# Initialize the GUI window
root = tk.Tk()
root.title("PDF to MP4 Converter")

# PDF selection
tk.Label(root, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=5)
pdf_entry = tk.Entry(root, width=50)
pdf_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=5)

# Output selection
tk.Label(root, text="Select Output MP4 File:").grid(row=1, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output).grid(row=1, column=2, padx=10, pady=5)

# Duration per page
tk.Label(root, text="Seconds per Page:").grid(row=2, column=0, padx=10, pady=5)
duration_entry = tk.Entry(root, width=10)
duration_entry.grid(row=2, column=1, padx=10, pady=5)
duration_entry.insert(0, "5")  # Default value

# Resolution settings
tk.Label(root, text="Resolution (Width x Height):").grid(row=3, column=0, padx=10, pady=5)
width_entry = tk.Entry(root, width=10)
width_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
width_entry.insert(0, "1280")  # Default width

height_entry = tk.Entry(root, width=10)
height_entry.grid(row=3, column=1, padx=10, pady=5, sticky="e")
height_entry.insert(0, "720")  # Default height

# Convert button
tk.Button(root, text="Convert to MP4", command=pdf_to_video).grid(row=4, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
