from dotenv import load_dotenv
import os

load_dotenv()
from backend import create_app


env = os.environ["FLASK_ENV"]  # crash if missing


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=env != "production",
    )
