"""
Premier League Stats Hub - Professional Dashboard
Season Selection, Multi-Player Comparison, Full Search
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

# Available seasons
SEASONS = ['2025/26', '2024/25', '2023/24', '2022/23', '2021/22', '2020/21', '2019/20']
CURRENT_SEASON = '2025/26'

# Player colors for multi-comparison
PLAYER_COLORS = [CYAN, MAGENTA, '#8B5CF6', '#F97316', '#22D3EE']

# Professional CSS with improved readability
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
    max-width: 1400px;
}}

/* ===== IMPROVED TEXT READABILITY ===== */
p, span, div, td, th, label {{
    color: var(--white) !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: var(--white) !important;
}}

/* ===== HEADER WITH PL LOGO ===== */
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

.pl-logo {{
    height: 70px;
    filter: brightness(0) invert(1);
}}

.logo-text {{
    text-align: left;
}}

.logo-title {{
    font-size: 1.8rem;
    font-weight: 900;
    color: var(--white) !important;
    letter-spacing: 3px;
    margin: 0;
    text-transform: uppercase;
}}

.logo-title span {{
    color: var(--cyan) !important;
}}

.logo-subtitle {{
    font-size: 0.85rem;
    color: var(--cyan) !important;
    letter-spacing: 2px;
    margin: 0.2rem 0 0 0;
    font-weight: 600;
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
    width: 10px;
    height: 10px;
    background: var(--cyan);
    border-radius: 50%;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

.status-text {{
    color: var(--white) !important;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0;
}}

/* ===== SEASON SELECTOR ===== */
.season-selector {{
    background: rgba(55, 0, 60, 0.8);
    border: 2px solid var(--cyan);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
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
    border: 1px solid rgba(255, 40, 130, 0.3);
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
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--cyan) !important;
    margin: 0;
    line-height: 1;
}}

.stat-label {{
    font-size: 0.75rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.9) !important;
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
    color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 700;
    font-size: 0.8rem;
    border: none;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: var(--white) !important;
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
    border-bottom: 3px solid var(--cyan);
}}

.section-title {{
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--white) !important;
    margin: 0;
    letter-spacing: 0.5px;
}}

/* ===== CUSTOM TABLE ===== */
.table-container {{
    background: rgba(26, 10, 31, 0.7);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 40, 130, 0.2);
    overflow-x: auto;
}}

.custom-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    min-width: 600px;
}}

.custom-table th {{
    background: linear-gradient(90deg, var(--magenta) 0%, #cc2266 100%);
    color: var(--white) !important;
    font-weight: 700;
    padding: 1rem 0.5rem;
    text-align: center;
    font-size: 0.75rem;
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
    padding: 0.8rem 0.5rem;
    text-align: center;
    color: var(--white) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    font-weight: 600;
    font-size: 0.85rem;
}}

.custom-table tr:hover {{
    background: rgba(255, 40, 130, 0.15);
}}

.custom-table tr:last-child td {{
    border-bottom: none;
}}

.team-cell {{
    text-align: left !important;
    font-weight: 700 !important;
    padding-left: 1rem !important;
}}

/* Position badges */
.pos-badge {{
    display: inline-block;
    width: 28px;
    height: 28px;
    line-height: 28px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.85rem;
}}

.pos-ucl {{
    background: var(--cyan);
    color: var(--purple) !important;
}}

.pos-uel {{
    background: #f97316;
    color: var(--white) !important;
}}

.pos-conf {{
    background: #22c55e;
    color: var(--white) !important;
}}

.pos-rel {{
    background: var(--magenta);
    color: var(--white) !important;
}}

.pos-normal {{
    background: rgba(255, 255, 255, 0.15);
    color: var(--white) !important;
}}

.points-cell {{
    font-weight: 900 !important;
    color: var(--cyan) !important;
    font-size: 1rem !important;
}}

.gd-positive {{
    color: var(--cyan) !important;
    font-weight: 700 !important;
}}

.gd-negative {{
    color: var(--magenta) !important;
    font-weight: 700 !important;
}}

/* Scorers table */
.goals-cell {{
    font-weight: 900 !important;
    color: var(--cyan) !important;
    font-size: 1.1rem !important;
}}

.player-name-cell {{
    text-align: left !important;
    font-weight: 700 !important;
    color: var(--white) !important;
}}

.position-badge {{
    display: inline-block;
    background: rgba(255, 40, 130, 0.4);
    color: var(--white) !important;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
}}

/* ===== PLAYER CARDS ===== */
.player-card {{
    background: linear-gradient(145deg, rgba(90, 0, 90, 0.5) 0%, rgba(55, 0, 60, 0.7) 100%);
    border: 2px solid rgba(0, 255, 133, 0.3);
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
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--cyan) !important;
    margin: 0;
}}

.player-team {{
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.8) !important;
    margin: 0.25rem 0 0 0;
    font-weight: 500;
}}

.player-position {{
    background: var(--magenta);
    color: var(--white) !important;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 800;
}}

.stats-category {{
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
}}

.stats-category:first-of-type {{
    margin-top: 0;
    padding-top: 0;
    border-top: none;
}}

.stats-category-title {{
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--magenta) !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0 0 0.75rem 0;
}}

.stats-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
    gap: 0.5rem;
}}

.stat-item {{
    background: rgba(55, 0, 60, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 0.6rem 0.4rem;
    text-align: center;
}}

.stat-item-label {{
    font-size: 0.65rem;
    color: rgba(255, 255, 255, 0.7) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 0.2rem 0;
    font-weight: 600;
}}

.stat-item-value {{
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--cyan) !important;
    margin: 0;
}}

/* ===== MULTI COMPARISON ===== */
.compare-players-header {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
    margin-bottom: 1.5rem;
}}

.compare-player-badge {{
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.85rem;
    text-align: center;
}}

/* ===== COMPARISON STATS ===== */
.compare-category {{
    background: rgba(26, 10, 31, 0.7);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 40, 130, 0.2);
}}

.compare-category-title {{
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--white) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid var(--magenta);
}}

.compare-stat-row {{
    display: flex;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}

.compare-stat-row:last-child {{
    border-bottom: none;
}}

.compare-stat-label {{
    width: 140px;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 600;
    text-transform: uppercase;
}}

.compare-stat-values {{
    flex: 1;
    display: flex;
    gap: 0.5rem;
}}

.compare-stat-value {{
    flex: 1;
    text-align: center;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 0.3rem;
    border-radius: 4px;
}}

.compare-stat-value.winner {{
    font-size: 1.05rem;
    font-weight: 900;
}}

/* ===== SELECT BOXES & TEXT INPUT ===== */
.stSelectbox label, .stTextInput label, .stMultiSelect label {{
    color: var(--white) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}}

.stSelectbox > div > div, .stTextInput > div > div, .stMultiSelect > div > div {{
    background: rgba(55, 0, 60, 0.9) !important;
    border: 2px solid rgba(0, 255, 133, 0.4) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
}}

.stTextInput input {{
    color: var(--white) !important;
    font-weight: 600 !important;
}}

.stTextInput input::placeholder {{
    color: rgba(255, 255, 255, 0.5) !important;
}}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {{
    background: rgba(55, 0, 60, 0.7) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-weight: 700 !important;
}}

/* ===== INFO BOX ===== */
.stAlert {{
    background: rgba(55, 0, 60, 0.7) !important;
    border: 2px solid rgba(0, 255, 133, 0.4) !important;
    color: var(--white) !important;
}}

/* ===== FOOTER ===== */
.footer {{
    text-align: center;
    padding: 2rem 1rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
}}

.footer p {{
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 0.8rem;
    margin: 0.25rem 0;
    font-weight: 500;
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
    .logo-title {{
        font-size: 1.4rem;
    }}
    .pl-logo {{
        height: 50px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

def get_sample_standings(season):
    """Get standings for a specific season"""
    # Simulated data varies slightly by season
    base_data = {
        'Team': ['Liverpool', 'Arsenal', 'Chelsea', 'Man City', 'Aston Villa', 'Brighton',
                 'Newcastle', 'Fulham', 'Bournemouth', 'Nottm Forest', 'Brentford', 'Man United',
                 'West Ham', 'Crystal Palace', 'Everton', 'Tottenham', 'Wolves', 'Leicester',
                 'Ipswich', 'Southampton'],
    }
    
    if season == '2025/26':
        return pd.DataFrame({
            'Pos': list(range(1, 21)),
            'Team': base_data['Team'],
            'P': [22]*20,
            'W': [16, 14, 13, 12, 11, 10, 10, 9, 9, 8, 8, 7, 7, 7, 6, 6, 5, 4, 3, 2],
            'D': [4, 5, 5, 6, 5, 6, 5, 7, 5, 8, 6, 8, 6, 5, 7, 5, 6, 5, 6, 5],
            'L': [2, 3, 4, 4, 6, 6, 7, 6, 8, 6, 8, 7, 9, 10, 9, 11, 11, 13, 13, 15],
            'GF': [52, 48, 45, 50, 38, 42, 35, 32, 38, 28, 36, 30, 28, 26, 22, 34, 28, 24, 20, 18],
            'GA': [18, 22, 25, 28, 28, 32, 30, 28, 35, 28, 34, 32, 35, 38, 32, 42, 40, 48, 45, 52],
            'GD': [34, 26, 20, 22, 10, 10, 5, 4, 3, 0, 2, -2, -7, -12, -10, -8, -12, -24, -25, -34],
            'Pts': [52, 47, 44, 42, 38, 36, 35, 34, 32, 32, 30, 29, 27, 26, 25, 23, 21, 17, 15, 11]
        })
    else:
        return pd.DataFrame({
            'Pos': list(range(1, 21)),
            'Team': ['Arsenal', 'Man City', 'Liverpool', 'Aston Villa', 'Chelsea', 'Newcastle',
                     'Brighton', 'Man United', 'Tottenham', 'Fulham', 'Brentford', 'West Ham',
                     'Crystal Palace', 'Bournemouth', 'Nottm Forest', 'Everton', 'Wolves',
                     'Leicester', 'Ipswich', 'Southampton'],
            'P': [38]*20,
            'W': [28, 27, 24, 22, 20, 18, 16, 16, 15, 14, 14, 13, 12, 12, 11, 10, 9, 8, 7, 5],
            'D': [5, 7, 8, 8, 10, 12, 12, 8, 9, 11, 9, 9, 12, 9, 11, 12, 11, 10, 9, 8],
            'L': [5, 4, 6, 8, 8, 8, 10, 14, 14, 13, 15, 16, 14, 17, 16, 16, 18, 20, 22, 25],
            'GF': [89, 95, 85, 72, 78, 68, 62, 58, 65, 52, 58, 48, 45, 52, 42, 38, 45, 42, 38, 32],
            'GA': [28, 32, 38, 48, 52, 45, 52, 58, 62, 48, 58, 62, 52, 68, 58, 52, 68, 72, 78, 85],
            'GD': [61, 63, 47, 24, 26, 23, 10, 0, 3, 4, 0, -14, -7, -16, -16, -14, -23, -30, -40, -53],
            'Pts': [89, 88, 80, 74, 70, 66, 60, 56, 54, 53, 51, 48, 48, 45, 44, 42, 38, 34, 30, 23]
        })

def get_all_players(season):
    """Get comprehensive player database"""
    players = pd.DataFrame({
        'Player': [
            'Mohamed Salah', 'Erling Haaland', 'Cole Palmer', 'Alexander Isak', 'Bryan Mbeumo',
            'Chris Wood', 'Bukayo Saka', 'Luis Diaz', 'Ollie Watkins', 'Nicolas Jackson',
            'Yoane Wissa', 'Matheus Cunha', 'Jarrod Bowen', 'Darwin Nunez', 'Anthony Gordon',
            'Bruno Fernandes', 'Martin Odegaard', 'Kevin De Bruyne', 'James Maddison', 'Phil Foden',
            'Eberechi Eze', 'Morgan Rogers', 'Brennan Johnson', 'Heung-Min Son', 'Marcus Rashford',
            'Dominic Solanke', 'Jean-Philippe Mateta', 'Joao Pedro', 'Evan Ferguson', 'Callum Wilson',
            'Virgil van Dijk', 'William Saliba', 'Gabriel Magalhaes', 'Ruben Dias', 'Lisandro Martinez',
            'Trent Alexander-Arnold', 'Reece James', 'Kyle Walker', 'Kieran Trippier', 'Ben White',
            'Declan Rice', 'Rodri', 'Bruno Guimaraes', 'Moises Caicedo', 'Enzo Fernandez',
            'Alisson Becker', 'Ederson', 'David Raya', 'Andre Onana', 'Robert Sanchez'
        ],
        'Team': [
            'Liverpool', 'Man City', 'Chelsea', 'Newcastle', 'Brentford',
            'Nottm Forest', 'Arsenal', 'Liverpool', 'Aston Villa', 'Chelsea',
            'Brentford', 'Wolves', 'West Ham', 'Liverpool', 'Newcastle',
            'Man United', 'Arsenal', 'Man City', 'Tottenham', 'Man City',
            'Crystal Palace', 'Aston Villa', 'Tottenham', 'Tottenham', 'Man United',
            'Tottenham', 'Crystal Palace', 'Brighton', 'Brighton', 'Newcastle',
            'Liverpool', 'Arsenal', 'Arsenal', 'Man City', 'Man United',
            'Liverpool', 'Chelsea', 'Man City', 'Newcastle', 'Arsenal',
            'Arsenal', 'Man City', 'Newcastle', 'Chelsea', 'Chelsea',
            'Liverpool', 'Man City', 'Arsenal', 'Man United', 'Chelsea'
        ],
        'Position': [
            'RW', 'ST', 'AM', 'ST', 'RW', 'ST', 'RW', 'LW', 'ST', 'ST',
            'ST', 'AM', 'RW', 'ST', 'LW', 'AM', 'AM', 'AM', 'AM', 'LW',
            'AM', 'AM', 'RW', 'LW', 'LW', 'ST', 'ST', 'ST', 'ST', 'ST',
            'CB', 'CB', 'CB', 'CB', 'CB', 'RB', 'RB', 'RB', 'RB', 'RB',
            'DM', 'DM', 'CM', 'DM', 'CM', 'GK', 'GK', 'GK', 'GK', 'GK'
        ],
        'Nation': [
            'Egypt', 'Norway', 'England', 'Sweden', 'France',
            'New Zealand', 'England', 'Colombia', 'England', 'Senegal',
            'DR Congo', 'Brazil', 'England', 'Uruguay', 'England',
            'Portugal', 'Norway', 'Belgium', 'England', 'England',
            'England', 'England', 'Wales', 'South Korea', 'England',
            'England', 'France', 'Brazil', 'Ireland', 'England',
            'Netherlands', 'France', 'Brazil', 'Portugal', 'Argentina',
            'England', 'England', 'England', 'England', 'England',
            'England', 'Spain', 'Brazil', 'Ecuador', 'Argentina',
            'Brazil', 'Brazil', 'Spain', 'Cameroon', 'Spain'
        ],
        'Age': [
            32, 24, 22, 25, 25, 33, 23, 27, 28, 23,
            28, 25, 27, 25, 24, 30, 25, 33, 28, 24,
            26, 22, 23, 32, 27, 27, 27, 23, 20, 32,
            33, 23, 27, 27, 26, 26, 25, 34, 34, 27,
            26, 28, 27, 23, 24, 32, 31, 29, 28, 27
        ],
        # Attacking
        'Goals': [20, 18, 15, 14, 14, 13, 10, 10, 9, 10, 11, 11, 8, 9, 8, 7, 6, 5, 6, 8,
                  7, 6, 7, 8, 6, 9, 10, 8, 5, 4, 3, 2, 3, 1, 1, 4, 1, 1, 2, 1,
                  6, 3, 5, 3, 4, 0, 0, 0, 0, 0],
        'xG': [15.8, 17.2, 12.4, 12.8, 11.2, 10.5, 8.8, 8.2, 10.4, 11.5, 9.8, 9.2, 6.8, 10.2, 7.5, 5.2, 4.8, 4.2, 4.8, 7.2,
               5.8, 5.2, 6.2, 7.8, 5.8, 8.5, 9.2, 7.4, 4.8, 3.8, 1.8, 1.2, 2.2, 0.8, 0.6, 2.4, 0.6, 0.4, 1.2, 0.8,
               4.2, 2.4, 3.8, 2.2, 3.2, 0, 0, 0, 0, 0],
        'Shots': [78, 72, 52, 58, 52, 42, 48, 42, 52, 58, 48, 48, 38, 55, 42, 48, 42, 32, 38, 45,
                  42, 35, 38, 48, 42, 45, 48, 42, 28, 22, 12, 8, 14, 8, 6, 18, 4, 4, 8, 6,
                  28, 18, 25, 18, 22, 0, 0, 0, 0, 0],
        'SoT': [35, 32, 25, 28, 24, 20, 22, 18, 24, 26, 22, 20, 16, 24, 18, 18, 16, 14, 15, 20,
                18, 14, 16, 22, 16, 20, 22, 18, 12, 10, 5, 3, 6, 3, 2, 8, 2, 2, 4, 2,
                12, 8, 10, 7, 9, 0, 0, 0, 0, 0],
        'ShotConv': [25.6, 25.0, 28.8, 24.1, 26.9, 31.0, 20.8, 23.8, 17.3, 17.2, 22.9, 22.9, 21.1, 16.4, 19.0, 14.6, 14.3, 15.6, 15.8, 17.8,
                     16.7, 17.1, 18.4, 16.7, 14.3, 20.0, 20.8, 19.0, 17.9, 18.2, 25.0, 25.0, 21.4, 12.5, 16.7, 22.2, 25.0, 25.0, 25.0, 16.7,
                     21.4, 16.7, 20.0, 16.7, 18.2, 0, 0, 0, 0, 0],
        'TouchBox': [105, 118, 88, 92, 82, 72, 78, 72, 88, 95, 78, 75, 65, 82, 68, 58, 52, 45, 52, 68,
                     58, 48, 55, 72, 55, 75, 82, 68, 45, 35, 15, 12, 18, 10, 8, 28, 8, 6, 12, 10,
                     35, 22, 28, 18, 25, 2, 2, 2, 2, 2],
        # Creative
        'Assists': [14, 4, 8, 5, 6, 2, 11, 5, 8, 6, 4, 5, 7, 4, 6, 9, 11, 10, 8, 6,
                    5, 8, 5, 7, 4, 3, 2, 5, 3, 2, 2, 1, 1, 2, 1, 8, 2, 3, 5, 4,
                    5, 6, 7, 4, 5, 1, 1, 0, 0, 1],
        'xA': [10.2, 3.2, 6.8, 4.2, 4.8, 1.2, 9.2, 4.2, 6.8, 5.2, 3.2, 4.2, 5.8, 3.5, 5.2, 7.8, 9.5, 8.8, 6.8, 5.2,
               4.2, 6.8, 4.2, 5.8, 3.5, 2.5, 1.8, 4.2, 2.5, 1.8, 1.5, 0.8, 0.8, 1.5, 0.8, 6.8, 1.5, 2.5, 4.2, 3.2,
               4.2, 5.2, 5.8, 3.2, 4.2, 0.8, 0.5, 0.2, 0.2, 0.5],
        'KeyPasses': [52, 22, 48, 25, 32, 10, 58, 32, 42, 32, 20, 35, 38, 22, 32, 65, 72, 58, 52, 42,
                      38, 48, 32, 42, 28, 18, 12, 28, 18, 12, 8, 5, 6, 12, 5, 42, 12, 18, 28, 22,
                      32, 38, 42, 22, 32, 5, 4, 2, 3, 4],
        'ThroughBalls': [14, 5, 16, 7, 9, 2, 18, 9, 14, 9, 6, 11, 11, 6, 9, 20, 24, 18, 14, 12,
                         10, 14, 8, 12, 7, 4, 3, 8, 4, 3, 2, 1, 1, 3, 1, 12, 3, 5, 8, 6,
                         8, 10, 12, 6, 9, 1, 1, 0, 1, 1],
        'Crosses': [32, 5, 22, 10, 25, 3, 38, 22, 18, 10, 8, 15, 32, 8, 18, 28, 22, 18, 22, 15,
                    18, 15, 22, 18, 15, 8, 5, 12, 6, 4, 2, 1, 2, 4, 2, 48, 18, 15, 35, 28,
                    12, 8, 12, 6, 10, 1, 0, 0, 1, 0],
        'PassAcc': [83.5, 79.2, 86.2, 82.5, 80.8, 73.5, 85.8, 82.2, 80.5, 79.5, 77.8, 81.2, 79.5, 75.8, 81.5, 87.2, 90.2, 89.8, 85.5, 86.2,
                    83.5, 84.2, 81.8, 82.5, 80.2, 78.5, 75.2, 82.2, 80.5, 76.8, 91.5, 92.2, 91.8, 93.2, 89.5, 82.8, 84.5, 88.2, 81.5, 85.2,
                    90.8, 93.5, 88.2, 86.5, 88.2, 85.2, 88.5, 82.2, 81.5, 80.2],
        'ProgPasses': [72, 35, 78, 45, 52, 20, 85, 48, 52, 42, 32, 58, 52, 32, 45, 98, 105, 88, 72, 62,
                       52, 58, 45, 58, 42, 25, 18, 38, 25, 18, 68, 72, 65, 85, 55, 88, 42, 62, 68, 58,
                       78, 92, 85, 52, 68, 45, 52, 38, 42, 35],
        # Dribbling
        'Dribbles': [58, 32, 65, 35, 48, 15, 68, 52, 42, 35, 28, 52, 45, 35, 42, 42, 48, 35, 45, 52,
                     55, 48, 42, 38, 48, 22, 18, 38, 25, 15, 8, 5, 6, 8, 12, 32, 18, 12, 22, 18,
                     28, 18, 35, 32, 38, 2, 2, 1, 2, 2],
        'DribbleSucc': [59.5, 58.2, 66.5, 63.2, 60.5, 52.5, 65.2, 61.5, 56.8, 57.5, 55.2, 59.2, 58.5, 52.8, 58.2, 56.5, 60.8, 57.5, 58.2, 62.5,
                        61.2, 59.5, 57.8, 55.2, 54.8, 52.5, 50.2, 58.5, 55.2, 50.5, 62.5, 60.2, 58.5, 65.2, 58.5, 62.8, 58.5, 55.2, 58.2, 60.5,
                        58.2, 65.5, 62.2, 60.5, 62.8, 50.2, 55.5, 48.2, 52.5, 50.2],
        'ProgCarries': [88, 52, 85, 58, 68, 25, 95, 68, 62, 52, 42, 72, 58, 48, 58, 78, 85, 65, 68, 72,
                        65, 68, 55, 62, 58, 35, 28, 52, 35, 22, 42, 48, 45, 55, 38, 72, 32, 42, 55, 48,
                        58, 52, 68, 45, 58, 8, 12, 6, 10, 8],
        'CarriesBox': [45, 42, 42, 35, 32, 20, 52, 38, 35, 32, 25, 35, 32, 32, 28, 28, 25, 20, 25, 32,
                       28, 28, 25, 28, 25, 28, 28, 28, 18, 12, 4, 2, 3, 3, 3, 18, 8, 5, 10, 8,
                       15, 8, 15, 12, 15, 0, 0, 0, 0, 0],
        # Defensive
        'Tackles': [20, 14, 16, 18, 24, 10, 30, 24, 26, 20, 16, 30, 34, 18, 22, 40, 26, 16, 22, 18,
                    22, 28, 22, 20, 18, 18, 12, 22, 15, 10, 28, 32, 30, 35, 38, 42, 32, 35, 45, 38,
                    68, 72, 58, 52, 48, 2, 2, 1, 2, 2],
        'TackleSucc': [62.5, 52.8, 58.5, 58.2, 60.5, 52.2, 62.8, 60.2, 59.5, 56.8, 58.2, 61.5, 63.2, 55.5, 59.2, 64.5, 60.2, 58.5, 59.5, 56.8,
                       60.5, 62.2, 58.5, 57.2, 56.5, 55.8, 52.5, 59.5, 56.2, 52.5, 72.5, 75.2, 73.8, 78.2, 70.5, 68.2, 65.5, 70.2, 68.5, 70.8,
                       72.8, 78.5, 70.2, 68.5, 70.2, 52.5, 55.2, 48.5, 52.2, 50.5],
        'Interceptions': [14, 10, 10, 12, 16, 8, 20, 16, 18, 14, 12, 20, 24, 12, 15, 30, 18, 12, 15, 12,
                          15, 20, 15, 14, 12, 12, 8, 15, 10, 6, 42, 48, 45, 52, 42, 35, 28, 38, 42, 35,
                          52, 58, 45, 38, 42, 4, 5, 2, 4, 3],
        'Blocks': [10, 8, 8, 10, 12, 6, 14, 10, 12, 10, 10, 14, 16, 8, 10, 20, 12, 8, 10, 8,
                   10, 14, 10, 10, 8, 10, 6, 10, 6, 4, 35, 42, 40, 45, 38, 18, 15, 22, 25, 20,
                   28, 32, 25, 22, 25, 2, 3, 1, 2, 2],
        'Clearances': [5, 10, 3, 8, 5, 15, 5, 5, 8, 5, 8, 10, 10, 6, 6, 8, 5, 3, 5, 3,
                       5, 8, 5, 5, 4, 8, 10, 6, 4, 6, 145, 155, 148, 142, 128, 25, 18, 35, 42, 28,
                       32, 28, 25, 18, 22, 8, 10, 5, 8, 6],
        'AerialsWon': [14, 32, 5, 25, 10, 35, 10, 8, 25, 18, 20, 16, 14, 22, 10, 10, 5, 5, 6, 5,
                       8, 12, 8, 10, 8, 22, 28, 15, 18, 18, 115, 125, 128, 105, 85, 22, 15, 28, 32, 18,
                       48, 42, 35, 28, 32, 8, 10, 5, 8, 6],
        # Physical/Playing Time
        'Apps': [22, 20, 21, 21, 22, 22, 20, 22, 22, 21, 22, 22, 21, 20, 21, 22, 19, 14, 20, 18,
                 21, 22, 21, 21, 20, 20, 21, 22, 18, 12, 22, 22, 22, 21, 20, 22, 15, 20, 22, 21,
                 22, 20, 22, 21, 22, 22, 21, 22, 22, 21],
        'Mins': [1925, 1685, 1842, 1788, 1898, 1875, 1695, 1608, 1862, 1755, 1722, 1895, 1768, 1525, 1752, 1912, 1608, 1045, 1685, 1425,
                 1752, 1865, 1725, 1788, 1642, 1685, 1772, 1858, 1425, 895, 1978, 1985, 1962, 1875, 1725, 1908, 1185, 1725, 1892, 1825,
                 1945, 1755, 1912, 1808, 1892, 1980, 1890, 1980, 1980, 1890],
        'Starts': [21, 18, 20, 20, 21, 21, 19, 18, 21, 19, 19, 21, 19, 17, 19, 21, 18, 11, 18, 16,
                   19, 21, 19, 20, 18, 18, 20, 21, 15, 10, 22, 22, 22, 21, 19, 21, 13, 19, 21, 20,
                   22, 19, 21, 20, 21, 22, 21, 22, 22, 21],
        'YellowCards': [3, 4, 2, 3, 5, 5, 3, 4, 4, 5, 4, 6, 5, 4, 4, 7, 3, 2, 4, 2,
                        4, 3, 4, 3, 5, 4, 5, 4, 2, 1, 3, 4, 5, 4, 6, 5, 2, 3, 5, 4,
                        6, 5, 5, 6, 4, 1, 1, 1, 2, 1],
        'RedCards': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
                     0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                     0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        # Pressures
        'Pressures': [158, 135, 142, 152, 178, 105, 192, 168, 172, 162, 132, 188, 182, 145, 158, 208, 178, 125, 162, 148,
                      158, 178, 162, 158, 148, 155, 142, 168, 128, 95, 145, 158, 152, 148, 168, 162, 118, 148, 175, 165,
                      245, 232, 218, 198, 212, 32, 28, 25, 30, 28],
        'Recoveries': [58, 42, 48, 48, 62, 35, 68, 58, 62, 52, 42, 72, 72, 45, 52, 88, 62, 45, 55, 48,
                       55, 65, 55, 52, 48, 52, 42, 55, 38, 28, 85, 92, 88, 95, 82, 72, 52, 68, 78, 68,
                       98, 105, 92, 78, 85, 25, 28, 22, 25, 22],
    })
    
    # Calculate derived stats
    players['G90'] = round(players['Goals'] / (players['Mins'] / 90), 2)
    players['A90'] = round(players['Assists'] / (players['Mins'] / 90), 2)
    players['GA90'] = round((players['Goals'] + players['Assists']) / (players['Mins'] / 90), 2)
    players['xGxA90'] = round((players['xG'] + players['xA']) / (players['Mins'] / 90), 2)
    players['MinsPG'] = round(players['Mins'] / players['Apps'], 1)
    
    return players

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
    html = '<div class="table-container"><table class="custom-table">'
    html += '<thead><tr><th>#</th><th>Player</th><th>Team</th><th>Pos</th><th>Goals</th><th>Assists</th><th>Apps</th></tr></thead>'
    html += '<tbody>'
    
    for idx, (_, row) in enumerate(df.iterrows()):
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
        textfont=dict(color=WHITE, size=11, family='Inter')
    ))
    
    fig.update_layout(
        height=550, margin=dict(l=0, r=50, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE, family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', zeroline=False, tickfont=dict(color=WHITE)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11, color=WHITE))
    )
    return fig

def create_multi_radar(players_data, metrics, labels):
    """Create radar chart for multiple players"""
    fig = go.Figure()
    
    # Calculate max values for normalization
    max_vals = {}
    for m in metrics:
        max_vals[m] = max([p.get(m, 1) for p in players_data] + [1])
    
    for i, p in enumerate(players_data):
        vals = [p.get(m, 0) / max_vals[m] * 100 for m in metrics]
        vals.append(vals[0])  # Close the polygon
        labels_closed = labels + [labels[0]]
        
        color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
        rgba_fill = f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15)'
        
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels_closed, fill='toself', name=p['Player'],
            line_color=color, fillcolor=rgba_fill
        ))
    
    fig.update_layout(
        height=400, margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.15)', tickfont=dict(color=WHITE, size=9), range=[0, 100]),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.15)', tickfont=dict(color=WHITE, size=10))
        ),
        legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center', font=dict(color=WHITE, size=11)),
        font=dict(color=WHITE, family='Inter')
    )
    return fig

def create_multi_bar(players_data, metric, label):
    """Create bar chart comparing multiple players on a single metric"""
    names = [p['Player'] for p in players_data]
    values = [p.get(metric, 0) for p in players_data]
    colors = [PLAYER_COLORS[i % len(PLAYER_COLORS)] for i in range(len(players_data))]
    
    fig = go.Figure(go.Bar(
        x=names, y=values, marker_color=colors,
        text=values, textposition='outside', textfont=dict(color=WHITE, size=12)
    ))
    
    fig.update_layout(
        title=dict(text=label, font=dict(size=13, color=WHITE)),
        height=280, margin=dict(l=10, r=10, t=40, b=60),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE, family='Inter'),
        xaxis=dict(tickangle=-30, tickfont=dict(color=WHITE, size=10)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', tickfont=dict(color=WHITE))
    )
    return fig

def render_multi_comparison_row(label, players_data, metric, is_pct=False):
    """Render comparison row for multiple players"""
    values = [p.get(metric, 0) for p in players_data]
    max_val = max(values) if values else 0
    
    fmt = lambda x: f"{x:.1f}%" if is_pct else f"{x:.1f}" if isinstance(x, float) else str(x)
    
    html = f'<div class="compare-stat-row"><div class="compare-stat-label">{label}</div><div class="compare-stat-values">'
    
    for i, v in enumerate(values):
        color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
        is_winner = v == max_val and values.count(max_val) == 1
        winner_class = 'winner' if is_winner else ''
        html += f'<div class="compare-stat-value {winner_class}" style="color: {color};">{fmt(v)}</div>'
    
    html += '</div></div>'
    return html

# ============ MAIN APP ============

def main():
    # Header with PL logo
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg" 
                 alt="Premier League" class="pl-logo" 
                 onerror="this.style.display='none'">
            <div class="logo-text">
                <h1 class="logo-title">PREMIER <span>LEAGUE</span></h1>
                <p class="logo-subtitle" id="season-subtitle">Statistics Hub</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Season selector at top
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_season = st.selectbox("Select Season", SEASONS, index=0, key='main_season')
    
    # Update subtitle
    st.markdown(f"""
    <script>
        document.getElementById('season-subtitle').innerText = 'Statistics Hub - {selected_season} Season';
    </script>
    """, unsafe_allow_html=True)
    
    # API Key
    api_key = None
    try:
        api_key = st.secrets.get("FOOTBALL_API_KEY")
    except:
        pass
    
    if not api_key:
        with st.expander("API Settings"):
            api_key = st.text_input("API Key", type="password", help="Get free key at football-data.org")
    
    # Load data
    standings = get_sample_standings(selected_season)
    players = get_all_players(selected_season)
    
    # Status
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot"></div>
        <p class="status-text">Showing {selected_season} Season Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    top_scorer = players.loc[players['Goals'].idxmax()]
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
            <p class="stat-number">{top_scorer['Player'].split()[-1]}</p>
            <p class="stat-label">Top Scorer</p>
        </div>
        <div class="stat-card">
            <p class="stat-number">{standings['Pts'].max()}</p>
            <p class="stat-label">Top Points</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["TABLE", "TOP SCORERS", "PLAYER SEARCH", "MULTI COMPARISON"])
    
    # ==================== TAB 1: STANDINGS ====================
    with tab1:
        st.markdown('<div class="section-header"><h2 class="section-title">League Standings</h2></div>', unsafe_allow_html=True)
        st.markdown(render_standings_table(standings), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Points Distribution</h2></div>', unsafe_allow_html=True)
        st.plotly_chart(create_chart(standings), width='stretch', config={'displayModeBar': False})
    
    # ==================== TAB 2: SCORERS ====================
    with tab2:
        st.markdown('<div class="section-header"><h2 class="section-title">Top Scorers</h2></div>', unsafe_allow_html=True)
        scorers = players.nlargest(15, 'Goals')
        st.markdown(render_scorers_table(scorers), unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h2 class="section-title">Goals vs Expected Goals</h2></div>', unsafe_allow_html=True)
        top10 = players.nlargest(10, 'Goals')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Goals', x=top10['Player'], y=top10['Goals'], marker_color=CYAN))
        fig.add_trace(go.Bar(name='xG', x=top10['Player'], y=top10['xG'], marker_color=MAGENTA))
        fig.update_layout(
            barmode='group', height=350, margin=dict(l=10, r=10, t=10, b=100),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=WHITE, family='Inter'),
            legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center', font=dict(color=WHITE)),
            xaxis=dict(tickangle=-45, tickfont=dict(color=WHITE)), 
            yaxis=dict(showgrid=True, gridcolor='rgba(255,40,130,0.1)', tickfont=dict(color=WHITE))
        )
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # ==================== TAB 3: PLAYER SEARCH ====================
    with tab3:
        st.markdown('<div class="section-header"><h2 class="section-title">Player Search</h2></div>', unsafe_allow_html=True)
        
        # Search box
        search_query = st.text_input("Search for any player", placeholder="Type player name...", key='player_search')
        
        # Filter players based on search
        if search_query:
            filtered = players[players['Player'].str.lower().str.contains(search_query.lower())]
        else:
            filtered = players
        
        # Dropdown of filtered players
        if len(filtered) > 0:
            selected_player = st.selectbox(
                f"Select from {len(filtered)} players",
                filtered['Player'].tolist(),
                key='profile_select'
            )
            
            if selected_player:
                p = players[players['Player'] == selected_player].iloc[0]
                
                # Header card
                st.markdown(f"""
                <div class="player-card">
                    <div class="player-header">
                        <div>
                            <h3 class="player-name">{p['Player']}</h3>
                            <p class="player-team">{p['Team']} | {p['Nation']} | Age {p['Age']}</p>
                        </div>
                        <span class="player-position">{p['Position']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Stats in columns
                col1, col2 = st.columns(2)
                
                with col1:
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
                            <div class="stat-item"><p class="stat-item-label">Goals/90</p><p class="stat-item-value">{p['G90']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="player-card">
                        <p class="stats-category-title">Dribbling & Carrying</p>
                        <div class="stats-row">
                            <div class="stat-item"><p class="stat-item-label">Dribbles</p><p class="stat-item-value">{p['Dribbles']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Success %</p><p class="stat-item-value">{p['DribbleSucc']:.1f}%</p></div>
                            <div class="stat-item"><p class="stat-item-label">Prog Carries</p><p class="stat-item-value">{p['ProgCarries']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Into Box</p><p class="stat-item-value">{p['CarriesBox']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
                            <div class="stat-item"><p class="stat-item-label">Recoveries</p><p class="stat-item-value">{p['Recoveries']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
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
                            <div class="stat-item"><p class="stat-item-label">Pass Acc %</p><p class="stat-item-value">{p['PassAcc']:.1f}%</p></div>
                            <div class="stat-item"><p class="stat-item-label">Prog Passes</p><p class="stat-item-value">{p['ProgPasses']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Assists/90</p><p class="stat-item-value">{p['A90']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="player-card">
                        <p class="stats-category-title">Pressing & Work Rate</p>
                        <div class="stats-row">
                            <div class="stat-item"><p class="stat-item-label">Pressures</p><p class="stat-item-value">{p['Pressures']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Recoveries</p><p class="stat-item-value">{p['Recoveries']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="player-card">
                        <p class="stats-category-title">Playing Time & Discipline</p>
                        <div class="stats-row">
                            <div class="stat-item"><p class="stat-item-label">Apps</p><p class="stat-item-value">{p['Apps']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Minutes</p><p class="stat-item-value">{p['Mins']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Starts</p><p class="stat-item-value">{p['Starts']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Mins/Game</p><p class="stat-item-value">{p['MinsPG']}</p></div>
                        </div>
                        <div class="stats-row" style="margin-top: 0.5rem;">
                            <div class="stat-item"><p class="stat-item-label">Yellow</p><p class="stat-item-value">{p['YellowCards']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">Red</p><p class="stat-item-value">{p['RedCards']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">G+A/90</p><p class="stat-item-value">{p['GA90']}</p></div>
                            <div class="stat-item"><p class="stat-item-label">xG+xA/90</p><p class="stat-item-value">{p['xGxA90']}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No players found matching your search")
    
    # ==================== TAB 4: MULTI COMPARISON ====================
    with tab4:
        st.markdown('<div class="section-header"><h2 class="section-title">Multi-Player Comparison (Up to 5)</h2></div>', unsafe_allow_html=True)
        
        # Season range selector
        col1, col2 = st.columns(2)
        with col1:
            compare_season_start = st.selectbox("From Season", SEASONS, index=0, key='cmp_season_start')
        with col2:
            compare_season_end = st.selectbox("To Season", SEASONS, index=0, key='cmp_season_end')
        
        st.markdown(f"**Comparing stats from {compare_season_start} to {compare_season_end}**")
        
        # Player selection with multiselect
        selected_players = st.multiselect(
            "Select up to 5 players to compare",
            players['Player'].tolist(),
            default=['Mohamed Salah', 'Erling Haaland'],
            max_selections=5,
            key='multi_compare'
        )
        
        if len(selected_players) >= 2:
            # Get player data
            players_data = [players[players['Player'] == name].iloc[0].to_dict() for name in selected_players]
            
            # Player badges header
            badges_html = '<div class="compare-players-header">'
            for i, p in enumerate(players_data):
                color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
                badges_html += f'<div class="compare-player-badge" style="background: {color}; color: {"#37003c" if color == CYAN else "#fff"};">{p["Player"]} ({p["Team"]})</div>'
            badges_html += '</div>'
            st.markdown(badges_html, unsafe_allow_html=True)
            
            # Overall Radar
            st.markdown('<div class="section-header"><h2 class="section-title">Overall Comparison</h2></div>', unsafe_allow_html=True)
            radar_metrics = ['Goals', 'Assists', 'KeyPasses', 'Dribbles', 'Tackles', 'Pressures']
            radar_labels = ['Goals', 'Assists', 'Key Passes', 'Dribbles', 'Tackles', 'Pressures']
            st.plotly_chart(create_multi_radar(players_data, radar_metrics, radar_labels), width='stretch', config={'displayModeBar': False})
            
            # Bar charts for key metrics
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_multi_bar(players_data, 'Goals', 'Goals'), width='stretch', config={'displayModeBar': False})
            with col2:
                st.plotly_chart(create_multi_bar(players_data, 'Assists', 'Assists'), width='stretch', config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_multi_bar(players_data, 'xG', 'Expected Goals (xG)'), width='stretch', config={'displayModeBar': False})
            with col2:
                st.plotly_chart(create_multi_bar(players_data, 'KeyPasses', 'Key Passes'), width='stretch', config={'displayModeBar': False})
            
            # Detailed stat comparisons
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Attacking</h3>
                {render_multi_comparison_row('Goals', players_data, 'Goals')}
                {render_multi_comparison_row('xG', players_data, 'xG')}
                {render_multi_comparison_row('Shots', players_data, 'Shots')}
                {render_multi_comparison_row('Shots on Target', players_data, 'SoT')}
                {render_multi_comparison_row('Conversion %', players_data, 'ShotConv', True)}
                {render_multi_comparison_row('Box Touches', players_data, 'TouchBox')}
                {render_multi_comparison_row('Goals/90', players_data, 'G90')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Creative & Passing</h3>
                {render_multi_comparison_row('Assists', players_data, 'Assists')}
                {render_multi_comparison_row('xA', players_data, 'xA')}
                {render_multi_comparison_row('Key Passes', players_data, 'KeyPasses')}
                {render_multi_comparison_row('Through Balls', players_data, 'ThroughBalls')}
                {render_multi_comparison_row('Crosses', players_data, 'Crosses')}
                {render_multi_comparison_row('Pass Accuracy %', players_data, 'PassAcc', True)}
                {render_multi_comparison_row('Prog Passes', players_data, 'ProgPasses')}
                {render_multi_comparison_row('Assists/90', players_data, 'A90')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Dribbling & Carrying</h3>
                {render_multi_comparison_row('Dribbles', players_data, 'Dribbles')}
                {render_multi_comparison_row('Dribble Success %', players_data, 'DribbleSucc', True)}
                {render_multi_comparison_row('Prog Carries', players_data, 'ProgCarries')}
                {render_multi_comparison_row('Carries Into Box', players_data, 'CarriesBox')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Defensive</h3>
                {render_multi_comparison_row('Tackles', players_data, 'Tackles')}
                {render_multi_comparison_row('Tackle Success %', players_data, 'TackleSucc', True)}
                {render_multi_comparison_row('Interceptions', players_data, 'Interceptions')}
                {render_multi_comparison_row('Blocks', players_data, 'Blocks')}
                {render_multi_comparison_row('Clearances', players_data, 'Clearances')}
                {render_multi_comparison_row('Aerials Won', players_data, 'AerialsWon')}
                {render_multi_comparison_row('Recoveries', players_data, 'Recoveries')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="compare-category">
                <h3 class="compare-category-title">Playing Time & Efficiency</h3>
                {render_multi_comparison_row('Appearances', players_data, 'Apps')}
                {render_multi_comparison_row('Minutes', players_data, 'Mins')}
                {render_multi_comparison_row('Starts', players_data, 'Starts')}
                {render_multi_comparison_row('G+A/90', players_data, 'GA90')}
                {render_multi_comparison_row('xG+xA/90', players_data, 'xGxA90')}
            </div>
            """, unsafe_allow_html=True)
        
        elif len(selected_players) == 1:
            st.info("Select at least 2 players to compare")
        else:
            st.info("Select 2-5 players to compare")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Data provided by Football-Data.org</p>
        <p>Not affiliated with Premier League</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
