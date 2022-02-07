from flask import Flask
from kruver import ImageManipulater,insert_db

app=Flask(__name__)


@app.route("/")
def index():
    return "hello world"

@app.route("/upload")
def glitch():
    test=ImageManipulater()
    test.find_image()
    test.sort()
    test.upload()
    insert_db(vars(test))
    return str(vars(test))

if __name__ =="__main__":
    app.run(debug=True)