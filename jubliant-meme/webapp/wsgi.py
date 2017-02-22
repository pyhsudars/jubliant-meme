import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'FlaskApp'))
)
from FlaskApp import app, createApp


createApp(app)

if __name__ == "__main__":
    app.run()
