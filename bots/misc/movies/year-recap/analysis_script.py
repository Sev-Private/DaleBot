#!/usr/bin/env python3


import os
import sys
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Define constants for the Google Sheets URL and credentials file
SHEET_URL = "https://docs.google.com/spreadsheets/d/1jnZHVMXvRCZFQDtwj-KazYPjniA-Vit8Rl0Z_sHHpRc/"  # Replace with your Google Sheets URL
CREDENTIALS_JSON = "my_credentials.json"  # Replace with the path to your credentials JSON file

# Function to authenticate and get the Google Sheets client
def authenticate_google_sheets(credentials_json):
    # Define the scope for Google Sheets and Google Drive API access
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    # Authenticate using the service account credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)
    
    return client

# Function to export a worksheet to a CSV string
def export_to_csv(worksheet):
    rows = worksheet.get_all_values()
    csv_data = "\n".join([";".join(row) for row in rows])
    return csv_data

# Main function to preprocess and write details to the output file
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process spreadsheet and extract data.")
    parser.add_argument('year', type=int, help="The year for which to run the analysis")
    args = parser.parse_args()
    
    year = args.year

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_json = os.path.join(script_dir, CREDENTIALS_JSON)

    # Authenticate and get the client
    client = authenticate_google_sheets(credentials_json)

    # Open the spreadsheet
    spreadsheet = client.open_by_url(SHEET_URL)
    
    # Extract the main file (first sheet)
    main_sheet = spreadsheet.get_worksheet(0)
    main_csv = export_to_csv(main_sheet)
    main_first_cell = main_sheet.cell(1, 1).value

    # Extract participant sheets
    participant_sheets = []
    for sheet in spreadsheet.worksheets()[1:]:
        participant_csv = export_to_csv(sheet)
        participant_name = sheet.title
        first_cell = sheet.cell(1, 1).value
        participant_sheets.append({
            "name": participant_name,
            "csv": participant_csv,
            "first_cell": first_cell
        })


    # Define the output file name with the year
    output_file = f"analysis_results_{year}.md"

    # Write details to the output file
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, "w") as file:
        file.write("# Spreadsheet Processing Results\n\n")
        file.write(f"## Main File\n\n")
        file.write(f"First cell: {main_first_cell}\n\n")
        file.write("## Participant Files\n\n")
        for participant in participant_sheets:
            file.write(f"Participant: {participant['name']}\n")
            file.write(f"First cell: {participant['first_cell']}\n\n")

    # Print message to indicate the results were saved
    print(f"Analysis complete for the year {year}. Results saved to {output_path}")

if __name__ == "__main__":
    main()
