"""
Modern Soccer Statistics Visualization Script
Fetches data from various sources and creates beautiful visualizations
"""

import soccerdata as sd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Set modern style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def fetch_premier_league_data(season='2021'):
    """Fetch Premier League data from FBref"""
    print(f"Fetching Premier League {season} data...")
    fbref = sd.FBref('ENG-Premier League', season)
    
    # Fetch various data types
    print("Fetching schedule data...")
    games = fbref.read_schedule()
    
    print("Fetching team season stats...")
    team_stats = fbref.read_team_season_stats(stat_type="standard")
    
    print("Fetching player stats...")
    player_stats = fbref.read_player_season_stats(stat_type="standard")
    
    return games, team_stats, player_stats

def create_team_performance_dashboard(team_stats, games):
    """Create a comprehensive team performance dashboard"""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Goals Scored vs Conceded', 'Win Rate by Team', 
                       'Points Distribution', 'Goal Difference'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Goals Scored vs Conceded (Scatter)
    fig.add_trace(
        go.Scatter(
            x=team_stats['goals_for'],
            y=team_stats['goals_against'],
            mode='markers+text',
            text=team_stats.index,
            textposition="top center",
            marker=dict(size=12, color=team_stats['points'], 
                       colorscale='Viridis', showscale=True,
                       colorbar=dict(title="Points")),
            name='Teams'
        ),
        row=1, col=1
    )
    
    # Win Rate
    if 'wins' in team_stats.columns and 'games' in team_stats.columns:
        win_rate = (team_stats['wins'] / team_stats['games']) * 100
        fig.add_trace(
            go.Bar(x=team_stats.index, y=win_rate, name='Win Rate %'),
            row=1, col=2
        )
    
    # Points Distribution
    fig.add_trace(
        go.Bar(x=team_stats.index, y=team_stats['points'], 
               marker_color='lightblue', name='Points'),
        row=2, col=1
    )
    
    # Goal Difference
    if 'goals_for' in team_stats.columns and 'goals_against' in team_stats.columns:
        goal_diff = team_stats['goals_for'] - team_stats['goals_against']
        fig.add_trace(
            go.Bar(x=team_stats.index, y=goal_diff, 
                   marker_color='coral', name='Goal Difference'),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text="Premier League Team Performance Dashboard",
        height=800,
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Goals For", row=1, col=1)
    fig.update_yaxes(title_text="Goals Against", row=1, col=1)
    fig.update_xaxes(title_text="Team", row=1, col=2)
    fig.update_yaxes(title_text="Win Rate %", row=1, col=2)
    fig.update_xaxes(title_text="Team", row=2, col=1)
    fig.update_yaxes(title_text="Points", row=2, col=1)
    fig.update_xaxes(title_text="Team", row=2, col=2)
    fig.update_yaxes(title_text="Goal Difference", row=2, col=2)
    
    return fig

def create_matplotlib_visualizations(team_stats, player_stats):
    """Create static matplotlib visualizations"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Premier League Statistics Analysis', fontsize=20, fontweight='bold')
    
    # 1. Goals For vs Goals Against
    ax1 = axes[0, 0]
    scatter = ax1.scatter(team_stats['goals_for'], team_stats['goals_against'],
                         s=team_stats['points']*10, alpha=0.6, 
                         c=team_stats['points'], cmap='viridis')
    ax1.set_xlabel('Goals For', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Goals Against', fontsize=12, fontweight='bold')
    ax1.set_title('Goals For vs Goals Against (Size = Points)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Points')
    
    # Add team labels
    for idx, row in team_stats.iterrows():
        ax1.annotate(idx, (row['goals_for'], row['goals_against']), 
                    fontsize=8, alpha=0.7)
    
    # 2. Points Distribution
    ax2 = axes[0, 1]
    team_stats_sorted = team_stats.sort_values('points', ascending=True)
    colors = plt.cm.RdYlGn(team_stats_sorted['points'] / team_stats_sorted['points'].max())
    ax2.barh(team_stats_sorted.index, team_stats_sorted['points'], color=colors)
    ax2.set_xlabel('Points', fontsize=12, fontweight='bold')
    ax2.set_title('League Standings (Points)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Goal Difference
    ax3 = axes[1, 0]
    if 'goals_for' in team_stats.columns and 'goals_against' in team_stats.columns:
        goal_diff = team_stats['goals_for'] - team_stats['goals_against']
        team_stats_sorted_gd = team_stats.loc[goal_diff.sort_values(ascending=True).index]
        goal_diff_sorted = goal_diff.sort_values(ascending=True)
        colors_gd = ['green' if x > 0 else 'red' for x in goal_diff_sorted]
        ax3.barh(team_stats_sorted_gd.index, goal_diff_sorted, color=colors_gd)
        ax3.set_xlabel('Goal Difference', fontsize=12, fontweight='bold')
        ax3.set_title('Goal Difference by Team', fontsize=14, fontweight='bold')
        ax3.axvline(x=0, color='black', linestyle='--', linewidth=1)
        ax3.grid(True, alpha=0.3, axis='x')
    
    # 4. Top Scorers (if player stats available)
    ax4 = axes[1, 1]
    if player_stats is not None and 'goals' in player_stats.columns:
        top_scorers = player_stats.nlargest(10, 'goals')[['goals']]
        ax4.barh(top_scorers.index, top_scorers['goals'], color='gold')
        ax4.set_xlabel('Goals', fontsize=12, fontweight='bold')
        ax4.set_title('Top 10 Goal Scorers', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')
    else:
        ax4.text(0.5, 0.5, 'Player stats not available', 
                ha='center', va='center', fontsize=14)
        ax4.set_title('Top Scorers', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_seaborn_heatmap(team_stats):
    """Create a correlation heatmap of team statistics"""
    # Select numeric columns for correlation
    numeric_cols = team_stats.select_dtypes(include=['number']).columns
    correlation_data = team_stats[numeric_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_data, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Team Statistics Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    return plt.gcf()

def main():
    """Main function to run the analysis"""
    print("=" * 60)
    print("SOCCER STATISTICS ANALYSIS & VISUALIZATION")
    print("=" * 60)
    
    try:
        # Fetch data
        games, team_stats, player_stats = fetch_premier_league_data(season='2021')
        
        print("\nData fetched successfully!")
        print(f"Teams: {len(team_stats)}")
        print(f"Games: {len(games)}")
        if player_stats is not None:
            print(f"Players: {len(player_stats)}")
        
        # Create visualizations
        print("\nCreating visualizations...")
        
        # 1. Interactive Plotly Dashboard
        print("Creating interactive dashboard...")
        plotly_fig = create_team_performance_dashboard(team_stats, games)
        plotly_fig.write_html("premier_league_dashboard.html")
        print("✓ Saved: premier_league_dashboard.html")
        
        # 2. Matplotlib visualizations
        print("Creating static visualizations...")
        matplotlib_fig = create_matplotlib_visualizations(team_stats, player_stats)
        matplotlib_fig.savefig("premier_league_stats.png", dpi=300, bbox_inches='tight')
        print("✓ Saved: premier_league_stats.png")
        
        # 3. Correlation heatmap
        print("Creating correlation heatmap...")
        heatmap_fig = create_seaborn_heatmap(team_stats)
        heatmap_fig.savefig("team_correlation_heatmap.png", dpi=300, bbox_inches='tight')
        print("✓ Saved: team_correlation_heatmap.png")
        
        # Show the matplotlib plots
        plt.show()
        
        print("\n" + "=" * 60)
        print("Analysis complete! Check the generated files:")
        print("  - premier_league_dashboard.html (Interactive)")
        print("  - premier_league_stats.png (Static)")
        print("  - team_correlation_heatmap.png (Heatmap)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have internet connection")
        print("2. Check if the season/year is valid")
        print("3. Some data sources may require specific configurations")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
