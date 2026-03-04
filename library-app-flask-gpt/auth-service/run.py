from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # For production use a WSGI server like gunicorn; this is for local dev.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=(app.config["ENV"] == "development"))
