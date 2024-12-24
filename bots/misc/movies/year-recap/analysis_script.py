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

def empty_counter(value):
    # Check if the value is mutable (e.g., list, dict)
    if isinstance(value, (list, dict, set)):  
        # If it's mutable, create a new copy for each person
        return {
            "Sev": value.copy(),
            "João": value.copy(),
            "Victor": value.copy(),
            "Baby": value.copy(),
            "Sand": value.copy(),
        }
    else:
        # If it's not mutable, just assign the value as is (e.g., 0)
        return {
            "Sev": value,
            "João": value,
            "Victor": value,
            "Baby": value,
            "Sand": value,
        }

def calculate_suggestion_metrics(filtered_main_sheet):
    suggestion_counts = empty_counter(0)
    suggestion_movies = empty_counter([])
    # Iterate over the filtered rows in the main sheet
    for row in filtered_main_sheet:
        suggester = row[3]  # Assuming "suggested by" is the 4th column (index 3)
        movie = row[0]  # Movie name is in the 1st column (index 0)

        # Count suggestions for each suggester and track movies they suggested
        if suggester == "Thiago Augusto":
            suggestion_counts["Sev"] += 1
            suggestion_movies["Sev"].append(movie)
        elif suggester == "joaovictorcosta1997@gmail.com":
            suggestion_counts["João"] += 1
            suggestion_movies["João"].append(movie)
        elif suggester == "Victor Eduardo":
            suggestion_counts["Victor"] += 1
            suggestion_movies["Victor"].append(movie)
        elif suggester == "Gustavo Paes":
            suggestion_counts["Baby"] += 1
            suggestion_movies["Baby"].append(movie)
        elif suggester == "sand.dejesus@gmail.com":
            suggestion_counts["Sand"] += 1
            suggestion_movies["Sand"].append(movie)

    # Find most and least suggestions
    most_suggested_count = max(suggestion_counts.values())
    least_suggested_count = min(suggestion_counts.values())

    most_suggested = [person for person, count in suggestion_counts.items() if count == most_suggested_count]
    least_suggested = [person for person, count in suggestion_counts.items() if count == least_suggested_count]

    return suggestion_counts, most_suggested, least_suggested, suggestion_movies

# Function to calculate the most and least participation
def calculate_participation_metrics(filtered_participant_sheets):
    participation_counts = empty_counter(0)

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

# Function to calculate the average rating given by each person
def calculate_average_ratings(filtered_participant_sheets):
    average_ratings = {}
    
    for participant in filtered_participant_sheets:
        participant_name = participant["name"]
        participant_csv = participant["csv"]
        rows = participant_csv.split("\n")
        
        total_ratings = 0
        rating_count = 0
        
        for row in rows[1:]:  # Skip header
            columns = row.split(";")
            if len(columns) > 1 and columns[1].strip():  # Check if there is a rating (non-blank)
                total_ratings += int(columns[1].strip())
                rating_count += 1
        
        if rating_count > 0:
            average_ratings[participant_name] = total_ratings / rating_count
    
    return average_ratings

# Function to calculate the average rating for each person's suggested movies
def calculate_average_rating_for_suggested_movies(filtered_participant_sheets, suggestion_movies):
    average_ratings_for_suggested = {}
    
    for person, movies in suggestion_movies.items():
        total_ratings = 0
        rating_count = 0
        
        # Find ratings for each suggested movie by the given person
        for movie in movies:
            for participant in filtered_participant_sheets:
                participant_csv = participant["csv"]
                rows = participant_csv.split("\n")
                for row in rows[1:]:  # Skip header
                    columns = row.split(";")
                    if len(columns) > 1 and columns[0] == movie and columns[1].strip():  # If rating is non-blank
                        total_ratings += int(columns[1].strip())
                        rating_count += 1
        
        if rating_count > 0:
            average_ratings_for_suggested[person] = total_ratings / rating_count
        else:
            average_ratings_for_suggested[person] = 0  # No ratings for suggested movies
    
    return average_ratings_for_suggested

# Function to calculate the average rating given to movies suggested by others
# and return most generous and most critical viewers
def calculate_average_rating_given_to_suggested_movies(filtered_participant_sheets, suggestion_movies):
    generosity = {}
    criticality = {}
    
    for person, suggested_movies in suggestion_movies.items():
        total_ratings = 0
        rating_count = 0
        total_ratings_critical = 0
        rating_count_critical = 0
        
        # Iterate through each participant's ratings
        for participant in filtered_participant_sheets:
            participant_name = participant["name"]
            participant_csv = participant["csv"]
            rows = participant_csv.split("\n")
            
            for row in rows[1:]:  # Skip header
                columns = row.split(";")
                if len(columns) > 1 and columns[0].strip():
                    movie = columns[0].strip()
                    rating = columns[1].strip()
                    if rating:  # Only consider movies with ratings
                        rating = int(rating)
                        
                        # Consider ratings for movies NOT suggested by this person (generosity)
                        if movie not in suggested_movies:
                            total_ratings += rating
                            rating_count += 1
                        # Consider ratings for movies that were suggested by the person (criticality)
                        elif movie in suggested_movies:
                            total_ratings_critical += rating
                            rating_count_critical += 1
        
        # Calculate average generosity and criticality
        if rating_count > 0:
            generosity[person] = total_ratings / rating_count
        else:
            generosity[person] = 0
        
        if rating_count_critical > 0:
            criticality[person] = total_ratings_critical / rating_count_critical
        else:
            criticality[person] = 0
    
    # Determine the most generous and most critical viewers
    most_generous_viewer = max(generosity, key=generosity.get)  # Highest generosity = most generous
    most_critical_viewer = min(criticality, key=criticality.get)  # Highest criticality = most critical
    
    return generosity, criticality, most_generous_viewer, most_critical_viewer


def calculate_biased_ratings(filtered_participant_sheets, suggestion_movies):
    biased_ratings = {}
    
    for person, suggested_movies in suggestion_movies.items():
        total_ratings = 0
        rating_count = 0
        
        # Iterate through each participant's ratings
        for participant in filtered_participant_sheets:
            participant_name = participant["name"]
            participant_csv = participant["csv"]
            rows = participant_csv.split("\n")
            
            for row in rows[1:]:  # Skip header
                columns = row.split(";")
                if len(columns) > 1 and columns[0].strip():
                    movie = columns[0].strip()
                    rating = columns[1].strip()
                    if rating:  # Only consider movies with ratings
                        rating = int(rating)
                        
                        # Only consider ratings for movies that the person suggested
                        if movie in suggested_movies and participant_name == person:
                            total_ratings += rating
                            rating_count += 1
        
        # Calculate average rating for own movies
        if rating_count > 0:
            biased_ratings[person] = total_ratings / rating_count
        else:
            biased_ratings[person] = 0
    
    # Determine the most and least biased viewers
    most_biased_viewer = max(biased_ratings, key=biased_ratings.get)  # Highest biased rating = most biased
    least_biased_viewer = min(biased_ratings, key=biased_ratings.get)  # Lowest biased rating = least biased
    
    return biased_ratings, most_biased_viewer, least_biased_viewer

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

    # Section for Suggestion and Participation
    formatted_file += "## Suggestion and Participation Metrics\n\n"
    
    # Suggestion Metrics
    formatted_file += "### Most and Least Suggestions\n\n"
    formatted_file += "Suggestions per person:\n"
    suggestion_counts, most_suggested, least_suggested, suggestion_movies = calculate_suggestion_metrics(filtered_main_sheet)
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

    # Section for Voting Patterns and Preferences
    formatted_file += "## Voting Patterns and Preferences\n\n"

    # Average Rating Metrics
    formatted_file += "### Average Rating Given by Each Person for all movies\n\n"
    average_ratings = calculate_average_ratings(participant_sheets)
    for person, avg_rating in average_ratings.items():
        formatted_file += f"- {person}: {avg_rating:.2f} average rating\n"

    # Average Rating for Suggested Movies
    formatted_file += "\n### Average Rating for All Suggested Movies of each person\n\n"
    average_ratings_for_suggested = calculate_average_rating_for_suggested_movies(participant_sheets, suggestion_movies)
    for person, avg_rating in average_ratings_for_suggested.items():
        formatted_file += f"{person}: {avg_rating:.2f}\n"
    formatted_file += "\n"

    # Most Generous and Most Critical Viewers
    formatted_file += "\n### Most Generous and Critical Viewers\n\n"
    generosity, criticality, most_generous_viewer, most_critical_viewer = calculate_average_rating_given_to_suggested_movies(participant_sheets, suggestion_movies)
    formatted_file += f"- **Most Generous Viewer**: {most_generous_viewer} ({generosity[most_generous_viewer]:.2f})\n"
    formatted_file += f"- **Most Critical Viewer**: {most_critical_viewer} ({criticality[most_critical_viewer]:.2f})\n"

    # Biased Ratings
    formatted_file += "\n### Most Biased and Least Biased Viewers\n\n"
    biased_ratings, most_biased_viewer, least_biased_viewer = calculate_biased_ratings(participant_sheets, suggestion_movies)
    formatted_file += f"- **Most Biased Viewer**: {most_biased_viewer} ({biased_ratings[most_biased_viewer]:.2f})\n"
    formatted_file += f"- **Least Biased Viewer**: {least_biased_viewer} ({biased_ratings[least_biased_viewer]:.2f})\n"



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
