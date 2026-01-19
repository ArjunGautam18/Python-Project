from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps

def main():
    window = Tk()
    window.title("Image Viewer")
    window.geometry("800x600")

    current_image = None
    original_image = None   # <-- stores original image

    # ---------------- Load Image ----------------
    def load_image():
        nonlocal current_image, original_image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            original_image = Image.open(file_path)
            current_image = original_image.copy()
            display_image(current_image)

    # ---------------- Apply Filters ----------------
    def apply_filter(filter_type):
        nonlocal current_image
        if current_image is None:
            return

        if filter_type == "grayscale":
            filtered_img = current_image.convert("L")

        elif filter_type == "sepia":
            gray = current_image.convert("L")
            filtered_img = ImageOps.colorize(gray, "#704214", "#C0A080")

        elif filter_type == "invert":
            filtered_img = ImageOps.invert(current_image.convert("RGB"))

        elif filter_type == "blur":
            filtered_img = current_image.filter(ImageFilter.BLUR)

        elif filter_type == "sharpen":
            filtered_img = current_image.filter(ImageFilter.SHARPEN)

        else:
            return

        current_image = filtered_img
        display_image(filtered_img)

    # ---------------- Revert Image ----------------
    def revert_image():
        nonlocal current_image
        if original_image is not None:
            current_image = original_image.copy()
            display_image(current_image)

    # ---------------- Display Image ----------------
    def display_image(img):
        img_copy = img.copy()
        img_copy.thumbnail((800, 500))
        tk_img = ImageTk.PhotoImage(img_copy)
        image_label.config(image=tk_img)
        image_label.image = tk_img

    # ---------------- GUI Components ----------------
    load_button = Button(window, text="Load Image", command=load_image)
    load_button.pack(pady=10)

    image_label = Label(window)
    image_label.pack(pady=10)

    Button(window, text="Grayscale", command=lambda: apply_filter("grayscale")).pack(side="left", padx=5)
    Button(window, text="Sepia", command=lambda: apply_filter("sepia")).pack(side="left", padx=5)
    Button(window, text="Invert", command=lambda: apply_filter("invert")).pack(side="left", padx=5)
    Button(window, text="Blur", command=lambda: apply_filter("blur")).pack(side="left", padx=5)
    Button(window, text="Sharpen", command=lambda: apply_filter("sharpen")).pack(side="left", padx=5)
    Button(window, text="Revert", command=revert_image).pack(side="left", padx=5)

    window.mainloop()

if __name__ == "__main__":
    main()
