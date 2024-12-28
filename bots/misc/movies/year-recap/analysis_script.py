#!/usr/bin/env python3

import argparse
import locale
import os
import pprint
import re
import statistics
import subprocess
from datetime import datetime

import gspread
import requests
import requests_cache
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


def initialize_config_and_return_arguments():
    # This works in systems where Portuguese locale is available
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    locale.setlocale(locale.LC_NUMERIC, "pt_BR.UTF-8")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Process spreadsheet and extract data."
    )
    parser.add_argument("year", type=int, help="The year for which to run the analysis")
    parser.add_argument(
        "--generate-slide",
        action="store_true",
        help="Set this flag to run the slide creation process",
    )
    args = parser.parse_args()

    load_dotenv()

    requests_cache.install_cache("api_cache", expire_after=43200)

    return args.year, args.generate_slide


# Function to authenticate and get the Google Sheets client
def authenticate_google_sheets(credentials_json):
    # Define the scope for Google Sheets and Google Drive API access
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

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
        "sand.dejesus@gmail.com": "Sand",
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


def fetch_imdb_movie_data(imdb_link):

    match = re.search(r"/title/(tt\d+)/", imdb_link)
    if match:
        imdb_id = match.group(1)
    else:
        print("No IMDb ID found.")
        return None

    base_url = "http://www.omdbapi.com/"
    params = {
        "apikey": os.getenv("IMDB_API_KEY"),
        "i": imdb_id,  # Search by IMDb ID
    }
    # Remove None values to avoid conflicts
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            print(f"Error: {data.get('Error')}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None


def convert_to_slide(md_file, script_dir, year):
    # Define the output file name with the year
    output_file = f"analysis_results_{year}.html"

    # Write details to the output file
    output_path = os.path.join(script_dir, output_file)

    try:
        # Run the Marp command
        command = ["marp", md_file, "--output", output_path]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Marp: {e}")

    return output_path


def preprocess_spreadsheet(year, script_dir):
    credentials_json = os.path.join(script_dir, os.getenv("CREDENTIALS_JSON"))

    # Authenticate and get the client
    client = authenticate_google_sheets(credentials_json)

    # Open the spreadsheet
    spreadsheet = client.open_by_url(os.getenv("SHEET_URL"))

    # Extract the main file (first sheet)
    main_sheet = spreadsheet.get_worksheet(0)
    main_csv = export_to_csv(main_sheet)
    rows = main_csv.split("\n")

    # Filter the movies by the given year and add to filtered main list
    filtered_movies = []
    filtered_main_sheet = {}
    for row in rows[1:]:  # Skipping the header
        columns = row.split(";")
        movie_name = columns[0]
        imdb_link = columns[1]
        if movie_name == "":
            break
        if len(columns) > 2:  # Ensure there is a date column
            try:
                date_watched = datetime.strptime(columns[2], "%d/%b./%Y")
                if date_watched.year == year:
                    filtered_movies.append(
                        movie_name
                    )  # Add movie name to the filtered list
                    filtered_main_sheet[movie_name] = {
                        "name": movie_name,
                        "imdb-link": imdb_link,
                        "suggester": set_participant_aliases(columns[3]),
                        "average-rating": locale.atof(columns[4]),
                        "individual-ratings": {},
                        "standard-deviation": 0,
                        "rating-range": 0,
                        "imdb-data": fetch_imdb_movie_data(imdb_link),
                    }
            except ValueError:
                print("ERROR: please check this before continuing")
                continue  # Skip if the date is invalid or in the wrong format

    # Extract participant sheets with filter
    participant_sheets = {}
    for sheet in spreadsheet.worksheets()[1:]:  # Ignore main sheet
        participant_csv = export_to_csv(sheet)
        participant_name = sheet.title
        rows = participant_csv.split("\n")
        filtered_rows = []
        for row in rows[1:]:  # Skipping the header
            columns = row.split(";")
            if (
                len(columns) > 1 and columns[0] in filtered_movies
            ):  # Only consider ratings for filtered movies
                filtered_rows.append(
                    {
                        "name": columns[0],
                        "rating": (
                            int(columns[1])
                            if len(columns) > 1 and columns[1].isdigit()
                            else None
                        ),
                    }
                )

        participant_sheets[participant_name] = {
            "csv": filtered_rows,
            "suggested-movies": [],
            "participation-count": 0,
            "all-average-rating": 0,
            "received-average-rating": 0,
            "critical-average-rating": 0,
            "bias-average-rating": 0,
            "worst-suggestion": None,
            "best-suggestion": None,
            "average-ratings": [],
            "mean-average-rating": None,
            "impact-on-group-mean-average": None,
        }
    return filtered_main_sheet, participant_sheets


def process_data(main_sheet, participant_sheets):
    # Track suggestions and ratings
    all_movie_average_ratings = []
    for movie_name, movie_row_data in main_sheet.items():
        suggester = movie_row_data["suggester"]
        movie_name = movie_row_data["name"]
        movie_average_rating = movie_row_data["average-rating"]
        all_movie_average_ratings.append(movie_average_rating)
        participant_sheets[suggester]["received-average-rating"] += movie_average_rating
        participant_sheets[suggester]["suggested-movies"].append(movie_name)
        participant_sheets[suggester]["average-ratings"].append(movie_average_rating)

        new_movie_item = {"name": movie_name, "rating": movie_average_rating}
        if (
            participant_sheets[suggester]["best-suggestion"] is None
            or participant_sheets[suggester]["best-suggestion"]["rating"]
            < movie_average_rating
        ):
            participant_sheets[suggester]["best-suggestion"] = new_movie_item.copy()

        if (
            participant_sheets[suggester]["worst-suggestion"] is None
            or participant_sheets[suggester]["worst-suggestion"]["rating"]
            > movie_average_rating
        ):
            participant_sheets[suggester]["worst-suggestion"] = new_movie_item.copy()

    overall_group_average = statistics.mean(all_movie_average_ratings)

    # Process ratings
    for participant_name, participant_data in participant_sheets.items():
        if participant_data["average-ratings"]:
            participant_data["mean-average-rating"] = statistics.mean(
                participant_data["average-ratings"]
            )
            participant_data["impact-on-group-mean-average"] = (
                participant_data["mean-average-rating"] - overall_group_average
            )

        for participant_movie_data in participant_data["csv"]:
            participant_rating = participant_movie_data["rating"]

            # Means participant watched given movie
            if participant_rating is not None:
                # Calculate individual participant's all-average-rating
                participant_data["participation-count"] += 1
                participant_data["all-average-rating"] += participant_rating

                # Means participant suggested that movie
                if (
                    participant_movie_data["name"]
                    in participant_data["suggested-movies"]
                ):
                    participant_data["bias-average-rating"] += participant_rating
                # Means participant did not suggest that movie
                else:
                    participant_data["critical-average-rating"] += participant_rating

                # Adds calculations of individual rating in the main sheet to check controversies
                main_sheet[participant_movie_data["name"]]["individual-ratings"][
                    participant_name
                ] = participant_rating

        suggested_movies_count = len(participant_data["suggested-movies"])

        if participant_data["participation-count"] > 0:
            participant_data["all-average-rating"] /= (
                participant_data["participation-count"] - suggested_movies_count
            )

            participant_data["critical-average-rating"] /= participant_data[
                "participation-count"
            ]

        if suggested_movies_count > 0:
            participant_data["received-average-rating"] /= suggested_movies_count

        if suggested_movies_count > 0:
            participant_data["bias-average-rating"] /= suggested_movies_count

    for movie_name, movie_data in main_sheet.items():
        ratings = list(movie_data["individual-ratings"].values())

        # Calculate standard deviation and range
        movie_data["standard-deviation"] = statistics.stdev(ratings)
        movie_data["rating-range"] = max(ratings) - min(ratings)

    return main_sheet, participant_sheets


def format_ouput_content(main_sheet, participant_sheets):
    output = "# Cinéfilos Processing Results\n\n---\n\n"

    # Section for Suggestion and Participation
    output += "## Suggestion and Participation Metrics\n\n"

    # Suggestion Metrics
    output += "### Most and Least Suggestions\n\n"
    output += "**Suggestions per person:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: len(x[1]["suggested-movies"])
    )
    # Print each user with their suggestion count
    for person, data in sorted_items:
        output += f"- {person}: {len(data['suggested-movies'])} suggestions\n"

    # Participation Metrics
    output += "\n---\n\n### Most and Least Participation\n\n"
    output += "**Participation per person:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: x[1]["participation-count"]
    )
    for person, data in sorted_items:
        output += f"- {person}: {data['participation-count']} participations\n"

    #  Section for Voting Patterns and Preferences
    output += "\n---\n\n## Voting Patterns and Preferences\n\n"

    # Average Rating Given Metrics
    output += (
        "### Average Rating Given by Each Person for all movies they've watched\n\n"
    )
    output += "**Rating per person:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: x[1]["all-average-rating"]
    )
    for person, data in sorted_items:
        output += f"- {person}: {data['all-average-rating']:.2f} given average rating\n"

    # Average Rating Received Metrics
    output += (
        "\n---\n\n### Average (of average) Rating of selected movies by that person\n\n"
    )
    output += "**Rating of selected movies:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: x[1]["received-average-rating"]
    )
    for person, data in sorted_items:
        output += f"- {person}: {data['received-average-rating']:.2f} received average rating\n"

    # Most Generous and Most Critical Viewers
    output += "\n---\n\n### Most Generous and Critical Viewers\n\n"
    output += "**Average rating given to movies of other people:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: x[1]["critical-average-rating"]
    )
    for person, data in sorted_items:
        output += (
            f"- {person}: {data['critical-average-rating']:.2f} given average rating\n"
        )

    # Biased Ratings
    output += "\n---\n\n### Most Biased and Least Biased Viewers\n\n"
    output += "**Average rating given to own movies:**\n"
    sorted_items = sorted(
        participant_sheets.items(), key=lambda x: x[1]["bias-average-rating"]
    )
    for person, data in sorted_items:
        output += (
            f"- {person}: {data['bias-average-rating']:.2f} given average rating\n"
        )

    #  Section for Best and Worst Suggestions
    output += "\n---\n\n## Best and Worst Suggestions\n\n"

    # Highest and Lowest Rated Movies
    output += "### Highest and Lowest Rated Movies\n\n"
    output += "**Average rating of each movie in order:**\n"
    sorted_items = sorted(main_sheet.items(), key=lambda x: x[1]["average-rating"])
    for index, (_, movie_data) in enumerate(sorted_items):
        output += f"- {movie_data['name']}, suggested by {movie_data['suggester']} with an average rating of {movie_data['average-rating']:.2f}"
        if index == 0:
            output += " **the worst movie we watched...**\n"
        elif index == len(sorted_items) - 1:
            output += " **won GOTY of the year!**\n"
        else:
            output += "\n"

    #  Section for Controversy and Consensus
    output += "\n---\n\n## Controversy and Consensus\n\n"

    # Most Controversial & Consensual Movies
    output += "### Most Controversial Movies\n\n"
    output += "**List of  movies based on how much people agreed on their rating using standard deviation and rating range, from least to most:**\n"
    sorted_items = sorted(main_sheet.items(), key=lambda x: x[1]["standard-deviation"])
    for index, (movie_name, movie_data) in enumerate(sorted_items):
        output += f"- {movie_data['name']}, suggested by {movie_data['suggester']} with standard deviation value of {movie_data['standard-deviation']:.2f} and rating range of {movie_data['rating-range']:.2f}"
        if index == 0:
            output += " **the movie we agreed on ratings the most...**\n"
        elif index == len(sorted_items) - 1:
            output += " **the most controversial movie!**\n"
        else:
            output += "\n"

    #  Section for User-Specific Metrics
    output += "\n---\n\n## User-Specific Metrics\n\n"

    # Personal Best/Worst Suggestions
    output += "### Personal Best/Worst Suggestions\n\n"
    for person, data in participant_sheets.items():
        if data["best-suggestion"] is not None:
            if data["worst-suggestion"]["name"] != data["best-suggestion"]["name"]:
                output += f"- {person}: best suggestion: {data['best-suggestion']['name']}, worst suggestion: {data['worst-suggestion']['name']}\n"
            else:
                output += f"- {person}: has only one suggestion: {data['best-suggestion']['name']}\n"
        else:
            output += f"- {person}: has no suggestions\n"

    # Suggesters' Impact on the Group's Average Rating
    output += "\n---\n\n### Suggesters' Impact on the Group's Average Rating\n\n"
    output += "**List of  movies based on how much someone's suggestion affect the gorup average, the higher the number, the better received their movies are, the lower, means it usually affects the average to go down:**\n"
    sorted_items = sorted(
        participant_sheets.items(),
        key=lambda x: (x[1].get("impact-on-group-mean-average") or float("inf")),
    )
    for person, data in sorted_items:
        if data["impact-on-group-mean-average"] is not None:
            output += f"- {person}: Average rating of their suggested movies:: {data['mean-average-rating']:.2f}, Impact on group's overall average: {data['impact-on-group-mean-average']:.2f}\n"
        else:
            output += f"- {person}: has no suggestions\n"

    return output


# Main function to preprocess and write details to the output file
def main():
    year, generate_slide = initialize_config_and_return_arguments()

    script_dir = define_script_dir()
    main_sheet, participant_sheets = preprocess_spreadsheet(year, script_dir)

    processed_main, processed_participant = process_data(main_sheet, participant_sheets)

    format_print(processed_main)
    format_print(processed_participant)

    content = format_ouput_content(processed_main, processed_participant)

    md_output_path = write_to_output_file(year, script_dir, content)

    # Print message to indicate the results were saved
    print(f"Analysis complete for the year {year}. Results saved to {md_output_path}")

    if generate_slide:
        pptx_output_path = convert_to_slide(md_output_path, script_dir, year)

        # Print message to indicate the results were saved
        print(
            f"Analysis complete for the year {year}. Results saved to {pptx_output_path}"
        )


if __name__ == "__main__":
    main()
