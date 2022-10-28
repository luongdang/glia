from contextlib import contextmanager

from .models import Log, SessionLocal


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_latest_log(n: int):
    with get_db() as db:
        return db.query(Log).order_by(Log.date.desc()).limit(n)


def add_log(**kwargs):
    log = Log(**kwargs)
    with get_db() as db:
        db.add(log)
        db.commit()
