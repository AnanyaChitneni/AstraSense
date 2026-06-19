import lightkurve as lk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================
#   ASTRASENSE — Data Pipeline (Updated)
#   Original 4 stars + 6 new stars = 10 total
# ============================================

def fetch_kepler_data(star_name="Kepler-452", quarter=3):
    """
    Fetches real light curve data from NASA Kepler telescope.
    Tries multiple quarters if the requested one has no data.
    """
    print(f"\n🌟 Fetching light curve for {star_name}...")
    print("   Connecting to NASA MAST archive...")

    for q in [quarter, 1, 2, 4, 5, 6]:
        try:
            search_result = lk.search_lightcurve(
                star_name, mission="Kepler", quarter=q
            )
            if len(search_result) == 0:
                continue
            lc = search_result[0].download()
            print(f"   Found {len(search_result)} observation(s) — Quarter {q} ✅")
            return lc
        except Exception as e:
            print(f"   Quarter {q} failed: {e}")
            continue

    print(f"   ❌ Could not fetch {star_name} from any quarter")
    return None


def preprocess_lightcurve(lc):
    """
    Cleans and normalizes the raw light curve data.
    """
    print(f"\n⚙️  Preprocessing light curve...")

    lc = lc.remove_nans()
    lc = lc.normalize()

    time = lc.time.value
    flux = lc.flux.value

    print(f"   Total data points : {len(time)}")
    print(f"   Time range        : {time[0]:.2f} to {time[-1]:.2f} (BJD days)")
    print(f"   Flux range        : {flux.min():.4f} to {flux.max():.4f}")
    print(f"   Preprocessing done ✅")

    return time, flux


def inject_noise(flux, noise_level=0.002):
    """
    Adds synthetic Gaussian noise to clean flux.
    """
    print(f"\n🔊 Injecting synthetic noise (level={noise_level})...")
    noise = np.random.normal(0, noise_level, size=flux.shape)
    noisy_flux = flux + noise
    print(f"   Noise injected ✅")
    return noisy_flux


def save_data(time, flux, noisy_flux, star_name="Kepler-452"):
    """
    Saves the clean and noisy data to CSV files.
    """
    print(f"\n💾 Saving data to CSV...")
    df = pd.DataFrame({
        'time': time,
        'clean_flux': flux,
        'noisy_flux': noisy_flux
    })
    filename = f"data/{star_name.replace('-','_')}_lightcurve.csv"
    df.to_csv(filename, index=False)
    print(f"   Saved to {filename} ✅")
    return df


def plot_lightcurve(time, flux, noisy_flux, star_name="Kepler-452"):
    """
    Plots the clean vs noisy light curve.
    """
    print(f"\n📊 Generating plot...")

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    fig.patch.set_facecolor('#050510')

    axes[0].plot(time, flux, color='#00D4FF', linewidth=0.8, alpha=0.9)
    axes[0].set_facecolor('#0A0A2E')
    axes[0].set_title(f'{star_name} — Clean Light Curve (NASA Kepler)',
                      color='white', fontsize=13, pad=10)
    axes[0].set_ylabel('Normalized Flux', color='#00D4FF')
    axes[0].tick_params(colors='gray')
    for spine in axes[0].spines.values():
        spine.set_color('#1a1a4e')
    axes[0].grid(True, alpha=0.15, color='#00D4FF')

    axes[1].plot(time, noisy_flux, color='#CC00FF', linewidth=0.6, alpha=0.8)
    axes[1].set_facecolor('#0A0A2E')
    axes[1].set_title(f'{star_name} — Noisy Light Curve (Simulated Telescope Noise)',
                      color='white', fontsize=13, pad=10)
    axes[1].set_ylabel('Normalized Flux', color='#CC00FF')
    axes[1].set_xlabel('Time (BJD — Barycentric Julian Date)', color='gray')
    axes[1].tick_params(colors='gray')
    for spine in axes[1].spines.values():
        spine.set_color('#1a1a4e')
    axes[1].grid(True, alpha=0.15, color='#CC00FF')

    plt.tight_layout(pad=3.0)
    plt.savefig(f'outputs/lightcurve_{star_name.replace("-","_")}.png',
                dpi=150, bbox_inches='tight', facecolor='#050510')
    print(f"   Plot saved ✅")
    plt.close()


# ============================================
#   MAIN — All 10 Stars
# ============================================
if __name__ == "__main__":

    print("=" * 55)
    print("   ASTRASENSE — Fetching All 10 Stars")
    print("=" * 55)

    original_stars = [
        ("Kepler-452", 3),
        ("Kepler-7",   3),
        ("Kepler-10",  3),
        ("Kepler-22",  3),
    ]

    new_stars = [
        ("Kepler-16",  3),
        ("Kepler-62",  3),
        ("Kepler-186", 3),
        ("Kepler-69",  3),
        ("Kepler-442", 5),
        ("Kepler-90",  3),
    ]

    import os
    all_dataframes = []

    print("\n📂 Loading existing original star data...")
    for star_name, _ in original_stars:
        csv_path = f"data/{star_name.replace('-','_')}_lightcurve.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            all_dataframes.append(df)
            print(f"   ✅ {star_name} loaded from CSV ({len(df):,} points)")
        else:
            print(f"   ⚠️  {star_name} CSV not found — fetching...")
            lc = fetch_kepler_data(star_name=star_name, quarter=3)
            if lc is not None:
                time, flux = preprocess_lightcurve(lc)
                noisy_flux = inject_noise(flux, noise_level=0.002)
                df = save_data(time, flux, noisy_flux, star_name=star_name)
                all_dataframes.append(df)

    print(f"\n{'='*55}")
    print("   Fetching 6 new star systems...")
    print(f"{'='*55}")

    for star_name, quarter in new_stars:
        csv_path = f"data/{star_name.replace('-','_')}_lightcurve.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            all_dataframes.append(df)
            print(f"\n   ✅ {star_name} already fetched ({len(df):,} points) — skipping")
            continue

        try:
            print(f"\n{'='*40}")
            lc = fetch_kepler_data(star_name=star_name, quarter=quarter)
            if lc is None:
                print(f"   ❌ {star_name} — no data found, skipping")
                continue
            time, flux = preprocess_lightcurve(lc)
            noisy_flux = inject_noise(flux, noise_level=0.002)
            df = save_data(time, flux, noisy_flux, star_name=star_name)
            all_dataframes.append(df)
            print(f"   ✅ {star_name} done! ({len(df):,} points)")
        except Exception as e:
            print(f"   ❌ {star_name} failed: {e}")
            continue

    if all_dataframes:
        combined = pd.concat(all_dataframes, ignore_index=True)
        combined.to_csv("data/combined_lightcurves.csv", index=False)
        print(f"\n{'='*55}")
        print(f"✅ Combined dataset rebuilt!")
        print(f"   Total data points : {len(combined):,}")
        print(f"   Stars included    : {len(all_dataframes)}")
        print(f"   Saved to          : data/combined_lightcurves.csv")
        print(f"{'='*55}")
    else:
        print("\n❌ No data collected — check your internet connection")