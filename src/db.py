from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3', echo=False)
Session = sessionmaker(bind=engine)


class Song(Base):
    __tablename__ = 'songs'

    # Default fields
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # from Spotify API
    song_name = Column(String)
    artist_name = Column(String)
    album_name = Column(String)
    popularity = Column(Integer)
    duration_ms = Column(String)
    explicit = Column(Boolean)
    spotify_uri = Column(String)
    album_image = Column(String)

    # From scraper
    scraper_name = Column(String)
    playlist_id = Column(String)
