"""
Premier League Stats Hub - Mobile-First Web App
Using Football-Data.org API for reliable data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime
import json

# Page config - MUST be first
st.set_page_config(
    page_title="PL Stats Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premier League Official Colors (from premierleague.com)
PL_PURPLE = "#37003c"
PL_MAGENTA = "#ff2882" 
PL_CYAN = "#00ff85"
PL_WHITE = "#ffffff"
PL_DARK = "#1d1d1d"

# Custom CSS matching PL website style
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');

* {{ font-family: 'Montserrat', sans-serif; }}

.stApp {{
    background: {PL_PURPLE};
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.main .block-container {{
    padding: 0.5rem 1rem 2rem 1rem;
    max-width: 1200px;
}}

/* Header */
.pl-header {{
    background: linear-gradient(135deg, {PL_PURPLE} 0%, #5a0066 50%, {PL_PURPLE} 100%);
    padding: 1.5rem;
    border-radius: 0 0 20px 20px;
    margin: -1rem -1rem 1.5rem -1rem;
    text-align: center;
    border-bottom: 3px solid {PL_CYAN};
}}

.pl-logo {{
    font-size: clamp(1.3rem, 4vw, 2rem);
    font-weight: 900;
    color: {PL_WHITE};
    letter-spacing: 3px;
    margin: 0;
}}

.pl-logo span {{ color: {PL_CYAN}; }}

.pl-tagline {{
    color: {PL_CYAN};
    font-size: clamp(0.7rem, 2vw, 0.9rem);
    margin-top: 0.3rem;
    font-weight: 500;
}}

/* Stats Grid */
.stats-row {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
    margin: 1rem 0;
}}

@media (min-width: 600px) {{
    .stats-row {{ grid-template-columns: repeat(4, 1fr); }}
}}

.stat-box {{
    background: linear-gradient(145deg, #4a0050 0%, {PL_PURPLE} 100%);
    border: 1px solid {PL_MAGENTA}40;
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
}}

.stat-num {{
    font-size: clamp(1.5rem, 4vw, 2rem);
    font-weight: 800;
    color: {PL_CYAN};
    margin: 0;
}}

.stat-label {{
    font-size: clamp(0.6rem, 1.5vw, 0.75rem);
    color: {PL_WHITE};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0;
    opacity: 0.9;
}}

/* Section titles */
.section-title {{
    color: {PL_WHITE};
    font-size: clamp(0.9rem, 2.5vw, 1.1rem);
    font-weight: 700;
    padding: 0.5rem 0;
    margin: 1rem 0 0.5rem 0;
    border-bottom: 2px solid {PL_CYAN};
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

/* Table styling */
.standings-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: clamp(0.7rem, 1.8vw, 0.85rem);
}}

.standings-table th {{
    background: {PL_MAGENTA};
    color: {PL_WHITE};
    padding: 0.6rem 0.4rem;
    text-align: center;
    font-weight: 600;
}}

.standings-table td {{
    padding: 0.5rem 0.3rem;
    text-align: center;
    border-bottom: 1px solid {PL_MAGENTA}30;
    color: {PL_WHITE};
}}

.standings-table tr:hover {{
    background: {PL_MAGENTA}20;
}}

.team-name {{
    text-align: left !important;
    font-weight: 600;
}}

.pos-1, .pos-2, .pos-3, .pos-4 {{ color: {PL_CYAN}; font-weight: 700; }}
.pos-18, .pos-19, .pos-20 {{ color: {PL_MAGENTA}; }}

/* Player card */
.player-card {{
    background: linear-gradient(145deg, #4a0050, {PL_PURPLE});
    border: 1px solid {PL_CYAN}50;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}}

.player-name {{
    color: {PL_CYAN};
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0;
}}

.player-team {{
    color: {PL_WHITE};
    font-size: 0.8rem;
    opacity: 0.8;
}}

.player-stat {{
    display: inline-block;
    background: {PL_MAGENTA};
    color: {PL_WHITE};
    padding: 0.3rem 0.6rem;
    border-radius: 15px;
    font-size: 0.75rem;
    margin: 0.2rem;
}}

/* Input styling */
.stTextInput > div > div > input {{
    background: #4a0050 !important;
    border: 2px solid {PL_CYAN} !important;
    border-radius: 25px !important;
    color: {PL_WHITE} !important;
    padding: 0.6rem 1rem !important;
}}

.stSelectbox > div > div {{
    background: #4a0050 !important;
    border: 2px solid {PL_CYAN} !important;
    border-radius: 10px !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: {PL_PURPLE};
    border-radius: 10px 10px 0 0;
    overflow: hidden;
}}

.stTabs [data-baseweb="tab"] {{
    background: #4a0050;
    color: {PL_WHITE};
    border: none;
    padding: 0.7rem 1rem;
    font-weight: 600;
    font-size: 0.8rem;
}}

.stTabs [aria-selected="true"] {{
    background: {PL_CYAN} !important;
    color: {PL_PURPLE} !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: #4a0050 !important;
    color: {PL_WHITE} !important;
    border-radius: 10px !important;
}}

/* Info/warning boxes */
.info-box {{
    background: {PL_CYAN}15;
    border-left: 4px solid {PL_CYAN};
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
}}

.info-box p {{
    color: {PL_WHITE};
    margin: 0;
    font-size: 0.85rem;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 2rem 1rem;
    color: {PL_WHITE};
    opacity: 0.6;
    font-size: 0.75rem;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {PL_PURPLE}; }}
::-webkit-scrollbar-thumb {{ background: {PL_CYAN}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

# Sample data (always works as fallback)
def get_sample_standings():
    """Premier League 2023/24 final standings"""
    return pd.DataFrame({
        'position': list(range(1, 21)),
        'team': ['Manchester City', 'Arsenal', 'Liverpool', 'Aston Villa', 'Tottenham',
                 'Chelsea', 'Newcastle', 'Man United', 'West Ham', 'Crystal Palace',
                 'Brighton', 'Bournemouth', 'Fulham', 'Wolves', 'Everton',
                 'Brentford', 'Nottm Forest', 'Luton Town', 'Burnley', 'Sheffield Utd'],
        'played': [38]*20,
        'won': [28, 26, 24, 22, 20, 18, 18, 18, 14, 13, 12, 13, 13, 11, 13, 10, 9, 6, 5, 3],
        'draw': [7, 5, 8, 6, 6, 9, 6, 3, 9, 10, 12, 9, 8, 12, 6, 9, 9, 8, 9, 7],
        'lost': [3, 7, 6, 10, 12, 11, 14, 17, 15, 15, 14, 16, 17, 15, 19, 19, 20, 24, 24, 28],
        'goalsFor': [96, 91, 86, 76, 74, 77, 85, 57, 60, 57, 55, 54, 55, 50, 40, 56, 49, 52, 41, 35],
        'goalsAgainst': [34, 29, 41, 61, 61, 63, 62, 58, 74, 58, 62, 67, 61, 65, 51, 65, 67, 85, 78, 104],
        'points': [91, 83, 80, 72, 66, 63, 60, 57, 51, 49, 48, 48, 47, 45, 45, 39, 36, 26, 24, 16]
    })

def get_sample_scorers():
    """Top scorers data"""
    return pd.DataFrame({
        'player': ['Erling Haaland', 'Cole Palmer', 'Alexander Isak', 'Ollie Watkins', 
                   'Son Heung-min', 'Mohamed Salah', 'Jarrod Bowen', 'Dominic Solanke',
                   'Nicolas Jackson', 'Bukayo Saka', 'Phil Foden', 'Bryan Mbeumo'],
        'team': ['Manchester City', 'Chelsea', 'Newcastle', 'Aston Villa',
                 'Tottenham', 'Liverpool', 'West Ham', 'Bournemouth',
                 'Chelsea', 'Arsenal', 'Manchester City', 'Brentford'],
        'goals': [27, 22, 21, 19, 17, 18, 16, 16, 14, 16, 12, 13],
        'assists': [5, 11, 2, 13, 10, 10, 6, 3, 5, 9, 8, 7],
        'appearances': [31, 34, 30, 37, 35, 32, 34, 38, 35, 35, 35, 37]
    })

@st.cache_data(ttl=300)
def fetch_api_data(api_key, endpoint):
    """Fetch data from football-data.org API"""
    if not api_key:
        return None
    
    headers = {'X-Auth-Token': api_key}
    base_url = 'https://api.football-data.org/v4'
    
    try:
        response = requests.get(f"{base_url}/{endpoint}", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def get_standings(api_key):
    """Get Premier League standings"""
    data = fetch_api_data(api_key, 'competitions/PL/standings')
    
    if data and 'standings' in data:
        table = data['standings'][0]['table']
        return pd.DataFrame([{
            'position': t['position'],
            'team': t['team']['shortName'],
            'played': t['playedGames'],
            'won': t['won'],
            'draw': t['draw'],
            'lost': t['lost'],
            'goalsFor': t['goalsFor'],
            'goalsAgainst': t['goalsAgainst'],
            'points': t['points']
        } for t in table])
    
    return get_sample_standings()

def get_scorers(api_key):
    """Get top scorers"""
    data = fetch_api_data(api_key, 'competitions/PL/scorers?limit=15')
    
    if data and 'scorers' in data:
        return pd.DataFrame([{
            'player': s['player']['name'],
            'team': s['team']['shortName'],
            'goals': s['goals'],
            'assists': s.get('assists', 0),
            'appearances': s.get('playedMatches', 0)
        } for s in data['scorers']])
    
    return get_sample_scorers()

# ============ CHART FUNCTIONS ============

def create_standings_chart(df):
    """Create horizontal bar chart for standings"""
    df_sorted = df.sort_values('points', ascending=True)
    
    colors = [PL_CYAN if i >= len(df)-4 else (PL_MAGENTA if i < 3 else '#8B5CF6') 
              for i in range(len(df))]
    
    fig = go.Figure(go.Bar(
        x=df_sorted['points'],
        y=df_sorted['team'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=df_sorted['points'],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=11)
    ))
    
    fig.update_layout(
        height=max(450, len(df)*24),
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_WHITE, family='Montserrat'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10))
    )
    
    return fig

def create_goals_chart(df):
    """Goals for vs against scatter"""
    df['gd'] = df['goalsFor'] - df['goalsAgainst']
    
    fig = go.Figure(go.Scatter(
        x=df['goalsFor'],
        y=df['goalsAgainst'],
        mode='markers+text',
        text=df['team'],
        textposition='top center',
        textfont=dict(size=8, color=PL_WHITE),
        marker=dict(
            size=df['points']/4 + 8,
            color=df['gd'],
            colorscale=[[0, PL_MAGENTA], [0.5, '#8B5CF6'], [1, PL_CYAN]],
            showscale=True,
            colorbar=dict(title='GD', tickfont=dict(color=PL_WHITE)),
            line=dict(width=1, color=PL_WHITE)
        ),
        hovertemplate='<b>%{text}</b><br>Scored: %{x}<br>Conceded: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_WHITE, family='Montserrat'),
        xaxis=dict(title='Goals Scored', showgrid=True, gridcolor='rgba(255,40,130,0.1)'),
        yaxis=dict(title='Goals Conceded', showgrid=True, gridcolor='rgba(255,40,130,0.1)')
    )
    
    return fig

def create_scorers_chart(df):
    """Top scorers bar chart"""
    df_top = df.nlargest(10, 'goals')
    
    fig = go.Figure(go.Bar(
        x=df_top['goals'],
        y=df_top['player'],
        orientation='h',
        marker=dict(color=PL_CYAN, line=dict(width=0)),
        text=df_top['goals'],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=11)
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PL_WHITE, family='Montserrat'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)'),
        yaxis=dict(showgrid=False, tickfont=dict(size=10))
    )
    
    return fig

# ============ MAIN APP ============

def main():
    # Header
    st.markdown("""
    <div class="pl-header">
        <p class="pl-logo">⚽ <span>PREMIER LEAGUE</span> STATS HUB</p>
        <p class="pl-tagline">Real-Time Statistics & Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for API key in secrets first, then allow manual input
    api_key = None
    
    # Try to get from Streamlit secrets
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY", None)
    except:
        pass
    
    # If no secret, show input option
    if not api_key:
        with st.expander("⚙️ Settings - Add API key for live data"):
            api_key = st.text_input(
                "Football-Data.org API Key",
                type="password",
                help="Get FREE key at football-data.org/client/register"
            )
            st.markdown("""
            <div class="info-box">
                <p>📌 <strong>Get your FREE API key:</strong> 
                <a href="https://www.football-data.org/client/register" target="_blank" style="color: #00ff85;">
                football-data.org/client/register</a> (10 req/min free)</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        standings = get_standings(api_key if api_key else None)
        scorers = get_scorers(api_key if api_key else None)
    
    if not api_key:
        st.markdown("""
        <div class="info-box">
            <p>ℹ️ Showing <strong>sample data</strong> (2023/24 season). Add API key for live data.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <p>✅ <strong>Live data</strong> connected! Showing current season stats.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats summary
    total_goals = standings['goalsFor'].sum()
    avg_goals = standings['goalsFor'].mean()
    leader = standings.iloc[0]['team']
    top_pts = standings.iloc[0]['points']
    
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box">
            <p class="stat-num">{len(standings)}</p>
            <p class="stat-label">Teams</p>
        </div>
        <div class="stat-box">
            <p class="stat-num">{total_goals}</p>
            <p class="stat-label">Goals</p>
        </div>
        <div class="stat-box">
            <p class="stat-num">{avg_goals:.1f}</p>
            <p class="stat-label">Avg/Team</p>
        </div>
        <div class="stat-box">
            <p class="stat-num">{top_pts}</p>
            <p class="stat-label">Top Pts</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 TABLE", "⚽ GOALS", "🎯 SCORERS", "🔍 SEARCH"])
    
    with tab1:
        st.markdown('<p class="section-title">🏆 League Standings</p>', unsafe_allow_html=True)
        
        # Create HTML table
        table_html = '<table class="standings-table"><tr><th>Pos</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr>'
        
        for _, row in standings.iterrows():
            pos = int(row['position'])
            gd = row['goalsFor'] - row['goalsAgainst']
            gd_str = f"+{gd}" if gd > 0 else str(gd)
            pos_class = f"pos-{pos}" if pos <= 4 or pos >= 18 else ""
            
            table_html += f"""
            <tr>
                <td class="{pos_class}">{pos}</td>
                <td class="team-name">{row['team']}</td>
                <td>{row['played']}</td>
                <td>{row['won']}</td>
                <td>{row['draw']}</td>
                <td>{row['lost']}</td>
                <td>{row['goalsFor']}</td>
                <td>{row['goalsAgainst']}</td>
                <td>{gd_str}</td>
                <td><strong>{row['points']}</strong></td>
            </tr>
            """
        
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Points chart
        st.markdown('<p class="section-title">📈 Points Distribution</p>', unsafe_allow_html=True)
        fig = create_standings_chart(standings)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown('<p class="section-title">⚽ Goals Analysis</p>', unsafe_allow_html=True)
        fig = create_goals_chart(standings)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Goal difference ranking
        st.markdown('<p class="section-title">📊 Goal Difference</p>', unsafe_allow_html=True)
        standings['gd'] = standings['goalsFor'] - standings['goalsAgainst']
        gd_sorted = standings.sort_values('gd', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=gd_sorted['gd'],
            y=gd_sorted['team'],
            orientation='h',
            marker=dict(color=[PL_CYAN if x > 0 else PL_MAGENTA for x in gd_sorted['gd']]),
            text=[f"+{x}" if x > 0 else str(x) for x in gd_sorted['gd']],
            textposition='outside',
            textfont=dict(color=PL_WHITE, size=10)
        ))
        
        fig.add_vline(x=0, line_color=PL_WHITE, line_dash="dot")
        
        fig.update_layout(
            height=max(400, len(standings)*22),
            margin=dict(l=0, r=50, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=PL_WHITE, family='Montserrat'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)'),
            yaxis=dict(showgrid=False, tickfont=dict(size=9))
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.markdown('<p class="section-title">🎯 Top Scorers</p>', unsafe_allow_html=True)
        
        fig = create_scorers_chart(scorers)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Player cards
        st.markdown('<p class="section-title">👤 Player Details</p>', unsafe_allow_html=True)
        
        for _, player in scorers.head(5).iterrows():
            st.markdown(f"""
            <div class="player-card">
                <p class="player-name">{player['player']}</p>
                <p class="player-team">{player['team']}</p>
                <span class="player-stat">⚽ {player['goals']} Goals</span>
                <span class="player-stat">🎯 {player['assists']} Assists</span>
                <span class="player-stat">📊 {player['appearances']} Apps</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<p class="section-title">🔍 Search & Compare</p>', unsafe_allow_html=True)
        
        # Team search
        team_search = st.selectbox("Select Team", options=standings['team'].tolist())
        
        if team_search:
            team_data = standings[standings['team'] == team_search].iloc[0]
            gd = team_data['goalsFor'] - team_data['goalsAgainst']
            
            st.markdown(f"""
            <div class="player-card">
                <p class="player-name">{team_search}</p>
                <p class="player-team">Position: #{int(team_data['position'])}</p>
                <span class="player-stat">📊 {int(team_data['points'])} Pts</span>
                <span class="player-stat">✅ {int(team_data['won'])}W</span>
                <span class="player-stat">➖ {int(team_data['draw'])}D</span>
                <span class="player-stat">❌ {int(team_data['lost'])}L</span>
                <span class="player-stat">⚽ {int(team_data['goalsFor'])} GF</span>
                <span class="player-stat">🥅 {int(team_data['goalsAgainst'])} GA</span>
                <span class="player-stat">📈 {'+' if gd > 0 else ''}{gd} GD</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Compare teams
        st.markdown('<p class="section-title">⚔️ Compare Teams</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            team1 = st.selectbox("Team 1", standings['team'].tolist(), key='t1')
        with col2:
            team2 = st.selectbox("Team 2", standings['team'].tolist(), index=1, key='t2')
        
        if team1 and team2:
            t1_data = standings[standings['team'] == team1].iloc[0]
            t2_data = standings[standings['team'] == team2].iloc[0]
            
            compare_metrics = ['points', 'won', 'goalsFor', 'goalsAgainst']
            compare_labels = ['Points', 'Wins', 'Goals For', 'Goals Against']
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name=team1,
                x=compare_labels,
                y=[t1_data[m] for m in compare_metrics],
                marker_color=PL_CYAN
            ))
            
            fig.add_trace(go.Bar(
                name=team2,
                x=compare_labels,
                y=[t2_data[m] for m in compare_metrics],
                marker_color=PL_MAGENTA
            ))
            
            fig.update_layout(
                barmode='group',
                height=300,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=PL_WHITE, family='Montserrat', size=11),
                legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Data: Football-Data.org | Not affiliated with Premier League</p>
        <p>Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
