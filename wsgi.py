"""
wsgi.py
-------

A WSGI entry point for running the Flask application.

This file can be used to run the Flask app locally or to deploy the app to a WSGI server like Gunicorn.
"""

from app.main import flask_app

# Run the Flask app
if __name__ == "__main__":
    flask_app.run(debug=True)