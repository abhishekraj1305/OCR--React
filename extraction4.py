import fitz  # PyMuPDF
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text() + "\n"
    return text.strip()

def parse_virdi_trucking_text(extracted_text):
    data = {
        "Company Name": "Virdi Trucking",
        "Address": "",
        "Phone": "",
        "Ticket Number": "",
        "Container Number": "",
        "Shipment ID": "",
        "Order Type": "",
        "S/S Line": "",
        "Vehicle Size": "",
        "Equipment Type": "",
        "Pickup Location": "",
        "Pickup Address": "",
        "Delivery Location": "",
        "Delivery Address": "",
        "Vessel Voyage, POP, Last Free Day": "Information not provided",
        "Weight": "Not provided",
        "Contents": "TBA",
        "ETA": "Not provided",
        "RV#": "Not provided",
        "RV Time": "TBA"
    }

    lines = extracted_text.split("\n")
    
    in_pickup_location = False
    in_delivery_location = False

    for i, line in enumerate(lines):
        line = line.strip()

        if "Dispatch Ticket" in line:
            match = re.search(r"Dispatch Ticket\s*[-:]\s*(.*)", line)
            if match:
                data["Ticket Number"] = match.group(1).strip()

        elif "Container Number" in line:
            match = re.search(r"Container Number\s*[-:]\s*(.*)", line)
            if match:
                data["Container Number"] = match.group(1).strip()

        elif "Shipment ID" in line:
            match = re.search(r"Shipment ID\s*[-:]\s*(.*)", line)
            if match:
                data["Shipment ID"] = match.group(1).strip()

        elif "Order Type" in line:
            match = re.search(r"Order Type\s*[-:]\s*(.*)", line)
            if match:
                data["Order Type"] = match.group(1).strip()

        elif "S/S Line" in line:
            match = re.search(r"S/S Line\s*[-:]\s*(.*)", line)
            if match:
                data["S/S Line"] = match.group(1).strip()

        elif "Vehicle Size" in line:
            match = re.search(r"Vehicle Size\s*[-:]\s*(.*)", line)
            if match:
                data["Vehicle Size"] = match.group(1).strip()

        elif "Equipment Type" in line:
            match = re.search(r"Equipment Type\s*[-:]\s*(.*)", line)
            if match:
                data["Equipment Type"] = match.group(1).strip()

        elif "Phone" in line:
            match = re.search(r"Phone\s*[-:]\s*(.*)", line)
            if match:
                data["Phone"] = match.group(1).strip()

        # Handle Pickup Location and Address
        if "Pickup" in line and "Location" in line:
            in_pickup_location = True
            data["Pickup Location"] = line.split("Location")[-1].strip()

        elif in_pickup_location and "Address" in line:
            data["Pickup Address"] = line.replace("Address -", "").strip()
            in_pickup_location = False

        elif in_pickup_location and "Delivery" not in line:
            data["Pickup Location"] += " " + line.strip()

        # Handle Delivery Location and Address
        if "Delivery" in line and "Location" in line:
            in_delivery_location = True
            data["Delivery Location"] = line.split("Location")[-1].strip()

        elif in_delivery_location and "Address" in line:
            data["Delivery Address"] = line.replace("Address -", "").strip()
            in_delivery_location = False

        elif in_delivery_location and not re.match(r"(Pickup|Vessel|Weight|Contents|ETA|RV#|RV Time)", line):
            data["Delivery Location"] += " " + line.strip()

    # Clean up any leading/trailing whitespace
    for key in data.keys():
        data[key] = data[key].strip()

    return data

# Path to the PDF file
pdf_path = "C:\\Users\\Abhishek Raj\\Downloads\\Virdi Trucking Ticket .pdf"

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Print the extracted text
print("Extracted Text:\n")
print(extracted_text)
print("\n" + "="*50 + "\n")

# Parse the text to extract specific information
parsed_data = parse_virdi_trucking_text(extracted_text)

# Print the parsed data
print("Parsed Data:\n")
for key, value in parsed_data.items():
    print(f"{key}: {value}")
print("\n" + "="*50 + "\n")

# Convert the parsed data into a DataFrame
df = pd.DataFrame([parsed_data])

# Save the DataFrame to an Excel file
output_path = "Virdi_Trucking_Ticket_Info.xlsx"
df.to_excel(output_path, index=False)

# Display the DataFrame
print("DataFrame:\n")
print(df)

print(f"\nData saved to {output_path}")
