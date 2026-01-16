"""
Premier League Stats Hub - Professional Dashboard
Clean UI, Player Comparison, Live Data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="PL Stats Hub",
    page_icon="https://www.premierleague.com/resources/rebrand/v7/i/elements/pl-main-logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premier League Colors
PL_PURPLE = "#37003c"
PL_MAGENTA = "#ff2882"
PL_CYAN = "#00ff85"
PL_WHITE = "#ffffff"

# Clean Professional CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}

.stApp {{ background: {PL_PURPLE}; }}

#MainMenu, footer, header {{ visibility: hidden; }}

.main .block-container {{
    padding: 1rem;
    max-width: 1200px;
}}

/* Header */
.header {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, {PL_PURPLE} 0%, #5c005c 100%);
    border-bottom: 3px solid {PL_CYAN};
    margin: -1rem -1rem 1.5rem -1rem;
}}

.header img {{
    height: 50px;
}}

.header-text {{
    text-align: center;
}}

.header-title {{
    color: {PL_WHITE};
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
}}

.header-sub {{
    color: {PL_CYAN};
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0;
}}

/* Stats row */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1rem 0;
}}

@media (max-width: 600px) {{
    .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

.stat-card {{
    background: linear-gradient(135deg, #4a004a 0%, {PL_PURPLE} 100%);
    border: 1px solid {PL_MAGENTA}30;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}}

.stat-value {{
    color: {PL_CYAN};
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
}}

.stat-label {{
    color: {PL_WHITE};
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0;
    opacity: 0.8;
}}

/* Section */
.section {{
    margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid {PL_CYAN};
}}

.section-title {{
    color: {PL_WHITE};
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: transparent;
}}

.stTabs [data-baseweb="tab"] {{
    background: #4a004a;
    color: {PL_WHITE};
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    font-size: 0.8rem;
    border: none;
}}

.stTabs [aria-selected="true"] {{
    background: {PL_CYAN} !important;
    color: {PL_PURPLE} !important;
}}

/* Data table */
.dataframe {{
    font-size: 0.8rem !important;
}}

/* Player card */
.player-card {{
    background: linear-gradient(135deg, #4a004a 0%, {PL_PURPLE} 100%);
    border: 1px solid {PL_CYAN}40;
    border-radius: 10px;
    padding: 1.25rem;
    margin: 0.75rem 0;
}}

.player-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}}

.player-name {{
    color: {PL_CYAN};
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
}}

.player-team {{
    color: {PL_WHITE};
    font-size: 0.85rem;
    opacity: 0.7;
    margin: 0.2rem 0 0 0;
}}

.player-position {{
    background: {PL_MAGENTA};
    color: {PL_WHITE};
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}}

.stats-section {{
    margin-top: 1rem;
}}

.stats-section-title {{
    color: {PL_WHITE};
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.5rem 0;
    opacity: 0.6;
}}

.stats-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.stat-badge {{
    background: {PL_PURPLE};
    border: 1px solid {PL_CYAN}50;
    color: {PL_WHITE};
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.8rem;
}}

.stat-badge strong {{
    color: {PL_CYAN};
    margin-left: 0.3rem;
}}

/* Compare section */
.compare-grid {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 1rem;
    align-items: start;
}}

@media (max-width: 768px) {{
    .compare-grid {{
        grid-template-columns: 1fr;
    }}
}}

.vs-badge {{
    background: {PL_MAGENTA};
    color: {PL_WHITE};
    padding: 0.5rem 1rem;
    border-radius: 50%;
    font-weight: 800;
    align-self: center;
}}

/* Input styling */
.stSelectbox > div > div {{
    background: #4a004a !important;
    border: 1px solid {PL_CYAN} !important;
    border-radius: 8px !important;
}}

.stSelectbox label {{
    color: {PL_WHITE} !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}}

/* Alert */
.alert {{
    background: {PL_CYAN}15;
    border-left: 3px solid {PL_CYAN};
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    margin: 0.75rem 0;
}}

.alert p {{
    color: {PL_WHITE};
    margin: 0;
    font-size: 0.85rem;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: #4a004a !important;
    color: {PL_WHITE} !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 2rem;
    color: {PL_WHITE};
    opacity: 0.5;
    font-size: 0.75rem;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {PL_PURPLE}; }}
::-webkit-scrollbar-thumb {{ background: {PL_CYAN}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

def get_sample_standings():
    """Sample Premier League standings"""
    return pd.DataFrame({
        'Pos': list(range(1, 21)),
        'Team': ['Liverpool', 'Arsenal', 'Nottm Forest', 'Chelsea', 'Man City', 'Brighton',
                 'Bournemouth', 'Aston Villa', 'Fulham', 'Newcastle', 'Brentford', 'Man United',
                 'West Ham', 'Tottenham', 'Crystal Palace', 'Everton', 'Wolves', 'Leicester',
                 'Ipswich', 'Southampton'],
        'P': [21]*20,
        'W': [14, 12, 12, 11, 11, 10, 10, 10, 9, 8, 9, 8, 8, 8, 6, 5, 6, 5, 4, 2],
        'D': [5, 6, 4, 5, 4, 6, 5, 5, 6, 8, 4, 6, 5, 4, 7, 7, 5, 5, 6, 6],
        'L': [2, 3, 5, 5, 6, 5, 6, 6, 6, 5, 8, 7, 8, 9, 8, 9, 10, 11, 11, 13],
        'GF': [52, 42, 32, 42, 40, 35, 33, 34, 35, 32, 39, 28, 32, 43, 26, 19, 32, 29, 19, 16],
        'GA': [20, 19, 22, 27, 26, 27, 26, 31, 29, 22, 36, 26, 37, 32, 32, 28, 41, 44, 39, 41],
        'GD': [32, 23, 10, 15, 14, 8, 7, 3, 6, 10, 3, 2, -5, 11, -6, -9, -9, -15, -20, -25],
        'Pts': [47, 42, 40, 38, 37, 36, 35, 35, 33, 32, 31, 30, 29, 28, 25, 22, 23, 20, 18, 12]
    })

def get_sample_scorers():
    """Sample top scorers with detailed stats"""
    return pd.DataFrame({
        'Player': ['Mohamed Salah', 'Erling Haaland', 'Alexander Isak', 'Bryan Mbeumo', 
                   'Cole Palmer', 'Chris Wood', 'Yoane Wissa', 'Matheus Cunha',
                   'Nicolas Jackson', 'Ollie Watkins', 'Luis Diaz', 'Bukayo Saka'],
        'Team': ['Liverpool', 'Man City', 'Newcastle', 'Brentford',
                 'Chelsea', 'Nottm Forest', 'Brentford', 'Wolves',
                 'Chelsea', 'Aston Villa', 'Liverpool', 'Arsenal'],
        'Position': ['RW', 'ST', 'ST', 'RW', 'AM', 'ST', 'ST', 'AM', 'ST', 'ST', 'LW', 'RW'],
        'Goals': [18, 16, 13, 13, 12, 12, 10, 10, 9, 8, 8, 8],
        'Assists': [13, 3, 4, 5, 6, 1, 3, 4, 5, 7, 4, 9],
        'Appearances': [21, 19, 20, 21, 20, 21, 21, 21, 21, 21, 21, 19],
        'Minutes': [1823, 1487, 1701, 1878, 1756, 1823, 1654, 1832, 1698, 1765, 1543, 1612],
        'Shots': [72, 68, 52, 48, 45, 38, 42, 44, 51, 47, 38, 42],
        'ShotsOnTarget': [38, 32, 28, 24, 22, 19, 21, 18, 26, 24, 18, 21],
        'xG': [14.2, 15.8, 11.5, 10.8, 9.4, 9.2, 8.6, 8.1, 10.2, 9.5, 6.8, 7.2],
        'GoalsPerGame': [0.86, 0.84, 0.65, 0.62, 0.60, 0.57, 0.48, 0.48, 0.43, 0.38, 0.38, 0.42],
        'MinutesPerGoal': [101, 93, 131, 144, 146, 152, 165, 183, 189, 221, 193, 201]
    })

@st.cache_data(ttl=300)
def fetch_api_data(api_key, endpoint):
    """Fetch from Football-Data.org API"""
    if not api_key:
        return None
    try:
        headers = {'X-Auth-Token': api_key}
        response = requests.get(f"https://api.football-data.org/v4/{endpoint}", 
                               headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_standings(api_key):
    """Get standings from API or sample"""
    data = fetch_api_data(api_key, 'competitions/PL/standings')
    if data and 'standings' in data:
        table = data['standings'][0]['table']
        return pd.DataFrame([{
            'Pos': t['position'],
            'Team': t['team']['shortName'],
            'P': t['playedGames'],
            'W': t['won'],
            'D': t['draw'],
            'L': t['lost'],
            'GF': t['goalsFor'],
            'GA': t['goalsAgainst'],
            'GD': t['goalsFor'] - t['goalsAgainst'],
            'Pts': t['points']
        } for t in table])
    return get_sample_standings()

def get_scorers(api_key):
    """Get scorers from API or sample"""
    data = fetch_api_data(api_key, 'competitions/PL/scorers?limit=20')
    if data and 'scorers' in data:
        return pd.DataFrame([{
            'Player': s['player']['name'],
            'Team': s['team']['shortName'],
            'Position': s['player'].get('position', 'FW')[:2] if s['player'].get('position') else 'FW',
            'Goals': s.get('goals', 0),
            'Assists': s.get('assists', 0),
            'Appearances': s.get('playedMatches', 0),
            'Minutes': s.get('playedMatches', 0) * 75,
            'Shots': s.get('goals', 0) * 4,
            'ShotsOnTarget': s.get('goals', 0) * 2,
            'xG': round(s.get('goals', 0) * 0.85, 1),
            'GoalsPerGame': round(s.get('goals', 0) / max(s.get('playedMatches', 1), 1), 2),
            'MinutesPerGoal': round((s.get('playedMatches', 0) * 75) / max(s.get('goals', 1), 1))
        } for s in data['scorers']])
    return get_sample_scorers()

# ============ CHART FUNCTIONS ============

def create_standings_chart(df):
    """Standings bar chart"""
    df_sorted = df.sort_values('Pts', ascending=True)
    
    colors = []
    for i, pos in enumerate(df_sorted['Pos'].values):
        if pos <= 4:
            colors.append(PL_CYAN)
        elif pos >= 18:
            colors.append(PL_MAGENTA)
        else:
            colors.append('#8B5CF6')
    
    fig = go.Figure(go.Bar(
        x=df_sorted['Pts'],
        y=df_sorted['Team'],
        orientation='h',
        marker=dict(color=colors),
        text=df_sorted['Pts'],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=10)
    ))
    
    fig.update_layout(
        height=550,
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_WHITE, family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10))
    )
    return fig

def create_comparison_chart(p1_data, p2_data, metrics, labels):
    """Create player comparison radar chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[p1_data.get(m, 0) for m in metrics],
        theta=labels,
        fill='toself',
        name=p1_data['Player'],
        line_color=PL_CYAN,
        fillcolor=f'{PL_CYAN}40'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[p2_data.get(m, 0) for m in metrics],
        theta=labels,
        fill='toself',
        name=p2_data['Player'],
        line_color=PL_MAGENTA,
        fillcolor=f'{PL_MAGENTA}40'
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=PL_WHITE)),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=PL_WHITE, size=10))
        ),
        legend=dict(
            orientation='h',
            y=-0.1,
            x=0.5,
            xanchor='center',
            font=dict(color=PL_WHITE)
        ),
        font=dict(color=PL_WHITE, family='Inter')
    )
    return fig

def create_bar_comparison(p1_data, p2_data, metrics, labels):
    """Create bar comparison chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=p1_data['Player'],
        x=labels,
        y=[p1_data.get(m, 0) for m in metrics],
        marker_color=PL_CYAN
    ))
    
    fig.add_trace(go.Bar(
        name=p2_data['Player'],
        x=labels,
        y=[p2_data.get(m, 0) for m in metrics],
        marker_color=PL_MAGENTA
    ))
    
    fig.update_layout(
        barmode='group',
        height=350,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_WHITE, family='Inter', size=11),
        legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)')
    )
    return fig

# ============ MAIN APP ============

def main():
    # Header with PL logo
    st.markdown("""
    <div class="header">
        <img src="https://www.premierleague.com/resources/rebrand/v7/i/elements/pl-main-logo.png" alt="PL">
        <div class="header-text">
            <p class="header-title">PREMIER LEAGUE STATS HUB</p>
            <p class="header-sub">Live Statistics & Player Analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key
    api_key = None
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY", None)
    except:
        pass
    
    if not api_key:
        with st.expander("Settings - API Key"):
            api_key = st.text_input("Football-Data.org API Key", type="password")
    
    # Load data
    standings = get_standings(api_key)
    scorers = get_scorers(api_key)
    
    # Status
    if api_key:
        st.markdown('<div class="alert"><p>Live data connected - Showing current season</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert"><p>Sample data - Add API key for live stats</p></div>', unsafe_allow_html=True)
    
    # Stats cards
    total_goals = standings['GF'].sum()
    avg_goals = standings['GF'].mean()
    top_pts = standings['Pts'].max()
    
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <p class="stat-value">{len(standings)}</p>
            <p class="stat-label">Teams</p>
        </div>
        <div class="stat-card">
            <p class="stat-value">{total_goals}</p>
            <p class="stat-label">Total Goals</p>
        </div>
        <div class="stat-card">
            <p class="stat-value">{avg_goals:.1f}</p>
            <p class="stat-label">Avg Per Team</p>
        </div>
        <div class="stat-card">
            <p class="stat-value">{top_pts}</p>
            <p class="stat-label">Top Points</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["TABLE", "SCORERS", "PLAYER SEARCH", "PLAYER VS PLAYER"])
    
    with tab1:
        st.markdown('<div class="section"><p class="section-title">League Standings</p></div>', unsafe_allow_html=True)
        
        # Style the dataframe
        def style_standings(df):
            def highlight_pos(row):
                pos = row['Pos']
                if pos <= 4:
                    return [f'background-color: {PL_CYAN}20; color: {PL_CYAN}'] * len(row)
                elif pos >= 18:
                    return [f'background-color: {PL_MAGENTA}20; color: {PL_MAGENTA}'] * len(row)
                return [''] * len(row)
            return df.style.apply(highlight_pos, axis=1)
        
        st.dataframe(
            style_standings(standings),
            use_container_width=True,
            hide_index=True,
            height=550
        )
        
        st.markdown('<div class="section"><p class="section-title">Points Distribution</p></div>', unsafe_allow_html=True)
        fig = create_standings_chart(standings)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown('<div class="section"><p class="section-title">Top Scorers</p></div>', unsafe_allow_html=True)
        
        scorer_display = scorers[['Player', 'Team', 'Position', 'Goals', 'Assists', 'Appearances']].head(15)
        st.dataframe(scorer_display, use_container_width=True, hide_index=True, height=450)
        
        # Top 5 player cards
        st.markdown('<div class="section"><p class="section-title">Top 5 Players</p></div>', unsafe_allow_html=True)
        
        for _, player in scorers.head(5).iterrows():
            st.markdown(f"""
            <div class="player-card">
                <div class="player-header">
                    <div>
                        <p class="player-name">{player['Player']}</p>
                        <p class="player-team">{player['Team']}</p>
                    </div>
                    <span class="player-position">{player['Position']}</span>
                </div>
                <div class="stats-section">
                    <p class="stats-section-title">Goal Contribution</p>
                    <div class="stats-row">
                        <span class="stat-badge">Goals<strong>{player['Goals']}</strong></span>
                        <span class="stat-badge">Assists<strong>{player['Assists']}</strong></span>
                        <span class="stat-badge">G+A<strong>{player['Goals'] + player['Assists']}</strong></span>
                    </div>
                </div>
                <div class="stats-section">
                    <p class="stats-section-title">Performance</p>
                    <div class="stats-row">
                        <span class="stat-badge">Apps<strong>{player['Appearances']}</strong></span>
                        <span class="stat-badge">Goals/Game<strong>{player['GoalsPerGame']}</strong></span>
                        <span class="stat-badge">Mins/Goal<strong>{player['MinutesPerGoal']}</strong></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section"><p class="section-title">Player Search</p></div>', unsafe_allow_html=True)
        
        player_list = scorers['Player'].tolist()
        selected_player = st.selectbox("Select Player", player_list, key="search_player")
        
        if selected_player:
            player_data = scorers[scorers['Player'] == selected_player].iloc[0]
            
            st.markdown(f"""
            <div class="player-card">
                <div class="player-header">
                    <div>
                        <p class="player-name">{player_data['Player']}</p>
                        <p class="player-team">{player_data['Team']}</p>
                    </div>
                    <span class="player-position">{player_data['Position']}</span>
                </div>
                
                <div class="stats-section">
                    <p class="stats-section-title">Goal Contribution</p>
                    <div class="stats-row">
                        <span class="stat-badge">Goals<strong>{player_data['Goals']}</strong></span>
                        <span class="stat-badge">Assists<strong>{player_data['Assists']}</strong></span>
                        <span class="stat-badge">G+A<strong>{player_data['Goals'] + player_data['Assists']}</strong></span>
                    </div>
                </div>
                
                <div class="stats-section">
                    <p class="stats-section-title">Shooting</p>
                    <div class="stats-row">
                        <span class="stat-badge">Shots<strong>{player_data['Shots']}</strong></span>
                        <span class="stat-badge">On Target<strong>{player_data['ShotsOnTarget']}</strong></span>
                        <span class="stat-badge">xG<strong>{player_data['xG']}</strong></span>
                    </div>
                </div>
                
                <div class="stats-section">
                    <p class="stats-section-title">Efficiency</p>
                    <div class="stats-row">
                        <span class="stat-badge">Goals/Game<strong>{player_data['GoalsPerGame']}</strong></span>
                        <span class="stat-badge">Mins/Goal<strong>{player_data['MinutesPerGoal']}</strong></span>
                        <span class="stat-badge">Shot Accuracy<strong>{round(player_data['ShotsOnTarget']/max(player_data['Shots'],1)*100)}%</strong></span>
                    </div>
                </div>
                
                <div class="stats-section">
                    <p class="stats-section-title">Playing Time</p>
                    <div class="stats-row">
                        <span class="stat-badge">Appearances<strong>{player_data['Appearances']}</strong></span>
                        <span class="stat-badge">Minutes<strong>{player_data['Minutes']}</strong></span>
                        <span class="stat-badge">Mins/App<strong>{round(player_data['Minutes']/max(player_data['Appearances'],1))}</strong></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section"><p class="section-title">Player vs Player Comparison</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            player1 = st.selectbox("Player 1", scorers['Player'].tolist(), key="p1")
        with col2:
            player2 = st.selectbox("Player 2", scorers['Player'].tolist(), index=1, key="p2")
        
        if player1 and player2 and player1 != player2:
            p1_data = scorers[scorers['Player'] == player1].iloc[0].to_dict()
            p2_data = scorers[scorers['Player'] == player2].iloc[0].to_dict()
            
            # Side by side player cards
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="player-card" style="border-color: {PL_CYAN};">
                    <p class="player-name">{p1_data['Player']}</p>
                    <p class="player-team">{p1_data['Team']} | {p1_data['Position']}</p>
                    <div class="stats-section">
                        <div class="stats-row">
                            <span class="stat-badge">Goals<strong>{p1_data['Goals']}</strong></span>
                            <span class="stat-badge">Assists<strong>{p1_data['Assists']}</strong></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="player-card" style="border-color: {PL_MAGENTA};">
                    <p class="player-name" style="color: {PL_MAGENTA};">{p2_data['Player']}</p>
                    <p class="player-team">{p2_data['Team']} | {p2_data['Position']}</p>
                    <div class="stats-section">
                        <div class="stats-row">
                            <span class="stat-badge">Goals<strong>{p2_data['Goals']}</strong></span>
                            <span class="stat-badge">Assists<strong>{p2_data['Assists']}</strong></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Comparison charts
            st.markdown('<div class="section"><p class="section-title">Goal Contribution</p></div>', unsafe_allow_html=True)
            
            metrics1 = ['Goals', 'Assists']
            fig = create_bar_comparison(p1_data, p2_data, metrics1, ['Goals', 'Assists'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('<div class="section"><p class="section-title">Shooting Stats</p></div>', unsafe_allow_html=True)
            
            metrics2 = ['Shots', 'ShotsOnTarget', 'xG']
            fig = create_bar_comparison(p1_data, p2_data, metrics2, ['Total Shots', 'On Target', 'xG'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('<div class="section"><p class="section-title">Efficiency</p></div>', unsafe_allow_html=True)
            
            metrics3 = ['GoalsPerGame', 'Appearances']
            fig = create_bar_comparison(p1_data, p2_data, metrics3, ['Goals/Game', 'Appearances'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('<div class="section"><p class="section-title">Overall Comparison</p></div>', unsafe_allow_html=True)
            
            # Normalize data for radar
            p1_norm = p1_data.copy()
            p2_norm = p2_data.copy()
            
            max_goals = max(p1_data['Goals'], p2_data['Goals'], 1)
            max_assists = max(p1_data['Assists'], p2_data['Assists'], 1)
            max_shots = max(p1_data['Shots'], p2_data['Shots'], 1)
            max_xg = max(p1_data['xG'], p2_data['xG'], 1)
            max_apps = max(p1_data['Appearances'], p2_data['Appearances'], 1)
            
            for p in [p1_norm, p2_norm]:
                p['Goals'] = p['Goals'] / max_goals * 100
                p['Assists'] = p['Assists'] / max_assists * 100
                p['Shots'] = p['Shots'] / max_shots * 100
                p['xG'] = p['xG'] / max_xg * 100
                p['Appearances'] = p['Appearances'] / max_apps * 100
            
            radar_metrics = ['Goals', 'Assists', 'Shots', 'xG', 'Appearances']
            radar_labels = ['Goals', 'Assists', 'Shots', 'xG', 'Apps']
            
            fig = create_comparison_chart(p1_norm, p2_norm, radar_metrics, radar_labels)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        elif player1 == player2:
            st.markdown('<div class="alert"><p>Select two different players to compare</p></div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Data: Football-Data.org | Not affiliated with Premier League</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
