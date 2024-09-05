# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system packages needed for pygit2 and GitPython, and install Python dependencies directly
RUN apt-get update && \
    apt-get install -y libgit2-dev git && \
    pip install --no-cache-dir pyyaml pygit2 gitpython && \
    apt-get clean

# Make sure all .py files are executable
RUN chmod +x *.py

# Run the main.py script when the container launches
ENTRYPOINT ["python", "main.py"]

# Default command to run with scale-type, you can override this with Docker run arguments
CMD ["--scale-type", "scale_up"]
