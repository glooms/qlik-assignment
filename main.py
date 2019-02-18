from service import app, db
from service.models import init_db, drop_db

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    try:
        init_db()
    except:
        db.session.rollback()
        drop_db()
    init_db()
