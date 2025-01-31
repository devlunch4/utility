import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_photo_dates(set_folder_path):
    """
    Extract and print taken or creation date for image files in a folder.

    Args:
        set_folder_path (str): Path to the image folder
    """
    # Supported image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.heic', '.raw']

    # Iterate through all files in the folder
    for filename in os.listdir(set_folder_path):
        # Create full file path
        filepath = os.path.join(set_folder_path, filename)

        # Check if file is an image
        if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in image_extensions:
            try:
                # Extract image metadata
                image = Image.open(filepath)
                exif_data = image._getexif()

                date_found = False
                if exif_data:
                    # Search for original photo date in EXIF data
                    for tag_id, value in exif_data.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        if tag_name == 'DateTimeOriginal':
                            print(f"File: {filename}, Photo Date: {value}")
                            date_found = True
                            break

                # Use file creation date if no EXIF date
                if not date_found:
                    creation_time = os.path.getctime(filepath)
                    formatted_time = datetime.fromtimestamp(creation_time).strftime('%Y:%m:%d %H:%M:%S')
                    print(f"File: {filename}, Creation Date: {formatted_time}")

            except Exception as e:
                print(f"File: {filename}, Error: {e}")


# Usage
folder_path = '/path/to/your/photo/folder'
get_photo_dates(folder_path)