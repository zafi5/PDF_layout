import fitz  # PyMuPDF for PDF layout analysis
import pytesseract
from PIL import Image
import camelot


# Extract plain text from the PDF
def extract_text_from_pdf(pdf_path):
    """Extract plain text from the entire PDF."""
    doc = fitz.open(pdf_path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")  # Extract plain text
        all_text.append({
            "page_number": page_num + 1,
            "text": page_text.strip()  # Remove leading/trailing spaces
        })

    return all_text


# Extract tables from the PDF using Camelot
def extract_tables_from_pdf(pdf_path):
    """Extract tables from the PDF."""
    tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")  # Change to "lattice" if needed
    extracted_tables = []

    for idx, table in enumerate(tables):
        # Save table as CSV for reference
        csv_path = f"table_{idx + 1}.csv"
        table.to_csv(csv_path)
        extracted_tables.append({
            "table_number": idx + 1,
            "dataframe": table.df,  # Table as a DataFrame
            "csv_path": csv_path
        })

    return extracted_tables


# Extract images from the PDF and apply OCR (if required)
def extract_images_from_pdf(pdf_path):
    """Extract images and run OCR."""
    doc = fitz.open(pdf_path)
    extracted_images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]

            # Save the image to a file
            img_path = f"extracted_image_{page_num}_{img_index}.png"
            with open(img_path, "wb") as img_file:
                img_file.write(image_data)

            # Apply OCR to the image
            img = Image.open(img_path)
            ocr_text = pytesseract.image_to_string(img)
            extracted_images.append({
                "page_number": page_num + 1,
                "image_path": img_path,
                "ocr_text": ocr_text.strip()
            })

    return extracted_images


# Main function to process the PDF
def process_pdf(pdf_path):
    print("Extracting text from PDF...")
    extracted_text = extract_text_from_pdf(pdf_path)

    print("Extracting tables from PDF...")
    extracted_tables = extract_tables_from_pdf(pdf_path)

    print("Extracting images from PDF...")
    extracted_images = extract_images_from_pdf(pdf_path)

    # Display extracted content
    print("\n--- Extracted Text ---")
    for page_data in extracted_text:
        print(f"Page {page_data['page_number']}:\n{page_data['text']}\n")

    print("\n--- Extracted Tables ---")
    for table_data in extracted_tables:
        print(f"Table {table_data['table_number']}:\n{table_data['dataframe']}\n")
        print(f"Table CSV Path: {table_data['csv_path']}")

    print("\n--- Extracted Images and OCR ---")
    for image_data in extracted_images:
        print(f"Page {image_data['page_number']} - Image Path: {image_data['image_path']}")
        print(f"Text from Image:\n{image_data['ocr_text']}\n")


# Test the script with your PDF
pdf_path = ''  # Replace with the path to your PDF
process_pdf(pdf_path)
