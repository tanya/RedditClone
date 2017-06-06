from reddit import app,db
import os

if __name__ == '__main__':
    db.create_all()
    app.run(port=5002,debug=True)
