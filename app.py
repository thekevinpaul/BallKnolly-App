"""
Premier League Stats Hub - Professional Dashboard
Comprehensive Player Analysis & Comparison
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
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
    flex-wrap: wrap;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    font-size: 0.75rem;
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

/* ===== CUSTOM TABLE - STANDINGS ===== */
.table-container {{
    background: rgba(26, 10, 31, 0.6);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 40, 130, 0.15);
    overflow-x: auto;
}}

.custom-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    min-width: 600px;
}}

.custom-table th {{
    background: linear-gradient(90deg, var(--magenta) 0%, #cc2266 100%);
    color: var(--white);
    font-weight: 600;
    padding: 0.9rem 0.5rem;
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
}}

.custom-table th:first-child {{
    border-radius: 10px 0 0 0;
}}

.custom-table th:last-child {{
    border-radius: 0 10px 0 0;
}}

.custom-table td {{
    padding: 0.7rem 0.4rem;
    text-align: center;
    color: var(--white);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-weight: 500;
    font-size: 0.8rem;
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
    padding-left: 0.8rem !important;
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

/* ===== SCORERS TABLE ===== */
.scorers-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}}

.scorers-table th {{
    background: linear-gradient(90deg, var(--magenta) 0%, #cc2266 100%);
    color: var(--white);
    font-weight: 600;
    padding: 0.9rem 0.6rem;
    text-align: center;
    font-size: 0.7rem;
    text-transform: uppercase;
}}

.scorers-table td {{
    padding: 0.75rem 0.5rem;
    text-align: center;
    color: var(--white);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-weight: 500;
}}

.scorers-table tr:hover {{
    background: rgba(255, 40, 130, 0.1);
}}

.player-name-cell {{
    text-align: left !important;
    font-weight: 600;
}}

.position-badge {{
    display: inline-block;
    background: rgba(255, 40, 130, 0.3);
    color: var(--white);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
}}

.goals-cell {{
    font-weight: 800;
    color: var(--cyan);
    font-size: 1rem;
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
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}}

.stats-category:first-of-type {{
    margin-top: 0;
    padding-top: 0;
    border-top: none;
}}

.stats-category-title {{
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--magenta);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 0 0.6rem 0;
}}

.stats-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 0.5rem;
}}

.stat-item {{
    background: rgba(55, 0, 60, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 0.6rem 0.5rem;
    text-align: center;
}}

.stat-item-label {{
    font-size: 0.65rem;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 0.2rem 0;
}}

.stat-item-value {{
    font-size: 1rem;
    font-weight: 700;
    color: var(--cyan);
    margin: 0;
}}

/* ===== COMPARISON LAYOUT ===== */
.comparison-header {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.5rem;
}}

.compare-player {{
    background: linear-gradient(145deg, rgba(90, 0, 90, 0.5) 0%, rgba(55, 0, 60, 0.7) 100%);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}}

.compare-player.p1 {{
    border: 2px solid var(--cyan);
}}

.compare-player.p2 {{
    border: 2px solid var(--magenta);
}}

.compare-name {{
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0;
}}

.compare-name.p1 {{
    color: var(--cyan);
}}

.compare-name.p2 {{
    color: var(--magenta);
}}

.compare-team {{
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.6);
    margin: 0.25rem 0 0 0;
}}

.vs-badge {{
    background: linear-gradient(135deg, var(--magenta) 0%, var(--purple) 100%);
    color: var(--white);
    padding: 0.75rem 1.25rem;
    border-radius: 50%;
    font-weight: 800;
    font-size: 1rem;
}}

/* ===== COMPARISON STATS ===== */
.compare-category {{
    background: rgba(26, 10, 31, 0.6);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 40, 130, 0.15);
}}

.compare-category-title {{
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--white);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--magenta);
}}

.compare-row {{
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.compare-row:last-child {{
    border-bottom: none;
}}

.compare-val {{
    font-size: 1rem;
    font-weight: 700;
}}

.compare-val.p1 {{
    color: var(--cyan);
    text-align: left;
}}

.compare-val.p2 {{
    color: var(--magenta);
    text-align: right;
}}

.compare-val.winner {{
    font-size: 1.1rem;
}}

.compare-label {{
    text-align: center;
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
}}

.compare-bar-container {{
    display: flex;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 0.25rem;
}}

.compare-bar {{
    height: 100%;
    transition: width 0.5s ease;
}}

.compare-bar.p1 {{
    background: var(--cyan);
}}

.compare-bar.p2 {{
    background: var(--magenta);
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

/* ===== INFO BOX ===== */
.stAlert {{
    background: rgba(55, 0, 60, 0.6) !important;
    border: 1px solid rgba(0, 255, 133, 0.3) !important;
    color: var(--white) !important;
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

/* Hide dataframe index */
.row_heading.level0 {{
    display: none;
}}

/* Mobile adjustments */
@media (max-width: 640px) {{
    .comparison-header {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    .vs-badge {{
        margin: 0.5rem auto;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

def get_sample_standings():
    return pd.DataFrame({
        'Pos': list(range(1, 21)),
        'Team': ['Arsenal', 'Man City', 'Aston Villa', 'Liverpool', 'Brentford', 'Newcastle',
                 'Man United', 'Chelsea', 'Fulham', 'Nottm Forest', 'Brighton', 'Everton',
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

def get_comprehensive_players():
    """Get detailed player stats with all categories"""
    return pd.DataFrame({
        'Player': ['Mohamed Salah', 'Erling Haaland', 'Alexander Isak', 'Bryan Mbeumo',
                   'Cole Palmer', 'Chris Wood', 'Yoane Wissa', 'Matheus Cunha',
                   'Nicolas Jackson', 'Ollie Watkins', 'Bukayo Saka', 'Luis Diaz',
                   'Jarrod Bowen', 'Bruno Fernandes', 'Martin Odegaard', 'Kevin De Bruyne'],
        'Team': ['Liverpool', 'Man City', 'Newcastle', 'Brentford',
                 'Chelsea', 'Nottm Forest', 'Brentford', 'Wolves',
                 'Chelsea', 'Aston Villa', 'Arsenal', 'Liverpool',
                 'West Ham', 'Man United', 'Arsenal', 'Man City'],
        'Position': ['RW', 'ST', 'ST', 'RW', 'AM', 'ST', 'ST', 'AM', 'ST', 'ST', 'RW', 'LW',
                     'RW', 'AM', 'AM', 'AM'],
        'Nation': ['Egypt', 'Norway', 'Sweden', 'France', 'England', 'New Zealand',
                   'DR Congo', 'Brazil', 'Senegal', 'England', 'England', 'Colombia',
                   'England', 'Portugal', 'Norway', 'Belgium'],
        'Age': [32, 24, 25, 25, 22, 33, 28, 25, 23, 28, 23, 27, 27, 30, 25, 33],
        # Attacking
        'Goals': [18, 16, 13, 13, 12, 12, 10, 10, 9, 8, 8, 8, 7, 6, 5, 4],
        'xG': [14.2, 15.8, 11.5, 10.8, 9.4, 9.2, 8.6, 8.1, 10.2, 9.5, 7.2, 6.8, 6.1, 4.2, 3.8, 3.2],
        'Shots': [72, 68, 52, 48, 45, 38, 42, 44, 51, 47, 42, 38, 35, 42, 38, 28],
        'SoT': [32, 28, 24, 22, 21, 18, 19, 18, 22, 20, 18, 16, 14, 15, 14, 12],
        'ShotConv': [25.0, 23.5, 25.0, 27.1, 26.7, 31.6, 23.8, 22.7, 17.6, 17.0, 19.0, 21.1, 20.0, 14.3, 13.2, 14.3],
        'TouchBox': [98, 112, 87, 76, 82, 68, 74, 71, 89, 84, 72, 68, 62, 54, 48, 42],
        'Offsides': [12, 18, 14, 8, 6, 10, 9, 5, 15, 11, 7, 8, 5, 3, 2, 2],
        # Creative/Passing
        'Assists': [13, 3, 4, 5, 6, 1, 3, 4, 5, 7, 9, 4, 6, 8, 10, 8],
        'xA': [9.2, 2.8, 3.2, 4.1, 5.8, 0.8, 2.4, 3.6, 4.2, 6.1, 7.8, 3.5, 5.2, 7.4, 9.1, 7.2],
        'KeyPasses': [48, 18, 22, 28, 42, 8, 18, 32, 28, 38, 52, 28, 34, 58, 68, 52],
        'ThroughBalls': [12, 4, 6, 8, 14, 2, 5, 10, 8, 12, 16, 8, 10, 18, 22, 16],
        'Crosses': [28, 4, 8, 22, 18, 2, 6, 12, 8, 14, 32, 18, 28, 22, 18, 14],
        'CrossAcc': [32.1, 25.0, 37.5, 36.4, 38.9, 50.0, 33.3, 41.7, 37.5, 35.7, 34.4, 38.9, 32.1, 36.4, 44.4, 42.9],
        'PassAcc': [82.4, 78.2, 81.5, 79.8, 85.2, 72.4, 76.8, 80.2, 78.5, 79.2, 84.8, 81.2, 78.4, 86.2, 89.4, 88.8],
        'ProgPasses': [68, 32, 42, 48, 72, 18, 28, 52, 38, 48, 78, 42, 48, 92, 98, 82],
        'FinalThird': [142, 88, 98, 108, 128, 62, 78, 98, 92, 102, 138, 96, 88, 142, 152, 118],
        'LongBalls': [22, 8, 12, 18, 28, 4, 8, 16, 12, 18, 24, 14, 18, 42, 38, 32],
        'LongBallAcc': [54.5, 50.0, 58.3, 55.6, 60.7, 50.0, 50.0, 56.3, 50.0, 55.6, 58.3, 57.1, 55.6, 61.9, 65.8, 62.5],
        # Dribbling/Carrying
        'Dribbles': [52, 28, 32, 42, 58, 12, 24, 48, 32, 38, 62, 48, 42, 38, 42, 32],
        'DribbleSucc': [58.4, 57.1, 62.5, 59.5, 65.5, 50.0, 54.2, 58.3, 56.3, 55.3, 64.5, 60.4, 57.1, 55.3, 59.5, 56.3],
        'ProgCarries': [82, 48, 52, 62, 78, 22, 38, 68, 48, 58, 88, 62, 52, 72, 78, 58],
        'CarriesBox': [42, 38, 32, 28, 38, 18, 22, 32, 28, 32, 48, 34, 28, 24, 22, 18],
        'Dispossessed': [28, 22, 18, 24, 26, 14, 18, 28, 24, 22, 32, 26, 22, 24, 20, 16],
        'Miscontrols': [32, 28, 22, 28, 24, 18, 22, 32, 28, 26, 28, 28, 26, 28, 22, 18],
        # Defensive
        'Tackles': [18, 12, 16, 22, 14, 8, 14, 28, 18, 24, 28, 22, 32, 38, 24, 14],
        'TackleSucc': [61.1, 50.0, 56.3, 59.1, 57.1, 50.0, 57.1, 60.7, 55.6, 58.3, 60.7, 59.1, 62.5, 63.2, 58.3, 57.1],
        'Interceptions': [12, 8, 10, 14, 8, 6, 10, 18, 12, 16, 18, 14, 22, 28, 16, 10],
        'Blocks': [8, 6, 8, 10, 6, 4, 8, 12, 8, 10, 12, 8, 14, 18, 10, 6],
        'Clearances': [4, 8, 6, 4, 2, 12, 6, 8, 4, 6, 4, 4, 8, 6, 4, 2],
        'AerialsWon': [12, 28, 22, 8, 4, 32, 18, 14, 16, 22, 8, 6, 12, 8, 4, 4],
        'AerialSucc': [41.7, 58.3, 55.0, 37.5, 25.0, 62.5, 50.0, 46.7, 50.0, 55.0, 33.3, 30.0, 42.9, 33.3, 25.0, 25.0],
        'Pressures': [148, 128, 142, 168, 132, 98, 124, 178, 152, 162, 182, 158, 172, 198, 168, 118],
        'PressSucc': [32.4, 28.1, 30.3, 33.3, 28.8, 26.5, 29.0, 32.6, 30.3, 31.5, 33.5, 31.6, 32.6, 34.3, 32.1, 28.8],
        'Recoveries': [52, 38, 42, 58, 42, 32, 38, 68, 48, 56, 62, 52, 68, 82, 58, 42],
        # Physical/Playing Time
        'Apps': [21, 19, 20, 21, 20, 21, 21, 21, 21, 21, 19, 21, 20, 21, 18, 12],
        'Mins': [1823, 1487, 1701, 1878, 1756, 1823, 1654, 1832, 1698, 1765, 1612, 1543, 1678, 1856, 1524, 892],
        'Starts': [20, 17, 19, 21, 19, 21, 18, 20, 19, 20, 18, 17, 18, 21, 17, 10],
        'MinsPG': [86.8, 78.3, 85.1, 89.4, 87.8, 86.8, 78.8, 87.2, 80.9, 84.0, 84.8, 73.5, 83.9, 88.4, 84.7, 74.3],
        'Fouls': [18, 14, 16, 22, 12, 24, 18, 28, 22, 20, 16, 18, 24, 32, 18, 12],
        'FoulsWon': [38, 28, 32, 42, 34, 22, 28, 48, 38, 36, 48, 38, 32, 42, 38, 28],
        'YellowCards': [2, 3, 2, 4, 1, 4, 3, 5, 4, 3, 2, 3, 4, 6, 2, 1],
        'RedCards': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        # Efficiency metrics
        'G90': [0.89, 0.97, 0.69, 0.62, 0.61, 0.59, 0.54, 0.49, 0.48, 0.41, 0.45, 0.47, 0.38, 0.29, 0.30, 0.40],
        'A90': [0.64, 0.18, 0.21, 0.24, 0.31, 0.05, 0.16, 0.20, 0.26, 0.36, 0.50, 0.23, 0.32, 0.39, 0.59, 0.81],
        'GA90': [1.53, 1.15, 0.90, 0.86, 0.92, 0.64, 0.71, 0.69, 0.74, 0.77, 0.95, 0.70, 0.70, 0.68, 0.89, 1.21],
        'xGxA90': [1.15, 1.00, 0.78, 0.71, 0.78, 0.49, 0.60, 0.58, 0.76, 0.80, 0.84, 0.60, 0.61, 0.56, 0.76, 1.05],
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

# ============ RENDER FUNCTIONS ============

def render_standings_table(df):
    """Render standings table with position badges"""
    html = '<div class="table-container"><table class="custom-table">'
    html += '<thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            val = row[col]
            if col == 'Pos':
                pos = int(val)
                if pos <= 4: badge = 'pos-ucl'
                elif pos == 5: badge = 'pos-uel'
                elif pos == 6: badge = 'pos-conf'
                elif pos >= 18: badge = 'pos-rel'
                else: badge = 'pos-normal'
                html += f'<td><span class="pos-badge {badge}">{pos}</span></td>'
            elif col == 'Team':
                html += f'<td class="team-cell">{val}</td>'
            elif col == 'Pts':
                html += f'<td class="points-cell">{val}</td>'
            elif col == 'GD':
                cls = 'gd-positive' if val > 0 else 'gd-negative' if val < 0 else ''
                html += f'<td class="{cls}">{f"+{val}" if val > 0 else val}</td>'
            else:
                html += f'<td>{val}</td>'
        html += '</tr>'
    
    html += '</tbody></table></div>'
    return html

def render_scorers_table(df):
    """Render scorers table"""
    html = '<div class="table-container"><table class="scorers-table">'
    html += '<thead><tr><th>#</th><th>Player</th><th>Team</th><th>Pos</th><th>Goals</th><th>Assists</th><th>Apps</th></tr></thead>'
    html += '<tbody>'
    
    for idx, row in df.iterrows():
        html += f'''<tr>
            <td>{idx + 1}</td>
            <td class="player-name-cell">{row['Player']}</td>
            <td>{row['Team']}</td>
            <td><span class="position-badge">{row['Position']}</span></td>
            <td class="goals-cell">{row['Goals']}</td>
            <td>{row['Assists']}</td>
            <td>{row['Apps']}</td>
        </tr>'''
    
    html += '</tbody></table></div>'
    return html

def create_chart(df):
    """Create points bar chart"""
    df_s = df.sort_values('Pts', ascending=True)
    colors = [CYAN if p <= 4 else MAGENTA if p >= 18 else '#8B5CF6' for p in df_s['Pos']]
    
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

def create_radar(p1, p2, metrics, labels):
    """Create radar comparison chart with proper rgba colors"""
    max_vals = {m: max(p1.get(m, 1), p2.get(m, 1), 1) for m in metrics}
    p1_vals = [p1.get(m, 0) / max_vals[m] * 100 for m in metrics]
    p2_vals = [p2.get(m, 0) / max_vals[m] * 100 for m in metrics]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=p1_vals + [p1_vals[0]], theta=labels + [labels[0]], fill='toself', name=p1['Player'],
        line_color=CYAN, fillcolor='rgba(0, 255, 133, 0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_vals + [p2_vals[0]], theta=labels + [labels[0]], fill='toself', name=p2['Player'],
        line_color=MAGENTA, fillcolor='rgba(255, 40, 130, 0.2)'
    ))
    
    fig.update_layout(
        height=350, margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=WHITE, size=8), range=[0, 100]),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=WHITE, size=9))
        ),
        legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center', font=dict(color=WHITE, size=10)),
        font=dict(color=WHITE, family='Inter')
    )
    return fig

def create_scatter_comparison(df, x_col, y_col, title, p1_name, p2_name):
    """Create scatter plot highlighting two players"""
    fig = go.Figure()
    
    # All players (faded)
    other = df[~df['Player'].isin([p1_name, p2_name])]
    fig.add_trace(go.Scatter(
        x=other[x_col], y=other[y_col], mode='markers+text',
        marker=dict(size=10, color='rgba(255,255,255,0.2)'),
        text=other['Player'], textposition='top center',
        textfont=dict(size=8, color='rgba(255,255,255,0.4)'),
        hovertemplate=f'%{{text}}<br>{x_col}: %{{x}}<br>{y_col}: %{{y}}<extra></extra>',
        showlegend=False
    ))
    
    # Player 1
    p1 = df[df['Player'] == p1_name]
    if not p1.empty:
        fig.add_trace(go.Scatter(
            x=p1[x_col], y=p1[y_col], mode='markers+text',
            marker=dict(size=16, color=CYAN, line=dict(width=2, color=WHITE)),
            text=[p1_name], textposition='top center',
            textfont=dict(size=10, color=CYAN),
            name=p1_name
        ))
    
    # Player 2
    p2 = df[df['Player'] == p2_name]
    if not p2.empty:
        fig.add_trace(go.Scatter(
            x=p2[x_col], y=p2[y_col], mode='markers+text',
            marker=dict(size=16, color=MAGENTA, line=dict(width=2, color=WHITE)),
            text=[p2_name], textposition='top center',
            textfont=dict(size=10, color=MAGENTA),
            name=p2_name
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=12, color=WHITE)),
        height=300, margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE, family='Inter'),
        xaxis=dict(title=x_col, showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False),
        yaxis=dict(title=y_col, showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', font=dict(size=10))
    )
    return fig

def render_comparison_row(label, v1, v2, is_pct=False):
    """Render a single comparison row with bar"""
    total = max(abs(v1) + abs(v2), 0.001)
    p1_pct = (v1 / total) * 100
    p2_pct = (v2 / total) * 100
    
    w1 = 'winner' if v1 > v2 else ''
    w2 = 'winner' if v2 > v1 else ''
    
    fmt = lambda x: f"{x:.1f}%" if is_pct else f"{x:.1f}" if isinstance(x, float) else str(x)
    
    return f'''
    <div class="compare-row">
        <div class="compare-val p1 {w1}">{fmt(v1)}</div>
        <div style="flex: 1; padding: 0 0.5rem;">
            <div class="compare-label">{label}</div>
            <div class="compare-bar-container">
                <div class="compare-bar p1" style="width: {p1_pct}%;"></div>
                <div class="compare-bar p2" style="width: {p2_pct}%;"></div>
            </div>
        </div>
        <div class="compare-val p2 {w2}">{fmt(v2)}</div>
    </div>
    '''

# ============ MAIN APP ============

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <div class="logo-icon">⚽</div>
            <div class="logo-text">
                <h1 class="logo-title">PREMIER <span>LEAGUE</span></h1>
                <p class="logo-subtitle">Statistics Hub - 2024/25 Season</p>
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
    players = get_comprehensive_players()
    
    # Status
    status = "Live data connected" if api_key else "Sample data mode"
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot"></div>
        <p class="status-text">{status} - Showing current season</p>
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
    tab1, tab2, tab3, tab4 = st.tabs(["TABLE", "TOP SCORERS", "PLAYER PROFILE", "PLAYER VS PLAYER"])
    
    # ==================== TAB 1: STANDINGS ====================
    with tab1:
        st.markdown('<div class="section-header"><h2 class="section-title">League Standings</h2></div>', unsafe_allow_html=True)
        st.markdown(render_standings_table(standings), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Points Distribution</h2></div>', unsafe_allow_html=True)
        st.plotly_chart(create_chart(standings), width='stretch', config={'displayModeBar': False})
    
    # ==================== TAB 2: SCORERS ====================
    with tab2:
        st.markdown('<div class="section-header"><h2 class="section-title">Top Scorers</h2></div>', unsafe_allow_html=True)
        st.markdown(render_scorers_table(players.head(12)), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Goals vs Expected Goals</h2></div>', unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Goals', x=players.head(10)['Player'], y=players.head(10)['Goals'], marker_color=CYAN))
        fig.add_trace(go.Bar(name='xG', x=players.head(10)['Player'], y=players.head(10)['xG'], marker_color=MAGENTA))
        fig.update_layout(
            barmode='group', height=350, margin=dict(l=10, r=10, t=10, b=80),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=WHITE, family='Inter'),
            legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'),
            xaxis=dict(tickangle=-45), yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)')
        )
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # ==================== TAB 3: PLAYER PROFILE ====================
    with tab3:
        st.markdown('<div class="section-header"><h2 class="section-title">Player Profile</h2></div>', unsafe_allow_html=True)
        
        selected = st.selectbox("Select a player", players['Player'].tolist(), key='profile')
        
        if selected:
            p = players[players['Player'] == selected].iloc[0]
            
            # Header card
            st.markdown(f"""
            <div class="player-card">
                <div class="player-header">
                    <div>
                        <h3 class="player-name">{p['Player']}</h3>
                        <p class="player-team">{p['Team']} - {p['Nation']} - Age {p['Age']}</p>
                    </div>
                    <span class="player-position">{p['Position']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Stats categories
            col1, col2 = st.columns(2)
            
            with col1:
                # ATTACKING
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Attacking</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Goals</p><p class="stat-item-value">{p['Goals']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">xG</p><p class="stat-item-value">{p['xG']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Shots</p><p class="stat-item-value">{p['Shots']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">On Target</p><p class="stat-item-value">{p['SoT']}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Conversion</p><p class="stat-item-value">{p['ShotConv']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Box Touches</p><p class="stat-item-value">{p['TouchBox']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Offsides</p><p class="stat-item-value">{p['Offsides']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Goals/90</p><p class="stat-item-value">{p['G90']:.2f}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # DRIBBLING
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Dribbling & Carrying</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Dribbles</p><p class="stat-item-value">{p['Dribbles']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Success %</p><p class="stat-item-value">{p['DribbleSucc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Prog Carries</p><p class="stat-item-value">{p['ProgCarries']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Into Box</p><p class="stat-item-value">{p['CarriesBox']}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Dispossessed</p><p class="stat-item-value">{p['Dispossessed']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Miscontrols</p><p class="stat-item-value">{p['Miscontrols']}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # DEFENSIVE
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Defensive</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Tackles</p><p class="stat-item-value">{p['Tackles']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Tkl %</p><p class="stat-item-value">{p['TackleSucc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Interceptions</p><p class="stat-item-value">{p['Interceptions']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Blocks</p><p class="stat-item-value">{p['Blocks']}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Clearances</p><p class="stat-item-value">{p['Clearances']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Aerials Won</p><p class="stat-item-value">{p['AerialsWon']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Aerial %</p><p class="stat-item-value">{p['AerialSucc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Recoveries</p><p class="stat-item-value">{p['Recoveries']}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # CREATIVE
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Creative & Passing</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Assists</p><p class="stat-item-value">{p['Assists']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">xA</p><p class="stat-item-value">{p['xA']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Key Passes</p><p class="stat-item-value">{p['KeyPasses']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Through Balls</p><p class="stat-item-value">{p['ThroughBalls']}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Crosses</p><p class="stat-item-value">{p['Crosses']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Cross Acc %</p><p class="stat-item-value">{p['CrossAcc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Pass Acc %</p><p class="stat-item-value">{p['PassAcc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Prog Passes</p><p class="stat-item-value">{p['ProgPasses']}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Final 1/3</p><p class="stat-item-value">{p['FinalThird']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Long Balls</p><p class="stat-item-value">{p['LongBalls']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Long Acc %</p><p class="stat-item-value">{p['LongBallAcc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Assists/90</p><p class="stat-item-value">{p['A90']:.2f}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # PRESSING
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Pressing & Work Rate</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Pressures</p><p class="stat-item-value">{p['Pressures']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Press Succ %</p><p class="stat-item-value">{p['PressSucc']:.1f}%</p></div>
                        <div class="stat-item"><p class="stat-item-label">Fouls</p><p class="stat-item-value">{p['Fouls']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Fouls Won</p><p class="stat-item-value">{p['FoulsWon']}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # PLAYING TIME
                st.markdown(f"""
                <div class="player-card">
                    <p class="stats-category-title">Playing Time & Discipline</p>
                    <div class="stats-row">
                        <div class="stat-item"><p class="stat-item-label">Appearances</p><p class="stat-item-value">{p['Apps']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Minutes</p><p class="stat-item-value">{p['Mins']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Starts</p><p class="stat-item-value">{p['Starts']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Mins/Game</p><p class="stat-item-value">{p['MinsPG']:.1f}</p></div>
                    </div>
                    <div class="stats-row" style="margin-top: 0.5rem;">
                        <div class="stat-item"><p class="stat-item-label">Yellow Cards</p><p class="stat-item-value">{p['YellowCards']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">Red Cards</p><p class="stat-item-value">{p['RedCards']}</p></div>
                        <div class="stat-item"><p class="stat-item-label">G+A/90</p><p class="stat-item-value">{p['GA90']:.2f}</p></div>
                        <div class="stat-item"><p class="stat-item-label">xG+xA/90</p><p class="stat-item-value">{p['xGxA90']:.2f}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== TAB 4: PLAYER VS PLAYER ====================
    with tab4:
        st.markdown('<div class="section-header"><h2 class="section-title">Player vs Player Comparison</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            p1_name = st.selectbox("Player 1", players['Player'].tolist(), index=0, key='cmp_p1')
        with col2:
            p2_name = st.selectbox("Player 2", players['Player'].tolist(), index=1, key='cmp_p2')
        
        if p1_name and p2_name and p1_name != p2_name:
            p1 = players[players['Player'] == p1_name].iloc[0].to_dict()
            p2 = players[players['Player'] == p2_name].iloc[0].to_dict()
            
            # Header comparison
            st.markdown(f"""
            <div class="comparison-header">
                <div class="compare-player p1">
                    <h3 class="compare-name p1">{p1['Player']}</h3>
                    <p class="compare-team">{p1['Team']} - {p1['Position']}</p>
                </div>
                <div class="vs-badge">VS</div>
                <div class="compare-player p2">
                    <h3 class="compare-name p2">{p2['Player']}</h3>
                    <p class="compare-team">{p2['Team']} - {p2['Position']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Overall Radar
            st.markdown('<div class="section-header"><h2 class="section-title">Overall Comparison</h2></div>', unsafe_allow_html=True)
            radar_metrics = ['Goals', 'Assists', 'KeyPasses', 'Dribbles', 'Tackles', 'Pressures']
            radar_labels = ['Goals', 'Assists', 'Key Passes', 'Dribbles', 'Tackles', 'Pressures']
            st.plotly_chart(create_radar(p1, p2, radar_metrics, radar_labels), width='stretch', config={'displayModeBar': False})
            
            # ===== ATTACKING COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Attacking</h3>
                {render_comparison_row('Goals', p1['Goals'], p2['Goals'])}
                {render_comparison_row('xG', p1['xG'], p2['xG'])}
                {render_comparison_row('Shots', p1['Shots'], p2['Shots'])}
                {render_comparison_row('Shots on Target', p1['SoT'], p2['SoT'])}
                {render_comparison_row('Conversion %', p1['ShotConv'], p2['ShotConv'], True)}
                {render_comparison_row('Box Touches', p1['TouchBox'], p2['TouchBox'])}
                {render_comparison_row('Goals/90', p1['G90'], p2['G90'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== CREATIVE COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Creative & Passing</h3>
                {render_comparison_row('Assists', p1['Assists'], p2['Assists'])}
                {render_comparison_row('xA', p1['xA'], p2['xA'])}
                {render_comparison_row('Key Passes', p1['KeyPasses'], p2['KeyPasses'])}
                {render_comparison_row('Through Balls', p1['ThroughBalls'], p2['ThroughBalls'])}
                {render_comparison_row('Crosses', p1['Crosses'], p2['Crosses'])}
                {render_comparison_row('Cross Accuracy %', p1['CrossAcc'], p2['CrossAcc'], True)}
                {render_comparison_row('Pass Accuracy %', p1['PassAcc'], p2['PassAcc'], True)}
                {render_comparison_row('Progressive Passes', p1['ProgPasses'], p2['ProgPasses'])}
                {render_comparison_row('Final Third Passes', p1['FinalThird'], p2['FinalThird'])}
                {render_comparison_row('Long Balls', p1['LongBalls'], p2['LongBalls'])}
                {render_comparison_row('Assists/90', p1['A90'], p2['A90'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== DRIBBLING COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Dribbling & Ball Carrying</h3>
                {render_comparison_row('Dribbles Attempted', p1['Dribbles'], p2['Dribbles'])}
                {render_comparison_row('Dribble Success %', p1['DribbleSucc'], p2['DribbleSucc'], True)}
                {render_comparison_row('Progressive Carries', p1['ProgCarries'], p2['ProgCarries'])}
                {render_comparison_row('Carries Into Box', p1['CarriesBox'], p2['CarriesBox'])}
                {render_comparison_row('Dispossessed', p2['Dispossessed'], p1['Dispossessed'])}
                {render_comparison_row('Miscontrols', p2['Miscontrols'], p1['Miscontrols'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== DEFENSIVE COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Defensive</h3>
                {render_comparison_row('Tackles', p1['Tackles'], p2['Tackles'])}
                {render_comparison_row('Tackle Success %', p1['TackleSucc'], p2['TackleSucc'], True)}
                {render_comparison_row('Interceptions', p1['Interceptions'], p2['Interceptions'])}
                {render_comparison_row('Blocks', p1['Blocks'], p2['Blocks'])}
                {render_comparison_row('Clearances', p1['Clearances'], p2['Clearances'])}
                {render_comparison_row('Aerials Won', p1['AerialsWon'], p2['AerialsWon'])}
                {render_comparison_row('Aerial Success %', p1['AerialSucc'], p2['AerialSucc'], True)}
                {render_comparison_row('Recoveries', p1['Recoveries'], p2['Recoveries'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== PRESSING COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Pressing & Work Rate</h3>
                {render_comparison_row('Pressures', p1['Pressures'], p2['Pressures'])}
                {render_comparison_row('Press Success %', p1['PressSucc'], p2['PressSucc'], True)}
                {render_comparison_row('Fouls Committed', p2['Fouls'], p1['Fouls'])}
                {render_comparison_row('Fouls Won', p1['FoulsWon'], p2['FoulsWon'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== PLAYING TIME COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Playing Time & Discipline</h3>
                {render_comparison_row('Appearances', p1['Apps'], p2['Apps'])}
                {render_comparison_row('Minutes Played', p1['Mins'], p2['Mins'])}
                {render_comparison_row('Starts', p1['Starts'], p2['Starts'])}
                {render_comparison_row('Mins/Game', p1['MinsPG'], p2['MinsPG'])}
                {render_comparison_row('Yellow Cards', p2['YellowCards'], p1['YellowCards'])}
                {render_comparison_row('Red Cards', p2['RedCards'], p1['RedCards'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== EFFICIENCY COMPARISON =====
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Efficiency & Output</h3>
                {render_comparison_row('Goals + Assists', p1['Goals'] + p1['Assists'], p2['Goals'] + p2['Assists'])}
                {render_comparison_row('G+A per 90', p1['GA90'], p2['GA90'])}
                {render_comparison_row('xG + xA', p1['xG'] + p1['xA'], p2['xG'] + p2['xA'])}
                {render_comparison_row('xG+xA per 90', p1['xGxA90'], p2['xGxA90'])}
            </div>
            """, unsafe_allow_html=True)
            
            # ===== SCATTER PLOTS =====
            st.markdown('<div class="section-header"><h2 class="section-title">Statistical Scatter Plots</h2></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_scatter_comparison(players, 'xG', 'Goals', 'Goals vs xG', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
            with col2:
                st.plotly_chart(create_scatter_comparison(players, 'xA', 'Assists', 'Assists vs xA', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_scatter_comparison(players, 'Shots', 'Goals', 'Goals vs Shots', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
            with col2:
                st.plotly_chart(create_scatter_comparison(players, 'KeyPasses', 'Assists', 'Assists vs Key Passes', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_scatter_comparison(players, 'Dribbles', 'ProgCarries', 'Prog Carries vs Dribbles', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
            with col2:
                st.plotly_chart(create_scatter_comparison(players, 'Tackles', 'Interceptions', 'Interceptions vs Tackles', p1_name, p2_name), width='stretch', config={'displayModeBar': False})
        
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
