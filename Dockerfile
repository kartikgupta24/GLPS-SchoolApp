# Start with a base Python image
FROM python:3.9-slim

# Install ODBC Driver 17 for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    gnupg2 \
    tds-dev \
    libxml2-dev \
    zlib1g-dev \
    libssl-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-tools.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    msodbcsql17 \
    mssql-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variables for the driver
ENV PATH="/opt/mssql-tools/bin:${PATH}"

# Command to run the application
CMD ["streamlit", "run", "your_app.py"]