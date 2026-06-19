import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, medfilt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from model import UNet1D, DDPMScheduler
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================
#   ASTRASENSE — Evaluation (Updated — 10 stars)
# ============================================

# All 10 stars — evaluates whichever CSVs exist
ALL_STARS = [
    "Kepler-452",
    "Kepler-7",
    "Kepler-10",
    "Kepler-22",
    "Kepler-16",
    "Kepler-62",
    "Kepler-186",
    "Kepler-69",
    "Kepler-442",
    "Kepler-90",
]


def load_model(model_path="models/best_model.pt"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UNet1D(in_channels=1, base_channels=64, time_embed_dim=128).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    print(f"   Model loaded from {model_path} ✅")
    return model, device


def savgol_denoise(noisy_signal, window=51, poly=3):
    return savgol_filter(noisy_signal, window_length=window, polyorder=poly)


def median_denoise(noisy_signal, kernel=11):
    return medfilt(noisy_signal, kernel_size=kernel)


def calculate_metrics(clean, denoised, method_name):
    min_len = min(len(clean), len(denoised))
    clean    = clean[:min_len]
    denoised = denoised[:min_len]

    rmse = np.sqrt(mean_squared_error(clean, denoised))
    mae  = mean_absolute_error(clean, denoised)
    signal_power = np.mean(clean ** 2)
    noise_power  = np.mean((clean - denoised) ** 2)
    snr  = 10 * np.log10(signal_power / (noise_power + 1e-10))

    return {"method": method_name, "RMSE": rmse, "MAE": mae, "SNR": snr}


def evaluate_star(star_name, model, scheduler, device):
    csv_path = f"data/{star_name.replace('-','_')}_lightcurve.csv"
    if not os.path.exists(csv_path):
        print(f"   ⚠️  {star_name} CSV not found — skipping")
        return None

    df = pd.read_csv(csv_path)
    clean_flux = df['clean_flux'].values.astype(np.float32)[:512]
    noisy_flux = df['noisy_flux'].values.astype(np.float32)[:512]

    mean, std   = clean_flux.mean(), clean_flux.std() + 1e-8
    clean_norm  = (clean_flux - mean) / std
    noisy_norm  = (noisy_flux - mean) / std

    # DDPM direct denoise
    model.eval()
    with torch.no_grad():
        x = torch.FloatTensor(noisy_norm).unsqueeze(0).unsqueeze(0).to(device)
        t = torch.tensor([500], device=device)
        ddpm_out = torch.clamp(model(x, t), -5, 5).squeeze().cpu().numpy()

    savgol_out = savgol_denoise(noisy_norm)
    median_out = median_denoise(noisy_norm)

    m_ddpm   = calculate_metrics(clean_norm, ddpm_out,   "DDPM")
    m_savgol = calculate_metrics(clean_norm, savgol_out, "Savitzky-Golay")
    m_median = calculate_metrics(clean_norm, median_out, "Median Filter")

    return {
        "star":         star_name,
        "ddpm_rmse":    round(m_ddpm["RMSE"],   4),
        "savgol_rmse":  round(m_savgol["RMSE"],  4),
        "median_rmse":  round(m_median["RMSE"],  4),
        "ddpm_mae":     round(m_ddpm["MAE"],     4),
        "ddpm_snr":     round(m_ddpm["SNR"],     2),
        "beats_median": m_ddpm["RMSE"] < m_median["RMSE"],
    }


def plot_all_stars_comparison(results):
    stars      = [r["star"] for r in results]
    ddpm_vals  = [r["ddpm_rmse"]   for r in results]
    savgol_vals= [r["savgol_rmse"] for r in results]
    median_vals= [r["median_rmse"] for r in results]

    x     = np.arange(len(stars))
    width = 0.26

    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor('#050510')
    ax.set_facecolor('#0A0A2E')

    ax.bar(x - width, ddpm_vals,   width, label='DDPM (Ours)', color='#00D4FF', alpha=0.85)
    ax.bar(x,         savgol_vals, width, label='Savitzky-Golay', color='#00FF88', alpha=0.85)
    ax.bar(x + width, median_vals, width, label='Median Filter',  color='#FF4444', alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(stars, rotation=30, ha='right', color='gray', fontsize=9)
    ax.set_title('AstraSense — RMSE Comparison Across All Stars',
                 color='white', fontsize=13, pad=15)
    ax.set_ylabel('RMSE (lower = better)', color='gray')
    ax.tick_params(colors='gray')
    ax.legend(facecolor='#0A0A2E', labelcolor='white')
    ax.grid(True, alpha=0.1, color='#00D4FF', axis='y')
    for spine in ax.spines.values():
        spine.set_color('#1a1a4e')

    plt.tight_layout()
    plt.savefig('outputs/all_stars_comparison.png',
                dpi=150, bbox_inches='tight', facecolor='#050510')
    print(f"\n   Saved to outputs/all_stars_comparison.png ✅")
    plt.close()


if __name__ == "__main__":
    print("=" * 55)
    print("   ASTRASENSE — Full Evaluation (10 Stars) 🔬")
    print("=" * 55)

    print(f"\n🧠 Loading trained model...")
    model, device  = load_model("models/best_model.pt")
    device_str     = "cuda" if torch.cuda.is_available() else "cpu"
    scheduler      = DDPMScheduler(num_timesteps=1000, device=device_str)

    all_results = []
    print(f"\n🔄 Evaluating all stars...")
    print("-" * 55)

    for star_name in ALL_STARS:
        print(f"\n   ⭐ {star_name}")
        result = evaluate_star(star_name, model, scheduler, device)
        if result is not None:
            all_results.append(result)
            print(f"      DDPM RMSE   : {result['ddpm_rmse']}")
            print(f"      SavGol RMSE : {result['savgol_rmse']}")
            print(f"      Median RMSE : {result['median_rmse']}")
            print(f"      Beats Median: {'✅' if result['beats_median'] else '❌'}")

    print("\n" + "=" * 55)
    print("   RESULTS SUMMARY")
    print("=" * 55)

    df_results = pd.DataFrame(all_results)
    print(df_results.to_string(index=False))

    beats = sum(1 for r in all_results if r["beats_median"])
    print(f"\n🏆 Beats Median Filter: {beats}/{len(all_results)} stars")
    print(f"📊 Avg DDPM RMSE      : {df_results['ddpm_rmse'].mean():.4f}")
    print(f"📊 Avg SavGol RMSE    : {df_results['savgol_rmse'].mean():.4f}")

    # Save results table
    df_results.to_csv("outputs/eval_results_all_stars.csv", index=False)
    print(f"\n   Results saved to outputs/eval_results_all_stars.csv ✅")

    plot_all_stars_comparison(all_results)

    print("\n" + "=" * 55)
    print("   Evaluation Complete 🎉")
    print("=" * 55)