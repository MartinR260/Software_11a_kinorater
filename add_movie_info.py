import azure.functions as func
import logging
import pyodbc


connection_string = "DRIVER={SQL Server};SERVER=kinorater1sqldbserver;DATABASE=kinorater1db;UID=martinadmin;PWD=admin123!"
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="add_movie_info")
def add_movie_info(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    movie_data = req.get_json()

    if movie_data:
        title = movie_data.get('title')
        year = movie_data.get('year')
        genre = movie_data.get('genre')
        description = movie_data.get('description')
        director = movie_data.get('director')
        actors = movie_data.get('actors')

        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Movies (MovieTitle, MovieYear, MovieGenre, MovieDescription, MovieDirector, MovieActors) VALUES (?, ?, ?, ?, ?, ?)", (title, year, genre, description, director, actors))
            conn.commit()

            return func.HttpResponse(f"Movie '{title}' added successfully.", status_code=200)
        except Exception as e:
            logging.error(str(e))
            return func.HttpResponse("An error occurred while processing the request.", status_code=500)
        finally:
            cursor.close()
            conn.close()
    else:
        return func.HttpResponse("No movie data provided.", status_code=400)
