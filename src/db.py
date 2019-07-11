from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    song_name = Column(String)
    artist_name = Column(String)
    album_name = Column(String)
    popularity = Column(Integer)
    duration_ms = Column(String)
    explicit = Column(Boolean)
    spotify_uri = Column(String, unique=True)
    album_image = Column(String)
