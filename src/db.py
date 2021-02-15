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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Default fields
    playlist_id = Column(String, primary_key=True)
    spotify_uri = Column(String, primary_key=True)

    # from Spotify API
    song_name = Column(String)
    artist_name = Column(String)
    album_name = Column(String)
    popularity = Column(Integer)
    duration_ms = Column(String)
    explicit = Column(Boolean)
    album_image = Column(String)

    # From scraper
    scraper_name = Column(String)
