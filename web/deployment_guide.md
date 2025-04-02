# Streamlit Deployment Guide

## Option 1: Streamlit Cloud (Easiest)

1. Create a GitHub repository and push your code:
   ```bash
   git init
   git add web/steel_calculator.py
   git add requirements.txt  # Create this file with dependencies
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/steel-calculator.git
   git push -u origin main
   ```

2. Create a `requirements.txt` file with:
   ```
   streamlit
   pandas
   xlsxwriter
   ```

3. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub
4. Click "New app" and select your repository
5. Set the main file path to `web/steel_calculator.py`
6. Click "Deploy"

Your app will be available at a URL like: `https://yourusername-steel-calculator-web-steel-calculator-xxxx.streamlit.app`

## Option 2: Deploy to Heroku

1. Create a `requirements.txt` file with all dependencies
2. Create a `Procfile` with:
   ```
   web: streamlit run web/steel_calculator.py --server.port=$PORT
   ```
3. Create a `setup.sh` file:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```
4. Install Heroku CLI and deploy:
   ```bash
   heroku login
   heroku create steel-calculator-app
   git push heroku main
   ```

## Option 3: Deploy to a VPS (Digital Ocean, AWS EC2, etc.)

1. Set up a VPS with Ubuntu
2. Install Python and dependencies
3. Clone your repository
4. Set up a systemd service to run your app
5. Configure Nginx as a reverse proxy
6. Set up SSL with Let's Encrypt

## Option 4: Docker Deployment

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "web/steel_calculator.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t steel-calculator .
   docker run -p 8501:8501 steel-calculator
   ```

3. Deploy to a container service like AWS ECS, Google Cloud Run, or Azure Container Instances
