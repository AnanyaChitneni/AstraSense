import streamlit as st
import sys, os, base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="AstraSense",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="stAppViewContainer"] {
    background: #000510 !important;
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stIFrame"] iframe {
    display: block !important;
    border: none !important;
    margin: 0 !important;
}
.stMainBlockContainer { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

def load_video_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

video_b64 = load_video_b64("assets/hero_video.mp4")
video_src = f"data:video/mp4;base64,{video_b64}" if video_b64 else ""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AstraSense</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{
    width:100%; background:#000510;
    overflow-x:hidden; scroll-behavior:smooth;
}}
::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-track {{ background:#000510; }}
::-webkit-scrollbar-thumb {{
    background:linear-gradient(#00d4ff,#0044aa); border-radius:4px;
}}

/* NAV */
nav {{
    position:fixed; top:0; left:0; right:0; z-index:1000;
    display:flex; align-items:center; justify-content:space-between;
    padding:0.9rem 2.5rem;
    background:rgba(0,5,20,0.8);
    border-bottom:1px solid rgba(0,180,255,0.15);
    backdrop-filter:blur(20px);
}}
.nav-logo {{
    font-family:'Orbitron',monospace;
    font-size:clamp(0.8rem,2vw,1.05rem); font-weight:900;
    background:linear-gradient(135deg,#00d4ff,#0055cc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:0.3rem; text-decoration:none;
}}
.nav-links {{ display:flex; gap:clamp(1rem,2.5vw,2.2rem); }}
.nav-links a {{
    font-family:'Share Tech Mono',monospace;
    font-size:clamp(0.55rem,1.1vw,0.68rem);
    color:rgba(180,220,255,0.65); text-decoration:none;
    letter-spacing:0.15rem; transition:color 0.25s; text-transform:uppercase;
}}
.nav-links a:hover {{ color:#00d4ff; }}

/* PART 1 */
.part1 {{
    position:relative; width:100%;
    padding-top:calc(56.25% - 0px);
    overflow:hidden; background:#000510;
}}
.part1 video {{
    position:absolute; top:0; left:0;
    width:100%; height:100%; object-fit:cover; display:block;
}}
.part1-overlay {{
    position:absolute; top:0; left:0; width:100%; height:100%;
    background:linear-gradient(180deg,
        rgba(0,5,20,0.25) 0%,rgba(0,8,30,0.2) 50%,rgba(0,5,20,0.7) 100%);
}}
#star-canvas {{
    position:absolute; top:0; left:0;
    width:100%; height:100%; pointer-events:none; z-index:2;
}}
.part1-content {{
    position:absolute; top:0; left:0; width:100%; height:100%; z-index:3;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    text-align:center; padding:4rem 1.5rem 2rem;
}}
.eyebrow {{
    font-family:'Share Tech Mono',monospace;
    font-size:clamp(0.5rem,1.3vw,0.68rem);
    color:rgba(0,210,255,0.7);
    letter-spacing:clamp(0.3rem,1.5vw,0.6rem);
    margin-bottom:1.2rem; text-transform:uppercase;
    opacity:0; animation:fadeUp 1s ease-out 0.3s forwards;
}}
.big-title {{
    font-family:'Orbitron',monospace;
    font-size:clamp(2.5rem,9vw,7.5rem); font-weight:900;
    background:linear-gradient(135deg,#00d4ff 0%,#0099ff 35%,#0055dd 65%,#00aaff 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:clamp(0.2rem,1.5vw,0.7rem); line-height:1;
    opacity:0;
    animation:fadeUp 1.1s ease-out 0.5s forwards,
              titleGlow 4s ease-in-out 1.5s infinite alternate;
}}
.tagline {{
    font-family:'Share Tech Mono',monospace;
    font-size:clamp(0.5rem,1.3vw,0.75rem);
    color:rgba(0,200,255,0.65);
    letter-spacing:clamp(0.15rem,0.8vw,0.45rem);
    margin-top:1rem; opacity:0;
    animation:fadeUp 1.1s ease-out 0.8s forwards;
}}
.glow-bar {{
    width:clamp(80px,20vw,220px); height:1px;
    background:linear-gradient(90deg,transparent,#00d4ff,#0066cc,transparent);
    margin:1.2rem auto; opacity:0;
    animation:fadeUp 1s ease-out 1s forwards;
}}
.desc-text {{
    font-family:'Exo 2',sans-serif;
    font-size:clamp(0.78rem,1.6vw,0.95rem);
    color:rgba(200,230,255,0.75);
    max-width:min(520px,85vw); line-height:1.8; font-weight:300;
    opacity:0; animation:fadeUp 1.1s ease-out 1.1s forwards;
}}
.scroll-hint {{
    position:absolute; bottom:1.5rem; left:50%;
    transform:translateX(-50%); z-index:4;
    font-family:'Share Tech Mono',monospace; font-size:0.6rem;
    color:rgba(0,200,255,0.5); letter-spacing:0.3rem; text-transform:uppercase;
    animation:fadeUp 1s ease-out 1.8s forwards,
              bounce 2s ease-in-out 2.5s infinite;
    opacity:0;
}}
@keyframes titleGlow {{
    from {{ filter:drop-shadow(0 0 20px rgba(0,180,255,0.3)); }}
    to   {{ filter:drop-shadow(0 0 55px rgba(0,150,255,0.6)); }}
}}
@keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(25px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes bounce {{
    0%,100% {{ transform:translateX(-50%) translateY(0); opacity:0.5; }}
    50%      {{ transform:translateX(-50%) translateY(-8px); opacity:0.9; }}
}}

/* PART 2 */
.part2 {{
    position:relative; width:100%;
    background:linear-gradient(180deg,rgba(0,5,18,0.97),rgba(0,8,28,0.99));
    padding:clamp(3rem,8vh,6rem) clamp(1rem,5vw,3rem); overflow:hidden;
}}
.part2::before {{
    content:''; position:absolute; inset:0;
    background-image:
        linear-gradient(rgba(0,100,200,0.04) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,100,200,0.04) 1px,transparent 1px);
    background-size:60px 60px; pointer-events:none;
}}
.orb {{ position:absolute; border-radius:50%; pointer-events:none; }}
.orb1 {{
    top:10%; left:5%; width:350px; height:350px;
    background:radial-gradient(circle,rgba(0,100,255,0.07),transparent 70%);
    animation:orbFloat 9s ease-in-out infinite alternate;
}}
.orb2 {{
    bottom:10%; right:5%; width:280px; height:280px;
    background:radial-gradient(circle,rgba(0,150,255,0.06),transparent 70%);
    animation:orbFloat 11s ease-in-out infinite alternate-reverse;
}}
@keyframes orbFloat {{
    from {{ transform:translate(0,0) scale(1); }}
    to   {{ transform:translate(40px,25px) scale(1.15); }}
}}
.part2-inner {{ max-width:1050px; margin:0 auto; text-align:center; position:relative; z-index:2; }}
.stats-wrap {{
    display:flex; justify-content:center; flex-wrap:wrap;
    margin-bottom:3.5rem;
    background:rgba(0,8,35,0.72);
    border:1px solid rgba(0,180,255,0.2);
    border-radius:20px; backdrop-filter:blur(20px);
    max-width:min(820px,95vw); margin-left:auto; margin-right:auto; overflow:hidden;
}}
.stat-box {{
    text-align:center; padding:1.8rem clamp(0.8rem,3vw,2rem);
    border-right:1px solid rgba(0,180,255,0.1);
    flex:1; min-width:110px; position:relative; transition:background 0.3s;
}}
.stat-box:last-child {{ border-right:none; }}
.stat-box:hover {{ background:rgba(0,50,150,0.2); }}
.stat-num {{
    font-family:'Orbitron',monospace;
    font-size:clamp(1.2rem,3vw,2.1rem); font-weight:700;
    color:#00d4ff; line-height:1; transition:text-shadow 0.3s;
}}
.stat-box:hover .stat-num {{ text-shadow:0 0 20px rgba(0,212,255,0.8); }}
.stat-lbl {{
    font-family:'Share Tech Mono',monospace;
    font-size:clamp(0.45rem,0.9vw,0.58rem);
    color:rgba(150,200,255,0.6); letter-spacing:0.15rem;
    margin-top:0.4rem; text-transform:uppercase;
}}
.stat-box::after {{
    content:''; position:absolute; bottom:0; left:20%; right:20%; height:1px;
    background:linear-gradient(90deg,transparent,#00d4ff,transparent);
    opacity:0; transition:opacity 0.3s;
}}
.stat-box:hover::after {{ opacity:1; }}
.cards-grid {{
    display:grid; grid-template-columns:repeat(5,1fr);
    gap:0.9rem; max-width:min(1000px,95vw); margin:0 auto;
}}
.page-card {{
    background:rgba(0,10,42,0.78);
    border:1px solid rgba(0,180,255,0.18);
    border-radius:14px; padding:clamp(1rem,2.5vw,1.5rem) 0.7rem;
    text-align:center; text-decoration:none; display:block;
    transition:all 0.35s ease; backdrop-filter:blur(12px);
    position:relative; overflow:hidden;
}}
.page-card::before {{
    content:''; position:absolute; inset:0;
    background:linear-gradient(135deg,rgba(0,150,255,0.07),transparent,rgba(0,100,200,0.04));
    opacity:0; transition:opacity 0.3s;
}}
.page-card:hover {{
    background:rgba(0,25,80,0.88); border-color:#00d4ff;
    transform:translateY(-8px);
    box-shadow:0 0 30px rgba(0,212,255,0.22),0 15px 35px rgba(0,0,0,0.5);
}}
.page-card:hover::before {{ opacity:1; }}
.card-icon {{
    font-size:clamp(1.3rem,2.5vw,1.9rem); margin-bottom:0.6rem; display:block;
    transition:transform 0.3s;
}}
.page-card:hover .card-icon {{ transform:scale(1.15) rotate(-5deg); }}
.card-title {{
    font-family:'Orbitron',monospace;
    font-size:clamp(0.48rem,0.9vw,0.62rem);
    color:#00d4ff; letter-spacing:0.12rem; margin-bottom:0.35rem;
    font-weight:700; display:block;
}}
.card-desc {{
    font-family:'Share Tech Mono',monospace;
    font-size:clamp(0.44rem,0.75vw,0.54rem);
    color:rgba(170,215,255,0.55); line-height:1.5; display:block;
}}
.card-arrow {{
    display:block; margin-top:0.6rem;
    font-family:'Share Tech Mono',monospace; font-size:0.55rem;
    color:rgba(0,212,255,0); transition:all 0.3s; letter-spacing:0.1rem;
}}
.page-card:hover .card-arrow {{ color:rgba(0,212,255,0.7); }}

/* TICKER */
.ticker-outer {{
    background:rgba(0,5,20,0.95);
    border-top:1px solid rgba(0,180,255,0.18);
    border-bottom:1px solid rgba(0,180,255,0.18);
    padding:0.6rem 0; overflow:hidden; width:100%;
}}
.ticker-inner {{
    display:inline-flex;
    animation:tickScroll 45s linear infinite; white-space:nowrap;
}}
@keyframes tickScroll {{
    from {{ transform:translateX(0); }}
    to   {{ transform:translateX(-50%); }}
}}
.tick-item {{
    font-family:'Share Tech Mono',monospace;
    font-size:0.63rem; color:rgba(0,200,255,0.7);
    letter-spacing:0.12rem; padding:0 2.5rem;
}}

/* PART 3 */
.part3 {{
    position:relative; width:100%; background:rgba(0,3,15,0.98);
    border-top:1px solid rgba(0,180,255,0.1);
    padding:clamp(3rem,8vh,5rem) clamp(1rem,5vw,3rem); overflow:hidden;
}}
.part3::before {{
    content:''; position:absolute; inset:0;
    background-image:
        linear-gradient(rgba(0,80,180,0.03) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,80,180,0.03) 1px,transparent 1px);
    background-size:80px 80px; pointer-events:none;
}}
.nebula {{ position:absolute; border-radius:50%; pointer-events:none; }}
.nebula1 {{
    top:-5%; right:-3%; width:500px; height:500px;
    background:radial-gradient(ellipse,rgba(0,80,200,0.06),transparent 70%);
    animation:nebDrift 15s ease-in-out infinite alternate;
}}
.nebula2 {{
    bottom:-5%; left:-3%; width:400px; height:400px;
    background:radial-gradient(ellipse,rgba(0,120,255,0.05),transparent 70%);
    animation:nebDrift 12s ease-in-out infinite alternate-reverse;
}}
@keyframes nebDrift {{
    from {{ transform:translate(0,0) scale(1); }}
    to   {{ transform:translate(30px,-20px) scale(1.1); }}
}}
.part3-inner {{ max-width:1200px; margin:0 auto; position:relative; z-index:2; }}
.sec-eyebrow {{
    font-family:'Share Tech Mono',monospace; font-size:0.65rem;
    color:rgba(0,200,255,0.55); letter-spacing:0.5rem;
    display:block; text-align:center; margin-bottom:0.8rem; text-transform:uppercase;
}}
.sec-heading {{
    font-family:'Exo 2',sans-serif; font-size:clamp(1.1rem,3vw,1.6rem);
    color:rgba(220,240,255,0.92); font-weight:300; text-align:center; margin-bottom:3rem;
}}
.feat-grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));
    gap:1.2rem;
}}
.feat-card {{
    background:rgba(0,8,35,0.88); border:1px solid rgba(0,150,255,0.13);
    border-radius:16px; padding:clamp(1.2rem,2.5vw,1.8rem) clamp(1rem,2vw,1.5rem);
    transition:all 0.35s ease; position:relative; overflow:hidden;
}}
.feat-card::before {{
    content:''; position:absolute; top:0; left:10%; right:10%; height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,180,255,0),transparent);
    transition:background 0.4s;
}}
.feat-card:hover::before {{
    background:linear-gradient(90deg,transparent,#00d4ff,transparent);
}}
.feat-card:hover {{
    border-color:rgba(0,200,255,0.35);
    box-shadow:0 0 30px rgba(0,180,255,0.1),0 15px 35px rgba(0,0,0,0.3);
    transform:translateY(-5px); background:rgba(0,12,45,0.95);
}}
.feat-icon {{
    font-size:clamp(1.5rem,2.5vw,2rem); margin-bottom:0.9rem; display:block;
    transition:transform 0.3s;
}}
.feat-card:hover .feat-icon {{ transform:scale(1.1); }}
.feat-title {{
    font-family:'Orbitron',monospace; font-size:clamp(0.6rem,1.1vw,0.7rem);
    color:#00d4ff; letter-spacing:0.2rem; margin-bottom:0.7rem; display:block;
}}
.feat-desc {{
    font-family:'Exo 2',sans-serif; font-size:clamp(0.78rem,1.3vw,0.86rem);
    color:rgba(170,210,255,0.62); line-height:1.75; font-weight:300;
}}
.feat-link {{
    display:inline-block; margin-top:1rem;
    font-family:'Share Tech Mono',monospace; font-size:0.58rem;
    color:rgba(0,212,255,0); letter-spacing:0.15rem; text-decoration:none;
    border-bottom:1px solid rgba(0,212,255,0); transition:all 0.3s; text-transform:uppercase;
}}
.feat-card:hover .feat-link {{
    color:rgba(0,212,255,0.7); border-bottom-color:rgba(0,212,255,0.4);
}}
.site-footer {{
    background:rgba(0,2,10,0.99); border-top:1px solid rgba(0,150,255,0.1);
    padding:2.5rem; text-align:center; width:100%;
}}
.footer-logo {{
    font-family:'Orbitron',monospace; font-size:0.65rem;
    color:rgba(0,180,255,0.5); letter-spacing:0.4rem; display:block; margin-bottom:0.7rem;
}}
.footer-text {{
    font-family:'Share Tech Mono',monospace; font-size:0.56rem;
    color:rgba(130,180,255,0.35); letter-spacing:0.14rem; line-height:2;
}}
.reveal {{
    opacity:0; transform:translateY(40px);
    transition:opacity 0.8s ease, transform 0.8s ease;
}}
.reveal-left {{
    opacity:0; transform:translateX(-50px);
    transition:opacity 0.8s ease, transform 0.8s ease;
}}
.reveal-right {{
    opacity:0; transform:translateX(50px);
    transition:opacity 0.8s ease, transform 0.8s ease;
}}
.reveal.visible,.reveal-left.visible,.reveal-right.visible {{
    opacity:1; transform:translate(0,0);
}}
.d1{{transition-delay:0.1s;}} .d2{{transition-delay:0.2s;}}
.d3{{transition-delay:0.3s;}} .d4{{transition-delay:0.4s;}}
.d5{{transition-delay:0.5s;}} .d6{{transition-delay:0.6s;}}
@media (max-width:768px) {{
    nav {{ padding:0.8rem 1rem; }}
    .nav-links {{ display:none; }}
    .cards-grid {{ grid-template-columns:1fr 1fr; gap:0.6rem; }}
    .stat-box {{ min-width:90px; padding:1.2rem 0.5rem; }}
}}
@media (max-width:480px) {{
    .cards-grid {{ grid-template-columns:1fr; }}
    .feat-grid  {{ grid-template-columns:1fr; }}
    .big-title  {{ font-size:2rem; letter-spacing:0.1rem; }}
}}
</style>
</head>
<body>

<!-- NAV — 5 links, no Observatory -->
<nav>
    <a href="/" class="nav-logo">◈ ASTRASENSE</a>
    <div class="nav-links">
        <a href="/Analysis">ANALYSIS</a>
        <a href="/Star_Catalogue">STAR CATALOGUE</a>
        <a href="/Noise_Lab">NOISE LAB</a>
        <a href="/Science">THE SCIENCE</a>
        <a href="/Performance">PERFORMANCE</a>
    </div>
</nav>

<!-- PART 1 -->
<div class="part1">
    {'<video autoplay muted loop playsinline><source src="' + video_src + '" type="video/mp4"></video>' if video_src else '<div style="position:absolute;inset:0;background:linear-gradient(180deg,#000c20,#000510);"></div>'}
    <div class="part1-overlay"></div>
    <canvas id="star-canvas"></canvas>
    <div class="part1-content">
        <div class="eyebrow">
            NASA KEPLER &nbsp;·&nbsp; TESS &nbsp;·&nbsp;
            DEEP LEARNING &nbsp;·&nbsp; SIGNAL ENHANCEMENT
        </div>
        <div class="big-title">ASTRASENSE</div>
        <div class="tagline">◈ &nbsp; EXOPLANET TRANSIT SIGNAL ENHANCEMENT &nbsp; ◈</div>
        <div class="glow-bar"></div>
        <div class="desc-text">
            An AI-powered research platform for denoising faint stellar
            light curves from NASA Kepler &amp; TESS space telescopes.
            Now trained on 10 star systems.
        </div>
    </div>
    <div class="scroll-hint">▼ &nbsp; SCROLL TO EXPLORE &nbsp; ▼</div>
</div>

<!-- PART 2 -->
<div class="part2">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="part2-inner">
        <div class="stats-wrap reveal">
            <div class="stat-box">
                <div class="stat-num" data-target="10" data-suffix="">0</div>
                <div class="stat-lbl">Stars Trained</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" data-target="200" data-suffix="K+">0</div>
                <div class="stat-lbl">Data Points</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" data-target="2.8" data-suffix="M" data-dec="1">0</div>
                <div class="stat-lbl">Parameters</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" style="font-size:clamp(1rem,2.5vw,1.5rem);">RTX 3050</div>
                <div class="stat-lbl">Compute</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" data-target="1000" data-suffix="+">0</div>
                <div class="stat-lbl">Epochs</div>
            </div>
        </div>

        <!-- 5 nav cards -->
        <div class="cards-grid">
            <a href="/Analysis" class="page-card reveal d1">
                <span class="card-icon">🔬</span>
                <span class="card-title">ANALYSIS</span>
                <span class="card-desc">Live NASA fetch &amp; AI denoising</span>
                <span class="card-arrow">EXPLORE →</span>
            </a>
            <a href="/Star_Catalogue" class="page-card reveal d2">
                <span class="card-icon">🪐</span>
                <span class="card-title">STAR CATALOGUE</span>
                <span class="card-desc">10 star systems &amp; 3D planets</span>
                <span class="card-arrow">EXPLORE →</span>
            </a>
            <a href="/Noise_Lab" class="page-card reveal d3">
                <span class="card-icon">⚗️</span>
                <span class="card-title">NOISE LAB</span>
                <span class="card-desc">Interactive noise simulation</span>
                <span class="card-arrow">EXPLORE →</span>
            </a>
            <a href="/Science" class="page-card reveal d4">
                <span class="card-icon">🌌</span>
                <span class="card-title">THE SCIENCE</span>
                <span class="card-desc">How exoplanet detection works</span>
                <span class="card-arrow">EXPLORE →</span>
            </a>
            <a href="/Performance" class="page-card reveal d5">
                <span class="card-icon">📊</span>
                <span class="card-title">PERFORMANCE</span>
                <span class="card-desc">Model metrics &amp; evaluation</span>
                <span class="card-arrow">EXPLORE →</span>
            </a>
        </div>
    </div>
</div>

<!-- TICKER -->
<div class="ticker-outer">
    <div class="ticker-inner">
        <span class="tick-item">◈ KEPLER-452b — EARTH'S COUSIN — 1,402 LIGHT YEARS</span>
        <span class="tick-item">◈ KEPLER-7b — FIRST CLOUD-MAPPED EXOPLANET</span>
        <span class="tick-item">◈ KEPLER-10b — FIRST CONFIRMED ROCKY EXOPLANET</span>
        <span class="tick-item">◈ KEPLER-22b — SUPER EARTH IN HABITABLE ZONE</span>
        <span class="tick-item">◈ KEPLER-16b — REAL TATOOINE — ORBITS TWO STARS</span>
        <span class="tick-item">◈ KEPLER-62f — POTENTIAL OCEAN WORLD — 1,200 LY</span>
        <span class="tick-item">◈ KEPLER-186f — FIRST EARTH-SIZE IN HABITABLE ZONE</span>
        <span class="tick-item">◈ KEPLER-69c — SUPER-VENUS — HABITABLE ZONE BOUNDARY</span>
        <span class="tick-item">◈ KEPLER-442b — EARTH SIMILARITY INDEX 0.84</span>
        <span class="tick-item">◈ KEPLER-90i — 8-PLANET SYSTEM — FOUND BY GOOGLE AI</span>
        <span class="tick-item">◈ ASTRASENSE DDPM — 2.8M PARAMS — RTX 3050 GPU</span>
        <span class="tick-item">◈ KEPLER-452b — EARTH'S COUSIN — 1,402 LIGHT YEARS</span>
        <span class="tick-item">◈ KEPLER-7b — FIRST CLOUD-MAPPED EXOPLANET</span>
        <span class="tick-item">◈ KEPLER-10b — FIRST CONFIRMED ROCKY EXOPLANET</span>
        <span class="tick-item">◈ KEPLER-22b — SUPER EARTH IN HABITABLE ZONE</span>
        <span class="tick-item">◈ KEPLER-16b — REAL TATOOINE — ORBITS TWO STARS</span>
        <span class="tick-item">◈ KEPLER-62f — POTENTIAL OCEAN WORLD — 1,200 LY</span>
        <span class="tick-item">◈ KEPLER-186f — FIRST EARTH-SIZE IN HABITABLE ZONE</span>
        <span class="tick-item">◈ KEPLER-69c — SUPER-VENUS — HABITABLE ZONE BOUNDARY</span>
        <span class="tick-item">◈ KEPLER-442b — EARTH SIMILARITY INDEX 0.84</span>
        <span class="tick-item">◈ KEPLER-90i — 8-PLANET SYSTEM — FOUND BY GOOGLE AI</span>
        <span class="tick-item">◈ ASTRASENSE DDPM — 2.8M PARAMS — RTX 3050 GPU</span>
    </div>
</div>

<!-- PART 3 -->
<div class="part3">
    <div class="nebula nebula1"></div>
    <div class="nebula nebula2"></div>
    <div class="part3-inner">
        <span class="sec-eyebrow reveal">◈ PLATFORM CAPABILITIES</span>
        <div class="sec-heading reveal d1">
            Everything you need to explore exoplanet science
        </div>
        <div class="feat-grid">
            <div class="feat-card reveal-left d1">
                <span class="feat-icon">🛰️</span>
                <span class="feat-title">LIVE NASA DATA</span>
                <div class="feat-desc">Connects directly to NASA MAST Archive in real time. Fetch light curves from Kepler and TESS telescopes for any of the 10 trained star systems.</div>
                <a href="/Analysis" class="feat-link">Launch Analysis →</a>
            </div>
            <div class="feat-card reveal d2">
                <span class="feat-icon">🧠</span>
                <span class="feat-title">DDPM AI DENOISING</span>
                <div class="feat-desc">1D Denoising Diffusion Probabilistic Model with U-Net backbone. Trained on 200K+ real NASA data points across 10 diverse exoplanet host stars.</div>
                <a href="/Performance" class="feat-link">View Performance →</a>
            </div>
            <div class="feat-card reveal-right d3">
                <span class="feat-icon">🪐</span>
                <span class="feat-title">10-STAR CATALOGUE</span>
                <div class="feat-desc">Interactive 3D spinning planet visualizations for all 10 trained stars — from circumbinary worlds to Earth-size habitable zone planets.</div>
                <a href="/Star_Catalogue" class="feat-link">Explore Stars →</a>
            </div>
            <div class="feat-card reveal-left d4">
                <span class="feat-icon">⚗️</span>
                <span class="feat-title">NOISE SIMULATION LAB</span>
                <div class="feat-desc">Inject custom noise types into real light curves and compare denoising methods live with animated Plotly visualizations and PSD analysis.</div>
                <a href="/Noise_Lab" class="feat-link">Enter Lab →</a>
            </div>
            <div class="feat-card reveal d5">
                <span class="feat-icon">📡</span>
                <span class="feat-title">TRANSIT DETECTION</span>
                <div class="feat-desc">Automatic transit detection, orbital period estimation, planet radius calculation and SNR improvement — computed live for any of the 10 trained stars.</div>
                <a href="/Analysis" class="feat-link">Try Now →</a>
            </div>
            <div class="feat-card reveal-right d6">
                <span class="feat-icon">📊</span>
                <span class="feat-title">MODEL PERFORMANCE</span>
                <div class="feat-desc">Full evaluation dashboard comparing DDPM against traditional filters across all 10 star systems. Training curves, RMSE, MAE and SNR metrics visualized beautifully.</div>
                <a href="/Performance" class="feat-link">View Metrics →</a>
            </div>
        </div>
    </div>
</div>

<div class="site-footer">
    <span class="footer-logo">◈ ASTRASENSE v2.0</span>
    <div class="footer-text">
        DEEP LEARNING EXOPLANET SIGNAL ENHANCEMENT &nbsp;◈&nbsp;
        1D DDPM U-NET &nbsp;◈&nbsp; 10 STAR SYSTEMS &nbsp;◈&nbsp;
        NASA KEPLER / TESS &nbsp;◈&nbsp; RTX 3050 GPU
    </div>
</div>

<script>
(function(){{
    var c=document.getElementById('star-canvas');
    if(!c) return;
    var ctx=c.getContext('2d');
    function resize(){{
        c.width=c.parentElement.offsetWidth;
        c.height=c.parentElement.offsetHeight;
    }}
    resize();
    window.addEventListener('resize',resize);
    var cols=['#00d4ff','#0088ff','#ffffff','#ffffff','#0055cc'];
    var stars=[];
    for(var i=0;i<220;i++){{
        stars.push({{
            x:Math.random()*c.width,y:Math.random()*c.height,
            r:Math.random()*1.5+0.2,a:Math.random()*Math.PI*2,
            s:Math.random()*0.006+0.002,
            col:cols[Math.floor(Math.random()*cols.length)]
        }});
    }}
    var shoots=[];
    setInterval(function(){{ shoots.push({{x:Math.random()*c.width*0.8,y:Math.random()*c.height*0.4,l:Math.random()*110+50,sp:Math.random()*7+3,a:1}}); }},4000);
    function draw(){{
        ctx.clearRect(0,0,c.width,c.height);
        stars.forEach(function(s){{
            var al=(Math.sin(Date.now()*s.s+s.a)+1)/2;
            ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
            ctx.fillStyle=s.col;ctx.globalAlpha=al*0.85;ctx.fill();ctx.globalAlpha=1;
        }});
        shoots.forEach(function(sh,i){{
            ctx.beginPath();ctx.moveTo(sh.x,sh.y);ctx.lineTo(sh.x-sh.l,sh.y-sh.l*0.2);
            var g=ctx.createLinearGradient(sh.x,sh.y,sh.x-sh.l,sh.y-sh.l*0.2);
            g.addColorStop(0,'rgba(255,255,255,'+sh.a+')');g.addColorStop(1,'rgba(0,0,0,0)');
            ctx.strokeStyle=g;ctx.lineWidth=1.5;ctx.globalAlpha=sh.a;ctx.stroke();ctx.globalAlpha=1;
            sh.x+=sh.sp;sh.y+=sh.sp*0.2;sh.a-=0.018;if(sh.a<=0)shoots.splice(i,1);
        }});
        requestAnimationFrame(draw);
    }}
    draw();
}})();
(function(){{
    var els=document.querySelectorAll('.reveal,.reveal-left,.reveal-right');
    var obs=new IntersectionObserver(function(entries){{
        entries.forEach(function(e){{ if(e.isIntersecting)e.target.classList.add('visible'); }});
    }},{{threshold:0.12}});
    els.forEach(function(el){{ obs.observe(el); }});
}})();
(function(){{
    var counters=document.querySelectorAll('.stat-num[data-target]');
    var done=false;
    function run(){{
        if(done)return;done=true;
        counters.forEach(function(el){{
            var target=parseFloat(el.getAttribute('data-target'));
            var suffix=el.getAttribute('data-suffix')||'';
            var dec=parseInt(el.getAttribute('data-dec')||'0');
            var steps=60;var step=0;var inc=target/steps;var cur=0;
            var t=setInterval(function(){{
                step++;cur+=inc;
                if(step>=steps){{cur=target;clearInterval(t);}}
                el.textContent=dec>0?cur.toFixed(dec)+suffix:Math.floor(cur)+suffix;
            }},2000/steps);
        }});
    }}
    var el=document.querySelector('.stats-wrap');
    if(el){{var obs=new IntersectionObserver(function(e){{if(e[0].isIntersecting)run();}},{{threshold:0.3}});obs.observe(el);}}
}})();
</script>
</body>
</html>"""

st.iframe(html, height=2500)