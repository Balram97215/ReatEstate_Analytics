# Deployment Guide for Streamlit

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Streamlit Cloud Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and main file: `app.py`
5. Click "Deploy"

### 3. Configure Secrets
In Streamlit Cloud:
1. Go to your app settings → Secrets
2. Add any required environment variables

## Key Configuration Files

- **config.py** - Main configuration (Google Drive ID, database settings)
- **.streamlit/config.toml** - Streamlit theme and UI settings
- **requirements.txt** - Python dependencies
- **.gitignore** - Files to exclude from version control

## Data Flow

1. User opens app.py
2. App checks if database exists locally
3. If not, downloads from Google Drive (first run only)
4. All queries use cached database connection
5. Data is cached for 1 hour (see queries.py)

## Troubleshooting

### Database Download Issues
- Check Google Drive file ID in config.py
- Ensure file is publicly shareable or accessible to your account
- Check internet connection

### Query Errors
- Verify database schema matches column names in queries.py
- Check that silver_parcels table exists
- Run test queries in sqlite3 directly

### Performance Issues
- Data is cached by Streamlit (TTL: 1 hour)
- Adjust cache duration in queries.py if needed
- Use @st.cache_data(ttl=3600) decorator

## Updates

To add new dashboards:
1. Create new page file in `pages/` directory
2. Add queries in `queries.py`
3. Use page naming convention: `NN_page_name.py`
4. Streamlit will auto-detect and add to navigation
