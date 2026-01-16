"""
Premier League Stats Hub - Live Data Dashboard
Real-time data from Football-Data.org API
Official PL Branding with Radikal Bold styling
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import base64

# Page config
st.set_page_config(
    page_title="Premier League Stats",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Official PL Brand Colors (from brandfetch.com/premierleague.com)
PL_PURPLE = "#360D3A"  # Valentino - Primary
PL_VIOLET = "#963CFF"  # Electric Violet - Accent
PL_GRAPE = "#541E5D"   # Grape - Secondary
PL_WHITE = "#FFFFFF"
PL_OFFWHITE = "#F5F5F5"
PL_DARK = "#1a0a1f"

# Season codes for API
SEASON_CODES = {
    '2025/26': '2025',
    '2024/25': '2024', 
    '2023/24': '2023',
    '2022/23': '2022',
    '2021/22': '2021',
    '2020/21': '2020',
}

CURRENT_SEASON = '2024/25'  # API may not have 2025/26 yet

# Professional CSS with PL Branding and Light Theme for Readability
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --pl-purple: {PL_PURPLE};
    --pl-violet: {PL_VIOLET};
    --pl-grape: {PL_GRAPE};
    --pl-white: {PL_WHITE};
    --pl-offwhite: {PL_OFFWHITE};
}}

* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}}

/* Light background for readability */
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

/* ===== HEADER ===== */
.pl-header {{
    background: linear-gradient(135deg, var(--pl-purple) 0%, var(--pl-grape) 100%);
    padding: 1.5rem 2rem;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}}

.pl-logo-section {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.pl-logo {{
    height: 60px;
}}

.pl-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    color: var(--pl-white);
    margin: 0;
    letter-spacing: 2px;
    line-height: 1;
}}

.pl-subtitle {{
    font-size: 0.85rem;
    color: rgba(255,255,255,0.8);
    margin: 0.25rem 0 0 0;
    font-weight: 500;
    letter-spacing: 1px;
}}

/* ===== NAV BAR ===== */
.nav-bar {{
    background: var(--pl-purple);
    padding: 0 2rem;
    display: flex;
    gap: 0;
    border-bottom: 3px solid var(--pl-violet);
}}

.nav-item {{
    color: var(--pl-white);
    padding: 1rem 1.5rem;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.2s;
    border-bottom: 3px solid transparent;
    margin-bottom: -3px;
}}

.nav-item:hover {{
    background: rgba(255,255,255,0.1);
}}

.nav-item.active {{
    border-bottom-color: var(--pl-violet);
    background: rgba(150, 60, 255, 0.2);
}}

/* ===== CONTENT AREA ===== */
.content-area {{
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
}}

/* ===== SEASON SELECTOR ===== */
.season-bar {{
    background: var(--pl-white);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}}

.season-label {{
    font-weight: 700;
    color: var(--pl-purple);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.live-badge {{
    background: #22c55e;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.4rem;
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
    50% {{ opacity: 0.5; }}
}}

/* ===== STATS CARDS ===== */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}}

@media (max-width: 900px) {{
    .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

.stat-card {{
    background: var(--pl-white);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid var(--pl-violet);
    transition: transform 0.2s, box-shadow 0.2s;
}}

.stat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}}

.stat-number {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: var(--pl-purple);
    margin: 0;
    line-height: 1;
}}

.stat-label {{
    font-size: 0.75rem;
    font-weight: 700;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0.5rem 0 0 0;
}}

/* ===== SECTION HEADERS ===== */
.section-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid var(--pl-purple);
}}

.section-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: var(--pl-purple);
    margin: 0;
    letter-spacing: 1px;
}}

/* ===== TABLES ===== */
.table-container {{
    background: var(--pl-white);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    overflow-x: auto;
}}

.standings-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}}

.standings-table th {{
    background: var(--pl-purple);
    color: var(--pl-white);
    font-weight: 700;
    padding: 1rem 0.75rem;
    text-align: center;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.standings-table th:nth-child(2) {{
    text-align: left;
}}

.standings-table td {{
    padding: 0.9rem 0.75rem;
    text-align: center;
    color: #333;
    border-bottom: 1px solid #eee;
    font-weight: 500;
}}

.standings-table tr:hover {{
    background: rgba(150, 60, 255, 0.05);
}}

.standings-table tr:last-child td {{
    border-bottom: none;
}}

.team-name {{
    text-align: left !important;
    font-weight: 700 !important;
    color: var(--pl-purple) !important;
}}

/* Position badges */
.pos-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.85rem;
}}

.pos-ucl {{
    background: #04f5ff;
    color: var(--pl-purple);
}}

.pos-uel {{
    background: #f97316;
    color: white;
}}

.pos-uecl {{
    background: #22c55e;
    color: white;
}}

.pos-rel {{
    background: #ef4444;
    color: white;
}}

.pos-normal {{
    background: #e5e7eb;
    color: #333;
}}

.points-cell {{
    font-weight: 900 !important;
    color: var(--pl-purple) !important;
    font-size: 1.1rem !important;
}}

.gd-positive {{
    color: #22c55e !important;
    font-weight: 700 !important;
}}

.gd-negative {{
    color: #ef4444 !important;
    font-weight: 700 !important;
}}

/* ===== SCORERS TABLE ===== */
.goals-badge {{
    background: var(--pl-violet);
    color: white;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-weight: 800;
    font-size: 1rem;
}}

/* ===== PLAYER CARDS ===== */
.player-card {{
    background: var(--pl-white);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    border-left: 4px solid var(--pl-violet);
}}

.player-name {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--pl-purple);
    margin: 0;
}}

.player-team {{
    font-size: 0.9rem;
    color: #666;
    margin: 0.25rem 0 0 0;
    font-weight: 500;
}}

.player-position {{
    display: inline-block;
    background: var(--pl-purple);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}}

.stats-grid-small {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}}

.stat-box {{
    background: var(--pl-offwhite);
    border-radius: 6px;
    padding: 0.75rem;
    text-align: center;
}}

.stat-box-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--pl-purple);
    margin: 0;
}}

.stat-box-label {{
    font-size: 0.65rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
    font-weight: 600;
}}

/* ===== COMPARISON ===== */
.compare-header {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}}

.compare-player {{
    background: var(--pl-white);
    border-radius: 8px;
    padding: 1.5rem 2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    min-width: 200px;
}}

.compare-vs {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: var(--pl-purple);
}}

.compare-stat-row {{
    background: var(--pl-white);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 0.5rem;
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    align-items: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}

.compare-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
}}

.compare-label {{
    text-align: center;
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    font-weight: 600;
}}

/* ===== TABS OVERRIDE ===== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: var(--pl-purple);
    border-radius: 8px 8px 0 0;
    padding: 0;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: rgba(255,255,255,0.8);
    border-radius: 0;
    padding: 1rem 2rem;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: none;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: white;
    background: rgba(255,255,255,0.1);
}}

.stTabs [aria-selected="true"] {{
    background: var(--pl-violet) !important;
    color: white !important;
}}

.stTabs [data-baseweb="tab-panel"] {{
    background: var(--pl-white);
    border-radius: 0 0 8px 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

/* ===== SELECT/INPUT OVERRIDES ===== */
.stSelectbox label, .stTextInput label, .stMultiSelect label {{
    color: var(--pl-purple) !important;
    font-weight: 700 !important;
}}

.stSelectbox > div > div {{
    background: white !important;
    border: 2px solid #ddd !important;
    border-radius: 6px !important;
}}

.stSelectbox > div > div:focus-within {{
    border-color: var(--pl-violet) !important;
}}

/* ===== LOADING ===== */
.loading-container {{
    text-align: center;
    padding: 3rem;
}}

.loading-text {{
    color: var(--pl-purple);
    font-weight: 600;
}}

/* ===== ERROR/INFO ===== */
.stAlert {{
    border-radius: 8px !important;
}}

/* ===== FOOTER ===== */
.footer {{
    text-align: center;
    padding: 2rem;
    margin-top: 2rem;
    border-top: 1px solid #ddd;
    color: #666;
    font-size: 0.8rem;
}}

/* Mobile */
@media (max-width: 768px) {{
    .pl-title {{
        font-size: 1.8rem;
    }}
    .content-area {{
        padding: 1rem;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============ API FUNCTIONS ============

API_BASE = "https://api.football-data.org/v4"

@st.cache_data(ttl=300, show_spinner=False)
def fetch_standings(api_key, season='2024'):
    """Fetch live standings from Football-Data.org"""
    if not api_key:
        return None, "No API key provided"
    
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/standings?season={season}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
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
        elif response.status_code == 403:
            return None, "API access denied. Check your API key."
        elif response.status_code == 429:
            return None, "API rate limit reached. Please wait."
        else:
            return None, f"API error: {response.status_code}"
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"Error fetching data: {str(e)}"

@st.cache_data(ttl=300, show_spinner=False)
def fetch_scorers(api_key, season='2024', limit=20):
    """Fetch live top scorers from Football-Data.org"""
    if not api_key:
        return None, "No API key provided"
    
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/scorers?season={season}&limit={limit}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'scorers' in data:
                df = pd.DataFrame([{
                    'Player': s['player']['name'],
                    'Team': s['team']['shortName'],
                    'Nationality': s['player'].get('nationality', 'N/A'),
                    'Position': (s['player'].get('position') or 'Forward')[:10],
                    'Goals': s.get('goals', 0),
                    'Assists': s.get('assists', 0) or 0,
                    'Penalties': s.get('penalties', 0) or 0,
                    'Played': s.get('playedMatches', 0)
                } for s in data['scorers']])
                return df, None
        elif response.status_code == 403:
            return None, "API access denied"
        else:
            return None, f"API error: {response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"

@st.cache_data(ttl=300, show_spinner=False)
def fetch_matches(api_key, season='2024', status='FINISHED'):
    """Fetch matches from Football-Data.org"""
    if not api_key:
        return None, "No API key provided"
    
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/matches?season={season}&status={status}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('matches', []), None
        else:
            return None, f"API error: {response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"

@st.cache_data(ttl=3600, show_spinner=False)  
def fetch_teams(api_key, season='2024'):
    """Fetch all teams"""
    if not api_key:
        return None, "No API key"
    try:
        headers = {'X-Auth-Token': api_key}
        url = f"{API_BASE}/competitions/PL/teams?season={season}"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json().get('teams', []), None
        return None, f"API error: {response.status_code}"
    except Exception as e:
        return None, str(e)

# ============ RENDER FUNCTIONS ============

def render_standings_table(df):
    """Render professional standings table"""
    html = '<div class="table-container"><table class="standings-table">'
    html += '<thead><tr><th>Pos</th><th>Club</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr></thead>'
    html += '<tbody>'
    
    for _, row in df.iterrows():
        pos = int(row['Pos'])
        
        # Position badge styling
        if pos <= 4:
            badge_class = 'pos-ucl'
        elif pos == 5:
            badge_class = 'pos-uel'
        elif pos == 6:
            badge_class = 'pos-uecl'
        elif pos >= 18:
            badge_class = 'pos-rel'
        else:
            badge_class = 'pos-normal'
        
        # GD styling
        gd = int(row['GD'])
        gd_class = 'gd-positive' if gd > 0 else 'gd-negative' if gd < 0 else ''
        gd_str = f"+{gd}" if gd > 0 else str(gd)
        
        html += f'''<tr>
            <td><span class="pos-badge {badge_class}">{pos}</span></td>
            <td class="team-name">{row['Team']}</td>
            <td>{row['P']}</td>
            <td>{row['W']}</td>
            <td>{row['D']}</td>
            <td>{row['L']}</td>
            <td>{row['GF']}</td>
            <td>{row['GA']}</td>
            <td class="{gd_class}">{gd_str}</td>
            <td class="points-cell">{row['Pts']}</td>
        </tr>'''
    
    html += '</tbody></table></div>'
    return html

def render_scorers_table(df):
    """Render top scorers table"""
    html = '<div class="table-container"><table class="standings-table">'
    html += '<thead><tr><th>#</th><th>Player</th><th>Club</th><th>Nat</th><th>Goals</th><th>Assists</th><th>Pens</th><th>Played</th></tr></thead>'
    html += '<tbody>'
    
    for idx, row in df.iterrows():
        html += f'''<tr>
            <td><span class="pos-badge pos-normal">{idx + 1}</span></td>
            <td class="team-name">{row['Player']}</td>
            <td>{row['Team']}</td>
            <td>{row['Nationality'][:3].upper() if row['Nationality'] != 'N/A' else 'N/A'}</td>
            <td><span class="goals-badge">{row['Goals']}</span></td>
            <td>{row['Assists']}</td>
            <td>{row['Penalties']}</td>
            <td>{row['Played']}</td>
        </tr>'''
    
    html += '</tbody></table></div>'
    return html

def create_points_chart(df):
    """Create horizontal bar chart for points"""
    df_sorted = df.sort_values('Pts', ascending=True)
    
    colors = []
    for pos in df_sorted['Pos']:
        if pos <= 4:
            colors.append('#04f5ff')
        elif pos >= 18:
            colors.append('#ef4444')
        else:
            colors.append(PL_VIOLET)
    
    fig = go.Figure(go.Bar(
        x=df_sorted['Pts'],
        y=df_sorted['Team'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=df_sorted['Pts'],
        textposition='outside',
        textfont=dict(color=PL_PURPLE, size=11, family='Inter')
    ))
    
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=60, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_PURPLE, family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(54,13,58,0.1)',
            zeroline=False,
            tickfont=dict(color='#666')
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color=PL_PURPLE, family='Inter')
        )
    )
    return fig

def create_goals_chart(df):
    """Create goals comparison bar chart"""
    top10 = df.head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Goals',
        x=top10['Player'],
        y=top10['Goals'],
        marker_color=PL_VIOLET,
        text=top10['Goals'],
        textposition='outside'
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=100),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_PURPLE, family='Inter'),
        xaxis=dict(tickangle=-45, tickfont=dict(color='#666')),
        yaxis=dict(showgrid=True, gridcolor='rgba(54,13,58,0.1)', tickfont=dict(color='#666')),
        showlegend=False
    )
    return fig

# ============ MAIN APP ============

def main():
    # Header
    st.markdown("""
    <div class="pl-header">
        <div class="pl-logo-section">
            <img src="https://www.premierleague.com/resources/rebrand/v7.129.2/i/elements/pl-main-logo.png" 
                 alt="Premier League" class="pl-logo"
                 onerror="this.src='https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg'">
            <div>
                <h1 class="pl-title">PREMIER LEAGUE</h1>
                <p class="pl-subtitle">Live Statistics Hub</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get API key
    api_key = None
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY")
    except:
        pass
    
    # Content area
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    # API Key input if not set
    if not api_key:
        st.warning("**API Key Required** - Enter your Football-Data.org API key to fetch live data.")
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Get your free API key at https://www.football-data.org/client/register"
        )
        st.info("**Free API key provides:** Live standings, top scorers, match results, and team data.")
    
    # Season selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        available_seasons = list(SEASON_CODES.keys())
        selected_season = st.selectbox("Select Season", available_seasons, index=1)  # Default to 2024/25
        season_code = SEASON_CODES[selected_season]
    
    with col3:
        if api_key:
            st.markdown("""
            <div class="live-badge">
                <div class="live-dot"></div>
                LIVE DATA
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not api_key:
        st.info("Enter your API key above to view live Premier League data.")
        return
    
    # Fetch data
    with st.spinner("Fetching live data from Premier League..."):
        standings, standings_error = fetch_standings(api_key, season_code)
        scorers, scorers_error = fetch_scorers(api_key, season_code)
    
    # Stats cards
    if standings is not None:
        total_goals = standings['GF'].sum()
        total_matches = standings['P'].sum() // 2
        leader = standings.iloc[0]['Team']
        top_points = standings.iloc[0]['Pts']
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <p class="stat-number">{len(standings)}</p>
                <p class="stat-label">Teams</p>
            </div>
            <div class="stat-card">
                <p class="stat-number">{total_goals}</p>
                <p class="stat-label">Goals Scored</p>
            </div>
            <div class="stat-card">
                <p class="stat-number">{leader}</p>
                <p class="stat-label">League Leader</p>
            </div>
            <div class="stat-card">
                <p class="stat-number">{top_points}</p>
                <p class="stat-label">Top Points</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["STANDINGS", "TOP SCORERS", "PLAYER COMPARISON"])
    
    # ===== TAB 1: STANDINGS =====
    with tab1:
        if standings_error:
            st.error(f"Could not load standings: {standings_error}")
        elif standings is not None:
            st.markdown('<div class="section-header"><h2 class="section-title">League Table</h2></div>', unsafe_allow_html=True)
            st.markdown(render_standings_table(standings), unsafe_allow_html=True)
            
            st.markdown("""
            <div style="display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap;">
                <span><span class="pos-badge pos-ucl">1</span> Champions League</span>
                <span><span class="pos-badge pos-uel">5</span> Europa League</span>
                <span><span class="pos-badge pos-uecl">6</span> Conference League</span>
                <span><span class="pos-badge pos-rel">18</span> Relegation</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="section-header"><h2 class="section-title">Points Distribution</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(create_points_chart(standings), use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Enter API key to load standings data.")
    
    # ===== TAB 2: TOP SCORERS =====
    with tab2:
        if scorers_error:
            st.error(f"Could not load scorers: {scorers_error}")
        elif scorers is not None and len(scorers) > 0:
            st.markdown('<div class="section-header"><h2 class="section-title">Golden Boot Race</h2></div>', unsafe_allow_html=True)
            st.markdown(render_scorers_table(scorers), unsafe_allow_html=True)
            
            st.markdown('<div class="section-header"><h2 class="section-title">Goals Chart</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(create_goals_chart(scorers), use_container_width=True, config={'displayModeBar': False})
            
            # Top 3 cards
            st.markdown('<div class="section-header"><h2 class="section-title">Top 3 Scorers</h2></div>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, (_, player) in enumerate(scorers.head(3).iterrows()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="player-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h3 class="player-name">{player['Player']}</h3>
                                <p class="player-team">{player['Team']}</p>
                            </div>
                            <span class="player-position">{player['Position']}</span>
                        </div>
                        <div class="stats-grid-small">
                            <div class="stat-box">
                                <p class="stat-box-value">{player['Goals']}</p>
                                <p class="stat-box-label">Goals</p>
                            </div>
                            <div class="stat-box">
                                <p class="stat-box-value">{player['Assists']}</p>
                                <p class="stat-box-label">Assists</p>
                            </div>
                            <div class="stat-box">
                                <p class="stat-box-value">{player['Played']}</p>
                                <p class="stat-box-label">Played</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No scorers data available for this season.")
    
    # ===== TAB 3: PLAYER COMPARISON =====
    with tab3:
        st.markdown('<div class="section-header"><h2 class="section-title">Compare Players</h2></div>', unsafe_allow_html=True)
        
        if scorers is not None and len(scorers) >= 2:
            player_list = scorers['Player'].tolist()
            
            col1, col2 = st.columns(2)
            with col1:
                player1 = st.selectbox("Player 1", player_list, index=0, key='p1')
            with col2:
                player2 = st.selectbox("Player 2", player_list, index=1 if len(player_list) > 1 else 0, key='p2')
            
            if player1 and player2 and player1 != player2:
                p1_data = scorers[scorers['Player'] == player1].iloc[0]
                p2_data = scorers[scorers['Player'] == player2].iloc[0]
                
                # Header
                st.markdown(f"""
                <div class="compare-header">
                    <div class="compare-player" style="border-left: 4px solid {PL_VIOLET};">
                        <h3 class="player-name">{p1_data['Player']}</h3>
                        <p class="player-team">{p1_data['Team']}</p>
                    </div>
                    <div class="compare-vs">VS</div>
                    <div class="compare-player" style="border-left: 4px solid #04f5ff;">
                        <h3 class="player-name" style="color: #04f5ff;">{p2_data['Player']}</h3>
                        <p class="player-team">{p2_data['Team']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Comparison stats
                stats_to_compare = [
                    ('Goals', 'Goals'),
                    ('Assists', 'Assists'),
                    ('Penalties', 'Penalties'),
                    ('Played', 'Matches Played'),
                ]
                
                for stat_key, stat_label in stats_to_compare:
                    v1 = p1_data.get(stat_key, 0)
                    v2 = p2_data.get(stat_key, 0)
                    
                    # Determine winner styling
                    v1_style = f"color: {PL_VIOLET};" + (" font-size: 1.6rem;" if v1 > v2 else "")
                    v2_style = "color: #04f5ff;" + (" font-size: 1.6rem;" if v2 > v1 else "")
                    
                    st.markdown(f"""
                    <div class="compare-stat-row">
                        <div class="compare-value" style="{v1_style}">{v1}</div>
                        <div class="compare-label">{stat_label}</div>
                        <div class="compare-value" style="{v2_style} text-align: right;">{v2}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Goals per game
                gpg1 = round(p1_data['Goals'] / max(p1_data['Played'], 1), 2)
                gpg2 = round(p2_data['Goals'] / max(p2_data['Played'], 1), 2)
                
                st.markdown(f"""
                <div class="compare-stat-row">
                    <div class="compare-value" style="color: {PL_VIOLET};">{gpg1}</div>
                    <div class="compare-label">Goals Per Game</div>
                    <div class="compare-value" style="color: #04f5ff; text-align: right;">{gpg2}</div>
                </div>
                """, unsafe_allow_html=True)
                
            elif player1 == player2:
                st.info("Select two different players to compare.")
        else:
            st.info("Load data to compare players.")
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>Data provided by <a href="https://www.football-data.org/" target="_blank">Football-Data.org</a></p>
        <p>Not affiliated with the Premier League. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
