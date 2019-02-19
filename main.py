from service import app, db
from service.models import User, init_db, drop_db

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
