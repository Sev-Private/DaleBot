#!/usr/bin/env python3


import os
import locale
from datetime import datetime
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

def empty_counter():
    return {
        "Sev": 0,
        "João": 0,
        "Victor": 0,
        "Baby": 0,
        "Sand": 0,
    }

# Function to calculate the most and least suggestions
def calculate_suggestion_metrics(filtered_main_sheet):
    suggestion_counts = empty_counter()

    # Iterate over the filtered rows in the main sheet
    for row in filtered_main_sheet:
        suggester = row[3]  # Assuming "suggested by" is the 4th column (index 3)
        
        # Count suggestions for each suggester
        if suggester == "Thiago Augusto":
            suggestion_counts["Sev"] += 1
        elif suggester == "joaovictorcosta1997@gmail.com":
            suggestion_counts["João"] += 1
        elif suggester == "Victor Eduardo":
            suggestion_counts["Victor"] += 1
        elif suggester == "Gustavo Paes":
            suggestion_counts["Baby"] += 1
        elif suggester == "sand.dejesus@gmail.com":
            suggestion_counts["Sand"] += 1

    # Find most and least suggestions
    most_suggested_count = max(suggestion_counts.values())
    least_suggested_count = min(suggestion_counts.values())

    most_suggested = [person for person, count in suggestion_counts.items() if count == most_suggested_count]
    least_suggested = [person for person, count in suggestion_counts.items() if count == least_suggested_count]

    return suggestion_counts, most_suggested, least_suggested


# Function to calculate the most and least participation
def calculate_participation_metrics(filtered_participant_sheets):
    participation_counts = empty_counter()

    # Iterate through each participant's filtered sheet and count non-blank ratings
    for participant in filtered_participant_sheets:
        participant_csv = participant["csv"]
        rows = participant_csv.split("\n")
        
        # Assuming movie names are in the first column, ratings are in the second column (index 1)
        for row in rows[1:]:  # Skip header
            columns = row.split(";")
            if len(columns) > 1 and columns[1].strip():  # Check if there is a rating (non-blank)
                if participant["name"] == "Sev":
                    participation_counts["Sev"] += 1
                elif participant["name"] == "João":
                    participation_counts["João"] += 1
                elif participant["name"] == "Victor":
                    participation_counts["Victor"] += 1
                elif participant["name"] == "Baby":
                    participation_counts["Baby"] += 1
                elif participant["name"] == "Sand":
                    participation_counts["Sand"] += 1

    # Find most and least participation
    most_participated_count = max(participation_counts.values())
    least_participated_count = min(participation_counts.values())

    most_participated = [person for person, count in participation_counts.items() if count == most_participated_count]
    least_participated = [person for person, count in participation_counts.items() if count == least_participated_count]

    return participation_counts, most_participated, least_participated

# Main function to preprocess and write details to the output file
def main():
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')  # This works in systems where Portuguese locale is available

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
    rows = main_csv.split("\n")
    
    # Filter the movies by the given year
    filtered_movies = []
    for row in rows[1:]:  # Skipping the header
        columns = row.split(";")
        if len(columns) > 2:  # Ensure there is a date column
            try:
                date_watched = datetime.strptime(columns[2], "%d/%b./%Y")  # Assuming date format is YYYY-MM-DD
                if date_watched.year == year:
                    filtered_movies.append(columns[0])  # Add movie name to the filtered list
            except ValueError:
                continue  # Skip if the date is invalid or in the wrong format
    # Filter the main sheet to only include the filtered movies
    filtered_main_sheet = []
    for row in rows[1:]:  # Skipping the header
        columns = row.split(";")
        if len(columns) > 0 and columns[0] in filtered_movies:
            filtered_main_sheet.append(columns)
    
    # Extract participant sheets
    participant_sheets = []
    for sheet in spreadsheet.worksheets()[1:]:
        participant_csv = export_to_csv(sheet)
        participant_name = sheet.title
        # Filter participant ratings based on the filtered movie list
        filtered_participant_ratings = []
        rows = participant_csv.split("\n")
        for row in rows[1:]:  # Skipping the header
            columns = row.split(";")
            if len(columns) > 1 and columns[0] in filtered_movies:  # Only consider ratings for filtered movies
                filtered_participant_ratings.append(row)
        
        participant_sheets.append({
            "name": participant_name,
            "csv": "\n".join(filtered_participant_ratings),
        })

    # Define the string which will be added to the final output
    formatted_file = "# Spreadsheet Processing Results\n\n"

    formatted_file += "## Suggestion and Participation Metrics\n\n"
    
    # Suggestion Metrics
    formatted_file += "### Most and Least Suggestions\n\n"
    formatted_file += "Suggestions per person:\n"
    suggestion_counts, most_suggested, least_suggested = calculate_suggestion_metrics(filtered_main_sheet)
    for person, count in suggestion_counts.items():
        formatted_file += f"- {person}: {count} suggestions\n"
    formatted_file += f"\n**Most Suggestions**: {most_suggested}\n"
    formatted_file += f"**Least Suggestions**: {least_suggested}\n\n"
    
    # Participation Metrics
    formatted_file += "### Most and Least Participation\n\n"
    formatted_file += "Participation per person:\n"
    participation_counts, most_participated, least_participated = calculate_participation_metrics(participant_sheets)
    for person, count in participation_counts.items():
        formatted_file += f"- {person}: {count} movies watched\n"
    formatted_file += f"\n**Most Participation**: {most_participated}\n"
    formatted_file += f"**Least Participation**: {least_participated}\n\n"

    # Define the output file name with the year
    output_file = f"analysis_results_{year}.md"

    # Write details to the output file
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, "w") as file:
        # Write final details in the file
        file.write(formatted_file)

    # Print message to indicate the results were saved
    print(f"Analysis complete for the year {year}. Results saved to {output_path}")

if __name__ == "__main__":
    main()
