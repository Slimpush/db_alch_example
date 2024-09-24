from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from models.models import Base, Client, City
from models.models import Author, Book, Genre


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BaseModel = Base

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = Session()

    city1 = City(name_city="Moscow", days_delivery=5)
    city2 = City(name_city="Saint Petersburg", days_delivery=3)

    client1 = Client(name_client="Ivan Ivanov", city=city1)
    client2 = Client(name_client="Petr Petrov", city=city2)

    author1 = Author(name_author="Fyodor Dostoevsky")
    author2 = Author(name_author="Leo Tolstoy")

    genre1 = Genre(name_genre="Classic Literature")
    genre2 = Genre(name_genre="Historical Fiction")

    book1 = Book(
        title="Crime and Punishment", author=author1, genre=genre1, price=500, amount=10
    )
    book2 = Book(
        title="War and Peace", author=author2, genre=genre2, price=700, amount=5
    )

    session.add_all(
        [city1, city2, client1, client2, author1, author2, genre1, genre2, book1, book2]
    )
    session.commit()
    session.close()
