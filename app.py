"""
Soccer Statistics Analysis - Streamlit Web App
Premier League Branded, Mobile-First Design
"""

import streamlit as st
import soccerdata as sd
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="PL Stats Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"  # Better for mobile
)

# Premier League Brand Colors
PL_PURPLE = "#37003c"
PL_PURPLE_LIGHT = "#4a0050"
PL_CYAN = "#00ff85"
PL_MAGENTA = "#ff2882"
PL_WHITE = "#ffffff"
PL_GRAY = "#f5f5f5"
PL_DARK = "#1a1a2e"

# Custom CSS for PL branding and mobile-first design
st.markdown(f"""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(180deg, {PL_PURPLE} 0%, {PL_DARK} 100%);
        min-height: 100vh;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main container */
    .main .block-container {{
        padding: 1rem 1rem 3rem 1rem;
        max-width: 100%;
    }}
    
    /* Header styling */
    .pl-header {{
        background: linear-gradient(135deg, {PL_PURPLE} 0%, {PL_PURPLE_LIGHT} 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 2px solid {PL_CYAN};
        box-shadow: 0 8px 32px rgba(0, 255, 133, 0.15);
    }}
    
    .pl-title {{
        color: {PL_WHITE};
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: 800;
        margin: 0;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    .pl-title span {{
        color: {PL_CYAN};
    }}
    
    .pl-subtitle {{
        color: {PL_CYAN};
        font-size: clamp(0.8rem, 2.5vw, 1rem);
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 500;
    }}
    
    /* Stats cards */
    .stats-container {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }}
    
    @media (min-width: 768px) {{
        .stats-container {{
            grid-template-columns: repeat(4, 1fr);
        }}
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, {PL_PURPLE_LIGHT} 0%, {PL_PURPLE} 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(0, 255, 133, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 255, 133, 0.2);
    }}
    
    .stat-value {{
        color: {PL_CYAN};
        font-size: clamp(1.5rem, 4vw, 2rem);
        font-weight: 700;
        margin: 0;
    }}
    
    .stat-label {{
        color: {PL_WHITE};
        font-size: clamp(0.7rem, 2vw, 0.85rem);
        margin: 0;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Section headers */
    .section-header {{
        color: {PL_WHITE};
        font-size: clamp(1rem, 3vw, 1.3rem);
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {PL_CYAN};
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Selector styling */
    .stSelectbox > div > div {{
        background: {PL_PURPLE_LIGHT} !important;
        border: 2px solid {PL_CYAN} !important;
        border-radius: 10px !important;
        color: {PL_WHITE} !important;
    }}
    
    .stSelectbox label {{
        color: {PL_WHITE} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        background: {PL_PURPLE_LIGHT} !important;
        border: 2px solid {PL_CYAN} !important;
        border-radius: 10px !important;
    }}
    
    .stMultiSelect label {{
        color: {PL_WHITE} !important;
        font-weight: 600 !important;
    }}
    
    /* Checkbox styling */
    .stCheckbox label {{
        color: {PL_WHITE} !important;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: {PL_PURPLE_LIGHT} !important;
        border-radius: 10px !important;
        color: {PL_WHITE} !important;
    }}
    
    /* Warning/Info boxes */
    .stAlert {{
        background: {PL_PURPLE_LIGHT} !important;
        border: 1px solid {PL_CYAN} !important;
        border-radius: 10px !important;
    }}
    
    /* Dataframe styling */
    .stDataFrame {{
        border-radius: 10px;
        overflow: hidden;
    }}
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 0.5rem;
        }}
        
        .pl-header {{
            padding: 1rem;
            border-radius: 12px;
        }}
        
        .element-container {{
            margin-bottom: 0.5rem;
        }}
    }}
    
    /* Chart container */
    .chart-container {{
        background: rgba(55, 0, 60, 0.5);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 255, 133, 0.2);
    }}
    
    /* Footer */
    .pl-footer {{
        text-align: center;
        color: {PL_WHITE};
        opacity: 0.7;
        padding: 2rem 1rem;
        font-size: 0.8rem;
    }}
    
    .pl-footer a {{
        color: {PL_CYAN};
        text-decoration: none;
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {PL_CYAN} !important;
    }}
    
    /* Metric styling */
    [data-testid="stMetricValue"] {{
        color: {PL_CYAN} !important;
        font-size: clamp(1.2rem, 3vw, 1.5rem) !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {PL_WHITE} !important;
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {PL_PURPLE_LIGHT};
        border-radius: 8px 8px 0 0;
        color: {PL_WHITE};
        border: 1px solid rgba(0, 255, 133, 0.3);
        padding: 0.5rem 1rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {PL_CYAN} !important;
        color: {PL_PURPLE} !important;
        font-weight: 700;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {PL_PURPLE};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {PL_CYAN};
        border-radius: 4px;
    }}
    </style>
""", unsafe_allow_html=True)

# Sample data for demo when scraping is blocked
def get_sample_data():
    """Return sample Premier League data for demo purposes"""
    team_data = {
        'team': ['Manchester City', 'Arsenal', 'Liverpool', 'Aston Villa', 'Tottenham', 
                 'Chelsea', 'Newcastle', 'Manchester Utd', 'West Ham', 'Crystal Palace',
                 'Brighton', 'Bournemouth', 'Fulham', 'Wolves', 'Everton',
                 'Brentford', 'Nottingham Forest', 'Luton Town', 'Burnley', 'Sheffield Utd'],
        'games': [38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38],
        'wins': [28, 26, 24, 22, 20, 18, 18, 18, 14, 13, 12, 13, 13, 11, 13, 10, 9, 6, 5, 3],
        'draws': [7, 5, 8, 6, 6, 9, 6, 3, 9, 10, 12, 9, 8, 12, 6, 9, 9, 8, 9, 7],
        'losses': [3, 7, 6, 10, 12, 11, 14, 17, 15, 15, 14, 16, 17, 15, 19, 19, 20, 24, 24, 28],
        'goals_for': [96, 91, 86, 76, 74, 77, 85, 57, 60, 57, 55, 54, 55, 50, 40, 56, 49, 52, 41, 35],
        'goals_against': [34, 29, 41, 61, 61, 63, 62, 58, 74, 58, 62, 67, 61, 65, 51, 65, 67, 85, 78, 104],
        'points': [91, 83, 80, 72, 66, 63, 60, 57, 51, 49, 48, 48, 47, 45, 45, 39, 36, 26, 24, 16]
    }
    team_stats = pd.DataFrame(team_data)
    team_stats = team_stats.set_index('team')
    
    player_data = {
        'player': ['Erling Haaland', 'Cole Palmer', 'Alexander Isak', 'Ollie Watkins', 'Son Heung-min',
                   'Mohamed Salah', 'Jarrod Bowen', 'Dominic Solanke', 'Nicolas Jackson', 'Bryan Mbeumo',
                   'Phil Foden', 'Bruno Fernandes', 'Bukayo Saka', 'Eberechi Eze', 'Anthony Gordon'],
        'goals': [27, 22, 21, 19, 17, 18, 16, 16, 14, 13, 12, 10, 16, 11, 11],
        'assists': [5, 11, 2, 13, 10, 10, 6, 3, 5, 7, 8, 8, 9, 4, 10],
        'team': ['Manchester City', 'Chelsea', 'Newcastle', 'Aston Villa', 'Tottenham',
                 'Liverpool', 'West Ham', 'Bournemouth', 'Chelsea', 'Brentford',
                 'Manchester City', 'Manchester Utd', 'Arsenal', 'Crystal Palace', 'Newcastle']
    }
    player_stats = pd.DataFrame(player_data)
    player_stats = player_stats.set_index('player')
    
    games = pd.DataFrame({'game': range(1, 381)})
    
    return games, team_stats, player_stats

# Cache data fetching
@st.cache_data(ttl=3600)
def fetch_league_data(league, season):
    """Fetch league data with caching"""
    try:
        fbref = sd.FBref(league, season)
        games = fbref.read_schedule()
        team_stats = fbref.read_team_season_stats(stat_type="standard")
        player_stats = fbref.read_player_season_stats(stat_type="standard")
        return games, team_stats, player_stats, None
    except Exception as e:
        if "403" in str(e) or "Forbidden" in str(e) or "Error" in str(e):
            games, team_stats, player_stats = get_sample_data()
            return games, team_stats, player_stats, "demo_mode"
        return None, None, None, str(e)

# Chart creation functions with PL branding
def create_standings_chart(team_stats):
    """Create league standings bar chart"""
    sorted_teams = team_stats.sort_values('points', ascending=True)
    
    # Create gradient colors based on position
    n_teams = len(sorted_teams)
    colors = [f'rgb({int(55 + (0-55)*i/n_teams)}, {int(0 + (255-0)*i/n_teams)}, {int(60 + (133-60)*i/n_teams)})' 
              for i in range(n_teams)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=sorted_teams.index,
        x=sorted_teams['points'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color=PL_CYAN, width=1)
        ),
        text=sorted_teams['points'],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=12, family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Points: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        height=max(500, n_teams * 28),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', color=PL_WHITE),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 133, 0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11)
        ),
        margin=dict(l=10, r=50, t=10, b=10)
    )
    
    return fig

def create_goals_chart(team_stats):
    """Create goals for vs against scatter plot"""
    fig = go.Figure()
    
    # Calculate goal difference for color
    goal_diff = team_stats['goals_for'] - team_stats['goals_against']
    
    fig.add_trace(go.Scatter(
        x=team_stats['goals_for'],
        y=team_stats['goals_against'],
        mode='markers+text',
        text=team_stats.index,
        textposition="top center",
        textfont=dict(size=9, color=PL_WHITE, family='Poppins'),
        marker=dict(
            size=team_stats['points'] / 3 + 10,
            color=goal_diff,
            colorscale=[[0, PL_MAGENTA], [0.5, PL_PURPLE_LIGHT], [1, PL_CYAN]],
            showscale=True,
            colorbar=dict(
                title=dict(text="Goal Diff", font=dict(color=PL_WHITE)),
                tickfont=dict(color=PL_WHITE)
            ),
            line=dict(width=2, color=PL_WHITE)
        ),
        hovertemplate='<b>%{text}</b><br>Goals For: %{x}<br>Goals Against: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title=dict(text="Goals Scored", font=dict(color=PL_CYAN)),
        yaxis_title=dict(text="Goals Conceded", font=dict(color=PL_CYAN)),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', color=PL_WHITE),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 133, 0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 133, 0.1)',
            zeroline=False
        ),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    return fig

def create_top_scorers_chart(player_stats):
    """Create top scorers horizontal bar chart"""
    if player_stats is None or 'goals' not in player_stats.columns:
        return None
    
    top_scorers = player_stats.nlargest(10, 'goals')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_scorers.index,
        x=top_scorers['goals'],
        orientation='h',
        marker=dict(
            color=PL_CYAN,
            line=dict(color=PL_WHITE, width=1)
        ),
        text=top_scorers['goals'],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=12, family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Goals: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', color=PL_WHITE),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 133, 0.1)',
            zeroline=False
        ),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=50, t=10, b=10)
    )
    
    return fig

def create_goal_diff_chart(team_stats):
    """Create goal difference chart"""
    goal_diff = team_stats['goals_for'] - team_stats['goals_against']
    sorted_gd = goal_diff.sort_values(ascending=True)
    
    colors = [PL_CYAN if x > 0 else PL_MAGENTA for x in sorted_gd]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=sorted_gd.index,
        x=sorted_gd.values,
        orientation='h',
        marker=dict(color=colors, line=dict(color=PL_WHITE, width=0.5)),
        text=[f"+{x}" if x > 0 else str(x) for x in sorted_gd.values],
        textposition='outside',
        textfont=dict(color=PL_WHITE, size=10, family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Goal Difference: %{x}<extra></extra>'
    ))
    
    fig.add_shape(
        type="line",
        x0=0, x1=0,
        y0=-0.5, y1=len(sorted_gd)-0.5,
        line=dict(color=PL_WHITE, width=2, dash="dot")
    )
    
    fig.update_layout(
        title=None,
        height=max(450, len(sorted_gd) * 25),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', color=PL_WHITE),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 133, 0.1)',
            zeroline=False
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        margin=dict(l=10, r=60, t=10, b=10)
    )
    
    return fig

def create_win_rate_chart(team_stats):
    """Create win rate donut/pie chart for top 5 teams"""
    if 'wins' not in team_stats.columns or 'games' not in team_stats.columns:
        return None
    
    win_rate = (team_stats['wins'] / team_stats['games']) * 100
    top_5 = win_rate.nlargest(5)
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=top_5.index,
        values=top_5.values,
        hole=0.5,
        marker=dict(
            colors=[PL_CYAN, PL_MAGENTA, PL_PURPLE_LIGHT, '#6b2d5c', '#9d4edd'],
            line=dict(color=PL_WHITE, width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=11, color=PL_WHITE, family='Poppins'),
        hovertemplate='<b>%{label}</b><br>Win Rate: %{value:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', color=PL_WHITE),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[dict(
            text='WIN<br>RATE',
            x=0.5, y=0.5,
            font=dict(size=14, color=PL_CYAN, family='Poppins', weight=700),
            showarrow=False
        )]
    )
    
    return fig

# Main App
def main():
    # Header
    st.markdown("""
        <div class="pl-header">
            <h1 class="pl-title">⚽ <span>Premier League</span> Stats Hub</h1>
            <p class="pl-subtitle">Interactive Statistics & Analysis Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # League and Season selectors in columns (mobile-friendly)
    col1, col2 = st.columns(2)
    
    leagues = {
        "Premier League": "ENG-Premier League",
        "La Liga": "ESP-La Liga",
        "Serie A": "ITA-Serie A",
        "Bundesliga": "GER-Bundesliga",
        "Ligue 1": "FRA-Ligue 1"
    }
    
    with col1:
        selected_league_name = st.selectbox(
            "🏆 League",
            options=list(leagues.keys()),
            index=0
        )
    
    with col2:
        current_year = datetime.now().year
        seasons = [str(year) for year in range(2018, current_year + 1)]
        selected_season = st.selectbox(
            "📅 Season",
            options=seasons,
            index=len(seasons) - 2
        )
    
    selected_league = leagues[selected_league_name]
    
    # Fetch data
    with st.spinner("Loading data..."):
        games, team_stats, player_stats, error = fetch_league_data(selected_league, selected_season)
    
    if error == "demo_mode":
        st.markdown(f"""
            <div style="background: linear-gradient(90deg, {PL_MAGENTA}22, {PL_PURPLE}22); 
                        padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem;
                        border-left: 4px solid {PL_CYAN};">
                <span style="color: {PL_CYAN};">ℹ️</span>
                <span style="color: {PL_WHITE}; font-size: 0.85rem;">
                    <strong>Demo Mode</strong> — Showing sample PL 2023/24 data
                </span>
            </div>
        """, unsafe_allow_html=True)
    elif error:
        st.error(f"Error: {error}")
        return
    
    if team_stats is None or team_stats.empty:
        st.warning("No data available")
        return
    
    # Stats Cards
    total_goals = int(team_stats['goals_for'].sum())
    avg_goals = team_stats['goals_for'].mean()
    top_team = team_stats['points'].idxmax()
    top_points = int(team_stats['points'].max())
    
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <p class="stat-value">{len(team_stats)}</p>
                <p class="stat-label">Teams</p>
            </div>
            <div class="stat-card">
                <p class="stat-value">{total_goals}</p>
                <p class="stat-label">Total Goals</p>
            </div>
            <div class="stat-card">
                <p class="stat-value">{avg_goals:.1f}</p>
                <p class="stat-label">Avg Goals</p>
            </div>
            <div class="stat-card">
                <p class="stat-value">{top_points}</p>
                <p class="stat-label">Top Points</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Standings", "⚽ Goals", "🎯 Scorers", "📈 Analysis"])
    
    with tab1:
        st.markdown('<p class="section-header">🏆 League Table</p>', unsafe_allow_html=True)
        fig = create_standings_chart(team_stats)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown('<p class="section-header">⚽ Goals Analysis</p>', unsafe_allow_html=True)
        fig = create_goals_chart(team_stats)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('<p class="section-header">📊 Goal Difference</p>', unsafe_allow_html=True)
        fig = create_goal_diff_chart(team_stats)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.markdown('<p class="section-header">🎯 Top Scorers</p>', unsafe_allow_html=True)
        fig = create_top_scorers_chart(player_stats)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Player data not available")
    
    with tab4:
        st.markdown('<p class="section-header">📈 Win Rate (Top 5)</p>', unsafe_allow_html=True)
        fig = create_win_rate_chart(team_stats)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Team comparison
        st.markdown('<p class="section-header">🔍 Compare Teams</p>', unsafe_allow_html=True)
        
        team_list = team_stats.index.tolist()
        selected_teams = st.multiselect(
            "Select teams to compare",
            options=team_list,
            default=team_list[:3] if len(team_list) >= 3 else team_list
        )
        
        if selected_teams:
            comparison_data = team_stats.loc[selected_teams][['points', 'wins', 'goals_for', 'goals_against']]
            comparison_data.columns = ['Points', 'Wins', 'Goals For', 'Goals Against']
            
            fig = go.Figure()
            
            colors = [PL_CYAN, PL_MAGENTA, PL_WHITE, '#9d4edd']
            
            for i, col in enumerate(comparison_data.columns):
                fig.add_trace(go.Bar(
                    name=col,
                    x=comparison_data.index,
                    y=comparison_data[col],
                    marker_color=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                barmode='group',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', color=PL_WHITE),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0, 255, 133, 0.1)'),
                margin=dict(l=10, r=10, t=50, b=10)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Data table expander
    with st.expander("📋 View Full Data Table"):
        st.dataframe(
            team_stats.style.background_gradient(cmap='Purples'),
            use_container_width=True
        )
    
    # Footer
    st.markdown(f"""
        <div class="pl-footer">
            <p>Built with ⚽ using Streamlit & SoccerData</p>
            <p>Data source: FBref | Not affiliated with Premier League</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
