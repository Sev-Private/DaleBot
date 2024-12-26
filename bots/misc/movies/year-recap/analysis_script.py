#!/usr/bin/env python3


import os
import locale
from datetime import datetime
import sys
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import pprint

# Define constants for the Google Sheets URL and credentials file
SHEET_URL = "https://docs.google.com/spreadsheets/d/1jnZHVMXvRCZFQDtwj-KazYPjniA-Vit8Rl0Z_sHHpRc/"  # Replace with your Google Sheets URL
CREDENTIALS_JSON = "my_credentials.json"  # Replace with the path to your credentials JSON file

def initialize_config_and_return_arguments():
     # This works in systems where Portuguese locale is available
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 
    locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process spreadsheet and extract data.")
    parser.add_argument('year', type=int, help="The year for which to run the analysis")
    args = parser.parse_args()
    
    return args.year

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

def format_print(data):
    pp = pprint.PrettyPrinter(indent=4, width=100)
    pp.pprint(data)

# Get the directory of the current script
def define_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def set_participant_aliases(suggester):
    # Map suggester to sheet_title
    suggester_map = {
        "Thiago Augusto": "Sev",
        "joaovictorcosta1997@gmail.com": "João",
        "Victor Eduardo": "Victor",
        "Gustavo Paes": "Baby",
        "sand.dejesus@gmail.com": "Sand"
    }

    if suggester in suggester_map:
        return suggester_map[suggester]
    return ""

def write_to_output_file(year, script_dir, content):
    # Define the output file name with the year
    output_file = f"analysis_results_{year}.md"

    # Write details to the output file
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, "w") as file:
        # Write final details in the file
        file.write(content)
    
    return output_path

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

    # Filter the movies by the given year and add to filtered main list
    filtered_movies = []
    filtered_main_sheet = []
    for row in rows[1:]:  # Skipping the header
        columns = row.split(";")
        if columns[0] == '':
            break
        if len(columns) > 2:  # Ensure there is a date column
            try:
                date_watched = datetime.strptime(columns[2], "%d/%b./%Y")
                if date_watched.year == year:
                    filtered_movies.append(columns[0])  # Add movie name to the filtered list
                    filtered_main_sheet.append({
                        "name": columns[0],
                        "imdb-link": columns[1],
                        "suggester": set_participant_aliases(columns[3]),
                        "average-rating": locale.atof(columns[4]),
                    }) # Add movie name to the main sheet file
            except ValueError:
                continue  # Skip if the date is invalid or in the wrong format
    
    # Extract participant sheets with filter
    participant_sheets = {}
    for sheet in spreadsheet.worksheets()[1:]: # Ignore main sheet
        participant_csv = export_to_csv(sheet)
        participant_name = sheet.title
        rows = participant_csv.split("\n")
        filtered_rows = []
        for row in rows[1:]:  # Skipping the header
            columns = row.split(";")
            if len(columns) > 1 and columns[0] in filtered_movies:  # Only consider ratings for filtered movies
                filtered_rows.append({
                    "name": columns[0],
                    "rating": int(columns[1]) if len(columns) > 1 and columns[1].isdigit() else None
                })

        participant_sheets[participant_name] = {
            'csv': filtered_rows,
            'suggestion-count': 0,
            'participation-count': 0,
            'all-average-rating': 0
        }
    return filtered_main_sheet, participant_sheets

def process_data(main_sheet, participant_sheets):
    for movie_row in main_sheet:
        participant_sheets[movie_row['suggester']]['suggestion-count'] += 1

    for participant, data in participant_sheets.items():
        for participant_row in data['csv']:
            participant_rating = participant_row['rating']
            if participant_rating is not None:
                participant_sheets[participant]['participation-count'] += 1
                participant_sheets[participant]['all-average-rating'] += participant_rating
        participant_sheets[participant]['all-average-rating'] /= participant_sheets[participant]['participation-count']


    return main_sheet, participant_sheets

def format_ouput_content(participant_sheets):
    output = "# Cinéfilos Processing Results\n\n"

    # Section for Suggestion and Participation
    output += "## Suggestion and Participation Metrics\n\n"

    # Suggestion Metrics
    output += "### Most and Least Suggestions\n\n"
    output += "**Suggestions per person:**"
    sorted_items = sorted(participant_sheets.items(), key=lambda x: x[1]['suggestion-count'])
    # Print each user with their suggestion count
    for person, data in sorted_items:
        output += f"- {person}: {data['suggestion-count']} suggestions\n"

    # Participation Metrics
    output += "\n### Most and Least Participation\n\n"
    output += "**Participation per person:**\n"
    sorted_items = sorted(participant_sheets.items(), key=lambda x: x[1]['participation-count'])
    for person, data in sorted_items:
        output += f"- {person}: {data['participation-count']} participation\n"

    #  Section for Voting Patterns and Preferences
    output += "\n## Voting Patterns and Preferences\n\n"

    # Average Rating Metrics
    output += "### Average Rating Given by Each Person for all movies they've watched\n\n"
    output += "**Rating per person:**\n"
    sorted_items = sorted(participant_sheets.items(), key=lambda x: x[1]['all-average-rating'])
    for person, data in sorted_items:
        output += f"- {person}: {data['all-average-rating']:.2f} average rating\n"

    return output

# Main function to preprocess and write details to the output file
def main():    
    year = initialize_config_and_return_arguments()

    script_dir = define_script_dir()
    main_sheet, participant_sheets = preprocess_spreadsheet(year, script_dir)

    processed_main, processed_participant = process_data(main_sheet, participant_sheets)

    format_print(processed_main)
    format_print(processed_participant)

    content = format_ouput_content(processed_participant)

    output_path =  write_to_output_file(year, script_dir, content)

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
