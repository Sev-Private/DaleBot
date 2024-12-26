# how to run full script
# python3 analysis_script.py 2024


# 1. Most and Least Suggestions  
# Count how many movies each friend has suggested to identify who suggested the most and the least movies.

def most_and_least_suggestions(main_df):
    # Count the number of suggestions made by each person
    suggestions_count = main_df['Indicado Por'].value_counts()
    
    # Find the person with the most and least suggestions
    most_suggested = suggestions_count.idxmax()
    least_suggested = suggestions_count.idxmin()
    
    return most_suggested, least_suggested

# Example usage with your main dataframe (main_df)
most_suggested, least_suggested = most_and_least_suggestions(main_df)

# Display results
print(f"Most Suggestions: {most_suggested}")
print(f"Least Suggestions: {least_suggested}")


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

# 2. Most and Least Participation  
# Count how many movies each person has voted on to determine who has participated in rating the most and least movies.

def most_and_least_participation(df_list):
    # Count how many movies each person has voted on
    participation_count = {name: df['Nota Individual'].notna().sum() for name, df in df_list.items()}
    
    # Find the person with the most and least participation
    most_participated = max(participation_count, key=participation_count.get)
    least_participated = min(participation_count, key=participation_count.get)
    
    return most_participated, least_participated

# Example usage with a dictionary of user dataframes (df_list)
most_participated, least_participated = most_and_least_participation(user_dfs)

# Display results
print(f"Most Participation: {most_participated}")
print(f"Least Participation: {least_participated}")


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


# 3. Average Rating Given by Each Person  
# Calculate the average rating each person gives to see who tends to rate movies higher or lower on average.

def average_rating_given(df_list):
    # Calculate the average rating each person gives
    avg_ratings = {name: df['Nota Individual'].mean() for name, df in df_list.items()}
    
    return avg_ratings

# Example usage with a dictionary of user dataframes (df_list)
avg_ratings = average_rating_given(user_dfs)

# Display results
print("Average Rating Given by Each Person:")
for person, avg_rating in avg_ratings.items():
    print(f"{person}: {avg_rating:.2f}")

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

# 4. Average Rating for Each Person's Suggested Movies  
# Find out how well each person's suggested movies are received on average.

def average_rating_for_suggested_movies(main_df, df_list):
    avg_ratings = {}
    
    for suggester in main_df['Indicado Por'].unique():
        # Filter movies suggested by the current suggester
        suggested_movies = main_df[main_df['Indicado Por'] == suggester]
        
        # Merge suggested movies with ratings from each person
        ratings = pd.concat([df.loc[df['Filme'].isin(suggested_movies['Filme']), ['Filme', 'Nota Individual']] for df in df_list.values()])
        
        # Calculate the average rating for the suggester's movies
        avg_rating = ratings['Nota Individual'].mean()
        avg_ratings[suggester] = avg_rating
    
    return avg_ratings

# Example usage with the main dataframe (main_df) and a dictionary of user dataframes (df_list)
avg_ratings_for_suggested = average_rating_for_suggested_movies(main_df, user_dfs)

# Display results
print("Average Rating for Each Person's Suggested Movies:")
for suggester, avg_rating in avg_ratings_for_suggested.items():
    print(f"{suggester}: {avg_rating:.2f}")


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




# 5. Most Generous and Most Critical Viewers  
# Identify who has the highest and lowest average votes when rating others' suggestions.

def most_generous_and_most_critical(df_list):
    # Calculate the average rating given by each person
    avg_ratings = {name: df['Nota Individual'].mean() for name, df in df_list.items()}
    
    # Find the most generous and most critical viewers
    most_generous = max(avg_ratings, key=avg_ratings.get)
    most_critical = min(avg_ratings, key=avg_ratings.get)
    
    return most_generous, most_critical

# Example usage with a dictionary of user dataframes (df_list)
most_generous, most_critical = most_generous_and_most_critical(user_dfs)

# Display results
print(f"Most Generous Viewer: {most_generous}")
print(f"Most Critical Viewer: {most_critical}")


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

# 6. Highest and Lowest Rated Movies  
# Identify the movie with the highest and lowest average scores, and track who suggested them.

def highest_and_lowest_rated_movies(main_df):
    # Calculate the average rating for each movie
    movie_avg_ratings = main_df.groupby('Filme')['Nota Final'].mean()
    
    # Find the highest and lowest rated movies
    highest_rated = movie_avg_ratings.idxmax()
    lowest_rated = movie_avg_ratings.idxmin()
    
    return highest_rated, lowest_rated

# Example usage with the main dataframe (main_df)
highest_rated, lowest_rated = highest_and_lowest_rated_movies(main_df)

# Display results
print(f"Highest Rated Movie: {highest_rated}")
print(f"Lowest Rated Movie: {lowest_rated}")


# 7. Top and Bottom Suggesters  
# Find out who suggested the movies with the highest and lowest average ratings across all their suggestions.

def top_and_bottom_suggesters(main_df, df_list):
    avg_ratings_per_suggester = {}
    
    # Calculate the average ratings for each suggester's movies
    for suggester in main_df['Indicado Por'].unique():
        # Filter movies suggested by the current suggester
        suggested_movies = main_df[main_df['Indicado Por'] == suggester]
        
        # Merge suggested movies with ratings from each person
        ratings = pd.concat([df.loc[df['Filme'].isin(suggested_movies['Filme']), ['Filme', 'Nota Individual']] for df in df_list.values()])
        
        # Calculate the average rating for the suggester's movies
        avg_rating = ratings['Nota Individual'].mean()
        avg_ratings_per_suggester[suggester] = avg_rating
    
    # Find the top and bottom suggester
    top_suggester = max(avg_ratings_per_suggester, key=avg_ratings_per_suggester.get)
    bottom_suggester = min(avg_ratings_per_suggester, key=avg_ratings_per_suggester.get)
    
    return top_suggester, bottom_suggester

# Example usage with the main dataframe (main_df) and a dictionary of user dataframes (df_list)
top_suggester, bottom_suggester = top_and_bottom_suggesters(main_df, user_dfs)

# Display results
print(f"Top Suggester: {top_suggester}")
print(f"Bottom Suggester: {bottom_suggester}")

# 8. Most Controversial Movie  
# Find the movie with the highest standard deviation or widest range in votes to identify the most polarizing movie.

def most_controversial_movie(df_list):
    # Calculate the standard deviation (controversy) for each movie's ratings
    movie_ratings = {}
    
    for df in df_list.values():
        for movie, rating in zip(df['Filme'], df['Nota Individual']):
            if pd.notna(rating):
                if movie not in movie_ratings:
                    movie_ratings[movie] = []
                movie_ratings[movie].append(rating)
    
    # Calculate the standard deviation for each movie
    movie_std_devs = {movie: np.std(ratings) for movie, ratings in movie_ratings.items()}
    
    # Find the most controversial movie (highest standard deviation)
    most_controversial = max(movie_std_devs, key=movie_std_devs.get)
    
    return most_controversial

# Example usage with a dictionary of user dataframes (df_list)
most_controversial = most_controversial_movie(user_dfs)

# Display results
print(f"Most Controversial Movie: {most_controversial}")


# 9. Most Consensual Movie  
# Identify the movie with the lowest standard deviation or smallest range in votes, showing the movie with the most similar ratings from everyone.

def most_consensual_movie(df_list):
    # Calculate the standard deviation (consensus) for each movie's ratings
    movie_ratings = {}
    
    for df in df_list.values():
        for movie, rating in zip(df['Filme'], df['Nota Individual']):
            if pd.notna(rating):
                if movie not in movie_ratings:
                    movie_ratings[movie] = []
                movie_ratings[movie].append(rating)
    
    # Calculate the standard deviation for each movie
    movie_std_devs = {movie: np.std(ratings)

# 10. Personal Best/Worst Suggestions  
# For each person, find their most and least liked movie based on group ratings.

def personal_best_and_worst_suggestions(main_df):
    personal_best_worst = {}

    # For each person, find their most and least liked movie based on group ratings
    for suggester in main_df['Indicado Por'].unique():
        suggested_movies = main_df[main_df['Indicado Por'] == suggester]
        
        # Find the most and least liked movie for each suggester
        most_liked_movie = suggested_movies.loc[suggested_movies['Nota Final'].idxmax()]
        least_liked_movie = suggested_movies.loc[suggested_movies['Nota Final'].idxmin()]
        
        personal_best_worst[suggester] = {
            'Most Liked Movie': most_liked_movie['Filme'],
            'Least Liked Movie': least_liked_movie['Filme']
        }
    
    return personal_best_worst

# Example usage with the main dataframe (main_df)
best_worst_suggestions = personal_best_and_worst_suggestions(main_df)

# Display results
print("Personal Best/Worst Suggestions:")
for suggester, movies in best_worst_suggestions.items():
    print(f"{suggester}: Most Liked - {movies['Most Liked Movie']}, Least Liked - {movies['Least Liked Movie']}")


# 11. Suggesters' Impact on the Group's Average Rating  
# Analyze how each person's movie choices affect the overall average rating for the group.

def suggesters_impact_on_group_avg(main_df, df_list):
    suggester_impact = {}

    # Calculate the overall group average rating
    group_avg_rating = main_df['Nota Final'].mean()
    
    # For each suggester, calculate the impact of their suggestions
    for suggester in main_df['Indicado Por'].unique():
        suggested_movies = main_df[main_df['Indicado Por'] == suggester]
        avg_rating_of_suggested = suggested_movies['Nota Final'].mean()
        
        # The impact is the difference between the suggester's movie ratings and the group average
        impact = avg_rating_of_suggested - group_avg_rating
        suggester_impact[suggester] = impact
    
    return suggester_impact

# Example usage with the main dataframe (main_df) and a dictionary of user dataframes (df_list)
suggester_impact = suggesters_impact_on_group_avg(main_df, user_dfs)

# Display results
print("Suggesters' Impact on the Group's Average Rating:")
for suggester, impact in suggester_impact.items():
    print(f"{suggester}: Impact = {impact:.2f}")


# 12. Highest Rated Movies by Genre  
# If the spreadsheet includes genres, determine which friend tends to suggest the highest-rated movies by genre.

def highest_rated_movies_by_genre(main_df, genre_column='Genre'):
    genre_avg_ratings = {}

    # Calculate the average rating for each genre
    for genre in main_df[genre_column].unique():
        genre_movies = main_df[main_df[genre_column] == genre]
        avg_rating = genre_movies['Nota Final'].mean()
        genre_avg_ratings[genre] = avg_rating
    
    return genre_avg_ratings

# Example usage with the main dataframe (main_df)
highest_rated_genres = highest_rated_movies_by_genre(main_df)

# Display results
print("Highest Rated Movies by Genre:")
for genre, avg_rating in highest_rated_genres.items():
    print(f"Genre: {genre}, Average Rating: {avg_rating:.2f}")


# 13. Trend Over Time  
# See if the group's ratings or a specific person's ratings have changed over time to spot trends in taste or voting behavior.

def trend_over_time(main_df, person=None):
    # Convert the date column to datetime
    main_df['Data'] = pd.to_datetime(main_df['Data'], format='%d/%b/%Y')
    
    if person:
        # Filter by a specific person if provided
        person_data = main_df[main_df['Indicado Por'] == person]
        trend = person_data.groupby(person_data['Data'].dt.month)['Nota Final'].mean()
    else:
        # Calculate the trend for the entire group
        trend = main_df.groupby(main_df['Data'].dt.month)['Nota Final'].mean()
    
    return trend

# Example usage with the main dataframe (main_df)
trend = trend_over_time(main_df)

# Display results
print("Trend Over Time:")
print(trend)


# 14. Most Similar and Different Tastes  
# Compare the average ratings between pairs of friends to find out who has the most and least similar tastes.

from sklearn.metrics import pairwise_distances
import numpy as np

def most_similar_and_different_tastes(df_list):
    # Create a matrix where rows are users and columns are movies
    user_movie_matrix = pd.DataFrame(index=df_list.keys())
    
    for name, df in df_list.items():
        user_movie_matrix[name] = df.set_index('Filme')['Nota Individual']
    
    # Replace NaN with zeros for calculating distance
    user_movie_matrix = user_movie_matrix.fillna(0)

    # Calculate pairwise distance between all users
    distance_matrix = pairwise_distances(user_movie_matrix, metric='cosine')

    # Get the most and least similar tastes
    most_similar_idx = np.argmin(distance_matrix)
    least_similar_idx = np.argmax(distance_matrix)
    
    most_similar = (list(df_list.keys())[most_similar_idx // len(df_list)],
                    list(df_list.keys())[most_similar_idx % len(df_list)])
    least_similar = (list(df_list.keys())[least_similar_idx // len(df_list)],
                     list(df_list.keys())[least_similar_idx % len(df_list)])
    
    return most_similar, least_similar

# Example usage with a dictionary of user dataframes (df_list)
most_similar, least_similar = most_similar_and_different_tastes(user_dfs)

# Display results
print(f"Most Similar Tastes: {most_similar}")
print(f"Least Similar Tastes: {least_similar}")


# 15. Best Voting Consistency  
# Identify who has the most consistent voting pattern (smallest standard deviation in their own votes).

def best_voting_consistency(df_list):
    consistency_scores = {}

    # Calculate the standard deviation of ratings for each user
    for name, df in df_list.items():
        consistency_scores[name] = np.std(df['Nota Individual'].dropna())
    
    # Find the user with the smallest standard deviation
    best_consistency = min(consistency_scores, key=consistency_scores.get)
    
    return best_consistency

# Example usage with a dictionary of user dataframes (df_list)
best_consistency = best_voting_consistency(user_dfs)

# Display results
print(f"Best Voting Consistency: {best_consistency}")


# 16. Total Number of Movies Watched  
# Count the number of movies each person has watched (i.e., the number of non-empty ratings they provided).

def total_movies_watched(df_list):
    total_movies = {}

    # Count the number of non-null ratings for each user
    for name, df in df_list.items():
        total_movies[name] = df['Nota Individual'].notna().sum()

    return total_movies

# Example usage with a dictionary of user dataframes (df_list)
movies_watched = total_movies_watched(user_dfs)

# Display results
print("Total Number of Movies Watched:")
for name, count in movies_watched.items():
    print(f"{name}: {count} movies")


# 17. Average Rating for Each User  
# Calculate the average rating for each person across all movies they rated.

def average_rating_for_user(df_list):
    avg_ratings = {}

    # Calculate the average rating for each user
    for name, df in df_list.items():
        avg_ratings[name] = df['Nota Individual'].mean()
    
    return avg_ratings

# Example usage with a dictionary of user dataframes (df_list)
avg_ratings_user = average_rating_for_user(user_dfs)

# Display results
print("Average Rating for Each User:")
for name, avg in avg_ratings_user.items():
    print(f"{name}: {avg:.2f}")


# 18. Highest Rated Movie  
# Identify the movie that a person rated the highest.

def highest_rated_movie(df):
    highest_movie = df.loc[df['Nota Individual'].idxmax()]
    return highest_movie['Filme']

# Example usage with a user dataframe (df)
highest_movie = highest_rated_movie(user_dfs['joao'])

# Display result
print(f"Highest Rated Movie: {highest_movie}")


# 19. Lowest Rated Movie  
# Identify the movie that a person rated the lowest.

def lowest_rated_movie(df):
    # Find the movie with the lowest rating for the user
    lowest_movie = df.loc[df['Nota Individual'].idxmin()]
    return lowest_movie['Filme']

# Example usage with a user dataframe (df)
lowest_movie = lowest_rated_movie(user_dfs['joao'])

# Display result
print(f"Lowest Rated Movie: {lowest_movie}")

# 20. Most Frequently Suggested Movies  
# Count the number of movies each person has suggested. This can help determine who suggests the most movies.

def most_frequently_suggested_movies(main_df):
    # Count the number of times each movie was suggested
    movie_counts = main_df['Filme'].value_counts()
    
    return movie_counts

# Example usage with the main dataframe (main_df)
most_suggested_movies = most_frequently_suggested_movies(main_df)

# Display results
print("Most Frequently Suggested Movies:")
print(most_suggested_movies)


# 21. Movies with the Most Controversial Ratings  
# Identify movies that have the highest variance in ratings for each person, indicating controversial or polarizing films.

def most_controversial_movies(df_list):
    movie_ratings = {}
    
    # Gather ratings for each movie from all users
    for df in df_list.values():
        for movie, rating in zip(df['Filme'], df['Nota Individual']):
            if pd.notna(rating):
                if movie not in movie_ratings:
                    movie_ratings[movie] = []
                movie_ratings[movie].append(rating)
    
    # Calculate the variance (controversy) for each movie's ratings
    movie_variances = {movie: np.var(ratings) for movie, ratings in movie_ratings.items()}
    
    # Sort by the highest variance (most controversial)
    most_controversial = sorted(movie_variances.items(), key=lambda x: x[1], reverse=True)
    
    return most_controversial

# Example usage with a dictionary of user dataframes (df_list)
controversial_movies = most_controversial_movies(user_dfs)

# Display results
print("Movies with the Most Controversial Ratings:")
for movie, variance in controversial_movies[:5]:  # Show top 5 controversial movies
    print(f"{movie}: Variance = {variance:.2f}")


# 22. Total Hours Spent Watching Movies  
# Use the IMDb API to fetch movie runtime data and calculate the total number of hours each person has spent watching movies based on the movies they've rated.

import imdb

def total_hours_watched(df_list):
    ia = imdb.IMDb()
    total_hours = {}

    for name, df in df_list.items():
        hours_spent = 0
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the runtime of the movie in minutes
                runtime = movie_details.get('runtime', [0])[0]  # Get runtime, default to 0 if not available
                hours_spent += runtime / 60  # Convert minutes to hours
        
        total_hours[name] = hours_spent
    
    return total_hours

# Example usage with a dictionary of user dataframes (df_list)
hours_watched = total_hours_watched(user_dfs)

# Display results
print("Total Hours Spent Watching Movies:")
for name, hours in hours_watched.items():
    print(f"{name}: {hours:.2f} hours")


# 23. Genres/Categories Most Liked or Disliked  
# Analyze the genre or category of movies that each person tends to rate highly or poorly. For this, you would retrieve the genre data from the IMDb API and group the ratings by genre.

def genres_most_liked_or_disliked(df_list):
    ia = imdb.IMDb()
    genre_ratings = {}

    for name, df in df_list.items():
        genre_ratings[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the genre(s) of the movie
                genres = movie_details.get('genres', [])
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                for genre in genres:
                    if genre not in genre_ratings[name]:
                        genre_ratings[name][genre] = []
                    genre_ratings[name][genre].append(rating)
    
    # Calculate the average rating for each genre for each user
    average_genre_ratings = {}
    for name, genres in genre_ratings.items():
        average_genre_ratings[name] = {genre: np.mean(ratings) for genre, ratings in genres.items()}
    
    return average_genre_ratings

# Example usage with a dictionary of user dataframes (df_list)
liked_disliked_genres = genres_most_liked_or_disliked(user_dfs)

# Display results
print("Genres Most Liked or Disliked:")
for name, genres in liked_disliked_genres.items():
    print(f"{name}:")
    for genre, avg_rating in genres.items():
        print(f"  {genre}: {avg_rating:.2f}")


# 24. Actors or Directors Preference  
# Track which actors or directors appear in the most highly rated movies for each person. This could reveal patterns in their preferences for specific actors or directors.

def actors_or_directors_preference(df_list):
    ia = imdb.IMDb()
    preferences = {}

    for name, df in df_list.items():
        preferences[name] = {'actors': {}, 'directors': {}}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the top actors and director of the movie
                actors = movie_details.get('cast', [])
                director = movie_details.get('directors', [])
                
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                # Track actors
                for actor in actors[:3]:  # Limit to top 3 actors
                    actor_name = actor['name']
                    if actor_name not in preferences[name]['actors']:
                        preferences[name]['actors'][actor_name] = []
                    preferences[name]['actors'][actor_name].append(rating)
                
                # Track director
                if director:
                    director_name = director[0]['name']
                    if director_name not in preferences[name]['directors']:
                        preferences[name]['directors'][director_name] = []
                    preferences[name]['directors'][director_name].append(rating)
    
    # Calculate the average rating for each actor and director for each user
    avg_preferences = {}
    for name, data in preferences.items():
        avg_preferences[name] = {
            'actors': {actor: np.mean(ratings) for actor, ratings in data['actors'].items()},
            'directors': {director: np.mean(ratings) for director, ratings in data['directors'].items()}
        }
    
    return avg_preferences

# Example usage with a dictionary of user dataframes (df_list)
actor_director_preferences = actors_or_directors_preference(user_dfs)

# Display results
print("Actors or Directors Preference:")
for name, data in actor_director_preferences.items():
    print(f"{name}:")
    print("  Actors:")
    for actor, avg_rating in data['actors'].items():
        print(f"    {actor}: {avg_rating:.2f}")
    print("  Directors:")
    for director, avg_rating in data['directors'].items():
        print(f"    {director}: {avg_rating:.2f}")


# 25. Most Frequent Rating Given  
# Calculate the most common rating (e.g., 3, 4, etc.) each person gives. This can show whether they tend to be more lenient or strict in their ratings.

def most_frequent_rating_given(df_list):
    most_frequent_ratings = {}

    for name, df in df_list.items():
        most_frequent = df['Nota Individual'].mode()[0]  # Get the most frequent rating
        most_frequent_ratings[name] = most_frequent
    
    return most_frequent_ratings

# Example usage with a dictionary of user dataframes (df_list)
frequent_ratings = most_frequent_rating_given(user_dfs)

# Display results
print("Most Frequent Rating Given:")
for name, rating in frequent_ratings.items():
    print(f"{name}: {rating}")


# 26. Movie Duration and Time Spent Watching Movies  
# Using the IMDb API, retrieve the runtime for each movie and calculate the total number of hours a person has spent watching movies.

import imdb

def total_time_spent_watching_movies(df_list):
    ia = imdb.IMDb()
    total_hours = {}

    for name, df in df_list.items():
        hours_spent = 0
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the runtime of the movie in minutes
                runtime = movie_details.get('runtime', [0])[0]  # Get runtime, default to 0 if not available
                hours_spent += runtime / 60  # Convert minutes to hours
        
        total_hours[name] = hours_spent
    
    return total_hours

# Example usage with a dictionary of user dataframes (df_list)
time_spent = total_time_spent_watching_movies(user_dfs)

# Display results
print("Total Time Spent Watching Movies:")
for name, hours in time_spent.items():
    print(f"{name}: {hours:.2f} hours")


# 27. Favorite Genres  
# Use the IMDb API to gather data about the genres of the movies each person watches. You can group these by genre and calculate the average rating for each genre to see which ones are favored or disliked.

def favorite_genres(df_list):
    ia = imdb.IMDb()
    genre_ratings = {}

    for name, df in df_list.items():
        genre_ratings[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the genre(s) of the movie
                genres = movie_details.get('genres', [])
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                for genre in genres:
                    if genre not in genre_ratings[name]:
                        genre_ratings[name][genre] = []
                    genre_ratings[name][genre].append(rating)
    
    # Calculate the average rating for each genre for each user
    average_genre_ratings = {}
    for name, genres in genre_ratings.items():
        average_genre_ratings[name] = {genre: np.mean(ratings) for genre, ratings in genres.items()}
    
    return average_genre_ratings

# Example usage with a dictionary of user dataframes (df_list)
liked_genres = favorite_genres(user_dfs)

# Display results
print("Favorite Genres:")
for name, genres in liked_genres.items():
    print(f"{name}:")
    for genre, avg_rating in genres.items():
        print(f"  {genre}: {avg_rating:.2f}")


# 28. Actor Patterns  
# Retrieve information about the cast of the movies and analyze if there is any correlation between the ratings and the presence of specific actors. 

def actor_patterns(df_list):
    ia = imdb.IMDb()
    actor_ratings = {}

    for name, df in df_list.items():
        actor_ratings[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the top actors of the movie
                actors = movie_details.get('cast', [])
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                for actor in actors[:3]:  # Limit to top 3 actors
                    actor_name = actor['name']
                    if actor_name not in actor_ratings[name]:
                        actor_ratings[name][actor_name] = []
                    actor_ratings[name][actor_name].append(rating)
    
    # Calculate the average rating for each actor for each user
    avg_actor_ratings = {}
    for name, actors in actor_ratings.items():
        avg_actor_ratings[name] = {actor: np.mean(ratings) for actor, ratings in actors.items()}
    
    return avg_actor_ratings

# Example usage with a dictionary of user dataframes (df_list)
actor_preferences = actor_patterns(user_dfs)

# Display results
print("Actor Patterns:")
for name, actors in actor_preferences.items():
    print(f"{name}:")
    for actor, avg_rating in actors.items():
        print(f"  {actor}: {avg_rating:.2f}")


# 29. Director Preferences  
# Track the directors of the movies a person rates highly or poorly to reveal patterns about who they like as filmmakers.

def director_preferences(df_list):
    ia = imdb.IMDb()
    director_ratings = {}

    for name, df in df_list.items():
        director_ratings[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the director(s) of the movie
                directors = movie_details.get('directors', [])
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                for director in directors:
                    director_name = director['name']
                    if director_name not in director_ratings[name]:
                        director_ratings[name][director_name] = []
                    director_ratings[name][director_name].append(rating)
    
    # Calculate the average rating for each director for each user
    avg_director_ratings = {}
    for name, directors in director_ratings.items():
        avg_director_ratings[name] = {director: np.mean(ratings) for director, ratings in directors.items()}
    
    return avg_director_ratings

# Example usage with a dictionary of user dataframes (df_list)
director_preferences_data = director_preferences(user_dfs)

# Display results
print("Director Preferences:")
for name, directors in director_preferences_data.items():
    print(f"{name}:")
    for director, avg_rating in directors.items():
        print(f"  {director}: {avg_rating:.2f}")


# 30. Release Year Preferences  
# Analyze if a person tends to favor movies from certain decades or years.

def release_year_preferences(df_list):
    ia = imdb.IMDb()
    year_ratings = {}

    for name, df in df_list.items():
        year_ratings[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Fetch the release year of the movie
                release_year = movie_details.get('year', 0)
                rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                if release_year not in year_ratings[name]:
                    year_ratings[name][release_year] = []
                year_ratings[name][release_year].append(rating)
    
    # Calculate the average rating for each release year for each user
    avg_year_ratings = {}
    for name, years in year_ratings.items():
        avg_year_ratings[name] = {year: np.mean(ratings) for year, ratings in years.items()}
    
    return avg_year_ratings

# Example usage with a dictionary of user dataframes (df_list)
year_preferences = release_year_preferences(user_dfs)

# Display results
print("Release Year Preferences:")
for name, years in year_preferences.items():
    print(f"{name}:")
    for year, avg_rating in years.items():
        print(f"  {year}: {avg_rating:.2f}")


# 31. Movie Sentiment  
# Using IMDb's ratings or reviews (if accessible), analyze whether people rate movies more favorably or poorly based on the general sentiment or reviews of a movie.

def movie_sentiment(df_list):
    ia = imdb.IMDb()
    sentiment_comparison = {}

    for name, df in df_list.items():
        sentiment_comparison[name] = {}
        
        for movie in df['Filme']:
            # Search for the movie by title on IMDb
            movies = ia.search_movie(movie)
            if movies:
                movie_id = movies[0].getID()
                movie_details = ia.get_movie(movie_id)
                
                # Get IMDb's rating for the movie
                imdb_rating = movie_details.get('rating', 0)
                user_rating = df[df['Filme'] == movie]['Nota Individual'].values[0]  # Get the user's rating for the movie
                
                sentiment_comparison[name][movie] = {'user_rating': user_rating, 'imdb_rating': imdb_rating}
    
    return sentiment_comparison

# Example usage with a dictionary of user dataframes (df_list)
sentiment_data = movie_sentiment(user_dfs)

# Display results
print("Movie Sentiment Comparison:")
for name, movies in sentiment_data.items():
    print(f"{name}:")
    for movie, ratings in movies.items():
        print(f"  {movie}: User Rating = {ratings['user_rating']}, IMDb Rating = {ratings['imdb_rating']}")



