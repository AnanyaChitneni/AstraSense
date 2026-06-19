# ============================================
#   ASTRASENSE — Shared Utilities
# ============================================
import streamlit as st
import torch
import base64
import os

# ============================================
#   SHARED COLOR PALETTE
# ============================================
COLORS = {
    'bg':        '#000008',
    'panel':     'rgba(8,12,40,0.95)',
    'panel2':    'rgba(5,8,30,0.98)',
    'border':    'rgba(0,180,255,0.2)',
    'cyan':      '#00d4ff',
    'blue':      '#0066cc',
    'deepblue':  '#003388',
    'white':     '#ffffff',
    'gray':      'rgba(255,255,255,0.5)',
    'dimgray':   'rgba(255,255,255,0.25)',
    'orange':    '#ff8c00',
    'green':     '#00ff88',
    'red':       '#ff4444',
    'purple':    '#4433aa',
}

# ============================================
#   SHARED FONTS
# ============================================
FONTS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;500;600&display=swap');
"""

# ============================================
#   BASE CSS — used by ALL pages
# ============================================
BASE_CSS = f"""
<style>
{FONTS}

*, *::before, *::after {{
    box-sizing: border-box;
}}

html, body {{
    background-color: {COLORS['bg']} !important;
}}

.stApp {{
    background-color: {COLORS['bg']} !important;
}}

#MainMenu, footer, header,
[data-testid="stToolbar"] {{
    display: none !important;
    visibility: hidden !important;
}}

[data-testid="stSidebar"],
section[data-testid="stSidebar"] {{
    display: none !important;
}}

.main .block-container {{
    padding: 0 1.5rem 3rem 1.5rem !important;
    max-width: 1400px !important;
}}

/* GLOW LINE */
.glow-line {{
    height: 1px;
    background: linear-gradient(
        90deg, transparent,
        {COLORS['cyan']}, #4433aa,
        {COLORS['orange']}, transparent
    );
    margin: 1.8rem 0;
}}

/* SECTION TITLE */
.sec-title {{
    font-family: 'Orbitron', monospace;
    font-size: 0.72rem;
    color: {COLORS['cyan']};
    letter-spacing: 0.4rem;
    margin: 1.8rem 0 1rem 0;
    text-transform: uppercase;
}}

/* GLASS PANEL */
.glass {{
    background: {COLORS['panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(20px);
}}

/* METRIC CARD */
.metric-card {{
    background: {COLORS['panel2']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
    padding: 1.3rem 0.8rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    border-color: {COLORS['cyan']};
    box-shadow: 0 0 20px rgba(0,212,255,0.15);
    transform: translateY(-3px);
}}

.mval {{
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
}}

.mlbl {{
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.58rem;
    color: {COLORS['dimgray']};
    letter-spacing: 0.2rem;
    margin-top: 0.4rem;
}}

/* NAV BAR */
.nav-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid {COLORS['border']};
    margin-bottom: 0.5rem;
}}

.nav-logo {{
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 900;
    background: linear-gradient(135deg, {COLORS['cyan']}, #4433aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.3rem;
}}

.nav-links {{
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: {COLORS['gray']};
    letter-spacing: 0.2rem;
    display: flex;
    gap: 2rem;
}}

/* STATUS */
.status-live {{
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: {COLORS['green']};
    letter-spacing: 0.2rem;
    padding: 0.4rem 0;
}}

.status-proc {{
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: {COLORS['orange']};
    letter-spacing: 0.2rem;
    padding: 0.4rem 0;
}}

/* BUTTONS */
.stButton > button {{
    background: linear-gradient(
        135deg,
        rgba(0,100,200,0.2),
        rgba(0,50,150,0.3)
    ) !important;
    border: 1px solid rgba(0,180,255,0.5) !important;
    color: {COLORS['cyan']} !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2rem !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}}

.stButton > button:hover {{
    background: linear-gradient(
        135deg,
        rgba(0,150,255,0.3),
        rgba(0,80,200,0.4)
    ) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.3) !important;
    border-color: {COLORS['cyan']} !important;
}}

/* INPUTS */
.stTextInput > div > div > input {{
    background: rgba(5,8,30,0.95) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    color: white !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 10px !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {COLORS['cyan']} !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.2) !important;
}}

div[data-baseweb="select"] > div {{
    background: rgba(5,8,30,0.95) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    border-radius: 10px !important;
    color: white !important;
}}

/* PROGRESS */
.stProgress > div > div > div {{
    background: linear-gradient(
        90deg, {COLORS['cyan']}, #4433aa
    ) !important;
    border-radius: 10px !important;
}}

/* SCROLLBAR */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: #050510; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient({COLORS['cyan']}, #4433aa);
    border-radius: 4px;
}}

/* STAR CANVAS */
#star-canvas {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
}}

/* RESPONSIVE */
@media (max-width: 768px) {{
    .hero-title {{
        font-size: 2.5rem !important;
        letter-spacing: 0.2rem !important;
    }}
    .nav-links {{ display: none; }}
    .main .block-container {{
        padding: 0 0.8rem 2rem 0.8rem !important;
    }}
}}
</style>
"""

# ============================================
#   STAR PARTICLES JS
# ============================================
STAR_JS = """
<canvas id="star-canvas"></canvas>
<script>
(function(){
    function run(){
        var c=document.getElementById('star-canvas');
        if(!c){setTimeout(run,500);return;}
        var ctx=c.getContext('2d');
        c.width=window.innerWidth;
        c.height=window.innerHeight;
        var stars=[];
        var cols=['#00d4ff','#0066cc','#ffffff',
                  '#ffffff','#ffffff','#003388'];
        for(var i=0;i<300;i++){
            stars.push({
                x:Math.random()*c.width,
                y:Math.random()*c.height,
                r:Math.random()*1.5+0.2,
                a:Math.random()*Math.PI*2,
                s:Math.random()*0.006+0.002,
                col:cols[Math.floor(Math.random()*cols.length)]
            });
        }
        var shoots=[];
        setInterval(function(){
            shoots.push({
                x:Math.random()*c.width*0.8,
                y:Math.random()*c.height*0.3,
                l:Math.random()*120+60,
                sp:Math.random()*8+4,
                a:1
            });
        },3000);
        function draw(){
            ctx.clearRect(0,0,c.width,c.height);
            stars.forEach(function(s){
                var al=(Math.sin(Date.now()*s.s+s.a)+1)/2;
                ctx.beginPath();
                ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
                ctx.fillStyle=s.col;
                ctx.globalAlpha=al*0.9;
                ctx.fill();
                if(s.r>1.2){
                    var g=ctx.createRadialGradient(
                        s.x,s.y,0,s.x,s.y,s.r*4);
                    g.addColorStop(0,s.col);
                    g.addColorStop(1,'transparent');
                    ctx.beginPath();
                    ctx.arc(s.x,s.y,s.r*4,0,Math.PI*2);
                    ctx.fillStyle=g;
                    ctx.globalAlpha=al*0.15;
                    ctx.fill();
                }
                ctx.globalAlpha=1;
            });
            shoots.forEach(function(sh,i){
                ctx.beginPath();
                ctx.moveTo(sh.x,sh.y);
                ctx.lineTo(sh.x-sh.l,sh.y-sh.l*0.2);
                var g=ctx.createLinearGradient(
                    sh.x,sh.y,sh.x-sh.l,sh.y-sh.l*0.2);
                g.addColorStop(0,'rgba(255,255,255,'+sh.a+')');
                g.addColorStop(1,'rgba(0,0,0,0)');
                ctx.strokeStyle=g;
                ctx.lineWidth=1.5;
                ctx.globalAlpha=sh.a;
                ctx.stroke();
                ctx.globalAlpha=1;
                sh.x+=sh.sp;
                sh.y+=sh.sp*0.2;
                sh.a-=0.02;
                if(sh.a<=0)shoots.splice(i,1);
            });
            requestAnimationFrame(draw);
        }
        draw();
        window.addEventListener('resize',function(){
            c.width=window.innerWidth;
            c.height=window.innerHeight;
        });
    }
    run();
})();
</script>
"""

# ============================================
#   NAVIGATION BAR
# ============================================
def render_nav(current_page="Home"):
    pages = {
        "Home":            "/",
        "Analysis":        "/Analysis",
        "Star Catalogue":  "/Star_Catalogue",
        "Noise Lab":       "/Noise_Lab",
        "Science":         "/Science",
        "Performance":     "/Performance",
    }
    links_html = ""
    for name, path in pages.items():
        active = "color:#00d4ff;" if name == current_page else ""
        links_html += f"""
            <a href="{path}" target="_self"
               style="text-decoration:none;
                      font-family:'Share Tech Mono',monospace;
                      font-size:0.68rem;
                      letter-spacing:0.15rem;
                      color:rgba(255,255,255,0.55);
                      {active}
                      transition:color 0.2s;">
                {name.upper()}
            </a>
        """
    st.markdown(f"""
        <div class='nav-bar'>
            <div class='nav-logo'>◈ ASTRASENSE</div>
            <div style='display:flex;gap:2rem;
                        flex-wrap:wrap;justify-content:flex-end;'>
                {links_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


# ============================================
#   IMAGE TO BASE64 (for local images)
# ============================================
def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


# ============================================
#   INSTRUMENT PANEL BACKGROUND
# (used by Catalogue, Noise Lab, Performance)
# ============================================
INSTRUMENT_BG = """
<style>
.inst-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: -1;
    background:
        radial-gradient(ellipse at 15% 50%,
            rgba(0,40,100,0.35) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%,
            rgba(0,20,80,0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 90%,
            rgba(0,10,50,0.4) 0%, transparent 60%),
        linear-gradient(180deg,
            #000510 0%,
            #000818 40%,
            #000510 100%);
}

/* Subtle grid overlay */
.inst-bg::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,100,200,0.03) 1px,
                        transparent 1px),
        linear-gradient(90deg,
                        rgba(0,100,200,0.03) 1px,
                        transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
}
</style>
<div class='inst-bg'></div>
"""


# ============================================
#   PLOTLY CHART DEFAULTS
# ============================================
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(5,8,30,0.95)',
    font=dict(
        family='Share Tech Mono',
        color='rgba(255,255,255,0.5)',
        size=9
    ),
    margin=dict(l=50, r=20, t=50, b=40),
)

GRID_COLOR  = 'rgba(0,100,200,0.08)'
LINE_COLOR  = 'rgba(0,180,255,0.15)'
TICK_STYLE  = dict(
    family='Share Tech Mono',
    size=8,
    color='rgba(255,255,255,0.3)'
)