from service import app, db
from service.models import User, init_db, drop_db

if __name__ == '__main__':
    try:
        init_db()
    except:
        db.session.rollback()
        drop_db()
        init_db()
    app.run(host='127.0.0.1', port=5000)
