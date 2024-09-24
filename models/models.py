import datetime
from typing import Annotated
from sqlalchemy import MetaData, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base

int_pk = Annotated[int, mapped_column(primary_key=True)]
metadata_obj = MetaData()

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"

    author_id: Mapped[int_pk]
    name_author: Mapped[str]
    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Genre(Base):
    __tablename__ = "genre"

    genre_id: Mapped[int_pk]
    name_genre: Mapped[str]
    books: Mapped[list["Book"]] = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[int_pk]
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.author_id", ondelete="CASCADE"), nullable=False
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.genre_id", ondelete="CASCADE"), nullable=False
    )
    price: Mapped[int]
    amount: Mapped[int]

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    buys: Mapped[list["BuyBook"]] = relationship("BuyBook", back_populates="book")


class Buy(Base):
    __tablename__ = "buy"

    buy_id: Mapped[int_pk]
    buy_description: Mapped[str]
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.client_id", ondelete="CASCADE"), nullable=False
    )

    client: Mapped["Client"] = relationship("Client", back_populates="buys")
    books: Mapped[list["BuyBook"]] = relationship("BuyBook", back_populates="buy")
    steps: Mapped[list["BuyStep"]] = relationship("BuyStep", back_populates="buy")


class BuyBook(Base):
    __tablename__ = "buy_book"

    buy_book_id: Mapped[int_pk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buy.buy_id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int]

    buy: Mapped["Buy"] = relationship("Buy", back_populates="books")
    book: Mapped["Book"] = relationship("Book", back_populates="buys")


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[int_pk]
    name_client: Mapped[str]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.city_id", ondelete="CASCADE"), nullable=False
    )

    city: Mapped["City"] = relationship("City", back_populates="clients")
    buys: Mapped[list["Buy"]] = relationship("Buy", back_populates="client")


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[int_pk]
    name_city: Mapped[str] = mapped_column(unique=True, nullable=False)
    days_delivery: Mapped[int]

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="city")


class Step(Base):
    __tablename__ = "step"

    step_id: Mapped[int_pk]
    name_step: Mapped[str]

    buy_steps: Mapped[list["BuyStep"]] = relationship("BuyStep", back_populates="step")


class BuyStep(Base):
    __tablename__ = "buy_step"

    buy_step_id: Mapped[int_pk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buy.buy_id", ondelete="CASCADE"), nullable=False
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey("step.step_id", ondelete="CASCADE"), nullable=False
    )
    date_step_beg: Mapped[datetime.datetime] = mapped_column(DateTime)
    date_step_end: Mapped[datetime.datetime | None] = mapped_column(DateTime)

    buy: Mapped["Buy"] = relationship("Buy", back_populates="steps")
    step: Mapped["Step"] = relationship("Step", back_populates="buy_steps")
