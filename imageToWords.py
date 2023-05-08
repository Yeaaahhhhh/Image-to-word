import os
from tkinter import filedialog
from tkinter import *
from PIL import Image

ascii_char = list("!@#$%^&*()_+|:<>,./1234567890-=")


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (255.0 + 1) / length
    return ascii_char[int(gray / unit)]


def select_images():
    global images
    images = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg")])
    images_label.config(text=f"Selected images: {len(images)}")


def generate_text_image():
    width = width_entry.get() or 600
    height = height_entry.get() or 600

    for img_path in images:
        im = Image.open(img_path)
        im = im.resize((int(width), int(height)), Image.NEAREST)
        txt = ""
        for i in range(int(height)):
            for j in range(int(width)):
                txt += get_char(*im.getpixel((j, i)))
            txt += '\n'

        output_path = output_entry.get() or os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_path, os.path.splitext(os.path.basename(img_path))[0] + "_text_image.txt")

        with open(output_file, 'w') as f:
            f.write(txt)

        if see_text_var.get():
            os.startfile(output_file)


def save_text_image_path():
    output_path = filedialog.askdirectory()
    output_entry.delete(0, END)
    output_entry.insert(0, output_path)


# Create the GUI
root = Tk()
root.title("Text Image Generator")

# Select images button
select_button = Button(root, text="Select Images", command=select_images)
select_button.grid(row=0, column=0, pady=10)

images_label = Label(root, text="Selected images: 0")
images_label.grid(row=0, column=1)

width_label = Label(root, text="Width: ")
width_label.grid(row=1, column=0)
width_entry = Entry(root)
width_entry.grid(row=1, column=1)

height_label = Label(root, text="Height: ")
height_label.grid(row=2, column=0)
height_entry = Entry(root)
height_entry.grid(row=2, column=1)

output_button = Button(root, text="Save Text Image To", command=save_text_image_path)
output_button.grid(row=3, column=0)

output_entry = Entry(root)
output_entry.grid(row=3, column=1)

generate_button = Button(root, text="Generate Text Image", command=generate_text_image)
generate_button.grid(row=4, column=0, pady=10)

see_text_var = IntVar()
see_text_check = Checkbutton(root, text="See the text", variable=see_text_var)
see_text_check.grid(row=4, column=1)

root.mainloop()