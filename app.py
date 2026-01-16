"""
Soccer Statistics Analysis - Streamlit Web App
Mobile-friendly interactive soccer statistics visualization
"""

import streamlit as st
import soccerdata as sd
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Soccer Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly design
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stSelectbox label {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    h1 {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
    }
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        h1 {
            font-size: 1.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Cache data fetching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_league_data(league, season):
    """Fetch league data with caching"""
    try:
        fbref = sd.FBref(league, season)
        games = fbref.read_schedule()
        team_stats = fbref.read_team_season_stats(stat_type="standard")
        player_stats = fbref.read_player_season_stats(stat_type="standard")
        return games, team_stats, player_stats, None
    except Exception as e:
        return None, None, None, str(e)

def create_goals_scatter(team_stats):
    """Create goals for vs goals against scatter plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=team_stats['goals_for'],
        y=team_stats['goals_against'],
        mode='markers+text',
        text=team_stats.index,
        textposition="top center",
        marker=dict(
            size=team_stats['points']*2 if 'points' in team_stats.columns else 12,
            color=team_stats['points'] if 'points' in team_stats.columns else [0]*len(team_stats),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Points"),
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      'Goals For: %{x}<br>' +
                      'Goals Against: %{y}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Goals For vs Goals Against",
        xaxis_title="Goals For",
        yaxis_title="Goals Against",
        height=500,
        template="plotly_white",
        font=dict(size=12)
    )
    
    return fig

def create_points_chart(team_stats):
    """Create points distribution bar chart"""
    sorted_teams = team_stats.sort_values('points', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=sorted_teams.index,
        x=sorted_teams['points'],
        orientation='h',
        marker=dict(
            color=sorted_teams['points'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Points")
        ),
        text=sorted_teams['points'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Points: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title="League Standings (Points)",
        xaxis_title="Points",
        yaxis_title="",
        height=max(600, len(sorted_teams) * 30),
        template="plotly_white",
        font=dict(size=11)
    )
    
    return fig

def create_goal_difference_chart(team_stats):
    """Create goal difference chart"""
    if 'goals_for' in team_stats.columns and 'goals_against' in team_stats.columns:
        goal_diff = team_stats['goals_for'] - team_stats['goals_against']
        sorted_gd = goal_diff.sort_values(ascending=True)
        
        colors = ['green' if x > 0 else 'red' for x in sorted_gd]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_gd.index,
            x=sorted_gd.values,
            orientation='h',
            marker=dict(color=colors),
            text=sorted_gd.values,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Goal Difference: %{x}<extra></extra>'
        ))
        
        fig.add_shape(
            type="line",
            x0=0, x1=0,
            y0=-0.5, y1=len(sorted_gd)-0.5,
            line=dict(color="black", width=2, dash="dash")
        )
        
        fig.update_layout(
            title="Goal Difference by Team",
            xaxis_title="Goal Difference",
            yaxis_title="",
            height=max(600, len(sorted_gd) * 30),
            template="plotly_white",
            font=dict(size=11)
        )
        
        return fig
    return None

def create_win_rate_chart(team_stats):
    """Create win rate chart"""
    if 'wins' in team_stats.columns and 'games' in team_stats.columns:
        win_rate = (team_stats['wins'] / team_stats['games']) * 100
        sorted_wr = win_rate.sort_values(ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_wr.index,
            x=sorted_wr.values,
            orientation='h',
            marker=dict(
                color=sorted_wr.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Win Rate %")
            ),
            text=[f"{x:.1f}%" for x in sorted_wr.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Win Rate: %{x:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Win Rate by Team",
            xaxis_title="Win Rate (%)",
            yaxis_title="",
            height=max(600, len(sorted_wr) * 30),
            template="plotly_white",
            font=dict(size=11)
        )
        
        return fig
    return None

def create_top_scorers_chart(player_stats):
    """Create top scorers chart"""
    if player_stats is not None and 'goals' in player_stats.columns:
        top_scorers = player_stats.nlargest(15, 'goals')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_scorers.index,
            x=top_scorers['goals'],
            orientation='h',
            marker=dict(
                color='gold',
                line=dict(color='orange', width=2)
            ),
            text=top_scorers['goals'],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Goals: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Top Goal Scorers",
            xaxis_title="Goals",
            yaxis_title="",
            height=max(500, len(top_scorers) * 30),
            template="plotly_white",
            font=dict(size=11)
        )
        
        return fig
    return None

def create_team_comparison(team_stats, selected_teams):
    """Create team comparison chart"""
    if not selected_teams:
        return None
    
    comparison_data = team_stats.loc[selected_teams]
    
    metrics = ['points', 'wins', 'goals_for', 'goals_against']
    available_metrics = [m for m in metrics if m in comparison_data.columns]
    
    if not available_metrics:
        return None
    
    fig = go.Figure()
    
    for metric in available_metrics:
        fig.add_trace(go.Bar(
            name=metric.replace('_', ' ').title(),
            x=comparison_data.index,
            y=comparison_data[metric],
            hovertemplate=f'<b>%{{x}}</b><br>{metric.replace("_", " ").title()}: %{{y}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Team Comparison",
        xaxis_title="Team",
        yaxis_title="Value",
        barmode='group',
        height=500,
        template="plotly_white",
        font=dict(size=12)
    )
    
    return fig

# Main App
def main():
    st.title("⚽ Soccer Statistics Analysis")
    st.markdown("### Interactive soccer statistics and visualizations")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # League selection
        leagues = {
            "Premier League": "ENG-Premier League",
            "La Liga": "ESP-La Liga",
            "Serie A": "ITA-Serie A",
            "Bundesliga": "GER-Bundesliga",
            "Ligue 1": "FRA-Ligue 1"
        }
        
        selected_league_name = st.selectbox(
            "Select League",
            options=list(leagues.keys()),
            index=0
        )
        selected_league = leagues[selected_league_name]
        
        # Season selection
        current_year = datetime.now().year
        seasons = [str(year) for year in range(2018, current_year + 1)]
        selected_season = st.selectbox(
            "Select Season",
            options=seasons,
            index=len(seasons) - 2  # Default to previous season
        )
        
        st.markdown("---")
        st.markdown("### 📊 Chart Options")
        
        show_goals_scatter = st.checkbox("Goals Scatter Plot", value=True)
        show_points = st.checkbox("Points Standings", value=True)
        show_goal_diff = st.checkbox("Goal Difference", value=True)
        show_win_rate = st.checkbox("Win Rate", value=True)
        show_top_scorers = st.checkbox("Top Scorers", value=True)
    
    # Fetch data
    with st.spinner(f"Fetching {selected_league_name} {selected_season} data..."):
        games, team_stats, player_stats, error = fetch_league_data(selected_league, selected_season)
    
    if error:
        st.error(f"Error fetching data: {error}")
        st.info("💡 **Tips:**\n- Check your internet connection\n- Try a different season\n- Some leagues may not have data for all seasons")
        return
    
    if team_stats is None or team_stats.empty:
        st.warning("No data available for this league and season.")
        return
    
    # Display key metrics
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Teams", len(team_stats))
    with col2:
        st.metric("Total Games", len(games) if games is not None and not games.empty else "N/A")
    with col3:
        if 'points' in team_stats.columns:
            st.metric("Avg Points", f"{team_stats['points'].mean():.1f}")
    with col4:
        if 'goals_for' in team_stats.columns:
            st.metric("Total Goals", int(team_stats['goals_for'].sum()))
    
    st.markdown("---")
    
    # Charts
    if show_goals_scatter:
        st.markdown("### 🎯 Goals Analysis")
        fig = create_goals_scatter(team_stats)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if show_points:
            st.markdown("### 🏆 League Standings")
            fig = create_points_chart(team_stats)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if show_win_rate:
            st.markdown("### 📊 Win Rate")
            fig = create_win_rate_chart(team_stats)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    if show_goal_diff:
        st.markdown("### ⚖️ Goal Difference")
        fig = create_goal_difference_chart(team_stats)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    if show_top_scorers:
        st.markdown("### ⚽ Top Goal Scorers")
        fig = create_top_scorers_chart(player_stats)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Team Comparison Section
    st.markdown("---")
    st.markdown("### 🔍 Team Comparison")
    
    if 'team' in team_stats.columns:
        team_list = team_stats['team'].tolist()
    else:
        team_list = team_stats.index.tolist()
    
    selected_teams = st.multiselect(
        "Select teams to compare",
        options=team_list,
        default=team_list[:3] if len(team_list) >= 3 else team_list
    )
    
    if selected_teams:
        fig = create_team_comparison(team_stats, selected_teams)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    with st.expander("📋 View Raw Data"):
        st.markdown("### Team Statistics")
        st.dataframe(team_stats, use_container_width=True)
        
        if player_stats is not None and not player_stats.empty:
            st.markdown("### Player Statistics")
            st.dataframe(player_stats.head(50), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Built with ⚽ using Streamlit & SoccerData</p>
            <p>Data source: FBref</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
