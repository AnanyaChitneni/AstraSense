# utils/mobile.py
# Shared mobile CSS injected into every page

MOBILE_CSS = """
<style>
/* ── GLOBAL MOBILE RESETS ── */
@media (max-width: 768px) {

    /* Block container padding */
    .main .block-container {
        padding-left: 0.4rem !important;
        padding-right: 0.4rem !important;
        padding-top: 0 !important;
    }

    /* Streamlit columns stack on mobile */
    [data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
    }

    /* Dataframes scroll horizontally */
    [data-testid="stDataFrame"] {
        overflow-x: auto !important;
    }
}
</style>
"""