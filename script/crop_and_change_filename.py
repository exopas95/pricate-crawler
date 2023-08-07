import os

from PIL import Image


def crop_image_center(img_path, save_path):
    try:
        image = Image.open(img_path)
        image = image.convert("RGB")

        width, height = image.size
        new_edge_length = min(width, height)

        # If the image is not square, crop it
        if width != height:
            left = (width - new_edge_length) / 2
            top = (height - new_edge_length) / 2
            right = (width + new_edge_length) / 2
            bottom = (height + new_edge_length) / 2

            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(save_path, "JPEG")
        else:
            image.save(save_path, "JPEG")

    except Exception as e:
        print(f"An error occurred while cropping image {img_path}: {e}")


# Path to the base directory
base_dir = "/Users/treenulbo/Downloads/NUGU_엣더룸_상품목록"

# Get a list of all subdirectories
subdirs = [
    os.path.join(base_dir, d)
    for d in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, d))
]

# Loop over all subdirectories
for subdir in subdirs:
    if "히피" in subdir:
        print("HERE")
    # Skip if directory is empty
    if not os.listdir(subdir):
        print(f"No images: {subdir}")
        continue

    # Process each file in the subdirectory
    print(f"Start cropping: {subdir}")

    files = sorted(os.listdir(subdir))
    main_found = False
    sub_count = 1

    # Check if any file contains 'main'
    for i, filename in enumerate(files):
        if "main" in filename:
            main_found = True
            break
    # If no file contains 'main', set the first file as 'main'
    if not main_found and files:
        os.rename(os.path.join(subdir, files[0]), os.path.join(subdir, "main.jpg"))
        files[0] = "main.jpg"

    for i, filename in enumerate(files):
        # Full path to the file
        filepath = os.path.join(subdir, filename)

        # Determine the new filename
        if "main" in filename:
            new_filename = "main.jpg"
        else:
            new_filename = f"sub_{sub_count}.jpg"
            sub_count += 1

        # Path where the cropped image will be saved
        save_path = os.path.join(subdir, new_filename)

        # Crop the image
        crop_image_center(filepath, save_path)
        if filepath != save_path:
            os.remove(filepath)
