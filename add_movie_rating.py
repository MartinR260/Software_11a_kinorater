import azure.functions as func
import logging
import pyodbc

connection_string = "DRIVER={SQL Server};SERVER=kinorater1sqldbserver;DATABASE=kinorater1db;UID=martinadmin;PWD=admin123!"
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="add_movie_rating")
def add_movie_rating(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rating_data = req.get_json()

    if rating_data:
        title = rating_data.get('title')
        opinion = rating_data.get('opinion')
        rating = rating_data.get('rating')
        rating_datetime = datetime.strptime(rating_data.get('datetime'), "%Y-%m-%d %H:%M:%S")
        author = rating_data.get('author')

        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Ratings (Title, RatingOpinion, Rating, RatingDateTime, RatingAuthor) VALUES (?, ?, ?, ?, ?)", (title, opinion, rating, rating_datetime, author))
            conn.commit()

            return func.HttpResponse(f"Rating for movie '{title}' added successfully.", status_code=200)
        except Exception as e:
            logging.error(str(e))
            return func.HttpResponse("An error occurred while processing the request.", status_code=500)
        finally:
            cursor.close()
            conn.close()
    else:
        return func.HttpResponse("No rating data provided.", status_code=400)
