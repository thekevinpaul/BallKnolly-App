# 🚀 Deployment Guide - Streamlit Cloud

## Step-by-Step Deployment Instructions

### Prerequisites
- GitHub account (free)
- This code pushed to a GitHub repository

### Deployment Steps

#### 1. Push Code to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Soccer Analysis App"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud

1. **Go to [streamlit.io/cloud](https://streamlit.io/cloud)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Fill in the details:**
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom name (e.g., `soccer-analysis`)
5. **Click "Deploy"**

#### 3. Wait for Deployment

- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Build your app
  - Deploy it

- This usually takes 2-5 minutes

#### 4. Access Your App

Once deployed, your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

### Updating Your App

1. Make changes to your code
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Updated app"
   git push
   ```
3. Streamlit Cloud will automatically redeploy!

### Troubleshooting

**App won't deploy:**
- Check that `app.py` is in the root directory
- Verify `requirements.txt` has all dependencies
- Check the logs in Streamlit Cloud dashboard

**Dependencies not installing:**
- Make sure all packages are in `requirements.txt`
- Check for version conflicts

**App crashes:**
- Check the logs in Streamlit Cloud
- Test locally first: `streamlit run app.py`

## Alternative: Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.
