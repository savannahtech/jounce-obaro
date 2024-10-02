# Use an official Python runtime as a parent image
FROM python:3.12.6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ../ /app

# RUN ls
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["uvicorn", "metric_benchmark.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
