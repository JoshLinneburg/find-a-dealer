import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir)

from flask.cli import FlaskGroup
from api import create_app

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    app.run(debug=True)