CREATE TABLE Movies (
    MovieTitle NVARCHAR(255) PRIMARY KEY,
    MovieYear INT,
    MovieGenre NVARCHAR(255),
    MovieDescription NVARCHAR(MAX),
    MovieDirector NVARCHAR(255),
    MovieActors NVARCHAR(MAX),
    MovieAverageRating DECIMAL(5,2)
);

CREATE TABLE Ratings (
    RatingId INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(255) NOT NULL,
    RatingOpinion NVARCHAR(MAX),
    Rating INT,
    RatingDateTime DATETIME,
    RatingAuthor NVARCHAR(255),
    FOREIGN KEY (Title) REFERENCES Movies(MovieTitle) ON DELETE CASCADE
);