from sqlalchemy import text
from config import settings
from database import Base, engine
import pytest

class TestConnectionDB:
    def test_connect(self):
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 'hello world'"))
            assert res.all()[0][0] == 'hello world'

    def test_get_mode_db(self):
        assert settings.database.POSTGRES_MODE == 'TEST'