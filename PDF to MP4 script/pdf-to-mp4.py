from pdf2image import convert_from_path
from moviepy.editor import ImageSequenceClip

# Convert PDF pages to images
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

# Create an MP4 video from the images
def create_video(images, output_path, duration=5):
    # Convert images to file paths
    image_files = []
    for i, img in enumerate(images):
        img_path = f"page_{i+1}.png"
        img.save(img_path)
        image_files.append(img_path)

    # Create the video
    clip = ImageSequenceClip(image_files, fps=1/duration)
    clip.write_videofile(output_path, codec='libx264', fps=24)

# Main function
def pdf_to_video(pdf_path, output_path, duration=5):
    images = pdf_to_images(pdf_path)
    create_video(images, output_path, duration)

# How to use
pdf_path = "input.pdf"
output_path = "output.mp4"
pdf_to_video(pdf_path, output_path)
