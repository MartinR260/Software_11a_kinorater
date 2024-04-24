import azure.functions as func
import logging
import pyodbc

connection_string = "DRIVER={SQL Server};SERVER=kinorater1sqldbserver;DATABASE=kinorater1db;UID=martinadmin;PWD=admin123!"
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="calculate_average_ratings")
def calculate_average_ratings(req: func.TimerRequest) -> None:
    logging.info('Python timer trigger function processed a request.')

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT MovieTitle FROM Movies")
        movies = cursor.fetchall()

        for movie in movies:
            movie_title = movie[0]
            cursor.execute("SELECT AVG(Rating) FROM Ratings WHERE Title=?", (movie_title,))
            average_rating = cursor.fetchone()[0]
            if average_rating is not None:
                cursor.execute("UPDATE Movies SET MovieAverageRating=? WHERE MovieTitle=?", (average_rating, movie_title))
                conn.commit()

    except Exception as e:
        logging.error(str(e))
    finally:
        cursor.close()
        conn.close()