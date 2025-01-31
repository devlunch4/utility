import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def get_photo_date(image_path):
    """
    Extract the original photo capture date from image EXIF metadata.

    Args:
        image_path (str): Full path to the image file

    Returns:
        str or None: Formatted capture date if available, otherwise None

    Features:
    - Opens image using Pillow library
    - Retrieves EXIF metadata
    - Searches for 'DateTimeOriginal' tag
    - Handles potential errors during EXIF extraction
    """
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return value
    except Exception as e:
        print(f"Error reading EXIF data for {image_path}: {e}")
    return None


def organize_photos_by_date(input_folder_path):
    """
    Organize photo files into year-month folders based on their capture date.

    Args:
        input_folder_path (str): Root directory containing photo files

    Workflow:
    - Creates 'sorted-folder' and 'no-date' subdirectories
    - Recursively scans input folder for image files
    - Extracts photo capture date using EXIF metadata
    - Moves files to organized folders:
      * Files with date: Year-Month named folders
      * Files without date: 'no-date' folder

    Handling:
    - Skips hidden files and system files
    - Provides console output for file movements
    - Handles potential file movement errors
    """
    # Create sorted folder and no-date subfolder
    if not os.path.exists(save_sorted_folder):
        os.makedirs(save_sorted_folder)

    no_date_folder = os.path.join(save_sorted_folder, 'no-date')
    os.makedirs(no_date_folder, exist_ok=True)

    # Scan main folder, ignoring hidden and system folders
    for folder_name in os.listdir(input_folder_path):
        if folder_name.startswith('.') or folder_name == 'sorted-folder':
            continue

        folder_path = os.path.join(input_folder_path, folder_name)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.startswith('.'):
                    continue

                file_path = os.path.join(folder_path, filename)

                if os.path.isfile(file_path):
                    photo_date = get_photo_date(file_path)

                    if photo_date:
                        try:
                            date_obj = datetime.strptime(photo_date, '%Y:%m:%d %H:%M:%S')
                            year_month = date_obj.strftime('%Y-%m')
                        except ValueError:
                            continue

                        target_folder = os.path.join(save_sorted_folder, year_month)
                        os.makedirs(target_folder, exist_ok=True)

                        try:
                            shutil.move(file_path, os.path.join(target_folder, filename))
                            print(f"Moved {filename} to {target_folder}")
                        except Exception as e:
                            print(f"Error moving {filename}: {e}")
                    else:
                        try:
                            shutil.move(file_path, os.path.join(no_date_folder, filename))
                            print(f"Moved {filename} to {no_date_folder}")
                        except Exception as e:
                            print(f"Error moving {filename}: {e}")


# Configuration
main_folder = '/Users/michael/PycharmProjects/utility/temp'
save_sorted_folder = os.path.join(main_folder, 'sorted-folder')
os.makedirs(save_sorted_folder, exist_ok=True)

# Execution
organize_photos_by_date(main_folder)