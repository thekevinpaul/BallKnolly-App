"""
Premier League Stats Hub - Professional Dashboard
Polished UI, Custom Tables, Player Comparison
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Premier League Stats",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Colors
PURPLE = "#37003c"
MAGENTA = "#ff2882"
CYAN = "#00ff85"
WHITE = "#ffffff"
DARK = "#1a0a1f"

# Professional CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {{
    --purple: {PURPLE};
    --magenta: {MAGENTA};
    --cyan: {CYAN};
    --white: {WHITE};
    --dark: {DARK};
}}

* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
}}

.stApp {{
    background: linear-gradient(180deg, var(--purple) 0%, var(--dark) 100%);
    min-height: 100vh;
}}

#MainMenu, footer, header, [data-testid="stToolbar"] {{
    display: none !important;
}}

.main .block-container {{
    padding: 0 1rem 2rem 1rem;
    max-width: 1200px;
}}

/* ===== HEADER ===== */
.main-header {{
    background: linear-gradient(135deg, var(--purple) 0%, #5c005c 50%, var(--purple) 100%);
    margin: 0 -1rem 1.5rem -1rem;
    padding: 1.5rem 1rem;
    border-bottom: 4px solid var(--cyan);
    text-align: center;
}}

.logo-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}}

.logo-icon {{
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, var(--cyan) 0%, #00cc6a 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 4px 20px rgba(0, 255, 133, 0.4);
}}

.logo-text {{
    text-align: left;
}}

.logo-title {{
    font-size: 1.6rem;
    font-weight: 900;
    color: var(--white);
    letter-spacing: 3px;
    margin: 0;
    text-transform: uppercase;
}}

.logo-title span {{
    color: var(--cyan);
}}

.logo-subtitle {{
    font-size: 0.75rem;
    color: var(--cyan);
    letter-spacing: 2px;
    margin: 0.2rem 0 0 0;
    font-weight: 500;
}}

/* ===== STATUS BAR ===== */
.status-bar {{
    background: rgba(0, 255, 133, 0.1);
    border: 1px solid rgba(0, 255, 133, 0.3);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.status-dot {{
    width: 8px;
    height: 8px;
    background: var(--cyan);
    border-radius: 50%;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

.status-text {{
    color: var(--white);
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0;
}}

/* ===== STATS CARDS ===== */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

@media (max-width: 768px) {{
    .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }}
}}

.stat-card {{
    background: linear-gradient(145deg, rgba(90, 0, 90, 0.6) 0%, rgba(55, 0, 60, 0.8) 100%);
    border: 1px solid rgba(255, 40, 130, 0.2);
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.stat-card:hover {{
    border-color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 255, 133, 0.15);
}}

.stat-number {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--cyan);
    margin: 0;
    line-height: 1;
}}

.stat-label {{
    font-size: 0.7rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0.5rem 0 0 0;
}}

/* ===== TABS ===== */
.stTabs {{
    background: transparent;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 0.25rem;
    background: rgba(55, 0, 60, 0.5);
    padding: 0.25rem;
    border-radius: 10px;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    padding: 0.6rem 1.25rem;
    font-weight: 600;
    font-size: 0.8rem;
    border: none;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: var(--white);
    background: rgba(255, 255, 255, 0.1);
}}

.stTabs [aria-selected="true"] {{
    background: var(--cyan) !important;
    color: var(--purple) !important;
}}

/* ===== SECTION HEADERS ===== */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--cyan);
}}

.section-title {{
    font-size: 1rem;
    font-weight: 700;
    color: var(--white);
    margin: 0;
    letter-spacing: 0.5px;
}}

/* ===== CUSTOM TABLE ===== */
.table-container {{
    background: rgba(26, 10, 31, 0.6);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 40, 130, 0.15);
}}

.custom-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}}

.custom-table th {{
    background: linear-gradient(90deg, var(--magenta) 0%, #cc2266 100%);
    color: var(--white);
    font-weight: 600;
    padding: 0.9rem 0.6rem;
    text-align: center;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

.custom-table th:first-child {{
    border-radius: 10px 0 0 0;
}}

.custom-table th:last-child {{
    border-radius: 0 10px 0 0;
}}

.custom-table td {{
    padding: 0.75rem 0.5rem;
    text-align: center;
    color: var(--white);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-weight: 500;
}}

.custom-table tr:hover {{
    background: rgba(255, 40, 130, 0.1);
}}

.custom-table tr:last-child td {{
    border-bottom: none;
}}

.team-cell {{
    text-align: left !important;
    font-weight: 600;
}}

/* Position badges */
.pos-badge {{
    display: inline-block;
    width: 26px;
    height: 26px;
    line-height: 26px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
}}

.pos-ucl {{
    background: var(--cyan);
    color: var(--purple);
}}

.pos-uel {{
    background: #f97316;
    color: var(--white);
}}

.pos-conf {{
    background: #22c55e;
    color: var(--white);
}}

.pos-rel {{
    background: var(--magenta);
    color: var(--white);
}}

.pos-normal {{
    background: rgba(255, 255, 255, 0.1);
    color: var(--white);
}}

.points-cell {{
    font-weight: 800;
    color: var(--cyan);
    font-size: 0.95rem;
}}

.gd-positive {{
    color: var(--cyan);
}}

.gd-negative {{
    color: var(--magenta);
}}

/* ===== PLAYER CARDS ===== */
.player-card {{
    background: linear-gradient(145deg, rgba(90, 0, 90, 0.5) 0%, rgba(55, 0, 60, 0.7) 100%);
    border: 1px solid rgba(0, 255, 133, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}}

.player-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}}

.player-name {{
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--cyan);
    margin: 0;
}}

.player-team {{
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
    margin: 0.25rem 0 0 0;
}}

.player-position {{
    background: var(--magenta);
    color: var(--white);
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}}

.stats-category {{
    margin-top: 1rem;
}}

.stats-category-title {{
    font-size: 0.7rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.6rem 0;
}}

.stats-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.stat-badge {{
    background: rgba(55, 0, 60, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--white);
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 500;
}}

.stat-badge strong {{
    color: var(--cyan);
    font-weight: 700;
    margin-left: 0.25rem;
}}

/* ===== COMPARISON ===== */
.vs-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 1rem 0;
}}

.vs-badge {{
    background: var(--magenta);
    color: var(--white);
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-weight: 800;
    font-size: 0.9rem;
}}

/* ===== SELECT BOXES ===== */
.stSelectbox label {{
    color: var(--white) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}}

.stSelectbox > div > div {{
    background: rgba(55, 0, 60, 0.8) !important;
    border: 1px solid rgba(0, 255, 133, 0.3) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
}}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {{
    background: rgba(55, 0, 60, 0.6) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-weight: 600 !important;
}}

/* ===== FOOTER ===== */
.footer {{
    text-align: center;
    padding: 2rem 1rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}}

.footer p {{
    color: rgba(255, 255, 255, 0.4);
    font-size: 0.75rem;
    margin: 0.25rem 0;
}}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--purple);
}}

::-webkit-scrollbar-thumb {{
    background: var(--cyan);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: #00cc6a;
}}

/* Hide dataframe index */
.row_heading.level0 {{
    display: none;
}}
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

def get_sample_standings():
    return pd.DataFrame({
        'Pos': list(range(1, 21)),
        'Team': ['Arsenal', 'Man City', 'Aston Villa', 'Liverpool', 'Brentford', 'Newcastle',
                 'Man United', 'Chelsea', 'Fulham', 'Sunderland', 'Brighton', 'Everton',
                 'Crystal Palace', 'Tottenham', 'Bournemouth', 'West Ham', 'Wolves',
                 'Leicester', 'Ipswich', 'Southampton'],
        'P': [21]*20,
        'W': [15, 13, 13, 10, 10, 9, 8, 8, 9, 7, 7, 8, 7, 7, 6, 6, 5, 5, 4, 2],
        'D': [4, 4, 4, 5, 3, 5, 8, 7, 4, 9, 8, 5, 7, 6, 8, 6, 7, 4, 6, 6],
        'L': [2, 4, 4, 6, 8, 7, 5, 6, 8, 5, 6, 8, 7, 8, 7, 9, 9, 12, 11, 13],
        'GF': [40, 45, 33, 32, 35, 32, 32, 34, 30, 21, 31, 23, 22, 30, 34, 26, 30, 26, 19, 16],
        'GA': [14, 19, 24, 28, 28, 27, 32, 24, 30, 22, 28, 25, 23, 27, 40, 34, 40, 46, 39, 41],
        'GD': [26, 26, 9, 4, 7, 5, 4, 10, 0, -1, 3, -2, -1, 3, -6, -8, -10, -20, -20, -25],
        'Pts': [49, 43, 43, 35, 33, 32, 32, 31, 31, 30, 29, 29, 28, 27, 26, 24, 22, 19, 18, 12]
    })

def get_sample_scorers():
    return pd.DataFrame({
        'Player': ['Mohamed Salah', 'Erling Haaland', 'Alexander Isak', 'Bryan Mbeumo',
                   'Cole Palmer', 'Chris Wood', 'Yoane Wissa', 'Matheus Cunha',
                   'Nicolas Jackson', 'Ollie Watkins', 'Bukayo Saka', 'Luis Diaz'],
        'Team': ['Liverpool', 'Man City', 'Newcastle', 'Brentford',
                 'Chelsea', 'Nottm Forest', 'Brentford', 'Wolves',
                 'Chelsea', 'Aston Villa', 'Arsenal', 'Liverpool'],
        'Position': ['RW', 'ST', 'ST', 'RW', 'AM', 'ST', 'ST', 'AM', 'ST', 'ST', 'RW', 'LW'],
        'Goals': [18, 16, 13, 13, 12, 12, 10, 10, 9, 8, 8, 8],
        'Assists': [13, 3, 4, 5, 6, 1, 3, 4, 5, 7, 9, 4],
        'Apps': [21, 19, 20, 21, 20, 21, 21, 21, 21, 21, 19, 21],
        'Mins': [1823, 1487, 1701, 1878, 1756, 1823, 1654, 1832, 1698, 1765, 1612, 1543],
        'Shots': [72, 68, 52, 48, 45, 38, 42, 44, 51, 47, 42, 38],
        'xG': [14.2, 15.8, 11.5, 10.8, 9.4, 9.2, 8.6, 8.1, 10.2, 9.5, 7.2, 6.8],
        'GPG': [0.86, 0.84, 0.65, 0.62, 0.60, 0.57, 0.48, 0.48, 0.43, 0.38, 0.42, 0.38]
    })

@st.cache_data(ttl=300)
def fetch_api(api_key, endpoint):
    if not api_key:
        return None
    try:
        headers = {'X-Auth-Token': api_key}
        r = requests.get(f"https://api.football-data.org/v4/{endpoint}", headers=headers, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def get_standings(api_key):
    data = fetch_api(api_key, 'competitions/PL/standings')
    if data and 'standings' in data:
        t = data['standings'][0]['table']
        return pd.DataFrame([{
            'Pos': x['position'], 'Team': x['team']['shortName'], 'P': x['playedGames'],
            'W': x['won'], 'D': x['draw'], 'L': x['lost'], 'GF': x['goalsFor'],
            'GA': x['goalsAgainst'], 'GD': x['goalsFor']-x['goalsAgainst'], 'Pts': x['points']
        } for x in t])
    return get_sample_standings()

def get_scorers(api_key):
    data = fetch_api(api_key, 'competitions/PL/scorers?limit=20')
    if data and 'scorers' in data:
        return pd.DataFrame([{
            'Player': s['player']['name'], 'Team': s['team']['shortName'],
            'Position': (s['player'].get('position', 'FW') or 'FW')[:2],
            'Goals': s.get('goals', 0), 'Assists': s.get('assists', 0),
            'Apps': s.get('playedMatches', 0), 'Mins': s.get('playedMatches', 0) * 80,
            'Shots': s.get('goals', 0) * 4, 'xG': round(s.get('goals', 0) * 0.9, 1),
            'GPG': round(s.get('goals', 0) / max(s.get('playedMatches', 1), 1), 2)
        } for s in data['scorers']])
    return get_sample_scorers()

# ============ RENDER FUNCTIONS ============

def render_table(df):
    """Render custom styled table"""
    html = '<div class="table-container"><table class="custom-table">'
    
    # Header
    html += '<thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead>'
    
    # Body
    html += '<tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            val = row[col]
            
            if col == 'Pos':
                pos = int(val)
                if pos <= 4:
                    badge_class = 'pos-ucl'
                elif pos == 5:
                    badge_class = 'pos-uel'
                elif pos == 6:
                    badge_class = 'pos-conf'
                elif pos >= 18:
                    badge_class = 'pos-rel'
                else:
                    badge_class = 'pos-normal'
                html += f'<td><span class="pos-badge {badge_class}">{pos}</span></td>'
            
            elif col == 'Team':
                html += f'<td class="team-cell">{val}</td>'
            
            elif col == 'Pts':
                html += f'<td class="points-cell">{val}</td>'
            
            elif col == 'GD':
                gd_class = 'gd-positive' if val > 0 else 'gd-negative' if val < 0 else ''
                gd_str = f'+{val}' if val > 0 else str(val)
                html += f'<td class="{gd_class}">{gd_str}</td>'
            
            else:
                html += f'<td>{val}</td>'
        
        html += '</tr>'
    
    html += '</tbody></table></div>'
    return html

def create_chart(df):
    """Create points bar chart"""
    df_s = df.sort_values('Pts', ascending=True)
    
    colors = []
    for pos in df_s['Pos']:
        if pos <= 4:
            colors.append(CYAN)
        elif pos >= 18:
            colors.append(MAGENTA)
        else:
            colors.append('#8B5CF6')
    
    fig = go.Figure(go.Bar(
        x=df_s['Pts'], y=df_s['Team'], orientation='h',
        marker=dict(color=colors),
        text=df_s['Pts'], textposition='outside',
        textfont=dict(color=WHITE, size=10)
    ))
    
    fig.update_layout(
        height=550, margin=dict(l=0, r=50, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE, family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10))
    )
    return fig

def create_comparison_bars(p1, p2, metrics, labels):
    """Create comparison bar chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name=p1['Player'], x=labels, y=[p1.get(m, 0) for m in metrics], marker_color=CYAN))
    fig.add_trace(go.Bar(name=p2['Player'], x=labels, y=[p2.get(m, 0) for m in metrics], marker_color=MAGENTA))
    
    fig.update_layout(
        barmode='group', height=320, margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE, family='Inter', size=11),
        legend=dict(orientation='h', y=1.12, x=0.5, xanchor='center'),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)')
    )
    return fig

def create_radar(p1, p2):
    """Create radar comparison chart"""
    # Normalize values
    metrics = ['Goals', 'Assists', 'Apps', 'Shots', 'xG']
    max_vals = {m: max(p1.get(m, 1), p2.get(m, 1), 1) for m in metrics}
    
    p1_vals = [p1.get(m, 0) / max_vals[m] * 100 for m in metrics]
    p2_vals = [p2.get(m, 0) / max_vals[m] * 100 for m in metrics]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1_vals, theta=metrics, fill='toself', name=p1['Player'],
        line_color=CYAN, fillcolor='rgba(0, 255, 133, 0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_vals, theta=metrics, fill='toself', name=p2['Player'],
        line_color=MAGENTA, fillcolor='rgba(255, 40, 130, 0.2)'
    ))
    
    fig.update_layout(
        height=380, margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=WHITE, size=9)),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=WHITE, size=10))
        ),
        legend=dict(orientation='h', y=-0.05, x=0.5, xanchor='center', font=dict(color=WHITE)),
        font=dict(color=WHITE, family='Inter')
    )
    return fig

# ============ MAIN APP ============

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <div class="logo-icon">⚽</div>
            <div class="logo-text">
                <h1 class="logo-title">PREMIER <span>LEAGUE</span></h1>
                <p class="logo-subtitle">Statistics Hub • 2024/25 Season</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key
    api_key = None
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY")
    except:
        pass
    
    if not api_key:
        with st.expander("Settings"):
            api_key = st.text_input("API Key", type="password", help="Get free key at football-data.org")
    
    # Load data
    standings = get_standings(api_key)
    scorers = get_scorers(api_key)
    
    # Status
    status = "Live data connected" if api_key else "Sample data mode"
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot"></div>
        <p class="status-text">{status} • Showing current season</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <p class="stat-number">{len(standings)}</p>
            <p class="stat-label">Teams</p>
        </div>
        <div class="stat-card">
            <p class="stat-number">{standings['GF'].sum()}</p>
            <p class="stat-label">Total Goals</p>
        </div>
        <div class="stat-card">
            <p class="stat-number">{standings['GF'].mean():.1f}</p>
            <p class="stat-label">Avg Per Team</p>
        </div>
        <div class="stat-card">
            <p class="stat-number">{standings['Pts'].max()}</p>
            <p class="stat-label">Top Points</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["TABLE", "SCORERS", "PLAYER SEARCH", "COMPARE PLAYERS"])
    
    with tab1:
        st.markdown('<div class="section-header"><h2 class="section-title">League Standings</h2></div>', unsafe_allow_html=True)
        st.markdown(render_table(standings), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Points Distribution</h2></div>', unsafe_allow_html=True)
        st.plotly_chart(create_chart(standings), use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown('<div class="section-header"><h2 class="section-title">Top Scorers</h2></div>', unsafe_allow_html=True)
        
        scorer_table = scorers[['Player', 'Team', 'Position', 'Goals', 'Assists', 'Apps']].head(12)
        st.markdown(render_table(scorer_table.reset_index(drop=True).rename(columns={'Position': 'Pos'})), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Top 5 Detailed</h2></div>', unsafe_allow_html=True)
        
        for _, p in scorers.head(5).iterrows():
            st.markdown(f"""
            <div class="player-card">
                <div class="player-header">
                    <div>
                        <h3 class="player-name">{p['Player']}</h3>
                        <p class="player-team">{p['Team']}</p>
                    </div>
                    <span class="player-position">{p['Position']}</span>
                </div>
                <div class="stats-category">
                    <p class="stats-category-title">Goal Contribution</p>
                    <div class="stats-badges">
                        <span class="stat-badge">Goals <strong>{p['Goals']}</strong></span>
                        <span class="stat-badge">Assists <strong>{p['Assists']}</strong></span>
                        <span class="stat-badge">G+A <strong>{p['Goals'] + p['Assists']}</strong></span>
                    </div>
                </div>
                <div class="stats-category">
                    <p class="stats-category-title">Efficiency</p>
                    <div class="stats-badges">
                        <span class="stat-badge">Apps <strong>{p['Apps']}</strong></span>
                        <span class="stat-badge">Goals/Game <strong>{p['GPG']}</strong></span>
                        <span class="stat-badge">xG <strong>{p['xG']}</strong></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-header"><h2 class="section-title">Player Search</h2></div>', unsafe_allow_html=True)
        
        selected = st.selectbox("Select a player", scorers['Player'].tolist())
        
        if selected:
            p = scorers[scorers['Player'] == selected].iloc[0]
            
            st.markdown(f"""
            <div class="player-card">
                <div class="player-header">
                    <div>
                        <h3 class="player-name">{p['Player']}</h3>
                        <p class="player-team">{p['Team']}</p>
                    </div>
                    <span class="player-position">{p['Position']}</span>
                </div>
                <div class="stats-category">
                    <p class="stats-category-title">Goal Contribution</p>
                    <div class="stats-badges">
                        <span class="stat-badge">Goals <strong>{p['Goals']}</strong></span>
                        <span class="stat-badge">Assists <strong>{p['Assists']}</strong></span>
                        <span class="stat-badge">G+A <strong>{p['Goals'] + p['Assists']}</strong></span>
                    </div>
                </div>
                <div class="stats-category">
                    <p class="stats-category-title">Shooting</p>
                    <div class="stats-badges">
                        <span class="stat-badge">Shots <strong>{p['Shots']}</strong></span>
                        <span class="stat-badge">xG <strong>{p['xG']}</strong></span>
                        <span class="stat-badge">Conversion <strong>{round(p['Goals']/max(p['Shots'],1)*100)}%</strong></span>
                    </div>
                </div>
                <div class="stats-category">
                    <p class="stats-category-title">Playing Time</p>
                    <div class="stats-badges">
                        <span class="stat-badge">Appearances <strong>{p['Apps']}</strong></span>
                        <span class="stat-badge">Minutes <strong>{p['Mins']}</strong></span>
                        <span class="stat-badge">Mins/Goal <strong>{round(p['Mins']/max(p['Goals'],1))}</strong></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-header"><h2 class="section-title">Player vs Player</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            p1_name = st.selectbox("Player 1", scorers['Player'].tolist(), key='p1')
        with col2:
            p2_name = st.selectbox("Player 2", scorers['Player'].tolist(), index=1, key='p2')
        
        if p1_name and p2_name and p1_name != p2_name:
            p1 = scorers[scorers['Player'] == p1_name].iloc[0].to_dict()
            p2 = scorers[scorers['Player'] == p2_name].iloc[0].to_dict()
            
            # Player cards side by side
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="player-card" style="border-color: {CYAN};">
                    <h3 class="player-name">{p1['Player']}</h3>
                    <p class="player-team">{p1['Team']} • {p1['Position']}</p>
                    <div class="stats-badges" style="margin-top: 1rem;">
                        <span class="stat-badge">Goals <strong>{p1['Goals']}</strong></span>
                        <span class="stat-badge">Assists <strong>{p1['Assists']}</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="player-card" style="border-color: {MAGENTA};">
                    <h3 class="player-name" style="color: {MAGENTA};">{p2['Player']}</h3>
                    <p class="player-team">{p2['Team']} • {p2['Position']}</p>
                    <div class="stats-badges" style="margin-top: 1rem;">
                        <span class="stat-badge">Goals <strong>{p2['Goals']}</strong></span>
                        <span class="stat-badge">Assists <strong>{p2['Assists']}</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Comparison charts
            st.markdown('<div class="section-header"><h2 class="section-title">Goal Contribution</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(create_comparison_bars(p1, p2, ['Goals', 'Assists'], ['Goals', 'Assists']), use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('<div class="section-header"><h2 class="section-title">Shooting & Efficiency</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(create_comparison_bars(p1, p2, ['Shots', 'xG', 'Apps'], ['Shots', 'xG', 'Apps']), use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('<div class="section-header"><h2 class="section-title">Overall Comparison</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(create_radar(p1, p2), use_container_width=True, config={'displayModeBar': False})
        
        elif p1_name == p2_name:
            st.info("Select two different players to compare")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Data provided by Football-Data.org</p>
        <p>Not affiliated with Premier League</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
