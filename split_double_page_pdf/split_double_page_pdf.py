# Import necessary libraries
import io  # For handling binary data
import logging  # For logging events
import os  # For working with file paths and checking file existence
import tkinter as tk  # For creating the graphical user interface (GUI)
from tkinter import filedialog, messagebox  # For using file explorer and message boxes in the GUI

from PIL import Image  # For image processing
from PyPDF2 import PdfReader, PdfWriter  # For reading and writing PDF files

# Setting up logging to keep track of conversion progress and errors
log_file_path = os.path.join(os.getcwd(), "split_double_page_pdf.log")  # 현재 작업 디렉토리 경로 사용
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Log the start time of the application
logging.info("Application started")


def split_double_page_pdf(input_pdf_path, output_pdf_path, compression_quality):
    """
    Splits a double-page PDF into two separate single-page PDFs and compresses images to reduce file size.

    첫 페이지를 왼쪽과 오른쪽으로 나누어 두 개의 페이지로 분할하고, 이미지 압축하여 파일 크기를 줄이는 함수
    """
    try:
        reader = PdfReader(input_pdf_path)  # Read the input PDF
        writer = PdfWriter()  # Create a PdfWriter to write output PDF

        # Iterate through each page in the input PDF
        for page in reader.pages:
            pdf_page_image = page.images[0]  # Get the first image from the page
            image_data = io.BytesIO(pdf_page_image.data)  # Convert image data to a byte stream
            image = Image.open(image_data)  # Open image using PIL

            width, height = image.size  # Get the image dimensions
            left_page = image.crop((0, 0, width // 2, height))  # Crop the left half
            right_page = image.crop((width // 2, 0, width, height))  # Crop the right half

            # Compress images according to the user-specified quality percentage
            # 사용자 지정 품질 비율에 따라 이미지 압축
            compression_quality = min(max(compression_quality, 60), 100)  # Ensure quality is between 60 and 100
            left_page_io = io.BytesIO()
            right_page_io = io.BytesIO()

            # Save left and right images with compression
            left_page.save(left_page_io, format="JPEG", quality=compression_quality)
            left_page_io.seek(0)

            right_page.save(right_page_io, format="JPEG", quality=compression_quality)
            right_page_io.seek(0)

            # Convert the compressed images back to PDF
            left_pdf = io.BytesIO()
            right_pdf = io.BytesIO()
            left_page.save(left_pdf, format="PDF")
            right_page.save(right_pdf, format="PDF")

            # Add the left and right pages to the output PDF
            writer.add_page(PdfReader(left_pdf).pages[0])
            writer.add_page(PdfReader(right_pdf).pages[0])

        # Save the final split and compressed PDF to the output path
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        return True
    except Exception as e:
        print(e)  # Print any errors encountered
        return False


def select_input_file():
    """
    Opens a file dialog to select the input PDF file.
    """
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF files", "*.pdf")]
    )
    input_file_var.set(file_path)  # Update the input file path
    update_status()  # Update status label


def select_output_file():
    """
    Opens a file dialog to specify the output file path.
    """
    file_path = filedialog.asksaveasfilename(
        title="Save Output PDF As",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    output_file_var.set(file_path)  # Update the output file path
    update_status()  # Update status label


def start_conversion():
    """
    Starts the PDF conversion process, checking for valid input and output paths.
    """
    input_path = input_file_var.get()
    output_path = output_file_var.get()
    compression_quality = quality_var.get()  # Get the user's compression quality percentage

    # Validate input file path
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid input PDF file.")
        log_conversion(input_path, output_path, "Failed")
        return

    # Validate output file path
    if not output_path:
        messagebox.showerror("Error", "Please specify a valid output file path.")
        log_conversion(input_path, output_path, "Failed")
        return

    # Attempt to split the PDF and save it to the output path with the selected quality
    success = split_double_page_pdf(input_path, output_path, compression_quality)

    if success:
        status_label.config(bg="green", text="Conversion Successful!")
        messagebox.showinfo("Success", "PDF has been successfully split, compressed, and saved!")
        log_conversion(input_path, output_path, "Success")
    else:
        status_label.config(bg="red", text="Error during conversion.")
        messagebox.showerror("Error", "An error occurred during the conversion process.")
        log_conversion(input_path, output_path, "Failed")


def log_conversion(input_path, output_path, result):
    """
    Logs the result of each conversion attempt (success or failure).
    """
    logging.info(f"\n>Input Path:\n{input_path}\n>Output Path:\n{output_path}\n>Result:\n{result}\n---\n")


def update_status():
    """
    Updates the status label based on whether input and output files have been selected.
    """
    input_path = input_file_var.get()
    output_path = output_file_var.get()

    if not input_path and not output_path:
        status_label.config(bg="red", fg="black", text="File setup needed (Input and Output files required)")
    elif input_path and output_path:
        status_label.config(bg="yellow", fg="black", text="Files ready (Input and Output files set)")
    else:
        status_label.config(bg="red", fg="black", text="File setup needed (Both files required)")


def reset_fields():
    """
    Resets all fields and labels to their initial state.
    """
    input_file_var.set("")  # Clear input file path
    output_file_var.set("")  # Clear output file path
    quality_var.set(100)  # Reset compression quality to 100%
    status_label.config(bg="red", text="File setup needed (Input and Output files required)")  # Reset status


# GUI initialization
root = tk.Tk()
root.title("Split_double_page_pdf")
root.geometry("500x500")

# Status label showing the current state of input and output files
status_label = tk.Label(root, text="File setup needed", width=40, height=2, bg="red", fg="white", anchor="w")
status_label.pack(pady=10, padx=10)

# Input file selection UI
input_file_var = tk.StringVar()
tk.Label(root, text="Input PDF File:").pack(anchor="w", padx=10, pady=5)
tk.Entry(root, textvariable=input_file_var, width=50).pack(anchor="w", padx=10)
tk.Button(root, text="Browse", command=select_input_file).pack(anchor="w", padx=10, pady=5)

# Output file path specification UI
output_file_var = tk.StringVar()
tk.Label(root, text="Output PDF File:").pack(anchor="w", padx=10, pady=5)
tk.Entry(root, textvariable=output_file_var, width=50).pack(anchor="w", padx=10)
tk.Button(root, text="Save As", command=select_output_file).pack(anchor="w", padx=10, pady=5)

# Quality selection UI (for compression) using Scale (slider)
quality_var = tk.IntVar(value=100)
tk.Label(root, text="Compression Quality (%):").pack(anchor="w", padx=10, pady=5)

quality_slider = tk.Scale(root, from_=50, to=100, orient="horizontal", variable=quality_var)
quality_slider.pack(anchor="w", padx=10, pady=5)

# Start conversion button
(tk.Button(root, text="Start Conversion", command=start_conversion, bg="lightblue", fg="black")
 .pack(side="right", padx=10, pady=5))

# Reset button (Initial 상태로 복원)
tk.Button(root, text="Reset", command=reset_fields, bg="lightcoral", fg="black").pack(side="right", padx=10, pady=5)

# Run the GUI
root.mainloop()

# Log the end time of the application
logging.info("Application ended")
