"""Ќ бва®©Є  Ї®¤Є«озҐ­Ёп Є Ў §Ґ ¤ ­­ле SQLite."""

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase



SQLALCHEMY_DATABASE_URL = "sqlite:///./taskmanager.db"



engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





class Base(DeclarativeBase):

    """Ѓ §®ўл© Є« бб ¤«п ўбҐе ¬®¤Ґ«Ґ©."""

    pass





def get_db():

    """ѓҐ­Ґа в®а бҐббЁ© Ў §л ¤ ­­ле."""

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

