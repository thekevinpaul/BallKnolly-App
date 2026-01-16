"""
Premier League Stats Hub - Comprehensive Player Analysis
Live data with detailed player statistics
Official PL Branding
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import base64
import os

# Page config
st.set_page_config(
    page_title="Premier League Stats",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Get the directory where app.py is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Load local PL logo
def get_logo_base64():
    """Load local PL logo as base64"""
    try:
        png_path = os.path.join(APP_DIR, "imgs", "Premier League_Logo_Alternative_1.png")
        if os.path.exists(png_path):
            with open(png_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        pass
    return None

LOGO_BASE64 = get_logo_base64()

# Official PL Brand Colors
PL_PURPLE = "#37003c"
PL_MAGENTA = "#ff2882"
PL_CYAN = "#04f5ff"
PL_GREEN = "#00ff85"
PL_WHITE = "#FFFFFF"
PL_OFFWHITE = "#f8f8f8"

# Season data
SEASONS = ['2024/25', '2023/24', '2022/23', '2021/22', '2020/21', '2019/20', '2018/19']
SEASON_API_MAP = {'2024/25': '2024', '2023/24': '2023', '2022/23': '2022', '2021/22': '2021', '2020/21': '2020', '2019/20': '2019', '2018/19': '2018'}

# Player comparison colors
PLAYER_COLORS = [PL_MAGENTA, PL_CYAN, PL_GREEN, "#ffd700", "#ff6b35"]

# Professional CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {{
    --pl-purple: {PL_PURPLE};
    --pl-magenta: {PL_MAGENTA};
    --pl-cyan: {PL_CYAN};
    --pl-green: {PL_GREEN};
    --pl-white: {PL_WHITE};
    --pl-offwhite: {PL_OFFWHITE};
}}

* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp {{
    background: var(--pl-offwhite) !important;
}}

#MainMenu, footer, header, [data-testid="stToolbar"] {{
    display: none !important;
}}

.main .block-container {{
    padding: 0;
    max-width: 100%;
}}

/* Header */
.pl-header {{
    background: linear-gradient(135deg, var(--pl-purple) 0%, #1a001e 100%);
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    border-bottom: 4px solid var(--pl-magenta);
}}

.pl-logo {{
    height: 70px;
    width: auto;
}}

.pl-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: var(--pl-white);
    margin: 0;
    letter-spacing: 3px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}

.pl-subtitle {{
    color: var(--pl-cyan);
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0.25rem 0 0 0;
}}

/* Content */
.content-area {{
    padding: 1.5rem 2rem;
    max-width: 1600px;
    margin: 0 auto;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: var(--pl-purple);
    border-radius: 8px 8px 0 0;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: rgba(255,255,255,0.7);
    padding: 1rem 1.5rem;
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: none;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: white;
    background: rgba(255,255,255,0.1);
}}

.stTabs [aria-selected="true"] {{
    background: var(--pl-magenta) !important;
    color: white !important;
}}

.stTabs [data-baseweb="tab-panel"] {{
    background: white;
    border-radius: 0 0 8px 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

/* Section headers */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid var(--pl-purple);
}}

.section-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--pl-purple);
    margin: 0;
    letter-spacing: 1px;
}}

/* Stats grid */
.stats-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1rem;
}}

.stat-card {{
    background: white;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-left: 4px solid var(--pl-magenta);
    transition: transform 0.2s;
}}

.stat-card:hover {{
    transform: translateY(-2px);
}}

.stat-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: var(--pl-purple);
    margin: 0;
    line-height: 1;
}}

.stat-label {{
    font-size: 0.65rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0.3rem 0 0 0;
    font-weight: 600;
}}

/* Tables */
.table-container {{
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}}

.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}}

.data-table th {{
    background: var(--pl-purple);
    color: white;
    font-weight: 700;
    padding: 0.9rem 0.6rem;
    text-align: center;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.data-table th:nth-child(2) {{
    text-align: left;
}}

.data-table td {{
    padding: 0.75rem 0.6rem;
    text-align: center;
    color: #333;
    border-bottom: 1px solid #eee;
    font-weight: 500;
}}

.data-table tr:hover {{
    background: rgba(255, 40, 130, 0.05);
}}

.team-cell {{
    text-align: left !important;
    font-weight: 700 !important;
    color: var(--pl-purple) !important;
}}

/* Position badges */
.pos-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.8rem;
}}

.pos-ucl {{ background: var(--pl-cyan); color: var(--pl-purple); }}
.pos-uel {{ background: #f97316; color: white; }}
.pos-uecl {{ background: var(--pl-green); color: var(--pl-purple); }}
.pos-rel {{ background: #ef4444; color: white; }}
.pos-mid {{ background: #e5e7eb; color: #333; }}

.pts-cell {{
    font-weight: 900 !important;
    color: var(--pl-purple) !important;
    font-size: 1.05rem !important;
}}

.gd-pos {{ color: var(--pl-green) !important; font-weight: 700 !important; }}
.gd-neg {{ color: #ef4444 !important; font-weight: 700 !important; }}

.goals-pill {{
    background: var(--pl-magenta);
    color: white;
    padding: 0.3rem 0.7rem;
    border-radius: 20px;
    font-weight: 800;
}}

/* Player cards */
.player-card {{
    background: white;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    border-top: 4px solid var(--pl-magenta);
}}

.player-name {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--pl-purple);
    margin: 0;
    letter-spacing: 0.5px;
}}

.player-team {{
    color: #666;
    font-size: 0.85rem;
    margin: 0.2rem 0 0 0;
    font-weight: 500;
}}

.player-pos {{
    display: inline-block;
    background: var(--pl-purple);
    color: white;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-top: 0.5rem;
}}

/* Category sections */
.stat-category {{
    background: linear-gradient(135deg, var(--pl-purple) 0%, #2d0033 100%);
    color: white;
    padding: 0.6rem 1rem;
    border-radius: 6px 6px 0 0;
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 1rem;
}}

.stat-category-content {{
    background: white;
    border: 1px solid #eee;
    border-top: none;
    border-radius: 0 0 6px 6px;
    padding: 1rem;
}}

.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 0.75rem;
}}

.stat-item {{
    background: var(--pl-offwhite);
    border-radius: 6px;
    padding: 0.75rem;
    text-align: center;
}}

.stat-item-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--pl-purple);
    margin: 0;
}}

.stat-item-label {{
    font-size: 0.6rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
    font-weight: 600;
}}

/* Compare layout */
.compare-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.compare-player-card {{
    background: white;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.compare-stat-bar {{
    background: white;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}

.compare-label {{
    text-align: center;
    font-size: 0.75rem;
    color: #666;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.compare-values {{
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
}}

.compare-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
}}

/* Search box styling */
.stTextInput > div > div > input {{
    border: 2px solid #ddd !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: var(--pl-magenta) !important;
    box-shadow: 0 0 0 2px rgba(255, 40, 130, 0.1) !important;
}}

.stMultiSelect > div {{
    border-radius: 8px !important;
}}

/* Live badge */
.live-indicator {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #22c55e;
    color: white;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
}}

.live-dot {{
    width: 8px;
    height: 8px;
    background: white;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 0.8rem;
    border-top: 1px solid #ddd;
    margin-top: 2rem;
}}

/* Mobile */
@media (max-width: 768px) {{
    .pl-title {{ font-size: 2rem; }}
    .content-area {{ padding: 1rem; }}
    .compare-grid {{ grid-template-columns: 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

# ============ API FUNCTIONS ============

API_BASE = "https://api.football-data.org/v4"

@st.cache_data(ttl=300, show_spinner=False)
def fetch_standings(api_key, season='2024'):
    """Fetch live standings"""
    if not api_key:
        return None, "No API key"
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/standings?season={season}"
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if 'standings' in data and len(data['standings']) > 0:
                table = data['standings'][0]['table']
                df = pd.DataFrame([{
                    'Pos': t['position'],
                    'Team': t['team']['shortName'],
                    'P': t['playedGames'],
                    'W': t['won'],
                    'D': t['draw'],
                    'L': t['lost'],
                    'GF': t['goalsFor'],
                    'GA': t['goalsAgainst'],
                    'GD': t['goalDifference'],
                    'Pts': t['points']
                } for t in table])
                return df, None
        return None, f"API error: {resp.status_code}"
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_scorers(api_key, season='2024', limit=50):
    """Fetch top scorers with detailed stats"""
    if not api_key:
        return None, "No API key"
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/scorers?season={season}&limit={limit}"
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if 'scorers' in data:
                players = []
                for s in data['scorers']:
                    player = s['player']
                    team = s['team']
                    players.append({
                        'id': player.get('id'),
                        'name': player.get('name', 'Unknown'),
                        'team': team.get('shortName', team.get('name', 'Unknown')),
                        'nationality': player.get('nationality', 'N/A'),
                        'position': player.get('position', 'Forward'),
                        'goals': s.get('goals', 0),
                        'assists': s.get('assists', 0) or 0,
                        'penalties': s.get('penalties', 0) or 0,
                        'played': s.get('playedMatches', 0),
                    })
                return players, None
        return None, f"API error: {resp.status_code}"
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_players(api_key, season='2024'):
    """Fetch all players from all teams"""
    if not api_key:
        return [], "No API key"
    try:
        headers = {'X-Auth-Token': api_key}
        # First get all teams
        teams_url = f"{API_BASE}/competitions/PL/teams?season={season}"
        teams_resp = requests.get(teams_url, headers=headers, timeout=15)
        
        if teams_resp.status_code != 200:
            return [], f"Failed to fetch teams: {teams_resp.status_code}"
        
        teams_data = teams_resp.json()
        all_players = []
        
        for team in teams_data.get('teams', []):
            team_name = team.get('shortName', team.get('name', 'Unknown'))
            for player in team.get('squad', []):
                all_players.append({
                    'id': player.get('id'),
                    'name': player.get('name', 'Unknown'),
                    'team': team_name,
                    'nationality': player.get('nationality', 'N/A'),
                    'position': player.get('position', 'Unknown'),
                    'dateOfBirth': player.get('dateOfBirth'),
                })
        
        return all_players, None
    except Exception as e:
        return [], str(e)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_player_matches(api_key, player_id, season='2024'):
    """Fetch player match data for detailed stats"""
    if not api_key or not player_id:
        return None, "Missing parameters"
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/persons/{player_id}/matches?season={season}&competitions=PL"
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"API error: {resp.status_code}"
    except Exception as e:
        return None, str(e)

# ============ RENDER FUNCTIONS ============

def render_header():
    """Render the header with PL branding"""
    logo_html = ""
    if LOGO_BASE64:
        logo_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" class="pl-logo" alt="Premier League">'
    else:
        # Fallback to external URL
        logo_html = '<img src="https://www.premierleague.com/resources/rebrand/v7.129.2/i/elements/pl-main-logo.png" class="pl-logo" alt="Premier League">'
    
    st.markdown(f"""
    <div class="pl-header">
        {logo_html}
        <div>
            <h1 class="pl-title">PREMIER LEAGUE</h1>
            <p class="pl-subtitle">Statistics Hub</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_standings_table(df):
    """Render standings table"""
    html = '<div class="table-container"><table class="data-table">'
    html += '<thead><tr><th>#</th><th>Club</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr></thead>'
    html += '<tbody>'
    
    for _, row in df.iterrows():
        pos = int(row['Pos'])
        if pos <= 4:
            badge_class = 'pos-ucl'
        elif pos == 5:
            badge_class = 'pos-uel'
        elif pos == 6:
            badge_class = 'pos-uecl'
        elif pos >= 18:
            badge_class = 'pos-rel'
        else:
            badge_class = 'pos-mid'
        
        gd = int(row['GD'])
        gd_class = 'gd-pos' if gd > 0 else 'gd-neg' if gd < 0 else ''
        gd_str = f"+{gd}" if gd > 0 else str(gd)
        
        html += f'''<tr>
            <td><span class="pos-badge {badge_class}">{pos}</span></td>
            <td class="team-cell">{row['Team']}</td>
            <td>{row['P']}</td><td>{row['W']}</td><td>{row['D']}</td><td>{row['L']}</td>
            <td>{row['GF']}</td><td>{row['GA']}</td>
            <td class="{gd_class}">{gd_str}</td>
            <td class="pts-cell">{row['Pts']}</td>
        </tr>'''
    
    html += '</tbody></table></div>'
    return html

def render_scorers_table(players):
    """Render scorers table"""
    html = '<div class="table-container"><table class="data-table">'
    html += '<thead><tr><th>#</th><th>Player</th><th>Team</th><th>Goals</th><th>Assists</th><th>Pens</th><th>Games</th><th>G/Game</th></tr></thead>'
    html += '<tbody>'
    
    for idx, p in enumerate(players[:20]):
        gpg = round(p['goals'] / max(p['played'], 1), 2)
        html += f'''<tr>
            <td><span class="pos-badge pos-mid">{idx + 1}</span></td>
            <td class="team-cell">{p['name']}</td>
            <td>{p['team']}</td>
            <td><span class="goals-pill">{p['goals']}</span></td>
            <td>{p['assists']}</td>
            <td>{p['penalties']}</td>
            <td>{p['played']}</td>
            <td>{gpg}</td>
        </tr>'''
    
    html += '</tbody></table></div>'
    return html

def render_player_stats_card(player, color=PL_MAGENTA):
    """Render detailed player stats card with categories"""
    # Calculate derived stats
    goals = player.get('goals', 0)
    assists = player.get('assists', 0)
    played = player.get('played', 1) or 1
    penalties = player.get('penalties', 0)
    
    gpg = round(goals / played, 2)
    apg = round(assists / played, 2)
    g_a = goals + assists
    g_a_pg = round(g_a / played, 2)
    non_pen_goals = goals - penalties
    
    html = f"""
    <div class="player-card" style="border-top-color: {color};">
        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <h3 class="player-name">{player['name']}</h3>
                <p class="player-team">{player['team']}</p>
            </div>
            <span class="player-pos">{player.get('position', 'Forward')}</span>
        </div>
        
        <!-- ATTACKING -->
        <div class="stat-category" style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);">Attacking</div>
        <div class="stat-category-content">
            <div class="stat-grid">
                <div class="stat-item">
                    <p class="stat-item-value">{goals}</p>
                    <p class="stat-item-label">Goals</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{non_pen_goals}</p>
                    <p class="stat-item-label">Non-Pen Goals</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{penalties}</p>
                    <p class="stat-item-label">Penalties</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{gpg}</p>
                    <p class="stat-item-label">Goals/Game</p>
                </div>
            </div>
        </div>
        
        <!-- CREATIVE -->
        <div class="stat-category" style="background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);">Creative & Passing</div>
        <div class="stat-category-content">
            <div class="stat-grid">
                <div class="stat-item">
                    <p class="stat-item-value">{assists}</p>
                    <p class="stat-item-label">Assists</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{apg}</p>
                    <p class="stat-item-label">Assists/Game</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{g_a}</p>
                    <p class="stat-item-label">Goals + Assists</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{g_a_pg}</p>
                    <p class="stat-item-label">G+A Per Game</p>
                </div>
            </div>
        </div>
        
        <!-- PLAYING TIME -->
        <div class="stat-category" style="background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);">Playing Time</div>
        <div class="stat-category-content">
            <div class="stat-grid">
                <div class="stat-item">
                    <p class="stat-item-value">{played}</p>
                    <p class="stat-item-label">Matches</p>
                </div>
                <div class="stat-item">
                    <p class="stat-item-value">{player.get('nationality', 'N/A')[:3].upper()}</p>
                    <p class="stat-item-label">Nationality</p>
                </div>
            </div>
        </div>
    </div>
    """
    return html

def create_comparison_chart(players_data, stat_key, stat_label, colors):
    """Create horizontal bar chart for comparison"""
    names = [p['name'].split()[-1] for p in players_data]  # Last names only
    values = [p.get(stat_key, 0) for p in players_data]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=names,
        orientation='h',
        marker=dict(color=colors[:len(players_data)]),
        text=values,
        textposition='outside',
        textfont=dict(size=14, family='Inter', color=PL_PURPLE)
    ))
    
    fig.update_layout(
        title=dict(text=stat_label, font=dict(size=14, color=PL_PURPLE, family='Inter')),
        height=max(150, 50 * len(players_data)),
        margin=dict(l=0, r=50, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis=dict(showgrid=False),
        font=dict(family='Inter', color='#333')
    )
    return fig

def create_radar_chart(players_data, colors):
    """Create radar chart for player comparison"""
    categories = ['Goals', 'Assists', 'Penalties', 'G+A', 'Games']
    
    fig = go.Figure()
    
    for i, player in enumerate(players_data):
        goals = player.get('goals', 0)
        assists = player.get('assists', 0)
        penalties = player.get('penalties', 0)
        played = player.get('played', 0)
        g_a = goals + assists
        
        # Normalize values for radar
        max_goals = max(p.get('goals', 1) for p in players_data) or 1
        max_assists = max(p.get('assists', 1) for p in players_data) or 1
        max_pens = max(p.get('penalties', 1) for p in players_data) or 1
        max_ga = max((p.get('goals', 0) + p.get('assists', 0)) for p in players_data) or 1
        max_played = max(p.get('played', 1) for p in players_data) or 1
        
        values = [
            (goals / max_goals) * 100,
            (assists / max_assists) * 100 if max_assists else 0,
            (penalties / max_pens) * 100 if max_pens else 0,
            (g_a / max_ga) * 100,
            (played / max_played) * 100
        ]
        
        # Convert hex to rgba
        hex_color = colors[i % len(colors)]
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            name=player['name'].split()[-1],
            line=dict(color=hex_color, width=3),
            fill='toself',
            fillcolor=f'rgba({r},{g},{b},0.15)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                linecolor='rgba(0,0,0,0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=12)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=60, r=60, t=40, b=60)
    )
    return fig

# ============ MAIN APP ============

def main():
    render_header()
    
    # Get API key
    api_key = None
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY")
    except:
        pass
    
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    # API Key input if not set
    if not api_key:
        st.warning("**API Key Required** - Get your free key at [football-data.org](https://www.football-data.org/client/register)")
        api_key = st.text_input("Enter your API Key:", type="password")
    
    # Season selector
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_season = st.selectbox("Season", SEASONS, index=0)
        season_code = SEASON_API_MAP.get(selected_season, '2024')
    with col2:
        if api_key:
            st.markdown('<div class="live-indicator"><div class="live-dot"></div>LIVE DATA</div>', unsafe_allow_html=True)
    
    if not api_key:
        st.info("Enter your API key to view live Premier League data.")
        return
    
    # Fetch all data
    with st.spinner("Loading Premier League data..."):
        standings, standings_err = fetch_standings(api_key, season_code)
        scorers, scorers_err = fetch_scorers(api_key, season_code)
        all_players, players_err = fetch_all_players(api_key, season_code)
    
    # Quick stats
    if standings is not None:
        total_goals = standings['GF'].sum()
        leader = standings.iloc[0]['Team']
        top_pts = standings.iloc[0]['Pts']
        
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card"><p class="stat-value">{len(standings)}</p><p class="stat-label">Teams</p></div>
            <div class="stat-card"><p class="stat-value">{total_goals}</p><p class="stat-label">Total Goals</p></div>
            <div class="stat-card"><p class="stat-value">{leader}</p><p class="stat-label">League Leader</p></div>
            <div class="stat-card"><p class="stat-value">{top_pts}</p><p class="stat-label">Top Points</p></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["STANDINGS", "TOP SCORERS", "PLAYER SEARCH", "COMPARE PLAYERS"])
    
    # ===== TAB 1: STANDINGS =====
    with tab1:
        if standings_err:
            st.error(f"Error: {standings_err}")
        elif standings is not None:
            st.markdown('<div class="section-header"><h2 class="section-title">League Table</h2></div>', unsafe_allow_html=True)
            st.markdown(render_standings_table(standings), unsafe_allow_html=True)
            
            st.markdown("""
            <div style="display: flex; gap: 1.5rem; margin: 1rem 0; flex-wrap: wrap; font-size: 0.8rem;">
                <span><span class="pos-badge pos-ucl">1</span> Champions League</span>
                <span><span class="pos-badge pos-uel">5</span> Europa League</span>
                <span><span class="pos-badge pos-uecl">6</span> Conference League</span>
                <span><span class="pos-badge pos-rel">18</span> Relegation</span>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== TAB 2: TOP SCORERS =====
    with tab2:
        if scorers_err:
            st.error(f"Error: {scorers_err}")
        elif scorers:
            st.markdown('<div class="section-header"><h2 class="section-title">Golden Boot Race</h2></div>', unsafe_allow_html=True)
            st.markdown(render_scorers_table(scorers), unsafe_allow_html=True)
            
            # Top 3 cards
            if len(scorers) >= 3:
                st.markdown('<div class="section-header"><h2 class="section-title">Top 3 Scorers</h2></div>', unsafe_allow_html=True)
                cols = st.columns(3)
                for i in range(3):
                    with cols[i]:
                        st.markdown(render_player_stats_card(scorers[i], PLAYER_COLORS[i]), unsafe_allow_html=True)
    
    # ===== TAB 3: PLAYER SEARCH =====
    with tab3:
        st.markdown('<div class="section-header"><h2 class="section-title">Search Any Player</h2></div>', unsafe_allow_html=True)
        
        # Combine all players and scorers for search
        searchable_players = []
        
        # Add scorers with their stats
        if scorers:
            for p in scorers:
                searchable_players.append(p)
        
        # Add other players from squads
        if all_players:
            scorer_names = {p['name'] for p in scorers} if scorers else set()
            for p in all_players:
                if p['name'] not in scorer_names:
                    searchable_players.append({
                        'id': p.get('id'),
                        'name': p['name'],
                        'team': p['team'],
                        'nationality': p.get('nationality', 'N/A'),
                        'position': p.get('position', 'Unknown'),
                        'goals': 0,
                        'assists': 0,
                        'penalties': 0,
                        'played': 0
                    })
        
        if searchable_players:
            # Search input
            search_query = st.text_input("Search player by name:", placeholder="e.g., Salah, Haaland, Palmer...")
            
            if search_query:
                # Filter players
                query_lower = search_query.lower()
                matches = [p for p in searchable_players if query_lower in p['name'].lower()]
                
                if matches:
                    st.markdown(f"**Found {len(matches)} player(s)**")
                    
                    # Show first 10 matches
                    for p in matches[:10]:
                        st.markdown(render_player_stats_card(p), unsafe_allow_html=True)
                else:
                    st.info(f"No players found matching '{search_query}'")
            else:
                st.info("Type a player name to search across all Premier League squads.")
                st.markdown(f"**{len(searchable_players)} players available**")
        else:
            st.warning("Could not load player data. Check API key.")
    
    # ===== TAB 4: COMPARE PLAYERS =====
    with tab4:
        st.markdown('<div class="section-header"><h2 class="section-title">Compare Up To 5 Players</h2></div>', unsafe_allow_html=True)
        
        # Build player options for comparison
        compare_options = []
        if scorers:
            for p in scorers:
                compare_options.append(p)
        
        if compare_options:
            # Season range selection
            col1, col2 = st.columns(2)
            with col1:
                from_season = st.selectbox("From Season", SEASONS, index=0, key='from_season')
            with col2:
                to_season = st.selectbox("To Season", SEASONS, index=0, key='to_season')
            
            st.markdown("---")
            
            # Player selection with search
            player_names = [p['name'] for p in compare_options]
            
            # Text search for adding players
            search_for_compare = st.text_input("Search player to add:", placeholder="Type to search...", key="compare_search")
            
            available_for_select = player_names
            if search_for_compare:
                available_for_select = [n for n in player_names if search_for_compare.lower() in n.lower()]
            
            selected_players = st.multiselect(
                "Select players to compare (up to 5):",
                options=available_for_select,
                max_selections=5,
                default=available_for_select[:2] if len(available_for_select) >= 2 else available_for_select[:1] if available_for_select else []
            )
            
            if len(selected_players) >= 2:
                # Get player data
                players_data = [p for p in compare_options if p['name'] in selected_players]
                
                # Season range note
                if from_season != to_season:
                    st.info(f"Showing stats for {selected_season} (season aggregation requires premium API)")
                
                # Player cards grid
                st.markdown('<div class="compare-grid">', unsafe_allow_html=True)
                cols = st.columns(len(players_data))
                for i, p in enumerate(players_data):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="compare-player-card" style="border-top: 4px solid {PLAYER_COLORS[i]};">
                            <h3 class="player-name" style="font-size: 1.2rem;">{p['name']}</h3>
                            <p class="player-team">{p['team']}</p>
                            <span class="player-pos">{p.get('position', 'FW')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Radar chart
                st.markdown('<div class="section-header"><h2 class="section-title">Overall Comparison</h2></div>', unsafe_allow_html=True)
                radar_fig = create_radar_chart(players_data, PLAYER_COLORS)
                st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
                
                # Stat comparisons
                st.markdown('<div class="section-header"><h2 class="section-title">Stat Breakdown</h2></div>', unsafe_allow_html=True)
                
                stat_comparisons = [
                    ('goals', 'Goals'),
                    ('assists', 'Assists'),
                    ('penalties', 'Penalties'),
                    ('played', 'Matches Played'),
                ]
                
                col1, col2 = st.columns(2)
                for i, (key, label) in enumerate(stat_comparisons):
                    with col1 if i % 2 == 0 else col2:
                        fig = create_comparison_chart(players_data, key, label, PLAYER_COLORS)
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                # Goals per game comparison
                st.markdown('<div class="section-header"><h2 class="section-title">Efficiency</h2></div>', unsafe_allow_html=True)
                
                # Calculate derived stats
                efficiency_data = []
                for p in players_data:
                    played = max(p.get('played', 1), 1)
                    efficiency_data.append({
                        'name': p['name'],
                        'gpg': round(p.get('goals', 0) / played, 2),
                        'apg': round(p.get('assists', 0) / played, 2),
                        'g_a_pg': round((p.get('goals', 0) + p.get('assists', 0)) / played, 2)
                    })
                
                cols = st.columns(len(efficiency_data))
                for i, e in enumerate(efficiency_data):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="player-card" style="border-top-color: {PLAYER_COLORS[i]};">
                            <h4 style="margin: 0; color: {PL_PURPLE};">{e['name'].split()[-1]}</h4>
                            <div class="stat-grid" style="margin-top: 0.75rem;">
                                <div class="stat-item">
                                    <p class="stat-item-value">{e['gpg']}</p>
                                    <p class="stat-item-label">Goals/Game</p>
                                </div>
                                <div class="stat-item">
                                    <p class="stat-item-value">{e['apg']}</p>
                                    <p class="stat-item-label">Assists/Game</p>
                                </div>
                                <div class="stat-item">
                                    <p class="stat-item-value">{e['g_a_pg']}</p>
                                    <p class="stat-item-label">G+A/Game</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
            elif len(selected_players) == 1:
                st.info("Select at least 2 players to compare.")
            else:
                st.info("Search and select players above to compare their stats.")
        else:
            st.warning("No player data available for comparison.")
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>Data provided by <a href="https://www.football-data.org/" target="_blank">Football-Data.org</a> API</p>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
