# Start FROM the official Selenium Firefox standalone image
FROM selenium/standalone-firefox:4.31.0-20250404

# Selenium images run as the 'seluser'. Switch to root temporarily
# only if you need to install system packages. Otherwise, try to avoid.
# USER root
# RUN apt-get update && apt-get install -y --no-install-recommends python3-pip <any-other-system-packages> && \
#     rm -rf /var/lib/apt/lists/*
# USER seluser # Switch back to the non-root user

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script requirements file (if you have one)
COPY requirements.txt .

# Install your Python script's dependencies
# Note: Ensure pip is available. The base image might have it,
# but if not, you'd need to install python3-pip as root (see commented section above)
# Use --user if installing as non-root seluser to avoid permission issues
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy everything from the current directory (build context)
# into the container's working directory (/app)
COPY . .

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "./main.py"]
