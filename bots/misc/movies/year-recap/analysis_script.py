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

# def empty_counter(value):
#     # Check if the value is mutable (e.g., list, dict)
#     if isinstance(value, (list, dict, set)):  
#         # If it's mutable, create a new copy for each person
#         return {
#             "Sev": value.copy(),
#             "João": value.copy(),
#             "Victor": value.copy(),
#             "Baby": value.copy(),
#             "Sand": value.copy(),
#         }
#     else:
#         # If it's not mutable, just assign the value as is (e.g., 0)
#         return {
#             "Sev": value,
#             "João": value,
#             "Victor": value,
#             "Baby": value,
#             "Sand": value,
#         }

# Get the directory of the current script
def define_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def preprocess_spreadsheet(year, script_dir):
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
    participant_sheets = {}
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

        participant_sheets[participant_name] = {
            "names": set_participant_aliases(participant_name),
            "csv": "\n".join(filtered_participant_ratings),
        }
    
    return filtered_main_sheet, participant_sheets

def set_participant_aliases(sheet_title):
    # Map sheet title to suggester
    suggester_map = {
        "Sev": "Thiago Augusto",
        "João": "joaovictorcosta1997@gmail.com",
        "Victor": "Victor Eduardo",
        "Baby": "Gustavo Paes",
        "Sand": "sand.dejesus@gmail.com"
    }

    if sheet_title in suggester_map:
        suggester = suggester_map[sheet_title]
        return [sheet_title, suggester]
    return []
    
def initialize_config_and_return_arguments()
     # This works in systems where Portuguese locale is available
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8') 
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process spreadsheet and extract data.")
    parser.add_argument('year', type=int, help="The year for which to run the analysis")
    args = parser.parse_args()
    
    return args.year

def format_ouput_content():
    return "this is a new test"

def write_to_output_file(year, script_dir, content):
    # Define the output file name with the year
    output_file = f"analysis_results_{year}.md"

    # Write details to the output file
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, "w") as file:
        # Write final details in the file
        file.write(content)


# Main function to preprocess and write details to the output file
def main():    
    year = initialize_config_and_return_arguments()

    script_dir = define_script_dir()
    main_sheet, participants_sheet = preprocess_spreadsheet(year, script_dir)

    print(main_sheet)

    print(participant_sheets)

    content = format_ouput_content()

    write_to_output_file(year, script_dir, content)

    # # Define the string which will be added to the final output
    # formatted_file = "# Spreadsheet Processing Results\n\n"

    # # Section for Suggestion and Participation
    # formatted_file += "## Suggestion and Participation Metrics\n\n"
    
    # # Suggestion Metrics
    # formatted_file += "### Most and Least Suggestions\n\n"
    # formatted_file += "Suggestions per person:\n"
    # suggestion_counts, most_suggested, least_suggested, suggestion_movies = calculate_suggestion_metrics(filtered_main_sheet)
    # for person, count in suggestion_counts.items():
    #     formatted_file += f"- {person}: {count} suggestions\n"
    # formatted_file += f"\n**Most Suggestions**: {most_suggested}\n"
    # formatted_file += f"**Least Suggestions**: {least_suggested}\n\n"
    
    # # Participation Metrics
    # formatted_file += "### Most and Least Participation\n\n"
    # formatted_file += "Participation per person:\n"
    # participation_counts, most_participated, least_participated = calculate_participation_metrics(participant_sheets)
    # for person, count in participation_counts.items():
    #     formatted_file += f"- {person}: {count} movies watched\n"
    # formatted_file += f"\n**Most Participation**: {most_participated}\n"
    # formatted_file += f"**Least Participation**: {least_participated}\n\n"

    # # Section for Voting Patterns and Preferences
    # formatted_file += "## Voting Patterns and Preferences\n\n"

    # # Average Rating Metrics
    # formatted_file += "### Average Rating Given by Each Person for all movies\n\n"
    # average_ratings = calculate_average_ratings(participant_sheets)
    # for person, avg_rating in average_ratings.items():
    #     formatted_file += f"- {person}: {avg_rating:.2f} average rating\n"

    # # Average Rating for Suggested Movies
    # formatted_file += "\n### Average Rating for All Suggested Movies of each person\n\n"
    # average_ratings_for_suggested = calculate_average_rating_for_suggested_movies(participant_sheets, suggestion_movies)
    # for person, avg_rating in average_ratings_for_suggested.items():
    #     formatted_file += f"{person}: {avg_rating:.2f}\n"
    # formatted_file += "\n"

    # # Most Generous and Most Critical Viewers
    # formatted_file += "\n### Most Generous and Critical Viewers\n\n"
    # generosity, criticality, most_generous_viewer, most_critical_viewer = calculate_average_rating_given_to_suggested_movies(participant_sheets, suggestion_movies)
    # formatted_file += f"- **Most Generous Viewer**: {most_generous_viewer} ({generosity[most_generous_viewer]:.2f})\n"
    # formatted_file += f"- **Most Critical Viewer**: {most_critical_viewer} ({criticality[most_critical_viewer]:.2f})\n"

    # # Biased Ratings
    # formatted_file += "\n### Most Biased and Least Biased Viewers\n\n"
    # biased_ratings, most_biased_viewer, least_biased_viewer = calculate_biased_ratings(participant_sheets, suggestion_movies)
    # formatted_file += f"- **Most Biased Viewer**: {most_biased_viewer} ({biased_ratings[most_biased_viewer]:.2f})\n"
    # formatted_file += f"- **Least Biased Viewer**: {least_biased_viewer} ({biased_ratings[least_biased_viewer]:.2f})\n"

    # Print message to indicate the results were saved
    print(f"Analysis complete for the year {year}. Results saved to {output_path}")

if __name__ == "__main__":
    main()
