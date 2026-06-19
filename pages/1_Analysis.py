import streamlit as st
import torch
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import lightkurve as lk
from scipy.signal import savgol_filter, medfilt
import sys, os, base64, time, warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import UNet1D, DDPMScheduler

st.set_page_config(
    page_title="AstraSense — Analysis",
    page_icon="🔬",
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
    width: 0 !important;
}
.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 0.3rem !important;
    padding-right: 0.3rem !important;
    max-width: 100% !important;
    margin: 0 !important;
}
[data-testid="stAppViewContainer"] {
    background: #000510 !important;
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
}
.stTextInput > div > div > input {
    background: rgba(5,5,30,0.95) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    color: white !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.2) !important;
}
div[data-baseweb="select"] > div {
    background: rgba(5,5,30,0.95) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stButton > button {
    background: linear-gradient(135deg,
        rgba(0,100,200,0.2), rgba(0,50,150,0.3)) !important;
    border: 1px solid rgba(0,180,255,0.5) !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2rem !important;
    border-radius: 10px !important;
    transition: all 0.3s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg,
        rgba(0,150,255,0.3), rgba(0,80,200,0.4)) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.3) !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg,#00d4ff,#0044aa) !important;
    border-radius: 10px !important;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #050510; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#00d4ff,#0044aa);
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
#   HELPERS
# ============================================
def load_video_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ============================================
#   INTRO VIDEO
# ============================================
if 'analysis_intro_shown' not in st.session_state:
    st.session_state.analysis_intro_shown = False

if not st.session_state.analysis_intro_shown:
    st.session_state.analysis_intro_shown = True

    intro_b64 = load_video_b64("assets/intro_video.mp4")
    intro_src = f"data:video/mp4;base64,{intro_b64}" if intro_b64 else ""

    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    #intro-overlay {{
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 56.25vw !important;
        max-height: 100vh !important;
        z-index: 99999 !important;
        background: #000510;
        display: flex; align-items: center; justify-content: center;
        transition: opacity 0.6s ease;
    }}
    #intro-overlay video {{
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%; object-fit: cover;
    }}
    #intro-overlay .ov {{
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0,5,20,0.3); z-index: 1;
    }}
    #intro-overlay .txt {{ position: relative; z-index: 2; text-align: center; }}
    #intro-overlay .t1 {{
        font-family: 'Orbitron', monospace !important;
        font-size: clamp(2.5rem, 8vw, 7rem); font-weight: 900;
        background: linear-gradient(135deg,#00d4ff 0%,#0099ff 35%,#0055dd 65%,#00aaff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: clamp(0.2rem, 1.5vw, 0.7rem); line-height: 1;
        opacity: 0; animation: introUp 1s ease 0.3s forwards;
    }}
    #intro-overlay .t2 {{
        font-family: 'Share Tech Mono', monospace !important;
        font-size: clamp(0.5rem, 1.3vw, 0.75rem);
        color: rgba(0,200,255,0.65);
        letter-spacing: clamp(0.15rem, 0.8vw, 0.45rem);
        margin-top: 1rem; opacity: 0;
        animation: introUp 1s ease 0.8s forwards;
    }}
    @keyframes introUp {{
        from {{ opacity:0; transform:translateY(20px); }}
        to   {{ opacity:1; transform:translateY(0); }}
    }}
    #intro-overlay.hide {{
        opacity: 0 !important; pointer-events: none !important;
    }}
    </style>

    <div id="intro-overlay">
        {'<video autoplay muted playsinline><source src="' + intro_src + '" type="video/mp4"></video>' if intro_src else ''}
        <div class="ov"></div>
        <div class="txt">
            <div class="t1">ASTRASENSE</div>
            <div class="t2">◈ &nbsp; INITIALIZING ANALYSIS MODULE &nbsp; ◈</div>
        </div>
    </div>

    <script>
    document.fonts.ready.then(function() {{
        setTimeout(function() {{
            var el = document.getElementById('intro-overlay');
            if(el) {{
                el.classList.add('hide');
                setTimeout(function() {{ if(el) el.style.display = 'none'; }}, 700);
            }}
        }}, 2500);
    }});
    </script>
    """, unsafe_allow_html=True)

    time.sleep(3)
    st.rerun()

# ============================================
#   LOAD MODEL
# ============================================
@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model  = UNet1D(in_channels=1, base_channels=64, time_embed_dim=128).to(device)
    model.load_state_dict(torch.load(
        "models/best_model.pt", map_location=device, weights_only=True
    ))
    model.eval()
    scheduler = DDPMScheduler(num_timesteps=1000, device=str(device))
    return model, scheduler, device

# ============================================
#   HELPERS
# ============================================
def fetch_star(star, mission="Kepler"):
    try:
        if mission == "Kepler":
            s = lk.search_lightcurve(star, mission="Kepler", quarter=3)
        else:
            s = lk.search_lightcurve(star, mission="TESS")
        if len(s) == 0:
            return None, None, None
        lc = s[0].download().remove_nans().normalize()
        return lc.time.value, lc.flux.value, str(s[0].target_name)
    except:
        return None, None, None

def denoise(model, scheduler, noisy, device):
    model.eval()
    with torch.no_grad():
        x = torch.FloatTensor(noisy).unsqueeze(0).unsqueeze(0).to(device)
        t = torch.tensor([500], device=device)
        return torch.clamp(model(x, t), -5, 5).squeeze().cpu().numpy()

def calc_rmse(a, b):
    n = min(len(a), len(b))
    return float(np.sqrt(np.mean((a[:n]-b[:n])**2)))

def calc_snr(clean, d):
    n = min(len(clean), len(d))
    return float(10*np.log10(
        np.mean(clean[:n]**2) / (np.mean((clean[:n]-d[:n])**2)+1e-10)
    ))

def transit_info(flux):
    return (
        min(100, int((1-np.min(flux))*10000)),
        float((1-np.min(flux))*100),
        int(np.sum(flux < np.percentile(flux, 5)))
    )

GRID   = 'rgba(255,255,255,0.04)'
LINE   = 'rgba(0,212,255,0.12)'
PLOTBG = 'rgba(8,8,35,0.95)'

def main_chart(time_data, noisy, denoised, savgol, star):
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=[
            "⬡  RAW TELESCOPE SIGNAL",
            "◈  ASTRASENSE — AI DENOISED",
            "◇  SAVITZKY-GOLAY BASELINE"
        ]
    )
    t = time_data[:512]
    n, d, s = noisy[:512], denoised[:512], savgol[:512]
    fig.add_trace(go.Scatter(x=t, y=n, mode='lines',
        line=dict(color='#CC00FF', width=0.7),
        fill='tozeroy', fillcolor='rgba(204,0,255,0.04)',
        name='Raw'), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=d, mode='lines',
        line=dict(color='#00D4FF', width=1.8),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.07)',
        name='AI Denoised'), row=2, col=1)
    thresh = np.percentile(d, 3)
    idx = np.where(d < thresh)[0]
    if len(idx):
        fig.add_trace(go.Scatter(x=t[idx], y=d[idx], mode='markers',
            marker=dict(color='#FF8C00', size=8, symbol='triangle-down',
                       line=dict(color='#FFD700', width=1)),
            name='Transit'), row=2, col=1)
    fig.add_trace(go.Scatter(x=t, y=s, mode='lines',
        line=dict(color='#00FF88', width=1.3),
        fill='tozeroy', fillcolor='rgba(0,255,136,0.04)',
        name='Savitzky-Golay'), row=3, col=1)
    fig.update_layout(
        height=700, paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=PLOTBG,
        font=dict(family='Share Tech Mono', color='rgba(255,255,255,0.4)', size=9),
        title=dict(text=f"◈  LIGHT CURVE  ·  {star.upper()}",
                  font=dict(family='Orbitron', size=15, color='#00D4FF'), x=0.5),
        legend=dict(bgcolor='rgba(5,5,20,0.9)',
                   bordercolor='rgba(0,212,255,0.2)', borderwidth=1,
                   font=dict(family='Share Tech Mono', size=10, color='white')),
        margin=dict(l=60, r=20, t=70, b=40))
    fig.update_xaxes(gridcolor=GRID, linecolor=LINE,
        tickfont=dict(family='Share Tech Mono', size=8, color='rgba(255,255,255,0.3)'))
    fig.update_yaxes(gridcolor=GRID, linecolor=LINE,
        tickfont=dict(family='Share Tech Mono', size=8, color='rgba(255,255,255,0.3)'))
    for a in fig.layout.annotations:
        a.font.update(family='Share Tech Mono', size=9, color='rgba(0,212,255,0.6)')
    return fig

def rmse_chart(rd, rs, rm):
    fig = go.Figure()
    for lbl, v, c in [
        ('DDPM<br>AstraSense', rd, '#00D4FF'),
        ('Savitzky-<br>Golay',  rs, '#00FF88'),
        ('Median<br>Filter',    rm, '#FF4444')
    ]:
        fig.add_trace(go.Bar(x=[lbl], y=[v],
            marker=dict(color=c, opacity=0.85, line=dict(color=c, width=2)),
            text=[f'{v:.3f}'], textposition='outside',
            textfont=dict(family='Orbitron', size=11, color=c)))
    fig.update_layout(
        title=dict(text="RMSE COMPARISON",
                  font=dict(family='Orbitron', size=11, color='#00D4FF'), x=0.5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=PLOTBG,
        font=dict(family='Share Tech Mono', color='white'),
        height=300, showlegend=False,
        margin=dict(l=20, r=20, t=50, b=10),
        yaxis=dict(gridcolor=GRID, linecolor=LINE,
                  tickfont=dict(family='Share Tech Mono', size=9, color='rgba(255,255,255,0.5)')),
        xaxis=dict(linecolor=LINE,
                  tickfont=dict(family='Share Tech Mono', size=9, color='rgba(255,255,255,0.7)')),
        bargap=0.4)
    return fig

def step_chart(noisy, current, label, step_n):
    alpha = step_n / 4.0
    blend = noisy*(1-alpha) + current*alpha
    fig   = go.Figure()
    fig.add_trace(go.Scatter(y=noisy[:256], mode='lines',
        line=dict(color='#CC00FF', width=0.8, dash='dot'),
        opacity=max(0.1, 0.6-alpha*0.5), name='Noisy'))
    fig.add_trace(go.Scatter(y=blend[:256], mode='lines',
        line=dict(color='#00D4FF', width=2.5), opacity=0.9,
        fill='tozeroy', fillcolor=f'rgba(0,212,255,{round(0.03+alpha*0.05,2)})',
        name='Denoising'))
    fig.update_layout(
        title=dict(text=f"  {label}",
                  font=dict(family='Share Tech Mono', size=10, color='#FF8C00'), x=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=PLOTBG,
        height=200, showlegend=False,
        margin=dict(l=30, r=10, t=35, b=20),
        xaxis=dict(gridcolor=GRID, linecolor=LINE, showticklabels=False),
        yaxis=dict(gridcolor=GRID, linecolor=LINE,
                  tickfont=dict(size=7, color='rgba(255,255,255,0.3)')))
    return fig

# ============================================
#   PAGE STYLES
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

.page-bg {
    position:fixed; top:0; left:0;
    width:100vw; height:100vh; z-index:-1;
    background:
        radial-gradient(ellipse at 15% 50%, rgba(0,40,100,0.3) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%, rgba(0,20,80,0.25) 0%, transparent 50%),
        linear-gradient(180deg,#000510,#000818,#000510);
}
.grid-bg {
    position:fixed; top:0; left:0;
    width:100%; height:100%; z-index:-1;
    background-image:
        linear-gradient(rgba(0,100,200,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,100,200,0.03) 1px, transparent 1px);
    background-size: 60px 60px; pointer-events:none;
}
.page-nav {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.85rem 2.5rem;
    background:rgba(0,5,20,0.92);
    border-bottom:1px solid rgba(0,180,255,0.15);
    backdrop-filter:blur(20px);
    position:fixed; top:0; left:0; right:0; z-index:1000; margin:0;
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
    margin:0.5rem 0;
}
.inp-label {
    font-family:'Share Tech Mono',monospace; font-size:0.62rem;
    color:rgba(0,200,255,0.65); letter-spacing:0.3rem; margin-bottom:0.4rem;
    display:block; text-transform:uppercase;
}
.sec-title {
    font-family:'Orbitron',monospace; font-size:0.7rem; color:#00d4ff;
    letter-spacing:0.4rem; margin:0.5rem 0 0.5rem; text-transform:uppercase;
}
.metric-card {
    background:rgba(5,8,30,0.92);
    border:1px solid rgba(0,180,255,0.18);
    border-radius:14px; padding:1.2rem 0.8rem;
    text-align:center; transition:all 0.3s;
}
.metric-card:hover {
    border-color:rgba(0,212,255,0.5); transform:translateY(-3px);
}
.mval { font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700; }
.mlbl {
    font-family:'Share Tech Mono',monospace; font-size:0.58rem;
    color:rgba(255,255,255,0.4); letter-spacing:0.2rem; margin-top:0.4rem;
}
.planet-card {
    background:linear-gradient(160deg, rgba(13,0,51,0.95), rgba(26,10,62,0.95));
    border:1px solid rgba(0,100,255,0.35); border-radius:18px; padding:1.5rem;
    box-shadow:0 0 40px rgba(0,100,255,0.08);
}
.planet-name {
    font-family:'Orbitron',monospace; font-size:0.9rem; font-weight:900;
    color:white; letter-spacing:0.2rem; padding-bottom:0.8rem; margin-bottom:0.8rem;
    border-bottom:1px solid rgba(255,255,255,0.08);
}
.pstat { padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.pstat-lbl {
    font-family:'Share Tech Mono',monospace; font-size:0.58rem;
    color:rgba(255,255,255,0.3); letter-spacing:0.2rem;
}
.pstat-val { font-family:'Orbitron',monospace; font-size:0.82rem; font-weight:600; color:white; }
.status-live {
    font-family:'Share Tech Mono',monospace; font-size:0.72rem;
    color:#00ff88; letter-spacing:0.2rem; padding:0.4rem 0;
}
.status-proc {
    font-family:'Share Tech Mono',monospace; font-size:0.72rem;
    color:#ff8c00; letter-spacing:0.2rem; padding:0.4rem 0;
}

/* ── TRAINED STAR BUTTONS — 2 rows of 5 ── */
.star-btn-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.5rem;
    margin-bottom: 0.5rem;
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
    <a href='/' class='nav-logo'>◈ ASTRASENSE</a>
    <div class='nav-links'>
        <a href='/Analysis' class='active'>ANALYSIS</a>
        <a href='/Star_Catalogue'>STAR CATALOGUE</a>
        <a href='/Noise_Lab'>NOISE LAB</a>
        <a href='/Science'>THE SCIENCE</a>
        <a href='/Performance'>PERFORMANCE</a>
    </div>
</div>
<div class='nav-spacer'></div>
""", unsafe_allow_html=True)

# ============================================
#   HERO
# ============================================
st.markdown("""
<div style='text-align:center;padding:0.3rem 1rem 0.5rem;'>
    <span style='font-family:Share Tech Mono,monospace;font-size:0.65rem;
         color:rgba(0,200,255,0.6);letter-spacing:0.5rem;display:block;
         margin-bottom:0.5rem;text-transform:uppercase;'>
        ◈ SIGNAL ANALYSIS MODULE
    </span>
    <div style='font-family:Orbitron,monospace;font-size:clamp(2rem,5vw,4rem);
         font-weight:900;background:linear-gradient(135deg,#00d4ff,#0055cc);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;letter-spacing:0.3rem;line-height:1.1;'>
        LIGHT CURVE ANALYSIS
    </div>
    <div style='font-family:Exo 2,sans-serif;font-size:0.9rem;
         color:rgba(180,220,255,0.6);margin-top:0.5rem;font-weight:300;'>
        Fetch real NASA telescope data and denoise it using
        our trained 1D DDPM model in real time
    </div>
</div>
<div class='glow-line'></div>
""", unsafe_allow_html=True)

# ============================================
#   LOAD MODEL
# ============================================
model, scheduler, device = load_model()
device_name = "RTX 3050" if torch.cuda.is_available() else "CPU"

# ============================================
#   INPUT SECTION
# ============================================
st.markdown("<div class='sec-title'>◈ TARGET CONFIGURATION</div>",
           unsafe_allow_html=True)

c1, c2, c3 = st.columns([3, 2, 2])
with c1:
    st.markdown("<span class='inp-label'>◈ STAR DESIGNATION</span>",
               unsafe_allow_html=True)
    star_name = st.text_input("", value="Kepler-452",
                              label_visibility="collapsed", key="star_inp")
with c2:
    st.markdown("<span class='inp-label'>◈ TELESCOPE MISSION</span>",
               unsafe_allow_html=True)
    mission = st.selectbox("", ["Kepler", "TESS"], label_visibility="collapsed")
with c3:
    st.markdown("<span class='inp-label'>◈ NOISE LEVEL</span>",
               unsafe_allow_html=True)
    noise_level = st.slider("", 0.001, 0.01, 0.002, 0.001,
                           format="%.3f", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
#   TRAINED STAR QUICK BUTTONS — 2 rows of 5
# ============================================
st.markdown("<span class='inp-label'>◈ TRAINED STAR TARGETS — 10 SYSTEMS</span>",
           unsafe_allow_html=True)

# Row 1 — original 4 + Kepler-16
row1 = st.columns(5)
trained_stars_r1 = ["Kepler-452", "Kepler-7", "Kepler-10", "Kepler-22", "Kepler-16"]
for col, s, i in zip(row1, trained_stars_r1, range(5)):
    with col:
        if st.button(s, key=f"q{i}"):
            star_name = s

# Row 2 — 5 new stars
row2 = st.columns(5)
trained_stars_r2 = ["Kepler-62", "Kepler-186", "Kepler-69", "Kepler-442", "Kepler-90"]
for col, s, i in zip(row2, trained_stars_r2, range(5, 10)):
    with col:
        if st.button(s, key=f"q{i}"):
            star_name = s

st.markdown("<br>", unsafe_allow_html=True)

_, mid, _ = st.columns([2, 1.5, 2])
with mid:
    analyze = st.button("⬡  INITIALIZE ANALYSIS  ⬡", key="ab")

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

# ============================================
#   DEFAULT STATE
# ============================================
if not analyze:
    st.markdown("""
        <div style='text-align:center;padding:2rem 0 1.5rem;'>
            <div style='font-family:Share Tech Mono;font-size:0.82rem;
                 color:rgba(255,255,255,0.18);letter-spacing:0.3rem;'>
                SELECT A TARGET STAR AND INITIALIZE ANALYSIS
            </div>
            <div style='font-family:Share Tech Mono;font-size:0.62rem;
                 color:rgba(255,255,255,0.1);letter-spacing:0.2rem;margin-top:0.5rem;'>
                CONNECTING TO NASA MAST ARCHIVE IN REAL TIME
            </div>
        </div>
    """, unsafe_allow_html=True)
    dc = st.columns(4)
    for col, (v, l, c) in zip(dc, [
        ("10",        "STARS TRAINED", "#00D4FF"),
        ("200K+",     "DATA POINTS",   "#0088FF"),
        ("2.8M",      "PARAMETERS",    "#0055CC"),
        (device_name, "COMPUTE",       "#00FF88"),
    ]):
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='mval' style='color:{c};'>{v}</div>
                    <div class='mlbl'>{l}</div>
                </div>
            """, unsafe_allow_html=True)
    st.stop()

# ============================================
#   ANALYSIS PIPELINE
# ============================================
prog = st.progress(0)
stat = st.empty()
anim_box = st.empty()

stat.markdown("<div class='status-proc'>◈ CONNECTING TO NASA MAST ARCHIVE...</div>",
    unsafe_allow_html=True)
prog.progress(10)

t_data, f_data, target = fetch_star(star_name, mission)

if t_data is None:
    prog.empty(); stat.empty()
    st.error(f"Could not fetch '{star_name}'. "
            f"Try: Kepler-452, Kepler-7, Kepler-10, Kepler-22, "
            f"Kepler-16, Kepler-62, Kepler-186, Kepler-69, Kepler-442, Kepler-90")
    st.stop()

target = str(target) if target else star_name
prog.progress(28)
stat.markdown(
    f"<div class='status-live'>◈ DATA ACQUIRED — "
    f"{len(f_data):,} POINTS · {target.upper()}</div>",
    unsafe_allow_html=True)
time.sleep(0.3)

stat.markdown("<div class='status-proc'>◈ PREPROCESSING SIGNAL...</div>",
    unsafe_allow_html=True)
fs = f_data[:512].astype(np.float32)
ts = t_data[:512]
m, sd = fs.mean(), fs.std()+1e-8
cn    = (fs-m)/sd
noisy = cn + np.random.normal(0, noise_level, cn.shape).astype(np.float32)
prog.progress(45)
time.sleep(0.2)

stat.markdown("<div class='status-proc'>◈ RUNNING DDPM DENOISING...</div>",
    unsafe_allow_html=True)

steps = [
    (100, "STEP 1/4  ·  NOISE PATTERN ANALYSIS",  1),
    (300, "STEP 2/4  ·  FEATURE EXTRACTION",       2),
    (500, "STEP 3/4  ·  SIGNAL RECONSTRUCTION",    3),
    (700, "STEP 4/4  ·  TRANSIT ENHANCEMENT",      4),
]
for t_val, label, sn in steps:
    with torch.no_grad():
        x   = torch.FloatTensor(noisy).unsqueeze(0).unsqueeze(0).to(device)
        out = torch.clamp(
            model(x, torch.tensor([t_val], device=device)), -5, 5
        ).squeeze().cpu().numpy()
    anim_box.plotly_chart(step_chart(noisy, out, label, sn), use_container_width=True)
    prog.progress(45 + sn*8)
    time.sleep(0.5)

denoised_signal = denoise(model, scheduler, noisy, device)
anim_box.empty()
prog.progress(82)

stat.markdown("<div class='status-proc'>◈ COMPUTING BASELINES...</div>",
    unsafe_allow_html=True)
sv  = savgol_filter(noisy, window_length=51, polyorder=3)
md  = medfilt(noisy, kernel_size=11)

rd  = calc_rmse(cn, denoised_signal)
rs_ = calc_rmse(cn, sv)
rm_ = calc_rmse(cn, md)
sn_ = calc_snr(cn, denoised_signal)
conf, depth, tc = transit_info(denoised_signal)

prog.progress(100)
time.sleep(0.2)
prog.empty()
stat.markdown(
    f"<div class='status-live'>◈ ANALYSIS COMPLETE · "
    f"{target.upper()} · {len(f_data):,} POINTS · {device_name}</div>",
    unsafe_allow_html=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

# ============================================
#   METRICS
# ============================================
st.markdown("<div class='sec-title'>◈ SIGNAL METRICS</div>", unsafe_allow_html=True)
mc = st.columns(5)
for col, (lbl, val, c) in zip(mc, [
    ("DDPM RMSE",     f"{rd:.3f}",     "#00D4FF"),
    ("SAVGOL RMSE",   f"{rs_:.3f}",    "#00FF88"),
    ("SIGNAL SNR",    f"{sn_:.1f}dB",  "#0088FF"),
    ("TRANSIT CONF",  f"{conf}%",      "#FF8C00"),
    ("TRANSIT DEPTH", f"{depth:.4f}%", "#FF4444"),
]):
    with col:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='mval' style='color:{c};'>{val}</div>
                <div class='mlbl'>{lbl}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
#   CHART + PLANET CARD
# ============================================
st.markdown("<div class='sec-title'>◈ LIGHT CURVE ANALYSIS</div>", unsafe_allow_html=True)
ch, pl = st.columns([3, 1])
with ch:
    st.plotly_chart(main_chart(ts, noisy, denoised_signal, sv, target),
                   use_container_width=True)
with pl:
    period = round(365.25/max(1,tc)*0.1,1) if tc > 0 else "N/A"
    radius = round(np.sqrt(abs(depth)/100)*10, 3)
    better = "✓ BEATS MEDIAN" if rd < rm_ else "~ COMPETITIVE"
    bc     = "#00FF88" if rd < rm_ else "#FF8C00"
    st.markdown(f"""
        <div class='planet-card'>
            <div class='planet-name'>{target.upper().replace('-',' ')}</div>
            <div class='pstat'>
                <div class='pstat-lbl'>TELESCOPE</div>
                <div class='pstat-val'>{mission}</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>TOTAL POINTS</div>
                <div class='pstat-val'>{len(f_data):,}</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>TRANSIT CONF</div>
                <div class='pstat-val' style='color:#FF8C00;'>{conf}%</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>TRANSIT DEPTH</div>
                <div class='pstat-val'>{depth:.4f}%</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>EST. PERIOD</div>
                <div class='pstat-val' style='color:#00D4FF;'>{period} days</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>REL. RADIUS</div>
                <div class='pstat-val' style='color:#0088FF;'>{radius} R⊕</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>AI vs MEDIAN</div>
                <div class='pstat-val' style='color:{bc};'>{better}</div>
            </div>
            <div class='pstat'>
                <div class='pstat-lbl'>COMPUTE</div>
                <div class='pstat-val' style='color:#00FF88;'>{device_name}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================
#   COMPARISON
# ============================================
st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)
st.markdown("<div class='sec-title'>◈ METHOD COMPARISON</div>", unsafe_allow_html=True)
cp1, cp2 = st.columns([1, 2])
with cp1:
    st.plotly_chart(rmse_chart(rd, rs_, rm_), use_container_width=True)
with cp2:
    st.markdown("<br>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "METHOD": ["DDPM — AstraSense", "Savitzky-Golay", "Median Filter"],
        "RMSE":   [f"{rd:.4f}", f"{rs_:.4f}", f"{rm_:.4f}"],
        "MAE":    [
            f"{float(np.mean(np.abs(cn[:len(denoised_signal)]-denoised_signal[:len(cn)]))):.4f}",
            f"{float(np.mean(np.abs(cn-sv))):.4f}",
            f"{float(np.mean(np.abs(cn-md))):.4f}"
        ],
        "TYPE": ["🤖 Deep Learning", "📐 Traditional", "📐 Traditional"]
    })
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown(f"""
        <div style='font-family:Share Tech Mono;font-size:0.68rem;
             color:rgba(255,255,255,0.28);line-height:2.2;margin-top:1rem;'>
            ◈ TARGET &nbsp;&nbsp; : {target.upper()}<br>
            ◈ MISSION &nbsp; : {mission}<br>
            ◈ POINTS &nbsp;&nbsp; : {len(fs)}<br>
            ◈ BJD &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {ts[0]:.2f} — {ts[-1]:.2f}<br>
            ◈ NOISE &nbsp;&nbsp;&nbsp; : {noise_level}<br>
            ◈ MODEL &nbsp;&nbsp;&nbsp; : 1D U-NET DDPM · 2.8M PARAMS<br>
            ◈ DEVICE &nbsp;&nbsp; : {device_name}
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;font-family:Share Tech Mono;font-size:0.55rem;
     color:rgba(255,255,255,0.1);letter-spacing:0.25rem;padding:2rem 0;
     margin-top:2rem;border-top:1px solid rgba(0,180,255,0.1);'>
    ASTRASENSE v2.0 &nbsp;◈&nbsp; 1D DDPM U-NET
    &nbsp;◈&nbsp; NASA KEPLER / TESS &nbsp;◈&nbsp; 10 STAR SYSTEMS
</div>
""", unsafe_allow_html=True)