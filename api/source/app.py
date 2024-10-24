from api import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()
## Note: uncommenting this breaks gunicorn
# app.run(debug=True)