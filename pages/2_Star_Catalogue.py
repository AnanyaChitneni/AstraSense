import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="AstraSense — Star Catalogue",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stHeader"],
[data-testid="stDecoration"],
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}
.main > div:first-child { padding-top: 0 !important; }
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 0.3rem !important;
    padding-right: 0.3rem !important;
    max-width: 100% !important;
    margin: 0 !important;
}
[data-testid="stAppViewContainer"] { background: #000510 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #050510; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#00d4ff,#0044aa); border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
#   ALL 10 STARS — REAL NASA DATA
# ============================================
STARS = {
    "Kepler-452": {
        "planet": "Kepler-452 b", "type": "Super Earth", "emoji": "🌍",
        "color": "#4488ff", "glow": "rgba(68,136,255,0.4)", "ring": False,
        "description": (
            "Kepler-452b is often called Earth's 'older cousin' — a super-Earth "
            "orbiting in the habitable zone of a sun-like star. At 1.6 times Earth's "
            "radius, it receives similar energy from its star as Earth does from the Sun, "
            "making it one of the most Earth-like worlds ever discovered."
        ),
        "stats": {
            "Planet Radius":    "1.63 × Earth",
            "Planet Type":      "Super Earth",
            "Discovery Method": "Transit",
            "Discovery Date":   "2015",
            "Orbital Radius":   "1.046 AU",
            "Orbital Period":   "384.8 days",
            "Eccentricity":     "0.0",
            "Star Type":        "G-type (Sun-like)",
            "Star Mass":        "1.037 × Sun",
            "Distance":         "1,402 light-years",
        },
        "highlight": "In the habitable zone of a Sun-like star",
        "tags": ["Habitable Zone", "Sun-like Star", "Super Earth"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-452-b/",
    },
    "Kepler-7": {
        "planet": "Kepler-7 b", "type": "Hot Jupiter", "emoji": "🪐",
        "color": "#ff8844", "glow": "rgba(255,136,68,0.4)", "ring": True,
        "description": (
            "Kepler-7b is a massive hot Jupiter — the first exoplanet to have its clouds "
            "mapped. Despite being nearly twice Jupiter's size, it is extraordinarily "
            "lightweight, with a density less than that of balsa wood. It completes one "
            "orbit every 4.9 days, racing around its star in extreme proximity."
        ),
        "stats": {
            "Planet Radius":    "1.622 × Jupiter",
            "Planet Type":      "Hot Jupiter",
            "Discovery Method": "Transit",
            "Discovery Date":   "2009",
            "Orbital Radius":   "0.06067 AU",
            "Orbital Period":   "4.9 days",
            "Eccentricity":     "0.0",
            "Planet Mass":      "0.441 × Jupiter",
            "Star Type":        "F-type",
            "Distance":         "1,040 light-years",
        },
        "highlight": "First exoplanet to have its clouds mapped",
        "tags": ["Hot Jupiter", "Cloud Mapped", "Ultra-low Density"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-7b/",
    },
    "Kepler-10": {
        "planet": "Kepler-10 b", "type": "Rocky", "emoji": "🌑",
        "color": "#cc6644", "glow": "rgba(204,102,68,0.4)", "ring": False,
        "description": (
            "Kepler-10b holds a historic distinction — it was the first confirmed rocky "
            "exoplanet ever discovered by the Kepler mission. Orbiting extremely close to "
            "its star, it completes a full orbit in just 0.84 days. Its surface temperature "
            "soars above 1,800°C, making it a scorched, molten world."
        ),
        "stats": {
            "Planet Radius":    "1.47 × Earth",
            "Planet Type":      "Rocky",
            "Discovery Method": "Transit",
            "Discovery Date":   "2011",
            "Orbital Radius":   "0.01684 AU",
            "Orbital Period":   "0.84 days",
            "Eccentricity":     "0.0",
            "Planet Mass":      "4.56 × Earth",
            "Star Type":        "G-type",
            "Distance":         "564 light-years",
        },
        "highlight": "First confirmed rocky exoplanet from Kepler",
        "tags": ["Rocky", "Historic", "Ultra-hot"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-10-b/",
    },
    "Kepler-22": {
        "planet": "Kepler-22 b", "type": "Super Earth", "emoji": "🌊",
        "color": "#44aaff", "glow": "rgba(68,170,255,0.4)", "ring": False,
        "description": (
            "Kepler-22b was the first confirmed exoplanet found in the habitable zone of "
            "a Sun-like star by NASA's Kepler mission. At 2.4 times Earth's radius, it "
            "could be a water world or a rocky super-Earth with a thick atmosphere — "
            "scientists are still investigating its true nature."
        ),
        "stats": {
            "Planet Radius":    "2.4 × Earth",
            "Planet Type":      "Super Earth",
            "Discovery Method": "Transit",
            "Discovery Date":   "2011",
            "Orbital Radius":   "0.849 AU",
            "Orbital Period":   "289.9 days",
            "Eccentricity":     "0.0",
            "Star Type":        "G-type (Sun-like)",
            "Star Mass":        "0.97 × Sun",
            "Distance":         "587 light-years",
        },
        "highlight": "First Kepler planet confirmed in habitable zone",
        "tags": ["Habitable Zone", "Water World?", "Super Earth"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-22b/",
    },
    "Kepler-16": {
        "planet": "Kepler-16 b", "type": "Circumbinary", "emoji": "☀️",
        "color": "#FFD700", "glow": "rgba(255,215,0,0.4)", "ring": True,
        "description": (
            "Kepler-16b is the real-life Tatooine — the first confirmed planet to orbit "
            "two stars simultaneously. This Saturn-sized circumbinary world completes one "
            "orbit around its binary star system every 229 days. Sunsets here would show "
            "two suns setting on the horizon."
        ),
        "stats": {
            "Planet Radius":    "0.754 × Jupiter",
            "Planet Type":      "Circumbinary Gas",
            "Discovery Method": "Transit",
            "Discovery Date":   "2011",
            "Orbital Radius":   "0.7048 AU",
            "Orbital Period":   "228.8 days",
            "Eccentricity":     "0.0069",
            "Planet Mass":      "0.333 × Jupiter",
            "Star Type":        "K + M binary",
            "Distance":         "245 light-years",
        },
        "highlight": "Real-life Tatooine — orbits two stars",
        "tags": ["Circumbinary", "Binary Star", "Tatooine"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-16b/",
    },
    "Kepler-62": {
        "planet": "Kepler-62 f", "type": "Super Earth", "emoji": "💧",
        "color": "#00BFFF", "glow": "rgba(0,191,255,0.4)", "ring": False,
        "description": (
            "Kepler-62f is one of the most promising Earth-like candidates ever found. "
            "At 1.4 times Earth's radius, it orbits comfortably within the habitable zone "
            "of its star. Climate models suggest it could support liquid water — possibly "
            "an ocean world covered in a global sea."
        ),
        "stats": {
            "Planet Radius":    "1.41 × Earth",
            "Planet Type":      "Super Earth",
            "Discovery Method": "Transit",
            "Discovery Date":   "2013",
            "Orbital Radius":   "0.718 AU",
            "Orbital Period":   "267.3 days",
            "Eccentricity":     "0.0",
            "Star Type":        "K-type",
            "Star Mass":        "0.69 × Sun",
            "Distance":         "1,200 light-years",
        },
        "highlight": "Potential ocean world in habitable zone",
        "tags": ["Habitable Zone", "Ocean World?", "K-type Star"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-62-f/",
    },
    "Kepler-186": {
        "planet": "Kepler-186 f", "type": "Earth-size", "emoji": "🌱",
        "color": "#00FF88", "glow": "rgba(0,255,136,0.4)", "ring": False,
        "description": (
            "Kepler-186f made history as the first Earth-size planet ever confirmed in "
            "the habitable zone of another star. Though its host star is a cooler M-dwarf, "
            "Kepler-186f receives about 30% less energy than Earth does from the Sun — "
            "placing it near the outer edge of the habitable zone."
        ),
        "stats": {
            "Planet Radius":    "1.17 × Earth",
            "Planet Type":      "Earth-size",
            "Discovery Method": "Transit",
            "Discovery Date":   "2014",
            "Orbital Radius":   "0.432 AU",
            "Orbital Period":   "129.9 days",
            "Eccentricity":     "0.0",
            "Star Type":        "M-dwarf",
            "Star Mass":        "0.478 × Sun",
            "Distance":         "582 light-years",
        },
        "highlight": "First Earth-size planet in a habitable zone",
        "tags": ["Earth-size", "Historic", "M-dwarf", "Habitable Zone"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-186-f/",
    },
    "Kepler-69": {
        "planet": "Kepler-69 c", "type": "Super Venus", "emoji": "🌋",
        "color": "#FF6633", "glow": "rgba(255,102,51,0.4)", "ring": False,
        "description": (
            "Kepler-69c orbits at the inner edge of its star's habitable zone, making it "
            "a potential super-Venus — a world scorched by a runaway greenhouse effect. "
            "At 1.71 times Earth's radius, it offers a stark comparison to true habitable "
            "zone planets and helps astronomers define the habitable zone's boundaries."
        ),
        "stats": {
            "Planet Radius":    "1.71 × Earth",
            "Planet Type":      "Super Venus",
            "Discovery Method": "Transit",
            "Discovery Date":   "2013",
            "Orbital Radius":   "0.64 AU",
            "Orbital Period":   "242.5 days",
            "Eccentricity":     "0.0",
            "Star Type":        "G-type (Sun-like)",
            "Star Mass":        "0.81 × Sun",
            "Distance":         "2,430 light-years",
        },
        "highlight": "Super-Venus at habitable zone inner boundary",
        "tags": ["Super-Venus", "Inner HZ Edge", "Greenhouse?"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-69-c/",
    },
    "Kepler-442": {
        "planet": "Kepler-442 b", "type": "Super Earth", "emoji": "⭐",
        "color": "#AAFFAA", "glow": "rgba(170,255,170,0.4)", "ring": False,
        "description": (
            "Kepler-442b holds one of the highest Earth Similarity Index scores ever "
            "calculated — 0.84 out of 1.0. It orbits comfortably in the habitable zone "
            "of a K-type star, receiving about 70% of Earth's solar flux. Among all "
            "known exoplanets, it ranks as one of the most genuinely Earth-like worlds."
        ),
        "stats": {
            "Planet Radius":    "1.34 × Earth",
            "Planet Type":      "Super Earth",
            "Discovery Method": "Transit",
            "Discovery Date":   "2015",
            "Orbital Radius":   "0.409 AU",
            "Orbital Period":   "112.3 days",
            "Eccentricity":     "0.04",
            "Star Type":        "K-type",
            "Star Mass":        "0.61 × Sun",
            "Distance":         "1,206 light-years",
        },
        "highlight": "Earth Similarity Index: 0.84 — near top of all known planets",
        "tags": ["High ESI", "Habitable Zone", "K-type Star"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-442-b/",
    },
    "Kepler-90": {
        "planet": "Kepler-90 i", "type": "Rocky", "emoji": "🔭",
        "color": "#CC88FF", "glow": "rgba(204,136,255,0.4)", "ring": False,
        "description": (
            "Kepler-90 hosts 8 confirmed planets — the same number as our own Solar "
            "System, making it the first known star to tie with the Sun for planet count. "
            "Kepler-90i was discovered by Google's AI in 2017, making it the first exoplanet "
            "found using machine learning. The system is a scaled-up, hotter version of ours."
        ),
        "stats": {
            "Planet Radius":    "1.32 × Earth",
            "Planet Type":      "Rocky",
            "Discovery Method": "Transit + AI",
            "Discovery Date":   "2017",
            "Orbital Radius":   "0.1017 AU",
            "Orbital Period":   "14.4 days",
            "Eccentricity":     "0.0",
            "Star Type":        "G-type (Sun-like)",
            "Star Mass":        "1.13 × Sun",
            "Distance":         "2,545 light-years",
        },
        "highlight": "8-planet system — found by Google AI",
        "tags": ["8-Planet System", "AI Discovery", "Machine Learning"],
        "nasa_url": "https://science.nasa.gov/exoplanet-catalog/kepler-90-i/",
    },
}

# ============================================
#   3D PLANET GENERATOR
# ============================================
def make_planet(star_key):
    s     = STARS[star_key]
    color = s["color"]
    glow  = s["glow"]

    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, np.pi,   60)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0.0, color],[0.4, color],[0.7, "rgba(255,255,255,0.15)"],[1.0, color]],
        showscale=False,
        lighting=dict(ambient=0.4, diffuse=0.8, specular=0.6, roughness=0.4, fresnel=0.8),
        lightposition=dict(x=2, y=3, z=4),
        opacity=0.95,
        name=s["planet"]
    ))

    scale = 1.12
    fig.add_trace(go.Surface(
        x=x*scale, y=y*scale, z=z*scale,
        colorscale=[[0, glow],[1, "rgba(0,0,0,0)"]],
        showscale=False, opacity=0.25, name="Atmosphere"
    ))

    if s["ring"]:
        theta = np.linspace(0, 2*np.pi, 200)
        for r in np.linspace(1.5, 2.2, 8):
            rx = r * np.cos(theta)
            ry = r * np.sin(theta) * 0.3
            rz = np.zeros_like(theta)
            fig.add_trace(go.Scatter3d(
                x=rx, y=ry, z=rz, mode='lines',
                line=dict(color=color, width=1.5),
                opacity=0.35, showlegend=False
            ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, range=[-2.5,2.5]),
            yaxis=dict(visible=False, range=[-2.5,2.5]),
            zaxis=dict(visible=False, range=[-2.5,2.5]),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(l=0,r=0,t=0,b=0), height=380,
    )
    return fig

# ============================================
#   PAGE STYLES
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

.page-bg {
    position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;
    background:
        radial-gradient(ellipse at 20% 30%, rgba(0,30,100,0.4) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 70%, rgba(0,20,80,0.3) 0%, transparent 50%),
        linear-gradient(180deg,#000510,#000818,#000510);
}
.grid-bg {
    position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;
    background-image:
        linear-gradient(rgba(0,100,200,0.03) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,100,200,0.03) 1px,transparent 1px);
    background-size:60px 60px; pointer-events:none;
}
.page-nav {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.85rem 2.5rem; background:rgba(0,5,20,0.92);
    border-bottom:1px solid rgba(0,180,255,0.15); backdrop-filter:blur(20px);
    position:fixed; top:0; left:0; right:0; z-index:1000;
}
.nav-logo {
    font-family:'Orbitron',monospace; font-size:1rem; font-weight:900;
    background:linear-gradient(135deg,#00d4ff,#0055cc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:0.3rem; text-decoration:none;
}
.nav-links { display:flex; gap:2rem; }
.nav-links a {
    font-family:'Share Tech Mono',monospace; font-size:0.65rem;
    color:rgba(180,220,255,0.6); text-decoration:none;
    letter-spacing:0.15rem; transition:color 0.2s; text-transform:uppercase;
}
.nav-links a:hover, .nav-links a.active { color:#00d4ff; }
.nav-spacer { height:52px; }
.glow-line {
    height:1px;
    background:linear-gradient(90deg,transparent,#00d4ff,#0044aa,transparent);
    margin:0.8rem 0;
}

.star-grid-10 {
    display:grid;
    grid-template-columns:repeat(5, 1fr);
    gap:0.8rem;
    margin-bottom:1.5rem;
}
.star-card {
    background:rgba(0,8,35,0.85);
    border:1px solid rgba(0,150,255,0.2);
    border-radius:16px; padding:1.1rem 0.8rem;
    text-align:center; cursor:pointer; transition:all 0.3s ease;
    backdrop-filter:blur(15px); position:relative; overflow:hidden;
}
.star-card:hover {
    border-color:#00d4ff; transform:translateY(-6px);
    box-shadow:0 0 30px rgba(0,212,255,0.2), 0 15px 35px rgba(0,0,0,0.4);
}
.star-card.active {
    border-color:#00d4ff; background:rgba(0,20,70,0.9);
    box-shadow:0 0 25px rgba(0,212,255,0.25);
}
.star-emoji { font-size:2rem; margin-bottom:0.5rem; display:block; }
.star-name {
    font-family:'Orbitron',monospace; font-size:0.65rem; font-weight:700;
    color:#00d4ff; letter-spacing:0.12rem; display:block; margin-bottom:0.25rem;
}
.star-type {
    font-family:'Share Tech Mono',monospace; font-size:0.54rem;
    color:rgba(180,220,255,0.5); letter-spacing:0.12rem;
}
.star-highlight {
    font-family:'Share Tech Mono',monospace; font-size:0.48rem;
    color:rgba(0,200,255,0.45); margin-top:0.4rem; line-height:1.4;
}

.detail-panel {
    background:rgba(0,5,25,0.92); border:1px solid rgba(0,180,255,0.18);
    border-radius:20px; padding:2rem; backdrop-filter:blur(20px);
}
.planet-title {
    font-family:'Orbitron',monospace; font-size:clamp(1.2rem,3vw,2rem);
    font-weight:900;
    background:linear-gradient(135deg,#00d4ff,#0055cc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:0.2rem; margin-bottom:0.5rem;
}
.planet-type-badge {
    display:inline-block; font-family:'Share Tech Mono',monospace;
    font-size:0.6rem; color:#00d4ff;
    border:1px solid rgba(0,212,255,0.4); border-radius:20px;
    padding:0.2rem 0.8rem; letter-spacing:0.2rem; margin-bottom:1rem;
}
.planet-desc {
    font-family:'Exo 2',sans-serif; font-size:0.88rem;
    color:rgba(180,220,255,0.7); line-height:1.8; font-weight:300;
    margin-bottom:1.5rem;
}
.tag-row { display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1.5rem; }
.tag {
    font-family:'Share Tech Mono',monospace; font-size:0.55rem;
    color:rgba(0,200,255,0.7); background:rgba(0,100,200,0.15);
    border:1px solid rgba(0,150,255,0.25); border-radius:12px;
    padding:0.2rem 0.7rem; letter-spacing:0.1rem;
}
.stats-table { width:100%; border-collapse:collapse; }
.stats-table tr { border-bottom:1px solid rgba(0,180,255,0.08); }
.stats-table td { padding:0.55rem 0.5rem; font-size:0.82rem; }
.stats-table td:first-child {
    font-family:'Share Tech Mono',monospace; color:rgba(150,200,255,0.5);
    font-size:0.62rem; letter-spacing:0.15rem; text-transform:uppercase; width:45%;
}
.stats-table td:last-child {
    font-family:'Orbitron',monospace; color:white; font-weight:600; font-size:0.8rem;
}
.nasa-btn {
    display:inline-block; font-family:'Share Tech Mono',monospace;
    font-size:0.62rem; color:rgba(0,200,255,0.8);
    border:1px solid rgba(0,200,255,0.3); border-radius:8px;
    padding:0.5rem 1.2rem; text-decoration:none; letter-spacing:0.2rem;
    transition:all 0.3s; margin-top:0.5rem; text-transform:uppercase;
}
.nasa-btn:hover {
    background:rgba(0,100,200,0.2); border-color:#00d4ff; color:#00d4ff;
}
.sec-title {
    font-family:'Orbitron',monospace; font-size:0.7rem; color:#00d4ff;
    letter-spacing:0.4rem; margin:1rem 0 0.8rem; text-transform:uppercase;
}

.compare-grid-10 {
    display:grid; grid-template-columns:repeat(5,1fr); gap:0.7rem;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .page-nav { padding: 0.7rem 1rem !important; }
    .nav-links { display: none !important; }
    .star-grid-10 { grid-template-columns: repeat(2, 1fr) !important; gap: 0.5rem !important; }
    .star-emoji { font-size: 1.4rem !important; }
    .star-name { font-size: 0.56rem !important; }
    .star-highlight { display: none !important; }
    .detail-panel { padding: 1rem !important; }
    .planet-title { font-size: 1rem !important; }
    .planet-desc { font-size: 0.78rem !important; }
    .stats-table td { font-size: 0.7rem !important; padding: 0.35rem 0.3rem !important; }
    .compare-grid-10 { grid-template-columns: repeat(2, 1fr) !important; gap: 0.5rem !important; }
}
@media (max-width: 480px) {
    .star-grid-10 { grid-template-columns: repeat(2, 1fr) !important; }
}
</style>
<div class='page-bg'></div>
<div class='grid-bg'></div>
""", unsafe_allow_html=True)

# ============================================
#   NAV
# ============================================
st.markdown("""
<div class='page-nav'>
    <a href='/' class='nav-logo' target="_self">◈ ASTRASENSE</a>
    <div class='nav-links'>
        <a href='/Analysis' target="_self">ANALYSIS</a>
        <a href='/Star_Catalogue' class='active' target="_self">STAR CATALOGUE</a>
        <a href='/Noise_Lab' target="_self">NOISE LAB</a>
        <a href='/Science' target="_self">THE SCIENCE</a>
        <a href='/Performance' target="_self">PERFORMANCE</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
#   HERO
# ============================================
st.markdown("""
<div style='text-align:center;padding:0.5rem 1rem 0.5rem;'>
    <span style='font-family:Share Tech Mono,monospace;font-size:0.65rem;
         color:rgba(0,200,255,0.6);letter-spacing:0.5rem;display:block;
         margin-bottom:0.5rem;text-transform:uppercase;'>
        ◈ EXOPLANET DATABASE — 10 STAR SYSTEMS
    </span>
    <div style='font-family:Orbitron,monospace;font-size:clamp(1.8rem,4vw,3.5rem);
         font-weight:900;background:linear-gradient(135deg,#00d4ff,#0055cc);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;letter-spacing:0.3rem;line-height:1.1;'>
        STAR CATALOGUE
    </div>
    <div style='font-family:Exo 2,sans-serif;font-size:0.9rem;
         color:rgba(180,220,255,0.6);margin-top:0.5rem;font-weight:300;'>
        Explore all 10 trained exoplanet host stars with real NASA orbital data
        and interactive 3D planet visualizations
    </div>
</div>
<div class='glow-line'></div>
""", unsafe_allow_html=True)

# ============================================
#   SESSION STATE
# ============================================
if 'selected_star' not in st.session_state:
    st.session_state.selected_star = "Kepler-452"

# ============================================
#   STAR SELECTOR
# ============================================
st.markdown("<div class='sec-title'>◈ SELECT A STAR SYSTEM — 10 AVAILABLE</div>",
           unsafe_allow_html=True)

cards_html = "<div class='star-grid-10'>"
for key, data in STARS.items():
    active_cls = "active" if st.session_state.selected_star == key else ""
    cards_html += f"""
        <div class='star-card {active_cls}'>
            <span class='star-emoji'>{data['emoji']}</span>
            <span class='star-name'>{key}</span>
            <span class='star-type'>{data['type']}</span>
            <div class='star-highlight'>{data['highlight']}</div>
        </div>"""
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

row1_keys = list(STARS.keys())[:5]
row2_keys = list(STARS.keys())[5:]

cols1 = st.columns(5)
for col, key in zip(cols1, row1_keys):
    with col:
        if st.button(f"SELECT {key}", key=f"sel_{key}", use_container_width=True):
            st.session_state.selected_star = key
            st.rerun()

cols2 = st.columns(5)
for col, key in zip(cols2, row2_keys):
    with col:
        if st.button(f"SELECT {key}", key=f"sel_{key}", use_container_width=True):
            st.session_state.selected_star = key
            st.rerun()

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

# ============================================
#   DETAIL VIEW
# ============================================
sel  = st.session_state.selected_star
data = STARS[sel]

st.markdown(f"<div class='sec-title'>◈ {data['planet'].upper()} — DETAIL VIEW</div>",
           unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    st.plotly_chart(make_planet(sel), use_container_width=True)
    st.markdown(f"""
        <div style='text-align:center;font-family:Share Tech Mono,monospace;
             font-size:0.6rem;color:rgba(0,200,255,0.4);
             letter-spacing:0.2rem;margin-top:-1rem;'>
            ↻ DRAG TO ROTATE  ·  SCROLL TO ZOOM
        </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
        <div class='detail-panel'>
            <div class='planet-title'>{data['planet'].upper()}</div>
            <div class='planet-type-badge'>{data['type'].upper()}</div>
            <div class='planet-desc'>{data['description']}</div>
            <div class='tag-row'>
                {''.join(f"<span class='tag'>{t}</span>" for t in data['tags'])}
            </div>
            <table class='stats-table'>
                {''.join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in data['stats'].items())}
            </table>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
#   ACTION BUTTONS
# ============================================
b1, b2, b3 = st.columns([1, 1, 2])
with b1:
    if st.button(f"🔬  ANALYZE  {sel}", use_container_width=True):
        st.switch_page("pages/1_Analysis.py")
with b2:
    st.markdown(f"""
        <a href='{data["nasa_url"]}' target='_blank' class='nasa-btn'
           style='display:block;text-align:center;margin-top:0.3rem;'>
            🛰️ &nbsp; VIEW ON NASA
        </a>
    """, unsafe_allow_html=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

# ============================================
#   QUICK COMPARISON
# ============================================
st.markdown("<div class='sec-title'>◈ QUICK COMPARISON — ALL 10 SYSTEMS</div>",
           unsafe_allow_html=True)

st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.58rem;"
            "color:rgba(0,200,255,0.4);letter-spacing:0.25rem;margin-bottom:0.5rem;'>"
            "◈ ORIGINAL 4 + KEPLER-16</div>", unsafe_allow_html=True)

compare_row1 = st.columns(5)
for col, key in zip(compare_row1, list(STARS.keys())[:5]):
    d = STARS[key]
    with col:
        radius = d['stats'].get('Planet Radius', 'N/A')
        period = d['stats'].get('Orbital Period', 'N/A')
        dist   = d['stats'].get('Distance', 'N/A')
        st.markdown(f"""
            <div style='background:rgba(0,8,35,0.85);border:1px solid rgba(0,150,255,0.18);
                 border-radius:14px;padding:1rem 0.8rem;text-align:center;'>
                <div style='font-size:1.6rem;margin-bottom:0.4rem;'>{d['emoji']}</div>
                <div style='font-family:Orbitron,monospace;font-size:0.6rem;color:#00d4ff;
                     letter-spacing:0.12rem;margin-bottom:0.6rem;'>{key}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>RADIUS</div>
                <div style='font-family:Orbitron,monospace;font-size:0.68rem;
                     color:white;margin-bottom:0.4rem;'>{radius}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>PERIOD</div>
                <div style='font-family:Orbitron,monospace;font-size:0.68rem;
                     color:white;margin-bottom:0.4rem;'>{period}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>DISTANCE</div>
                <div style='font-family:Orbitron,monospace;font-size:0.62rem;
                     color:rgba(0,200,255,0.8);'>{dist}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.58rem;"
            "color:rgba(0,200,255,0.4);letter-spacing:0.25rem;margin-bottom:0.5rem;'>"
            "◈ NEW 5 ADDITIONS</div>", unsafe_allow_html=True)

compare_row2 = st.columns(5)
for col, key in zip(compare_row2, list(STARS.keys())[5:]):
    d = STARS[key]
    with col:
        radius = d['stats'].get('Planet Radius', 'N/A')
        period = d['stats'].get('Orbital Period', 'N/A')
        dist   = d['stats'].get('Distance', 'N/A')
        st.markdown(f"""
            <div style='background:rgba(0,8,35,0.85);border:1px solid rgba(0,150,255,0.18);
                 border-radius:14px;padding:1rem 0.8rem;text-align:center;'>
                <div style='font-size:1.6rem;margin-bottom:0.4rem;'>{d['emoji']}</div>
                <div style='font-family:Orbitron,monospace;font-size:0.6rem;color:#00d4ff;
                     letter-spacing:0.12rem;margin-bottom:0.6rem;'>{key}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>RADIUS</div>
                <div style='font-family:Orbitron,monospace;font-size:0.68rem;
                     color:white;margin-bottom:0.4rem;'>{radius}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>PERIOD</div>
                <div style='font-family:Orbitron,monospace;font-size:0.68rem;
                     color:white;margin-bottom:0.4rem;'>{period}</div>
                <div style='font-family:Share Tech Mono,monospace;font-size:0.5rem;
                     color:rgba(150,200,255,0.5);letter-spacing:0.1rem;'>DISTANCE</div>
                <div style='font-family:Orbitron,monospace;font-size:0.62rem;
                     color:rgba(0,200,255,0.8);'>{dist}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;font-family:Share Tech Mono;font-size:0.55rem;
     color:rgba(255,255,255,0.1);letter-spacing:0.25rem;padding:2rem 0;
     margin-top:2rem;border-top:1px solid rgba(0,180,255,0.1);'>
    ASTRASENSE v2.0 &nbsp;◈&nbsp; STAR CATALOGUE &nbsp;◈&nbsp; 10 STAR SYSTEMS
    &nbsp;◈&nbsp; NASA KEPLER REAL ORBITAL DATA
</div>
""", unsafe_allow_html=True)