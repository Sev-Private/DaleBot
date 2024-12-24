# Movie Rating Analysis - Metrics and Insights

This project provides a set of metrics and insights to analyze the movie ratings given by a group of friends. The metrics cover various aspects such as suggestions, ratings, preferences, and trends over time. Additionally, we have integrated IMDb data (e.g., genres, actors, runtime) to enhance the analysis.

## Suggestion and Participation Metrics

1. **Most and Least Suggestions**  
   Count how many movies each friend has suggested to identify who suggested the most and the least movies.

2. **Most and Least Participation**  
   Count how many movies each person has voted on to determine who has participated in rating the most and least movies.

---

## Voting Patterns and Preferences

3. **Average Rating Given by Each Person**  
   Calculate the average rating each person gives to see who tends to rate movies higher or lower on average.

4. **Average Rating for Each Person's Suggested Movies**  
   Find out how well each person's suggested movies are received on average.

5. **Most Generous and Most Critical Viewers**  
   Identify who has the highest and lowest average votes when rating others' suggestions.

---

## Best and Worst Suggestions

6. **Highest and Lowest Rated Movies**  
   Identify the movie with the highest and lowest average scores, and track who suggested them.

7. **Top and Bottom Suggesters**  
   Find out who suggested the movies with the highest and lowest average ratings across all their suggestions.

---

## Controversy and Consensus

8. **Most Controversial Movie**  
   Find the movie with the highest standard deviation or widest range in votes to identify the most polarizing movie.

9. **Most Consensual Movie**  
   Identify the movie with the lowest standard deviation or smallest range in votes, showing the movie with the most similar ratings from everyone.

---

## Other Interesting Metrics

10. **Personal Best/Worst Suggestions**  
    For each person, find their most and least liked movie based on group ratings.

11. **Suggesters' Impact on the Group's Average Rating**  
    Analyze how each person's movie choices affect the overall average rating for the group.

12. **Highest Rated Movies by Genre**  
    If the spreadsheet includes genres, determine which friend tends to suggest the highest-rated movies by genre.

13. **Trend Over Time**  
    See if the group's ratings or a specific person's ratings have changed over time to spot trends in taste or voting behavior.

14. **Most Similar and Different Tastes**  
    Compare the average ratings between pairs of friends to find out who has the most and least similar tastes.

15. **Best Voting Consistency**  
    Identify who has the most consistent voting pattern (smallest standard deviation in their own votes).

---

## User-Specific Metrics

16. **Total Number of Movies Watched**  
    Count the number of movies each person has watched (i.e., the number of non-empty ratings they provided).

17. **Average Rating for Each User**  
    Calculate the average rating for each person across all movies they rated. This provides insight into their general sentiment towards the movies.

18. **Highest Rated Movie**  
    Identify the movie that a person rated the highest.

19. **Lowest Rated Movie**  
    Identify the movie that a person rated the lowest.

20. **Most Frequently Suggested Movies**  
    Count the number of movies each person has suggested. This can help determine who suggests the most movies.

21. **Movies with the Most Controversial Ratings**  
    Identify movies that have the highest variance in ratings for each person, indicating controversial or polarizing films.

22. **Total Hours Spent Watching Movies**  
    Use the IMDb API to fetch movie runtime data and calculate the total number of hours each person has spent watching movies based on the movies they've rated.

23. **Genres/Categories Most Liked or Disliked**  
    Analyze the genre or category of movies that each person tends to rate highly or poorly. For this, you would retrieve the genre data from the IMDb API and group the ratings by genre.

24. **Actors or Directors Preference**  
    Track which actors or directors appear in the most highly rated movies for each person. This could reveal patterns in their preferences for specific actors or directors.

25. **Most Frequent Rating Given**  
    Calculate the most common rating (e.g., 3, 4, etc.) each person gives. This can show whether they tend to be more lenient or strict in their ratings.

---

## IMDb-Related Metrics

26. **Movie Duration and Time Spent Watching Movies**  
    Using the IMDb API, retrieve the runtime for each movie and calculate the total number of hours a person has spent watching movies.

27. **Favorite Genres**  
    Use the IMDb API to gather data about the genres of the movies each person watches. You can group these by genre and calculate the average rating for each genre to see which ones are favored or disliked.

28. **Actor Patterns**  
    Retrieve information about the cast of the movies and analyze if there is any correlation between the ratings and the presence of specific actors. For example, does a person consistently rate movies with a certain actor highly?

29. **Director Preferences**  
    Similar to actors, you can also track the directors of the movies a person rates highly or poorly. This could reveal patterns about who they like as filmmakers.

30. **Release Year Preferences**  
    Analyze if a person tends to favor movies from certain decades or years. This can help in understanding whether they are more inclined towards classic films or more contemporary ones.

31. **Movie Sentiment**  
    Using IMDb's ratings or reviews (if accessible), you could analyze whether people rate movies more favorably or poorly based on the general sentiment or reviews of a movie. You could cross-reference their ratings with the IMDb ratings to see if their preferences align with general audiences.

---

## Advanced IMDb-Related Ideas

32. **Collaborative Filtering**  
    Based on user ratings, you can implement collaborative filtering to suggest new movies to each person based on their preferences. This could be done using the ratings provided by similar users (those who have rated movies similarly in the past).

33. **Clustering of Preferences**  
    You could cluster users based on their preferences and suggest movies that are popular within a cluster. For example, if a group of people tends to rate movies in a particular genre similarly, you could suggest movies within that genre.

34. **Sentiment Analysis for Detailed Insights**  
    Use sentiment analysis on IMDb reviews to gather insights into how each user feels about movies beyond just numeric ratings. This would involve processing the text of movie reviews to categorize them as positive, negative, or neutral and see if their ratings align with sentiment.

35. **Actor-Director Collaborations**  
    If you observe that a person consistently enjoys movies by a specific director or featuring certain actors, you can analyze the common collaborations between those actors and directors. This might uncover hidden preferences they haven't explicitly noted in their ratings.

