# ⚽ Soccer Statistics Analysis - Web App

A beautiful, mobile-friendly web application for analyzing soccer statistics with interactive visualizations.

## 🚀 Quick Start

### Prerequisites

- **Python 3.11** (recommended) or Python 3.10
- Download from: https://www.python.org/downloads/
- ⚠️ **Important**: Check "Add Python to PATH" during Windows installation

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`

## 🌐 Free Online Hosting

### Option 1: Streamlit Cloud (Recommended - Easiest)

1. **Create a GitHub account** (if you don't have one)
2. **Push this code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```
3. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
4. **Sign in with GitHub**
5. **Click "New app"**
6. **Select your repository and branch**
7. **Set main file path:** `app.py`
8. **Click "Deploy"** - Your app will be live in minutes!

Your app will be available at: `https://your-app-name.streamlit.app`

### Option 2: Other Free Hosting Options

- **Render**: [render.com](https://render.com) - Free tier available
- **Railway**: [railway.app](https://railway.app) - Free tier available
- **Heroku**: Limited free tier (may require credit card)

## 📱 Features

- ✅ **Mobile-Responsive Design** - Works perfectly on phones and tablets
- ✅ **Interactive Charts** - Powered by Plotly
- ✅ **Multiple Leagues** - Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- ✅ **Multiple Seasons** - Analyze data from 2018 to present
- ✅ **Real-time Data** - Fetches live data from FBref
- ✅ **Team Comparison** - Compare multiple teams side-by-side
- ✅ **Top Scorers** - View leading goal scorers
- ✅ **Beautiful UI** - Modern gradient design

## 📊 Available Visualizations

1. **Goals Scatter Plot** - Goals for vs goals against with points overlay
2. **League Standings** - Points distribution bar chart
3. **Goal Difference** - Visual representation of goal difference
4. **Win Rate** - Win percentage by team
5. **Top Scorers** - Leading goal scorers chart
6. **Team Comparison** - Side-by-side team statistics

## 🛠️ Customization

### Change Default League
Edit `app.py` and modify the `selected_league_name` default in the sidebar.

### Add More Leagues
Add to the `leagues` dictionary in the sidebar section:
```python
leagues = {
    "Your League": "LEAGUE-CODE",
    ...
}
```

### Modify Charts
All chart functions are in `app.py` and can be customized:
- `create_goals_scatter()`
- `create_points_chart()`
- `create_goal_difference_chart()`
- `create_win_rate_chart()`
- `create_top_scorers_chart()`

## 📦 Project Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## 🔧 Troubleshooting

### Data Fetching Issues
- Check your internet connection
- Some leagues may not have data for all seasons
- Try a different season if data is unavailable

### Installation Issues
- Make sure Python 3.8+ is installed
- Use `python -m pip install -r requirements.txt` if `pip` doesn't work

### Deployment Issues
- Ensure `requirements.txt` includes all dependencies
- Check that `app.py` is in the root directory
- Verify the main file path in hosting settings

## 📝 Notes

- Data is cached for 1 hour to improve performance
- First load may take a few seconds while fetching data
- The app uses the `soccerdata` library which scrapes data from FBref
- Please use responsibly and in compliance with website terms of service

## 🎨 Features in Detail

### Mobile-Friendly
- Responsive design that adapts to screen size
- Touch-friendly controls
- Optimized for portrait and landscape modes

### Interactive Charts
- Hover to see detailed information
- Zoom and pan on charts
- Download charts as images
- Responsive to screen size

### Data Caching
- Data is cached for 1 hour
- Faster subsequent loads
- Reduces API calls

## 📄 License

This project uses the soccerdata library. Please refer to the [soccerdata repository](https://github.com/probberechts/soccerdata) for licensing information.

## 🤝 Contributing

Feel free to fork this project and add your own features!

---

**Made with ⚽ and ❤️**
