import csv
import ebcdic

# Replace placeholders with your actual values
ebcdic_file_path = "path/to/your/ebcdic.file"
csv_file_path = "path/to/output.csv"
encoding = 'cp500'  # Adjust the encoding if needed

with open(ebcdic_file_path, 'rb') as infile, open(csv_file_path, 'w', newline='') as outfile:
    reader = ebcdic.reader(infile, encoding)
    writer = csv.writer(outfile)

    # Write header row (if you know the field names)
    writer.writerow(['field1', 'field2', ...]) 

    # Read and write data rows
    for record in reader:
        writer.writerow(record)
