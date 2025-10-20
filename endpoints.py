from flask import Flask, jsonify
from raspagem import df

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)
