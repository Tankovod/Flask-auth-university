from flask_sqlalchemy import SQLAlchemy


class Settings:
    DB_URL = "postgresql://univer:univer@localhost:5432/univer"
    SQLITE_URL = "sqlite:///db.sqlite"
    db_lite = SQLAlchemy()


settings = Settings()
