FROM python:3.10.4

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the source code
COPY . .

# Expose the application's port
EXPOSE 5000

# Set the entrypoint to gunicorn
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
