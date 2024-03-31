import azure.functions as func
import json
import pyodbc
import datetime
import statistics

def get_database_connection():
    server = 'cineratersqlserver.database.windows.net'
    database = 'cineraterdb'
    username = 'martinr14'
    password = 'MartinR1!'
    driver = 'ODBC Driver 17 for SQL Server'  
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(connection_string)

def add_movie_info(title, year, genre, description, director, actors):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Movies (MovieTitle, MovieYear, MovieGenre, MovieDescription, MovieDirector, MovieActors) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, year, genre, description, director, actors))
        conn.commit()
        return "Movie information added successfully."
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def add_movie_rating(title, opinion, rating, author):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        current_datetime = datetime.datetime.now()
        cursor.execute("INSERT INTO Ratings (Title, RatingOpinion, Rating, RatingDateTime, RatingAuthor) VALUES (?, ?, ?, ?, ?)",
                       (title, opinion, rating, current_datetime, author))
        conn.commit()
        return "Rating added successfully."
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def calculate_average_ratings():
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Title, AVG(Rating) AS MovieAverageRating FROM Ratings GROUP BY Title")
        average_ratings = cursor.fetchall()

        for row in average_ratings:
            title, average_rating = row
            cursor.execute("UPDATE Movies SET MovieAverageRating = ? WHERE MovieTitle = ?", (average_rating, title))
            conn.commit()

        return "Average ratings calculated and updated successfully."
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def search_movie_by_title(title=None):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        if title:
            cursor.execute("SELECT * FROM Movies WHERE MovieTitle LIKE ?", ('%' + title + '%',))
        else:
            cursor.execute("SELECT * FROM Movies")

        movies = cursor.fetchall()
        return movies
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def main(req: func.HttpRequest) -> func.HttpResponse:
    action = req.params.get('action')
    
    if action == 'add_movie_info':
        req_body = req.get_json()
        title = req_body.get('title')
        year = req_body.get('year')
        genre = req_body.get('genre')
        description = req_body.get('description')
        director = req_body.get('director')
        actors = req_body.get('actors')
        result = add_movie_info(title, year, genre, description, director, actors)
        return func.HttpResponse(result)
    
    elif action == 'add_movie_rating':
        req_body = req.get_json()
        title = req_body.get('title')
        opinion = req_body.get('opinion')
        rating = req_body.get('rating')
        author = req_body.get('author')
        result = add_movie_rating(title, opinion, rating, author)
        return func.HttpResponse(result)
    
    elif action == 'calculate_average_ratings':
        result = calculate_average_ratings()
        return func.HttpResponse(result)
    
    elif action == 'search_movie_by_title':
        title = req.params.get('title')
        movies = search_movie_by_title(title)
        movie_list = []
        for movie in movies:
            movie_dict = {
                'Title': movie.MovieTitle,
                'Year': movie.MovieYear,
                'Genre': movie.MovieGenre,
                'Description': movie.MovieDescription,
                'Director': movie.MovieDirector,
                'Actors': movie.MovieActors,
                'AverageRating': movie.MovieAverageRating
            }
            movie_list.append(movie_dict)
        return func.HttpResponse(body=json.dumps(movie_list), mimetype='application/json')
    
    else:
        return func.HttpResponse("Invalid action", status_code=400)
