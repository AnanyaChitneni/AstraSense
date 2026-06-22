import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal as scipy_signal
import sys, os, base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="AstraSense — Noise Lab",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def img_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bg_b64   = img_b64(os.path.join(BASE_DIR, "assets", "noiselab_bg.jpg"))
bg_src   = f"data:image/jpeg;base64,{bg_b64}" if bg_b64 else ""

st.markdown(f"""
<style>
html, body {{
    background-color: #000408 !important;
    background-image:
        radial-gradient(ellipse at 15% 50%, rgba(0,20,70,0.55) 0%, transparent 60%),
        radial-gradient(ellipse at 85% 20%, rgba(0,15,55,0.45) 0%, transparent 55%),
        url("{bg_src}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stAppViewBlockContainer"],
.main, section.main, .block-container {{
    background: transparent !important;
    background-color: transparent !important;
}}
.page-bg {{
    position:fixed; top:0; left:0;
    width:100vw; height:100vh; z-index:-2;
    background-image:
        radial-gradient(ellipse at 15% 50%, rgba(0,20,70,0.55) 0%, transparent 60%),
        radial-gradient(ellipse at 85% 20%, rgba(0,15,55,0.45) 0%, transparent 55%),
        url("{bg_src}");
    background-size:cover; background-position:center;
    background-attachment:fixed;
}}
.content-overlay {{
    position:fixed; top:52px; left:0; right:0; bottom:0; z-index:0;
    background:rgba(0,2,12,0.84);
    backdrop-filter:blur(4px);
    pointer-events:none;
}}
.main .block-container,
[data-testid="stAppViewBlockContainer"] {{ position:relative; z-index:1; }}
</style>
<div class='page-bg'></div>
<div class='content-overlay'></div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],[data-testid="stSidebar"],
[data-testid="stSidebarNav"],[data-testid="stHeader"],
[data-testid="stDecoration"],section[data-testid="stSidebar"] {
    display:none !important; visibility:hidden !important; height:0 !important;
}
.main > div:first-child { padding-top:0 !important; }
.main .block-container {
    padding-top:0 !important;
    padding-bottom:2rem !important;
    padding-left:0.6rem !important;
    padding-right:0.6rem !important;
    max-width:100% !important;
    margin:0 !important;
}

.stSlider > div > div > div {
    background:rgba(0,60,120,0.3) !important; height:2px !important;
}
.stSlider > div > div > div > div {
    background:#00d4ff !important; height:2px !important;
}
.stSlider > div > div > div > div > div {
    background:#00d4ff !important;
    border:2px solid rgba(0,220,255,0.65) !important;
    width:12px !important; height:12px !important;
    box-shadow:0 0 8px rgba(0,212,255,0.5) !important;
}
[data-testid="stThumbValue"] { display:none !important; }
[data-testid="stTickBarMin"],[data-testid="stTickBarMax"] {
    color:rgba(0,150,220,0.35) !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:0.46rem !important;
}

div[data-baseweb="select"] > div {
    background:rgba(0,5,22,0.97) !important;
    border:1px solid rgba(0,120,200,0.28) !important;
    border-radius:10px !important;
    color:rgba(160,215,255,0.85) !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:0.72rem !important;
}

.stNumberInput input {
    background:rgba(0,5,22,0.97) !important;
    border:1px solid rgba(0,120,200,0.28) !important;
    color:rgba(160,215,255,0.85) !important;
    font-family:'Share Tech Mono',monospace !important;
    border-radius:10px !important; font-size:0.72rem !important;
}

::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:#000408; }
::-webkit-scrollbar-thumb { background:linear-gradient(#00d4ff,#0044aa); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

BG    = 'rgba(0,4,20,0.97)'
GRID  = 'rgba(0,80,160,0.07)'
GLINE = 'rgba(0,140,230,0.13)'

C = {
    'clean'   : '#00E5AA',
    'noisy'   : '#38BDF8',
    'residual': '#FBBF24',
    'photon'  : '#00D4FF',
    'stellar' : '#A78BFA',
    'instr'   : '#34D399',
    'cosmic'  : '#FB923C',
    'sys'     : '#F472B6',
    'ok'      : '#00E5AA',
    'mid'     : '#FBBF24',
    'bad'     : '#F87171',
}

def _base(h, title=""):
    d = dict(
        height=h, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=BG,
        font=dict(family='Share Tech Mono', color='rgba(110,175,235,0.4)', size=7),
        margin=dict(l=46, r=14, t=38 if title else 8, b=28))
    if title:
        d['title'] = dict(text=title,
                          font=dict(family='Orbitron', size=10, color='#00D4FF'),
                          x=0, xanchor='left', pad=dict(l=5))
    return d

def _ax(label=""):
    d = dict(gridcolor=GRID, linecolor=GLINE, zeroline=False,
             tickfont=dict(family='Share Tech Mono', size=7,
                           color='rgba(110,175,235,0.38)'), showgrid=True)
    if label:
        d['title'] = dict(text=label, font=dict(
            family='Share Tech Mono', size=7, color='rgba(0,175,235,0.42)'))
    return d

def _legend():
    return dict(font=dict(family='Share Tech Mono', size=8,
                           color='rgba(180,220,255,0.7)'),
                bgcolor='rgba(0,4,20,0.92)',
                bordercolor='rgba(0,130,200,0.18)', borderwidth=1)

def make_clean(t, depth):
    f = np.ones_like(t)
    t0, dur = 5.0, 0.5
    for i in range(len(t)):
        if abs(t[i]-t0) < dur/2:
            ph = (t[i]-t0)/(dur/2)
            f[i] = 1.0 - depth*(1-ph**2)**0.5
    f += 0.0008*np.sin(2*np.pi*t/8.5+0.3)
    f += 0.0004*np.sin(2*np.pi*t/3.2+1.1)
    return f

def make_noisy(flux, t, nl, sv, ins, cr, sy, ntype, seed):
    np.random.seed(seed); n = flux.copy(); L = len(t)
    if   ntype == "Gaussian": n += np.random.normal(0, nl*0.003, L)
    elif ntype == "Poisson" : n += np.random.poisson(nl*10,L)*0.0001 - nl*0.001
    elif ntype == "Pink 1/f":
        w=np.random.randn(L); ff=np.fft.rfft(w)
        fr=np.fft.rfftfreq(L); fr[0]=1e-10; ff/=np.sqrt(fr)
        n += np.fft.irfft(ff,L)*nl*0.002
    elif ntype == "Shot"    : n += np.random.exponential(nl*0.002,L)-nl*0.002
    n += sv*0.002*np.sin(2*np.pi*t/6.3+0.7)
    n += np.random.normal(0, ins*0.001, L)
    k = int(cr*5)
    if k:
        idx = np.random.choice(L, k, replace=False)
        n[idx] += np.random.exponential(0.005, k)
    n += sy*0.001*np.polyval(np.random.randn(3)*0.1, t/t[-1])
    return n

def decompose(t, nl, sv, ins, cr, sy, seed):
    np.random.seed(seed); L = len(t)
    cosmic = np.zeros(L)
    k = int(cr*5)
    if k:
        idx = np.random.choice(L, k, replace=False)
        cosmic[idx] = np.random.exponential(0.005, k)
    return {
        'Photon':      np.random.normal(0, nl*0.003, L),
        'Stellar Var': sv*0.002*np.sin(2*np.pi*t/6.3+0.7),
        'Instrument':  np.random.normal(0, ins*0.001, L),
        'Cosmic Ray':  cosmic,
        'Systematics': sy*0.001*np.polyval(np.random.randn(3)*0.1, t/t[-1]),
    }

def fig_comparison(t, clean, noisy):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04,
                        subplot_titles=['CLEAN SIGNAL', 'NOISY SIGNAL'])
    fig.add_trace(go.Scatter(x=t, y=clean, mode='lines', name='Clean',
        line=dict(color=C['clean'], width=1.5),
        fill='tozeroy', fillcolor='rgba(0,229,170,0.05)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=noisy, mode='lines', name='Noisy',
        line=dict(color=C['noisy'], width=0.9),
        fill='tozeroy', fillcolor='rgba(56,189,248,0.04)'), row=2, col=1)
    lay = _base(300, '◈ SIGNAL COMPARISON')
    lay.update(showlegend=False,
               xaxis=_ax(), xaxis2=_ax('TIME (DAYS)'),
               yaxis=_ax('FLUX'), yaxis2=_ax('FLUX'))
    for a in ['xaxis','xaxis2','yaxis','yaxis2']:
        fig.layout[a].update(**_ax())
    fig.layout['xaxis2'].update(title=dict(text='TIME (DAYS)',
        font=dict(family='Share Tech Mono', size=7, color='rgba(0,175,235,0.42)')))
    fig.update_layout(**lay)
    for ann in fig.layout.annotations:
        ann.font.update(family='Share Tech Mono', size=8,
                        color='rgba(0,195,255,0.45)')
    return fig

def fig_residual(t, clean, noisy):
    res = noisy - clean
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=res, mode='lines', name='Residual',
        line=dict(color=C['residual'], width=0.9),
        fill='tozeroy', fillcolor='rgba(251,191,36,0.04)'))
    fig.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.09)')
    lay = _base(220, '◈ NOISE RESIDUAL  (NOISY − CLEAN)')
    lay.update(showlegend=False, xaxis=_ax('TIME (DAYS)'), yaxis=_ax('RESIDUAL'))
    fig.update_layout(**lay)
    return fig

def fig_psd(clean, noisy, dt):
    fc, pc = scipy_signal.welch(clean, fs=1/dt, nperseg=128)
    fn, pn = scipy_signal.welch(noisy, fs=1/dt, nperseg=128)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fc[1:], y=pc[1:], mode='lines', name='Clean',
        line=dict(color=C['clean'], width=1.4),
        fill='tozeroy', fillcolor='rgba(0,229,170,0.04)'))
    fig.add_trace(go.Scatter(x=fn[1:], y=pn[1:], mode='lines', name='Noisy',
        line=dict(color=C['noisy'], width=0.9),
        fill='tozeroy', fillcolor='rgba(56,189,248,0.03)'))
    lay = _base(220, '◈ POWER SPECTRAL DENSITY')
    xd = {**_ax('FREQ (1/DAY)'), 'type': 'log'}
    yd = {**_ax('POWER'),        'type': 'log'}
    lay.update(xaxis=xd, yaxis=yd, legend=_legend())
    fig.update_layout(**lay)
    return fig

def fig_histogram(clean, noisy):
    res = noisy - clean
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=res, nbinsx=55, name='Distribution',
        marker=dict(color='rgba(56,189,248,0.52)',
                    line=dict(color='rgba(0,212,255,0.2)', width=0.4))))
    lay = _base(220, '◈ NOISE DISTRIBUTION')
    lay.update(showlegend=False,
               xaxis=_ax('RESIDUALS'), yaxis=_ax('COUNT'))
    fig.update_layout(**lay)
    return fig

def fig_snr(snr_val):
    col = C['ok'] if snr_val>10 else C['mid'] if snr_val>5 else C['bad']
    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=max(0, snr_val),
        delta=dict(reference=10,
                   font=dict(family='Share Tech Mono', size=10)),
        number=dict(font=dict(family='Orbitron', size=24, color=col),
                    suffix=' dB'),
        gauge=dict(
            axis=dict(range=[0,30],
                      tickfont=dict(family='Share Tech Mono', size=7,
                                    color='rgba(110,175,235,0.38)')),
            bar=dict(color=col, thickness=0.25),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,130,200,0.18)',
            steps=[dict(range=[0,5],   color='rgba(248,113,113,0.08)'),
                   dict(range=[5,10],  color='rgba(251,191,36,0.08)'),
                   dict(range=[10,30], color='rgba(0,229,170,0.08)')],
            threshold=dict(line=dict(color=col, width=2.5),
                           thickness=0.78, value=max(0, snr_val))),
        title=dict(text='SNR',
                   font=dict(family='Orbitron', size=12,
                             color='rgba(0,200,255,0.6)'))))
    fig.update_layout(height=230, paper_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='white'),
                      margin=dict(l=20, r=20, t=30, b=5))
    return fig

def fig_transit(rp, impact, depth):
    tx = np.linspace(-0.5, 0.5, 600)
    dur = 0.5*np.sqrt(max(0, 1-impact**2))
    fy  = np.ones_like(tx)
    for i in range(len(tx)):
        if abs(tx[i]) < dur/2:
            ph = tx[i]/(dur/2)
            fy[i] = 1.0 - depth*(1-0.3*(1-np.sqrt(max(0, 1-ph**2))))
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=1-depth,
                  fillcolor='rgba(56,189,248,0.04)', line_width=0)
    fig.add_trace(go.Scatter(x=tx, y=fy, mode='lines',
        line=dict(color=C['noisy'], width=2.2),
        fill='tozeroy', fillcolor='rgba(56,189,248,0.04)'))
    fig.add_hline(y=1-depth, line_dash='dot',
                  line_color='rgba(251,191,36,0.5)',
                  annotation_text=f"depth  {depth*100:.3f}%",
                  annotation_font=dict(family='Share Tech Mono',
                                       size=8, color=C['residual']))
    lay = _base(240, '◈ TRANSIT SHAPE MODEL')
    lay.update(showlegend=False,
               xaxis=_ax('ORBITAL PHASE'), yaxis=_ax('RELATIVE FLUX'))
    fig.update_layout(**lay)
    return fig

def fig_component(data, label, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data, mode='lines',
        line=dict(color=color, width=1.1),
        fill='tozeroy', fillcolor='rgba(0,180,255,0.03)'))
    lay = _base(118)
    lay.update(showlegend=False,
               title=dict(text=label,
                          font=dict(family='Share Tech Mono', size=8, color=color),
                          x=0, xanchor='left', pad=dict(l=4)),
               xaxis={**_ax(), 'showticklabels': False},
               yaxis=_ax(),
               margin=dict(l=30, r=6, t=28, b=6))
    fig.update_layout(**lay)
    return fig

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

.page-nav {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.85rem 2.5rem;
    background:rgba(0,4,16,0.97);
    border-bottom:1px solid rgba(0,130,220,0.15);
    backdrop-filter:blur(20px);
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
    background:linear-gradient(90deg,transparent,rgba(0,180,255,0.38),transparent);
    margin:0.7rem 0;
}
.sec-title {
    font-family:'Orbitron',monospace; font-size:0.68rem;
    color:#00d4ff; letter-spacing:0.38rem;
    margin:0.8rem 0 0.6rem; text-transform:uppercase;
}
.sec-title::before { content:'◈ '; color:rgba(0,200,255,0.5); font-size:0.6rem; }

.control-panel {
    background:rgba(0,4,20,0.96);
    border:1px solid rgba(0,120,200,0.2);
    border-radius:18px;
    padding:1.4rem 1.6rem 1.2rem;
    margin-bottom:0.8rem;
}
.cp-row { display:grid; gap:1.2rem; align-items:start; }
.cp-5  { grid-template-columns:repeat(5,1fr); }
.cp-6  { grid-template-columns:repeat(6,1fr); }
.cp-3  { grid-template-columns:repeat(3,1fr); }
.cp-section {
    font-family:'Share Tech Mono',monospace; font-size:0.52rem;
    color:rgba(0,170,230,0.45); letter-spacing:0.3rem;
    text-transform:uppercase;
    border-bottom:1px solid rgba(0,100,170,0.13);
    padding-bottom:0.3rem;
    margin-bottom:0.9rem;
    margin-top:0;
}
.sl-lbl {
    font-family:'Share Tech Mono',monospace; font-size:0.52rem;
    color:rgba(110,175,235,0.5); letter-spacing:0.16rem;
    text-transform:uppercase; display:block; margin-bottom:0;
}

.chips-row {
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:0.6rem; margin-bottom:0.8rem;
}
.chip {
    background:rgba(0,4,20,0.97);
    border:1px solid rgba(0,120,200,0.2);
    border-radius:14px; padding:0.8rem 0.5rem;
    text-align:center; transition:border-color 0.3s;
}
.chip:hover { border-color:rgba(0,200,255,0.38); }
.chip-v {
    font-family:'Orbitron',monospace;
    font-size:1.05rem; font-weight:700; line-height:1.1; display:block;
}
.chip-l {
    font-family:'Share Tech Mono',monospace; font-size:0.44rem;
    color:rgba(110,175,235,0.45); letter-spacing:0.1rem;
    margin-top:0.22rem; text-transform:uppercase; display:block;
}

.derived {
    background:rgba(0,4,20,0.97);
    border:1px solid rgba(0,120,200,0.2);
    border-radius:14px; padding:1rem 0.9rem;
}
.d-title {
    font-family:'Orbitron',monospace; font-size:0.56rem;
    color:#00d4ff; letter-spacing:0.28rem; text-transform:uppercase;
    border-bottom:1px solid rgba(0,100,170,0.12);
    padding-bottom:0.38rem; margin-bottom:0.6rem;
}
.d-row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:0.28rem 0; border-bottom:1px solid rgba(0,65,120,0.09);
}
.d-row:last-child { border-bottom:none; }
.d-l {
    font-family:'Share Tech Mono',monospace; font-size:0.5rem;
    color:rgba(110,175,235,0.45); letter-spacing:0.12rem; text-transform:uppercase;
}
.d-v { font-family:'Orbitron',monospace; font-size:0.7rem; font-weight:600; }

.comp-title {
    font-family:'Share Tech Mono',monospace; font-size:0.54rem;
    letter-spacing:0.18rem; text-transform:uppercase; display:block;
    margin-bottom:0.15rem;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .page-nav { padding: 0.7rem 1rem !important; }
    .nav-links { display: none !important; }
    .control-panel { padding: 1rem 0.8rem !important; }
    .cp-5 { grid-template-columns: repeat(2, 1fr) !important; }
    .cp-6 { grid-template-columns: repeat(2, 1fr) !important; }
    .chips-row { grid-template-columns: repeat(2, 1fr) !important; }
    .chip-v { font-size: 0.85rem !important; }
    .derived { padding: 0.8rem 0.7rem !important; }
}
@media (max-width: 480px) {
    .cp-5 { grid-template-columns: 1fr !important; }
    .cp-6 { grid-template-columns: 1fr !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='page-nav'>
    <a href='/' class='nav-logo' target="_self">◈ ASTRASENSE</a>
    <div class='nav-links'>
        <a href='/Analysis' target="_self">ANALYSIS</a>
        <a href='/Star_Catalogue' target="_self">STAR CATALOGUE</a>
        <a href='/Noise_Lab' class='active' target="_self">NOISE LAB</a>
        <a href='/Science' target="_self">THE SCIENCE</a>
        <a href='/Performance' target="_self">PERFORMANCE</a>
    </div>
</div>
<div class='nav-spacer'></div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:0.5rem 1rem 0.7rem;'>
    <span style='font-family:Share Tech Mono,monospace;font-size:0.6rem;
         color:rgba(0,170,230,0.5);letter-spacing:0.5rem;
         display:block;margin-bottom:0.5rem;text-transform:uppercase;'>
        ◈ INTERACTIVE SIMULATION
    </span>
    <div style='font-family:Orbitron,monospace;
         font-size:clamp(1.7rem,3.8vw,3rem);font-weight:900;
         background:linear-gradient(135deg,#00d4ff,#0055cc);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;letter-spacing:0.3rem;line-height:1.1;'>
        NOISE SIMULATION LAB
    </div>
    <div style='font-family:Exo 2,sans-serif;font-size:0.85rem;
         color:rgba(130,195,255,0.5);margin-top:0.45rem;font-weight:300;'>
        Configure noise parameters above — all charts update instantly below
    </div>
</div>
<div class='glow-line'></div>
""", unsafe_allow_html=True)

st.markdown("<div class='control-panel'>", unsafe_allow_html=True)

st.markdown("<div class='cp-section'>NOISE COMPONENTS</div>", unsafe_allow_html=True)
st.markdown("<div class='cp-row cp-5'>", unsafe_allow_html=True)

A1, A2, A3, A4, A5 = st.columns(5)
with A1:
    st.markdown("<span class='sl-lbl'>NOISE LEVEL</span>", unsafe_allow_html=True)
    nl = st.slider("", 0.1, 2.0, 0.5, 0.05, format="%.2f", key="nl", label_visibility="collapsed")
with A2:
    st.markdown("<span class='sl-lbl'>STELLAR VAR.</span>", unsafe_allow_html=True)
    sv = st.slider("", 0.0, 1.0, 0.3, 0.05, format="%.2f", key="sv", label_visibility="collapsed")
with A3:
    st.markdown("<span class='sl-lbl'>INSTRUMENT</span>", unsafe_allow_html=True)
    ins = st.slider("", 0.0, 1.0, 0.4, 0.05, format="%.2f", key="ins", label_visibility="collapsed")
with A4:
    st.markdown("<span class='sl-lbl'>COSMIC RAYS</span>", unsafe_allow_html=True)
    cr = st.slider("", 0.0, 1.0, 0.2, 0.05, format="%.2f", key="cr", label_visibility="collapsed")
with A5:
    st.markdown("<span class='sl-lbl'>SYSTEMATICS</span>", unsafe_allow_html=True)
    sy = st.slider("", 0.0, 1.0, 0.3, 0.05, format="%.2f", key="sy", label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='cp-section' style='margin-top:0.9rem;'>TRANSIT PARAMETERS &amp; CONFIGURATION</div>",
            unsafe_allow_html=True)

B1, B2, B3, B4, B5, B6 = st.columns(6)
with B1:
    st.markdown("<span class='sl-lbl'>Rp / Rs RATIO</span>", unsafe_allow_html=True)
    rp = st.slider("", 0.01, 0.20, 0.10, 0.005, format="%.3f", key="rp", label_visibility="collapsed")
with B2:
    st.markdown("<span class='sl-lbl'>IMPACT PARAM</span>", unsafe_allow_html=True)
    imp = st.slider("", 0.00, 0.90, 0.00, 0.05, format="%.2f", key="imp", label_visibility="collapsed")
with B3:
    st.markdown("<span class='sl-lbl'>TRANSIT DEPTH</span>", unsafe_allow_html=True)
    tdep = st.slider("", 0.001, 0.05, 0.01, 0.001, format="%.3f", key="tdep", label_visibility="collapsed")
with B4:
    st.markdown("<span class='sl-lbl'>NOISE TYPE</span>", unsafe_allow_html=True)
    ntype = st.selectbox("", ["Gaussian", "Poisson", "Pink 1/f", "Shot"], label_visibility="collapsed", key="ntype")
with B5:
    st.markdown("<span class='sl-lbl'>TARGET STAR</span>", unsafe_allow_html=True)
    star = st.selectbox("",
        ["Kepler-452","Kepler-7","Kepler-10","Kepler-22",
         "Kepler-16","Kepler-62","Kepler-186","Kepler-69",
         "Kepler-442","Kepler-90"],
        label_visibility="collapsed", key="star")
with B6:
    st.markdown("<span class='sl-lbl'>RANDOM SEED</span>", unsafe_allow_html=True)
    seed = st.number_input("", 0, 9999, 42, label_visibility="collapsed", key="seed")

st.markdown("</div>", unsafe_allow_html=True)

t      = np.linspace(0, 10, 1000)
dt     = t[1] - t[0]
clean  = make_clean(t, tdep)
noisy  = make_noisy(clean, t, nl, sv, ins, cr, sy, ntype, int(seed))
res    = noisy - clean
snr    = float(10*np.log10(np.mean(clean**2)/(np.mean(res**2)+1e-10)))
rms    = float(np.std(res)*1e6)
peak   = float(np.max(np.abs(res))*1e6)
comps  = decompose(t, nl, sv, ins, cr, sy, int(seed))

snr_c = C['ok'] if snr>10 else C['mid'] if snr>5 else C['bad']
st.markdown(f"""
<div class='chips-row'>
    <div class='chip'>
        <span class='chip-v' style='color:{snr_c};'>{snr:.1f} dB</span>
        <span class='chip-l'>SIGNAL-TO-NOISE</span>
    </div>
    <div class='chip'>
        <span class='chip-v' style='color:{C['noisy']};'>{rms:.0f} ppm</span>
        <span class='chip-l'>RMS NOISE</span>
    </div>
    <div class='chip'>
        <span class='chip-v' style='color:{C['residual']};'>{peak:.0f} ppm</span>
        <span class='chip-l'>PEAK NOISE</span>
    </div>
    <div class='chip'>
        <span class='chip-v' style='color:{C['stellar']};'>{tdep*100:.2f}%</span>
        <span class='chip-l'>TRANSIT DEPTH</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

st.markdown("<div class='sec-title'>SIGNAL COMPARISON</div>", unsafe_allow_html=True)
st.plotly_chart(fig_comparison(t, clean, noisy), use_container_width=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

st.markdown("<div class='sec-title'>SPECTRAL &amp; STATISTICAL ANALYSIS</div>", unsafe_allow_html=True)
R2a, R2b, R2c = st.columns(3)
with R2a:
    st.plotly_chart(fig_residual(t, clean, noisy), use_container_width=True)
with R2b:
    st.plotly_chart(fig_psd(clean, noisy, dt), use_container_width=True)
with R2c:
    st.plotly_chart(fig_histogram(clean, noisy), use_container_width=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

st.markdown("<div class='sec-title'>TRANSIT MODEL &amp; DIAGNOSTICS</div>", unsafe_allow_html=True)
R3a, R3b, R3c = st.columns([1.6, 0.9, 0.9])
with R3a:
    st.plotly_chart(fig_transit(rp, imp, tdep), use_container_width=True)
with R3b:
    pr  = rp*10; fd = rp**2*1e6; dur = abs(imp-1)*8
    st.markdown(f"""
    <div class='derived'>
        <div class='d-title'>DERIVED PARAMS</div>
        <div class='d-row'><span class='d-l'>PLANET RADIUS</span><span class='d-v' style='color:white;'>{pr:.2f} R⊕</span></div>
        <div class='d-row'><span class='d-l'>FLUX DROP</span><span class='d-v' style='color:{C['noisy']};'>{fd:.0f} ppm</span></div>
        <div class='d-row'><span class='d-l'>DURATION</span><span class='d-v' style='color:{C['clean']};'>~{dur:.1f} hrs</span></div>
        <div class='d-row'><span class='d-l'>IMPACT b</span><span class='d-v' style='color:{C['residual']};'>{imp:.2f}</span></div>
        <div class='d-row'><span class='d-l'>NOISE TYPE</span><span class='d-v' style='color:{C['stellar']};font-size:0.6rem;'>{ntype}</span></div>
        <div class='d-row'><span class='d-l'>STAR</span><span class='d-v' style='color:rgba(160,215,255,0.85);font-size:0.58rem;'>{star}</span></div>
        <div class='d-row'><span class='d-l'>Rp / Rs</span><span class='d-v' style='color:{C['cosmic']};'>{rp:.3f}</span></div>
    </div>
    """, unsafe_allow_html=True)
with R3c:
    st.plotly_chart(fig_snr(snr), use_container_width=True)

st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)

st.markdown("<div class='sec-title'>NOISE COMPONENTS BREAKDOWN</div>", unsafe_allow_html=True)
comp_colors = [C['photon'], C['stellar'], C['instr'], C['cosmic'], C['sys']]
comp_cols   = st.columns(5)
for col, (name, data), color in zip(comp_cols, comps.items(), comp_colors):
    with col:
        st.markdown(f"<span class='comp-title' style='color:{color};'>{name}</span>", unsafe_allow_html=True)
        st.plotly_chart(fig_component(data, name, color), use_container_width=True)

st.markdown("""
<div style='text-align:center;font-family:Share Tech Mono;font-size:0.5rem;
     color:rgba(80,130,190,0.18);letter-spacing:0.25rem;
     padding:1.5rem 0 1rem;border-top:1px solid rgba(0,100,180,0.08);
     margin-top:1rem;'>
    ASTRASENSE v2.0 &nbsp;◈&nbsp; NOISE SIMULATION LAB
    &nbsp;◈&nbsp; REAL-TIME SIGNAL PROCESSING
</div>
""", unsafe_allow_html=True)