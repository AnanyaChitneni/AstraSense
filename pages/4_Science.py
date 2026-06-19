import streamlit as st
import base64, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="AstraSense — The Science",
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
[data-testid="stHeader"],
[data-testid="stDecoration"],
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
}
[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
    pointer-events: none !important;
}
.stApp {
    margin: 0 !important;
    padding: 0 !important;
    overflow-x: hidden !important;
}
.main {
    padding: 0 !important;
    margin: 0 !important;
}
.main > div:first-child {
    padding: 0 !important;
    margin: 0 !important;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
    min-width: 100% !important;
}
[data-testid="stMain"] {
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
[data-testid="stAppViewContainer"] {
    background: #000510 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow-x: hidden !important;
}
[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
.block-container,
.main .block-container,
[class*="block-container"] {
    padding-top: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    padding-bottom: 0rem !important;
    margin: 0 !important;
}
section.main > div {
    padding: 0 !important;
    margin: 0 !important;
}
.element-container {
    margin: 0 !important;
    padding: 0 !important;
}
.element-container:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
[data-testid="stIFrame"] {
    width: 100% !important;
    min-width: 100% !important;
    display: block !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    margin-top: -1rem !important;
}
[data-testid="stIFrame"] > iframe {
    display: block !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}
iframe {
    display: block !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

def img_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_b64 = img_b64("assets/science_bg.jpg")
bg_src = f"data:image/jpeg;base64,{bg_b64}" if bg_b64 else ""

ch1_b64 = img_b64("assets/science_ch1.jpg")
ch1_src = f"data:image/jpeg;base64,{ch1_b64}" if ch1_b64 else ""

ch2_b64 = img_b64("assets/science_ch2.jpg")
ch2_src = f"data:image/jpeg;base64,{ch2_b64}" if ch2_b64 else ""

ch3_b64 = img_b64("assets/science_ch3.jpg")
ch3_src = f"data:image/jpeg;base64,{ch3_b64}" if ch3_b64 else ""

ch7_b64 = img_b64("assets/science_ch7.jpg")
ch7_src = f"data:image/jpeg;base64,{ch7_b64}" if ch7_b64 else ""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<base target="_self">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{
    width:100%;background:#000510;
    overflow-x:hidden;scroll-behavior:smooth;
    font-family:'Exo 2',sans-serif;
    scrollbar-width:none;-ms-overflow-style:none;
}}
::-webkit-scrollbar{{width:0px;display:none;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:transparent;}}

nav{{
    position:fixed;top:0;left:0;right:0;z-index:1000;
    display:flex;align-items:center;justify-content:space-between;
    padding:0.85rem 2.5rem;
    background:rgba(0,4,18,0.92);
    border-bottom:1px solid rgba(0,180,255,0.15);
    backdrop-filter:blur(20px);
}}
.nav-logo{{
    font-family:'Orbitron',monospace;font-size:1rem;font-weight:900;
    background:linear-gradient(135deg,#00d4ff,#0055cc);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;letter-spacing:0.3rem;text-decoration:none;
}}
.nav-links{{display:flex;gap:2rem;}}
.nav-links a{{
    font-family:'Share Tech Mono',monospace;
    font-size:0.65rem;color:rgba(180,220,255,0.6);
    text-decoration:none;letter-spacing:0.15rem;
    transition:color 0.2s;text-transform:uppercase;
}}
.nav-links a:hover,.nav-links a.active{{color:#00d4ff;}}

/* HERO — 16:9 with nav offset */
.hero{{
    position:relative;width:100%;
    padding-top:56.25%;
    overflow:hidden;background:#000510;
    margin-top:52px;
}}
.hero-img{{
    position:absolute;top:0;left:0;
    width:100%;height:100%;object-fit:cover;
}}
.hero-overlay{{
    position:absolute;top:0;left:0;
    width:100%;height:100%;
    background:linear-gradient(
        135deg,
        rgba(0,0,0,0.78) 0%,
        rgba(0,5,20,0.55) 50%,
        rgba(0,0,0,0.28) 100%
    );
}}
.hero-content{{
    position:absolute;bottom:0;left:0;
    padding:3rem 4rem 3.5rem;z-index:2;
    max-width:680px;
}}
.hero-eyebrow{{
    font-family:'Share Tech Mono',monospace;
    font-size:0.62rem;color:rgba(0,200,255,0.7);
    letter-spacing:0.45rem;text-transform:uppercase;
    margin-bottom:1rem;display:block;
}}
.hero-title{{
    font-family:'Orbitron',monospace;
    font-size:clamp(2rem,5vw,4rem);
    font-weight:900;color:white;
    line-height:1.1;margin-bottom:1.2rem;
    text-shadow:0 2px 25px rgba(0,0,0,0.9);
}}
.hero-desc{{
    font-family:'Exo 2',sans-serif;
    font-size:clamp(0.85rem,1.4vw,1rem);
    color:rgba(220,235,255,0.78);
    line-height:1.85;font-weight:300;
    text-shadow:0 1px 10px rgba(0,0,0,0.95);
}}

/* GLOW DIVIDER */
.glow-div{{
    height:1px;width:100%;
    background:linear-gradient(90deg,
        transparent,rgba(0,180,255,0.35),transparent);
}}

/* SECTIONS — solid backgrounds, no bg image */
.section{{
    position:relative;width:100%;
    padding:clamp(3rem,6vw,5rem) clamp(2rem,6vw,6rem);
    overflow:hidden;
}}
.section-dark{{background:#000512;}}
.section-darker{{background:#00030c;}}
.section-mid{{background:#000618;}}
.section::before{{
    content:'';position:absolute;inset:0;
    background-image:
        linear-gradient(rgba(0,80,180,0.04) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,80,180,0.04) 1px,transparent 1px);
    background-size:60px 60px;pointer-events:none;
}}
.section-inner{{
    max-width:1200px;margin:0 auto;
    position:relative;z-index:2;
}}
.section-eyebrow{{
    font-family:'Share Tech Mono',monospace;
    font-size:0.62rem;color:rgba(0,200,255,0.55);
    letter-spacing:0.5rem;text-transform:uppercase;
    display:block;margin-bottom:0.8rem;
}}
.section-title{{
    font-family:'Orbitron',monospace;
    font-size:clamp(1.2rem,3vw,2rem);font-weight:900;
    background:linear-gradient(135deg,#00d4ff,#0055cc);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;letter-spacing:0.2rem;
    margin-bottom:1.5rem;display:block;
}}
.section-body{{
    font-family:'Exo 2',sans-serif;
    font-size:clamp(0.85rem,1.4vw,0.96rem);
    color:rgba(190,220,255,0.7);
    line-height:1.9;font-weight:300;
}}
.section-body p{{margin-bottom:1rem;}}
.section-body strong{{color:rgba(0,210,255,0.85);font-weight:500;}}

.two-col{{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:clamp(2rem,4vw,4rem);
    align-items:center;
}}
.two-col.reverse{{direction:rtl;}}
.two-col.reverse > *{{direction:ltr;}}

.img-panel{{
    border-radius:16px;overflow:hidden;
    border:1px solid rgba(0,180,255,0.15);
    box-shadow:0 0 40px rgba(0,100,255,0.1);
    position:relative;background:#000a20;
}}
.img-panel img{{
    width:100%;height:100%;
    object-fit:cover;display:block;
    filter:brightness(0.88) contrast(1.05);
}}
.img-caption{{
    position:absolute;bottom:0;left:0;right:0;
    background:linear-gradient(transparent,rgba(0,5,20,0.92));
    padding:1.5rem 1.2rem 0.9rem;
    font-family:'Share Tech Mono',monospace;
    font-size:0.56rem;color:rgba(0,200,255,0.55);
    letter-spacing:0.2rem;text-transform:uppercase;
}}

.steps-grid{{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:1.1rem;margin-top:2rem;
}}
.step-card{{
    background:rgba(0,8,35,0.9);
    border:1px solid rgba(0,150,255,0.14);
    border-radius:14px;padding:1.4rem 1.2rem;
    transition:all 0.3s;
}}
.step-card:hover{{
    border-color:rgba(0,200,255,0.35);
    transform:translateY(-4px);
    box-shadow:0 0 25px rgba(0,180,255,0.1);
}}
.step-num{{
    font-family:'Orbitron',monospace;
    font-size:1.8rem;font-weight:900;
    color:rgba(0,180,255,0.12);line-height:1;margin-bottom:0.7rem;
}}
.step-title{{
    font-family:'Orbitron',monospace;
    font-size:0.68rem;color:#00d4ff;
    letter-spacing:0.2rem;margin-bottom:0.5rem;text-transform:uppercase;
}}
.step-body{{
    font-family:'Exo 2',sans-serif;
    font-size:0.8rem;color:rgba(165,208,255,0.58);
    line-height:1.7;font-weight:300;
}}

.compare-grid{{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:1rem;margin-top:2rem;
}}
.compare-card{{
    background:rgba(0,8,35,0.9);
    border:1px solid rgba(0,150,255,0.14);
    border-radius:14px;padding:1.4rem 1.1rem;text-align:center;
}}
.ccard-icon{{font-size:1.8rem;margin-bottom:0.7rem;}}
.ccard-title{{
    font-family:'Orbitron',monospace;
    font-size:0.65rem;color:#00d4ff;
    letter-spacing:0.18rem;margin-bottom:0.5rem;text-transform:uppercase;
}}
.ccard-rmse{{
    font-family:'Orbitron',monospace;
    font-size:1.4rem;font-weight:700;margin-bottom:0.2rem;
}}
.ccard-body{{
    font-family:'Exo 2',sans-serif;
    font-size:0.76rem;color:rgba(155,198,255,0.52);
    line-height:1.65;font-weight:300;margin-top:0.5rem;
}}

.stat-row{{
    display:grid;grid-template-columns:repeat(4,1fr);
    gap:0.9rem;margin-top:1.5rem;
}}
.stat-item{{
    text-align:center;padding:1.1rem;
    background:rgba(0,8,35,0.9);
    border:1px solid rgba(0,150,255,0.14);border-radius:12px;
}}
.stat-val{{
    font-family:'Orbitron',monospace;
    font-size:1.5rem;font-weight:700;color:#00d4ff;line-height:1;
}}
.stat-lbl{{
    font-family:'Share Tech Mono',monospace;
    font-size:0.5rem;color:rgba(120,185,255,0.48);
    letter-spacing:0.14rem;margin-top:0.35rem;text-transform:uppercase;
}}

.timeline{{position:relative;padding-left:2.2rem;margin-top:1.8rem;}}
.timeline::before{{
    content:'';position:absolute;
    left:0.55rem;top:0.3rem;bottom:0;width:1px;
    background:linear-gradient(180deg,#00d4ff,rgba(0,100,200,0.3),transparent);
}}
.t-item{{position:relative;margin-bottom:1.8rem;}}
.t-dot{{
    position:absolute;left:-2.2rem;top:0.2rem;
    width:11px;height:11px;background:#00d4ff;border-radius:50%;
    box-shadow:0 0 8px rgba(0,212,255,0.5);
}}
.t-year{{
    font-family:'Orbitron',monospace;
    font-size:0.6rem;color:rgba(0,195,255,0.6);
    letter-spacing:0.2rem;margin-bottom:0.25rem;
}}
.t-title{{
    font-family:'Orbitron',monospace;
    font-size:0.78rem;color:white;letter-spacing:0.1rem;margin-bottom:0.35rem;
}}
.t-body{{
    font-family:'Exo 2',sans-serif;
    font-size:0.8rem;color:rgba(155,198,255,0.55);
    line-height:1.7;font-weight:300;
}}

.page-footer{{
    background:#00020a;
    border-top:1px solid rgba(0,120,200,0.12);
    padding:2rem;text-align:center;
}}
.footer-logo{{
    font-family:'Orbitron',monospace;
    font-size:0.62rem;color:rgba(0,165,240,0.4);
    letter-spacing:0.4rem;display:block;margin-bottom:0.6rem;
}}
.footer-txt{{
    font-family:'Share Tech Mono',monospace;
    font-size:0.52rem;color:rgba(95,155,215,0.28);
    letter-spacing:0.14rem;line-height:2;
}}

.reveal{{
    opacity:0;transform:translateY(22px);
    transition:opacity 0.75s ease,transform 0.75s ease;
}}
.reveal.visible{{opacity:1;transform:none;}}

@media(max-width:768px){{
    nav{{padding:0.8rem 1rem;}}
    .nav-links{{display:none;}}
    .two-col{{grid-template-columns:1fr;}}
    .compare-grid{{grid-template-columns:1fr;}}
    .stat-row{{grid-template-columns:1fr 1fr;}}
    .hero-content{{padding:2rem 1.5rem;}}
    .section{{padding:2.5rem 1.2rem;}}
}}
</style>
</head>
<body>

<nav>
    <a href="/" class="nav-logo">◈ ASTRASENSE</a>
    <div class="nav-links">
        <a href='/Analysis' target="_self">ANALYSIS</a>
        <a href='/Star_Catalogue' target="_self">STAR CATALOGUE</a>
        <a href='/Noise_Lab' target="_self">NOISE LAB</a>
        <a href='/Science' target="_self">THE SCIENCE</a>
        <a href='/Performance' target="_self">PERFORMANCE</a>
    </div>
</nav>

<!-- HERO — bg image only here -->
<div class="hero">
    {'<img class="hero-img" src="' + bg_src + '" alt="Astronaut in space">' if bg_src else '<div class="hero-img" style="background:linear-gradient(135deg,#000510,#001030,#000510);"></div>'}
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <span class="hero-eyebrow">◈ THE SCIENCE BEHIND ASTRASENSE</span>
        <div class="hero-title">Hunting Planets<br>Across the Stars</div>
        <div class="hero-desc">
            How do astronomers find worlds orbiting distant suns?
            How does AI recover faint signals buried in cosmic noise?
            Explore the science powering AstraSense — from photons
            to planets, from noise to discovery.
        </div>
    </div>
</div>

<div class="glow-div"></div>

<!-- CH 1 -->
<div class="section section-dark">
<div class="section-inner">
    <div class="two-col">
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 01</span>
            <span class="section-title">What Are Exoplanets?</span>
            <div class="section-body">
                <p>An <strong>exoplanet</strong> is any planet orbiting a star
                outside our Solar System. For most of human history we had no
                idea whether other stars harbored worlds. That changed in 1992
                when the first confirmed exoplanet was detected.</p>
                <p>Today NASA has confirmed over <strong>5,700 exoplanets</strong>
                across thousands of star systems — from scorching hot Jupiters
                racing around their stars in days, to icy super-Earths in habitable
                zones where liquid water might exist.</p>
                <p>The critical question: <strong>Are any of these worlds home
                to life?</strong> To answer it we must first find them — detecting
                incredibly faint signals in noisy telescope data.</p>
            </div>
            <div class="stat-row">
                <div class="stat-item reveal">
                    <div class="stat-val">5,700+</div>
                    <div class="stat-lbl">Confirmed Exoplanets</div>
                </div>
                <div class="stat-item reveal">
                    <div class="stat-val">4,000+</div>
                    <div class="stat-lbl">Star Systems</div>
                </div>
                <div class="stat-item reveal">
                    <div class="stat-val">1992</div>
                    <div class="stat-lbl">First Confirmed</div>
                </div>
                <div class="stat-item reveal">
                    <div class="stat-val">~20%</div>
                    <div class="stat-lbl">Sun-like w/ Earths</div>
                </div>
            </div>
        </div>
        <div class="img-panel reveal" style="height:390px;">
            {'<img src="' + ch1_src + '" alt="Exoplanet">' if ch1_src else '<div style="width:100%;height:100%;background:linear-gradient(135deg,#000a20,#001540);"></div>'}
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 2 -->
<div class="section section-mid">
<div class="section-inner">
    <div class="two-col reverse">
        <div class="img-panel reveal" style="height:360px;">
            {'<img src="' + ch2_src + '" alt="Transit method">' if ch2_src else '<div style="width:100%;height:100%;background:linear-gradient(135deg,#000a20,#001540);"></div>'}
        </div>
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 02</span>
            <span class="section-title">The Transit Detection Method</span>
            <div class="section-body">
                <p>The <strong>transit method</strong> is how NASA's Kepler and TESS
                missions find most exoplanets. When a planet passes in front of its
                host star it blocks a tiny fraction of the star's light — causing a
                brief measurable <strong>dimming</strong>.</p>
                <p>This dimming is recorded as a <strong>light curve</strong> — a
                graph of stellar brightness over time. A transit appears as a
                characteristic dip. By measuring its depth, duration and periodicity
                astronomers calculate the planet's size, orbital period and distance.</p>
                <p>The challenge: these dips are <strong>incredibly small</strong>.
                Jupiter blocks just 1% of its star's light. Earth blocks 0.01%.
                Detecting this against stellar noise is a monumental signal
                processing challenge.</p>
            </div>
        </div>
    </div>
    <div class="steps-grid">
        <div class="step-card reveal">
            <div class="step-num">01</div>
            <div class="step-title">Observe the Star</div>
            <div class="step-body">Telescope continuously monitors stellar
            brightness every few minutes over months or years.</div>
        </div>
        <div class="step-card reveal">
            <div class="step-num">02</div>
            <div class="step-title">Detect the Dip</div>
            <div class="step-body">A planet crossing the star causes brightness
            to drop 0.01–1%. This repeating pattern signals a candidate.</div>
        </div>
        <div class="step-card reveal">
            <div class="step-num">03</div>
            <div class="step-title">Measure Properties</div>
            <div class="step-body">Dip depth reveals planet radius. Period
            between transits gives orbital period. Duration constrains distance.</div>
        </div>
        <div class="step-card reveal">
            <div class="step-num">04</div>
            <div class="step-title">Confirm Discovery</div>
            <div class="step-body">Multiple transits, follow-up observations and
            radial velocity measurements confirm the planet is real.</div>
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 3 -->
<div class="section section-darker">
<div class="section-inner">
    <div class="two-col">
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 03</span>
            <span class="section-title">The Noise Problem</span>
            <div class="section-body">
                <p>Space telescopes are extraordinarily precise — but not
                perfect. Real telescope data is corrupted by multiple noise
                sources that can <strong>mask or mimic</strong> planetary
                transit signals.</p>
                <p><strong>Photon noise</strong> arises from the quantum nature
                of light itself. <strong>Stellar variability</strong> — starspots,
                flares and oscillations — causes the star's brightness to fluctuate.
                <strong>Instrument systematics</strong> come from thermal drifts and
                detector artifacts. <strong>Cosmic rays</strong> cause sudden spikes.</p>
                <p>Together these noise sources can bury a weak planetary signal
                completely. The SNR of faint transits can be below 1 — noise
                <strong>larger than the signal itself</strong>. This is where
                AI-powered denoising becomes essential.</p>
            </div>
        </div>
        <div class="img-panel reveal" style="height:360px;">
            {'<img src="' + ch3_src + '" alt="Kepler spacecraft">' if ch3_src else '<div style="width:100%;height:100%;background:linear-gradient(135deg,#000a20,#001540);"></div>'}
            <div class="img-caption">◈ NASA Kepler Space Telescope — discovered 2,600+ exoplanets</div>
        </div>
    </div>
    <div class="compare-grid" style="margin-top:2.5rem;">
        <div class="compare-card reveal">
            <div class="ccard-icon">⚡</div>
            <div class="ccard-title">Photon Noise</div>
            <div class="ccard-body">Fundamental quantum limit. Even perfect
            instruments suffer from random photon arrival. Scales as √N.</div>
        </div>
        <div class="compare-card reveal">
            <div class="ccard-icon">🌟</div>
            <div class="ccard-title">Stellar Variability</div>
            <div class="ccard-body">Stars are not static. Sunspots, granulation
            and oscillations create brightness variations that mimic or
            obscure planetary signals.</div>
        </div>
        <div class="compare-card reveal">
            <div class="ccard-icon">🛰️</div>
            <div class="ccard-title">Instrument Systematics</div>
            <div class="ccard-body">Thermal drifts, pointing jitter and detector
            pixel variations introduce correlated noise that traditional
            filters struggle to remove.</div>
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 4 -->
<div class="section section-dark">
<div class="section-inner">
    <div class="two-col reverse">
        <div class="img-panel reveal" style="height:360px;">
            <div style="position:absolute;inset:0;
                 background:linear-gradient(135deg,
                     rgba(0,5,30,0.97),rgba(0,15,60,0.92));
                 display:flex;align-items:center;
                 justify-content:center;padding:2rem;">
                <div style="text-align:center;">
                    <div style="font-family:'Share Tech Mono',monospace;
                         font-size:0.62rem;color:rgba(0,200,255,0.55);
                         letter-spacing:0.3rem;margin-bottom:1.5rem;">
                        THE DIFFUSION PROCESS
                    </div>
                    <div style="display:flex;align-items:center;
                         gap:1rem;justify-content:center;flex-wrap:wrap;">
                        <div style="text-align:center;">
                            <div style="font-family:'Orbitron',monospace;
                                 font-size:0.65rem;color:#00FF88;
                                 margin-bottom:0.4rem;">CLEAN</div>
                            <div style="width:60px;height:40px;
                                 background:rgba(0,255,136,0.15);
                                 border:1px solid rgba(0,255,136,0.3);
                                 border-radius:6px;"></div>
                        </div>
                        <div style="font-family:'Orbitron',monospace;
                             font-size:0.7rem;color:rgba(0,200,255,0.5);">
                             →→→<br>
                             <span style="font-size:0.48rem;color:rgba(0,180,255,0.4);">
                             ADD NOISE</span>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Orbitron',monospace;
                                 font-size:0.65rem;color:#FF8C00;
                                 margin-bottom:0.4rem;">NOISY</div>
                            <div style="width:60px;height:40px;
                                 background:rgba(255,140,0,0.15);
                                 border:1px solid rgba(255,140,0,0.3);
                                 border-radius:6px;"></div>
                        </div>
                        <div style="font-family:'Orbitron',monospace;
                             font-size:0.7rem;color:rgba(0,200,255,0.5);">
                             ←←←<br>
                             <span style="font-size:0.48rem;color:rgba(0,180,255,0.4);">
                             AI LEARNS</span>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Orbitron',monospace;
                                 font-size:0.65rem;color:#00D4FF;
                                 margin-bottom:0.4rem;">DENOISED</div>
                            <div style="width:60px;height:40px;
                                 background:rgba(0,212,255,0.15);
                                 border:1px solid rgba(0,212,255,0.3);
                                 border-radius:6px;"></div>
                        </div>
                    </div>
                    <div style="font-family:'Share Tech Mono',monospace;
                         font-size:0.52rem;color:rgba(0,180,255,0.4);
                         margin-top:2rem;line-height:2.2;letter-spacing:0.1rem;">
                        FORWARD: X₀ → X₁ → · · · → X₁₀₀₀<br>
                        REVERSE: X₁₀₀₀ → · · · → X₁ → X₀
                    </div>
                    <div style="margin-top:1.5rem;font-family:'Share Tech Mono',monospace;
                         font-size:0.5rem;color:rgba(100,165,230,0.45);
                         line-height:2.2;letter-spacing:0.1rem;">
                        TIMESTEPS &nbsp;: 1,000 &nbsp;·&nbsp;
                        SCHEDULE &nbsp;: LINEAR BETA<br>
                        TRAINED ON: 133,413 NASA POINTS
                    </div>
                </div>
            </div>
        </div>
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 04</span>
            <span class="section-title">How DDPM Works</span>
            <div class="section-body">
                <p>A <strong>Denoising Diffusion Probabilistic Model (DDPM)</strong>
                is a class of generative AI originally developed for image synthesis.
                AstraSense adapts this for 1D astronomical time series.</p>
                <p>During training the model observes clean light curves gradually
                corrupted by noise over 1,000 steps — from pristine signal to pure
                Gaussian noise. It learns the <strong>statistical pattern of
                this corruption</strong>.</p>
                <p>At inference time, given a noisy signal, the model runs the
                process in reverse — iteratively removing noise step by step.
                The <strong>U-Net backbone</strong> preserves fine-grained transit
                features while suppressing noise at multiple frequency scales.</p>
                <p>This is fundamentally different from Savitzky-Golay which applies
                fixed math. DDPM <strong>learns the data distribution</strong> and
                recovers features that simple filters would smooth away.</p>
            </div>
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 5 -->
<div class="section section-mid">
<div class="section-inner">
    <div class="two-col">
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 05</span>
            <span class="section-title">The U-Net Architecture</span>
            <div class="section-body">
                <p>The <strong>U-Net</strong> was originally designed for
                biomedical image segmentation. Its encoder-decoder structure
                with <strong>skip connections</strong> makes it ideal for
                signal restoration — capturing both coarse structure and
                fine detail simultaneously.</p>
                <p>In AstraSense the 1D U-Net processes 512-point light curve
                segments. The <strong>encoder</strong> progressively downsamples
                capturing noise patterns at multiple timescales. The
                <strong>decoder</strong> upsamples back to full resolution
                guided by skip connections that preserve transit shape details.</p>
                <p>A <strong>time embedding</strong> module encodes the diffusion
                timestep, allowing the model to behave differently at different
                denoising stages — aggressive early on, precise in final steps.</p>
            </div>
        </div>
        <div class="reveal" style="background:rgba(0,5,25,0.95);
             border:1px solid rgba(0,150,255,0.15);
             border-radius:14px;padding:1.5rem;">
            <div style="text-align:center;font-family:'Orbitron',monospace;
                 font-size:0.62rem;color:#00d4ff;letter-spacing:0.3rem;
                 margin-bottom:1.2rem;">U-NET ARCHITECTURE</div>
            <div style="display:flex;flex-direction:column;gap:0.45rem;">
                <div style="background:rgba(0,100,200,0.18);
                     border:1px solid rgba(0,150,255,0.28);
                     border-radius:6px;padding:0.35rem 0.8rem;
                     font-family:'Share Tech Mono',monospace;
                     font-size:0.54rem;color:rgba(0,200,255,0.7);text-align:center;">
                     INPUT · 512 POINTS</div>
                <div style="padding-left:0.8rem;">
                    <div style="background:rgba(0,80,180,0.18);
                         border:1px solid rgba(0,130,255,0.22);
                         border-radius:6px;padding:0.35rem 0.8rem;
                         font-family:'Share Tech Mono',monospace;
                         font-size:0.54rem;color:rgba(0,180,255,0.7);text-align:center;">
                         ENCODER L1 · CONV + NORM</div>
                </div>
                <div style="padding-left:1.6rem;">
                    <div style="background:rgba(0,60,150,0.18);
                         border:1px solid rgba(0,100,220,0.2);
                         border-radius:6px;padding:0.35rem 0.8rem;
                         font-family:'Share Tech Mono',monospace;
                         font-size:0.54rem;color:rgba(0,160,255,0.7);text-align:center;">
                         BOTTLENECK · 128 pts</div>
                </div>
                <div style="padding-left:0.8rem;">
                    <div style="background:rgba(0,80,180,0.18);
                         border:1px solid rgba(0,130,255,0.22);
                         border-radius:6px;padding:0.35rem 0.8rem;
                         font-family:'Share Tech Mono',monospace;
                         font-size:0.54rem;color:rgba(0,180,255,0.7);text-align:center;">
                         DECODER L1 · UPSAMPLE</div>
                    <div style="font-family:'Share Tech Mono',monospace;
                         font-size:0.48rem;color:rgba(0,220,120,0.45);
                         text-align:right;margin-top:0.2rem;">← skip connection</div>
                </div>
                <div style="background:rgba(0,100,200,0.18);
                     border:1px solid rgba(0,150,255,0.28);
                     border-radius:6px;padding:0.35rem 0.8rem;
                     font-family:'Share Tech Mono',monospace;
                     font-size:0.54rem;color:rgba(0,200,255,0.7);text-align:center;">
                     OUTPUT · 512 POINTS</div>
            </div>
            <div style="margin-top:1rem;padding-top:0.8rem;
                 border-top:1px solid rgba(0,100,180,0.15);
                 font-family:'Share Tech Mono',monospace;
                 font-size:0.5rem;color:rgba(100,165,230,0.45);
                 line-height:2.2;letter-spacing:0.1rem;">
                PARAMETERS &nbsp;: 2,877,441<br>
                TIME EMBED &nbsp;&nbsp;: 128-DIM SINUSOIDAL<br>
                TRAINING &nbsp;&nbsp;&nbsp;: 133,413 NASA PTS<br>
                HARDWARE &nbsp;&nbsp;&nbsp;: RTX 3050 · 6GB VRAM
            </div>
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 6 -->
<div class="section section-darker">
<div class="section-inner">
    <span class="section-eyebrow">◈ CHAPTER 06</span>
    <span class="section-title">Results & Impact</span>
    <div class="section-body" style="max-width:680px;margin-bottom:2rem;">
        <p>AstraSense was trained and evaluated on real NASA Kepler data
        from 4 exoplanet host stars, compared against two classical
        denoising baselines used in professional astronomy.</p>
    </div>
    <div class="compare-grid">
        <div class="compare-card reveal"
             style="border-color:rgba(0,212,255,0.28);background:rgba(0,15,50,0.92);">
            <div class="ccard-icon">🤖</div>
            <div class="ccard-title">DDPM — AstraSense</div>
            <div class="ccard-rmse" style="color:#00D4FF;">2.75</div>
            <div style="font-family:'Share Tech Mono',monospace;
                 font-size:0.48rem;color:rgba(0,190,255,0.45);">RMSE</div>
            <div class="ccard-body">Deep learning trained on 133K real NASA
            data points. Learns statistical structure of stellar noise.</div>
        </div>
        <div class="compare-card reveal">
            <div class="ccard-icon">📐</div>
            <div class="ccard-title">Savitzky-Golay</div>
            <div class="ccard-rmse" style="color:#00FF88;">2.03</div>
            <div style="font-family:'Share Tech Mono',monospace;
                 font-size:0.48rem;color:rgba(0,190,255,0.45);">RMSE</div>
            <div class="ccard-body">60-year-old polynomial smoothing.
            Industry standard — still competitive but lacks adaptability.</div>
        </div>
        <div class="compare-card reveal">
            <div class="ccard-icon">📊</div>
            <div class="ccard-title">Median Filter</div>
            <div class="ccard-rmse" style="color:#FF8C00;">3.01</div>
            <div style="font-family:'Share Tech Mono',monospace;
                 font-size:0.48rem;color:rgba(0,190,255,0.45);">RMSE</div>
            <div class="ccard-body">Classical sliding median window.
            Robust to outliers but blurs sharp transit edges.</div>
        </div>
    </div>
    <div class="reveal" style="background:rgba(0,15,50,0.7);
         border:1px solid rgba(0,180,255,0.15);border-radius:12px;
         padding:1.2rem 1.5rem;margin-top:1.5rem;
         font-family:'Exo 2',sans-serif;font-size:0.84rem;
         color:rgba(178,218,255,0.62);line-height:1.85;font-weight:300;">
        <strong style="color:#00d4ff;">Key finding:</strong>
        AstraSense DDPM beats the 60-year-old Median Filter and is
        competitive with Savitzky-Golay — demonstrating that modern
        deep learning can match and exceed classical methods even when
        trained on a consumer laptop GPU with limited data.
    </div>
</div>
</div>

<div class="glow-div"></div>

<!-- CH 7 -->
<div class="section section-dark">
<div class="section-inner">
    <div class="two-col">
        <div class="reveal">
            <span class="section-eyebrow">◈ CHAPTER 07</span>
            <span class="section-title">Milestones in Exoplanet Science</span>
            <div class="timeline">
                <div class="t-item">
                    <div class="t-dot"></div>
                    <div class="t-year">1992</div>
                    <div class="t-title">First Confirmed Exoplanet</div>
                    <div class="t-body">Wolszczan & Frail detect planets
                    orbiting pulsar PSR 1257+12 using timing variations.</div>
                </div>
                <div class="t-item">
                    <div class="t-dot"></div>
                    <div class="t-year">2009</div>
                    <div class="t-title">Kepler Space Telescope Launches</div>
                    <div class="t-body">NASA launches Kepler which discovers
                    over 2,600 confirmed exoplanets using transit photometry.</div>
                </div>
                <div class="t-item">
                    <div class="t-dot"></div>
                    <div class="t-year">2015</div>
                    <div class="t-title">Kepler-452b Discovered</div>
                    <div class="t-body">The most Earth-like planet found —
                    a super-Earth in the habitable zone of a Sun-like star,
                    1,400 light-years away.</div>
                </div>
                <div class="t-item">
                    <div class="t-dot"></div>
                    <div class="t-year">2018</div>
                    <div class="t-title">TESS Mission Begins</div>
                    <div class="t-body">Transiting Exoplanet Survey Satellite
                    extends planet hunting to the nearest brightest stars.</div>
                </div>
               
            </div>
        </div>
        <div class="img-panel reveal" style="height:500px;">
            {'<img src="' + ch7_src + '" alt="TESS satellite">' if ch7_src else '<div style="width:100%;height:100%;background:linear-gradient(135deg,#000a20,#001540);"></div>'}
            <div class="img-caption">◈ NASA TESS — Transiting Exoplanet Survey Satellite</div>
        </div>
    </div>
</div>
</div>

<div class="glow-div"></div>

<div class="page-footer">
    <span class="footer-logo">◈ ASTRASENSE</span>
    <div class="footer-txt">
        DEEP LEARNING EXOPLANET SIGNAL ENHANCEMENT &nbsp;◈&nbsp;
        1D DDPM U-NET &nbsp;◈&nbsp; NASA KEPLER / TESS &nbsp;◈&nbsp; RTX 3050 GPU
    </div>
</div>

<script>
(function(){{
    var els = document.querySelectorAll('.reveal');
    var obs = new IntersectionObserver(function(entries){{
        entries.forEach(function(e){{
            if(e.isIntersecting) e.target.classList.add('visible');
        }});
    }},{{threshold:0.08}});
    els.forEach(function(el){{ obs.observe(el); }});
}})();
</script>
</body>
</html>"""

st.iframe(html, height=5800)