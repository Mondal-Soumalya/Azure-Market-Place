# FROM python:3.11-slim

# WORKDIR /app

# # Install ONLY Node.js (for building React)
# RUN apt-get update && apt-get install -y \
#     curl \
#     && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
#     && apt-get install -y nodejs \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Copy code
# COPY . .

# # Build React
# WORKDIR /app/Frontend
# RUN npm install && npm run build

# # Return to backend
# WORKDIR /app

# # Create folders
# RUN mkdir -p SubmittedFiles/IncidentFiles SubmittedFiles/ServiceDeskFiles TempFilesDump

# EXPOSE 5000
# ENV FLASK_APP=app.py
# ENV PYTHONUNBUFFERED=1

# CMD ["python", "app.py"]

##############################################################################################################

#############################################
# Stage 1: Frontend Builder (Node)
#############################################
FROM node:20 AS frontend-builder

# Set working directory for frontend
WORKDIR /app/Frontend

# Install dependencies
COPY Frontend/package*.json ./
RUN npm install

# Copy all frontend code and build React/Vite app
COPY Frontend .
RUN npm run build



#############################################
# Stage 2: Backend Runtime (Python)
#############################################
FROM python:3.11-slim AS backend

# Backend working directory
WORKDIR /app

#############################################
# Install Python dependencies
#############################################
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#############################################
# Copy backend application code
#############################################
COPY Backend Backend
COPY DatabaseHandler DatabaseHandler
COPY app.py .
COPY .env .env

#############################################
# Copy ONLY the built React app (DO NOT copy the whole Frontend folder)
#############################################
RUN mkdir -p Frontend
COPY --from=frontend-builder /app/Frontend/dist ./Frontend/dist

#############################################
# Create runtime folders (empty folders required by your app)
#############################################
RUN mkdir -p SubmittedFiles/IncidentFiles
RUN mkdir -p SubmittedFiles/ServiceDeskFiles
RUN mkdir -p TempFilesDump

#############################################
# Expose Flask port
#############################################
EXPOSE 5000

#############################################
# Environment config
#############################################
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

#############################################
# Start Flask application
#############################################
CMD ["python", "app.py"]