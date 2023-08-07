import os

from PIL import ImageOps, ImageChops, Image


def crop_image_center(img_path, save_path):
    try:
        image = Image.open(img_path)
        image = image.convert("RGB")

        # Convert image to grayscale
        gray_image = image.convert("L")

        # Get bounding box of non-white pixels
        bbox = gray_image.getbbox()

        # Crop the image to this bounding box
        image = image.crop(bbox)

        width, height = image.size
        new_edge_length = min(width, height)

        # Find the position of the white line
        for y in range(
            height // 2, height
        ):  # start from the center and go towards the bottom
            row = image.crop((0, y, width, y + 1))
            if all(pixel == (255, 255, 255) for pixel in list(row.getdata())):
                split_position = y
                break
        else:  # if no white line was found towards the bottom, search towards the top
            for y in range(
                height // 2, -1, -1
            ):  # start from the center and go towards the top
                row = image.crop((0, y, width, y + 1))
                if all(pixel == (255, 255, 255) for pixel in list(row.getdata())):
                    split_position = y
                    break
            else:
                split_position = None

        if split_position is not None:
            # If a white line was found, split the image into two parts
            top_image = image.crop((0, 0, width, split_position))
            bottom_image = image.crop((0, split_position, width, height))

            # Crop and save the top image
            crop_and_save(top_image, save_path.replace(".jpg", "_top.jpg"))

            # Crop and save the bottom image
            crop_and_save(bottom_image, save_path.replace(".jpg", "_bottom.jpg"))

        else:
            # If no white line was found, this is a single image
            left = (width - new_edge_length) / 2
            top = (height - new_edge_length) / 2
            right = (width + new_edge_length) / 2
            bottom = (height + new_edge_length) / 2

            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(save_path, "JPEG")

    except Exception as e:
        print(f"An error occurred while cropping image {img_path}: {e}")


def crop_and_save(image, save_path):
    image = trim(image)
    width, height = image.size
    new_edge_length = min(width, height)

    left = (width - new_edge_length) / 2
    top = (height - new_edge_length) / 2
    right = (width + new_edge_length) / 2
    bottom = (height + new_edge_length) / 2

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(save_path, "JPEG")


def trim(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))  # Create a new white background
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


# Path to the base directory
base_dir = "/Users/treenulbo/Downloads/attheroom"

# Get a list of all subdirectories
subdirs = [
    os.path.join(base_dir, d)
    for d in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, d))
]

# Loop over all subdirectories
for subdir in subdirs:
    # Skip if directory is empty
    if subdir == f"{base_dir}/3줄 진주 레이어드 목걸이 (2color)":
        if not os.listdir(subdir):
            print(f"No images: {subdir}")
            continue

        # Process each file in the subdirectory
        print(f"Start cropping: {subdir}")
        for filename in os.listdir(subdir):
            # Full path to the file
            filepath = os.path.join(subdir, filename)

            # If this is a cropped image, remove it
            if "cropped" in filename:
                os.remove(filepath)
                continue

            # Path where the cropped image will be saved
            base, ext = os.path.splitext(filepath)
            save_path = base + "_cropped" + ext

            # Crop the image
            crop_image_center(filepath, save_path)
