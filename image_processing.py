# Import necessary libraries
from PIL import Image, ImageFilter, ImageTk
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Load Images
image_default = Image.open(r'images/ronaldo.jpg')
img_default_2 = cv2.imread('images/ronaldo.jpg')  # Load as color image

value = 7

# Max & Min filter
max_image = image_default.filter(ImageFilter.MaxFilter(size=value))
min_image = image_default.filter(ImageFilter.MinFilter(size=value))

# Image - Average processing
m, n, _ = img_default_2.shape
mk = np.ones([value, value], dtype=int) / (value * value)

img_gen = np.zeros([m, n, 3], dtype=np.uint8)
img_gen2 = img_gen.copy()

# Average Filter
for i in range(1, m - 1):
    for j in range(1, n - 1):
        for c in range(3):
            data = (
                img_default_2[i - 1, j - 1, c] * mk[0, 0] +
                img_default_2[i - 1, j, c] * mk[0, 1] +
                img_default_2[i - 1, j + 1, c] * mk[0, 2] +
                img_default_2[i, j - 1, c] * mk[1, 0] +
                img_default_2[i, j, c] * mk[1, 1] +
                img_default_2[i, j + 1, c] * mk[1, 2] +
                img_default_2[i + 1, j - 1, c] * mk[2, 0] +
                img_default_2[i + 1, j, c] * mk[2, 1] +
                img_default_2[i + 1, j + 1, c] * mk[2, 2]
            )
            img_gen[i, j, c] = data

# Median Filter
for i in range(1, m - 1):
    for j in range(1, n - 1):
        for c in range(3):
            data_v2 = [
                img_default_2[i - 1, j - 1, c],
                img_default_2[i - 1, j, c],
                img_default_2[i - 1, j + 1, c],
                img_default_2[i, j - 1, c],
                img_default_2[i, j, c],
                img_default_2[i, j + 1, c],
                img_default_2[i + 1, j - 1, c],
                img_default_2[i + 1, j, c],
                img_default_2[i + 1, j + 1, c]
            ]
            data_v2 = sorted(data_v2)
            img_gen2[i, j, c] = data_v2[4]

# Apply Median Blur and Gaussian Blur
median_blur_image = cv2.medianBlur(img_default_2, value)
gaussian_blur_image = cv2.GaussianBlur(img_default_2, (value, value), 0)

# Apply Laplacian Filter
laplacian_image = cv2.Laplacian(img_default_2, cv2.CV_64F)
laplacian_image = cv2.convertScaleAbs(laplacian_image)

# Apply Sobel Filter
sobel_x = cv2.Sobel(img_default_2, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(img_default_2, cv2.CV_64F, 0, 1, ksize=5)
sobel_image = cv2.sqrt(sobel_x ** 2 + sobel_y ** 2)
sobel_image = cv2.convertScaleAbs(sobel_image)


# Function to update the displayed image
def update_image(filter_type):
    filtered_img = None
    if filter_type == 'Max':
        filtered_img = max_image
    elif filter_type == 'Min':
        filtered_img = min_image
    elif filter_type == 'Average':
        filtered_img = cv2.cvtColor(img_gen, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)
    elif filter_type == 'Median':
        filtered_img = cv2.cvtColor(img_gen2, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)
    elif filter_type == 'Median Blur':
        filtered_img = cv2.cvtColor(median_blur_image, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)
    elif filter_type == 'Gaussian Blur':
        filtered_img = cv2.cvtColor(gaussian_blur_image, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)
    elif filter_type == 'Laplacian':
        filtered_img = cv2.cvtColor(laplacian_image, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)
    elif filter_type == 'Sobel':
        filtered_img = cv2.cvtColor(sobel_image, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_img)

    if filtered_img:
        filtered_img_tk = ImageTk.PhotoImage(filtered_img)
        filtered_label.config(image=filtered_img_tk)
        filtered_label.image = filtered_img_tk


# Create a GUI window using Tkinter
root = tk.Tk()
root.title("Image Filtering")

# Create frames for layout
frame_left = tk.Frame(root)
frame_right = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

# Original Image
original_img = Image.open(r'images/ronaldo.jpg')
original_img_tk = ImageTk.PhotoImage(original_img)
original_label = Label(frame_left, text="Original Image", font=("Helvetica", 12))
original_label.pack()
original_image_label = Label(frame_left, image=original_img_tk)
original_image_label.pack()

# Dropdown menu for filters
filter_options = ['Max', 'Min', 'Average', 'Median', 'Median Blur', 'Gaussian Blur', 'Laplacian', 'Sobel']
selected_filter = tk.StringVar(value="Max")
filter_dropdown = ttk.Combobox(frame_right, textvariable=selected_filter, values=filter_options, state="readonly")
filter_dropdown.pack()
filter_dropdown.bind("<<ComboboxSelected>>", lambda event: update_image(selected_filter.get()))
# Filtered Image
filtered_label = Label(frame_right)
filtered_label.pack()


# Default filter display
update_image("Max")

# Run the Tkinter event loop
root.mainloop()
