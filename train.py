import torch
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from model import UNet1D, DDPMScheduler
import warnings
warnings.filterwarnings('ignore')

# ============================================
#   ASTRASENSE — Training Pipeline (Updated)
#   Now trains on all 10 stars
#   Run locally after data_pipeline.py
# ============================================


class LightCurveDataset(Dataset):
    def __init__(self, csv_path, window_size=512, noise_level=0.002):
        df = pd.read_csv(csv_path)
        self.clean_flux  = df['clean_flux'].values.astype(np.float32)
        self.window_size = window_size
        self.noise_level = noise_level

        self.windows = []
        step = window_size // 2
        for i in range(0, len(self.clean_flux) - window_size, step):
            window = self.clean_flux[i:i + window_size]
            self.windows.append(window)

        print(f"   Dataset created: {len(self.windows)} windows of size {window_size}")

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        clean = self.windows[idx]
        mean  = clean.mean()
        std   = clean.std() + 1e-8
        clean = (clean - mean) / std

        noise = np.random.normal(0, self.noise_level, clean.shape).astype(np.float32)
        noisy = clean + noise

        return torch.FloatTensor(clean).unsqueeze(0), torch.FloatTensor(noisy).unsqueeze(0)


def train(
    csv_path      = "data/combined_lightcurves.csv",
    epochs        = 1000,
    batch_size    = 16,
    learning_rate = 5e-5,
    window_size   = 512,
    save_every    = 50,
    resume_from   = None,     # pass "models/best_model.pt" to fine-tune
):
    print("=" * 55)
    print("   ASTRASENSE — Training Started 🚀")
    print("   10 Star Systems — Extended Run")
    print("=" * 55)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n💻 Device         : {device}")
    if torch.cuda.is_available():
        print(f"   GPU            : {torch.cuda.get_device_name(0)}")

    print(f"\n📂 Loading dataset from {csv_path}...")
    dataset    = LightCurveDataset(csv_path, window_size=window_size)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True,
                            num_workers=0, pin_memory=torch.cuda.is_available())
    print(f"   Total windows      : {len(dataset)}")
    print(f"   Batches per epoch  : {len(dataloader)}")

    print(f"\n🧠 Building model...")
    model = UNet1D(in_channels=1, base_channels=64, time_embed_dim=128).to(device)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   Parameters         : {total_params:,}")

    # ── Resume from existing checkpoint if provided ──
    start_epoch = 0
    if resume_from and __import__('os').path.exists(resume_from):
        model.load_state_dict(torch.load(resume_from, map_location=device))
        print(f"   Resumed from       : {resume_from} ✅")

    scheduler  = DDPMScheduler(num_timesteps=1000, device=str(device))
    optimizer  = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    lr_sched   = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=epochs, eta_min=1e-6
    )

    epoch_losses  = []
    best_loss     = float('inf')

    print(f"\n🔁 Training for {epochs} epochs...")
    print("-" * 55)

    for epoch in range(start_epoch, epochs):
        model.train()
        batch_losses = []

        for clean, _ in dataloader:
            clean = clean.to(device)
            optimizer.zero_grad()
            loss = scheduler.get_loss(model, clean, device)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            batch_losses.append(loss.item())

        avg_loss = float(np.mean(batch_losses))
        epoch_losses.append(avg_loss)
        lr_sched.step()

        # ── Save best model ──
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), "models/best_model.pt")
            # Timestamped backup only every 100 epochs to save disk space
            if (epoch + 1) % 100 == 0:
                torch.save(model.state_dict(),
                           f"models/best_model_loss_{avg_loss:.4f}.pt")

        # ── Periodic checkpoint ──
        if (epoch + 1) % save_every == 0:
            torch.save(model.state_dict(),
                       f"models/checkpoint_epoch_{epoch+1}.pt")

        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"   Epoch [{epoch+1:4d}/{epochs}] | "
                  f"Loss: {avg_loss:.6f} | "
                  f"Best: {best_loss:.6f} | "
                  f"LR: {lr_sched.get_last_lr()[0]:.2e}")

    print("-" * 55)
    print(f"\n✅ Training complete!")
    print(f"   Best loss         : {best_loss:.6f}")
    print(f"   Model saved to    : models/best_model.pt")

    plot_training_curve(epoch_losses)
    return model, scheduler, epoch_losses


def plot_training_curve(losses):
    print(f"\n📊 Saving training curve...")
    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor('#050510')
    ax.set_facecolor('#0A0A2E')

    ax.plot(losses, color='#00D4FF', linewidth=1.5, label='Training Loss', alpha=0.85)
    if len(losses) > 10:
        smooth = pd.Series(losses).rolling(10).mean()
        ax.plot(smooth, color='#FF8C00', linewidth=2,
                linestyle='--', label='Smoothed (10-ep MA)')

    # Mark best epoch
    best_ep  = int(np.argmin(losses))
    best_val = losses[best_ep]
    ax.scatter([best_ep], [best_val], color='#FFD700', s=80,
               zorder=5, label=f'Best ep {best_ep+1} ({best_val:.4f})')

    ax.set_title('AstraSense — DDPM Training Loss · 10 Star Systems',
                 color='white', fontsize=13, pad=15)
    ax.set_xlabel('Epoch', color='gray')
    ax.set_ylabel('MSE Loss', color='gray')
    ax.tick_params(colors='gray')
    ax.legend(facecolor='#0A0A2E', labelcolor='white')
    ax.grid(True, alpha=0.12, color='#00D4FF')
    for spine in ax.spines.values():
        spine.set_color('#1a1a4e')

    plt.tight_layout()
    plt.savefig('outputs/training_curve.png',
                dpi=150, bbox_inches='tight', facecolor='#050510')
    print(f"   Saved to outputs/training_curve.png ✅")
    plt.close()


def test_denoising(model, scheduler,
                   csv_path="data/Kepler_452_lightcurve.csv"):
    """Quick sanity check on Kepler-452 after training."""
    print(f"\n🔬 Quick denoising test on {csv_path}...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    import os
    if not os.path.exists(csv_path):
        print(f"   ⚠️  {csv_path} not found — skipping test")
        return

    df         = pd.read_csv(csv_path)
    clean_flux = df['clean_flux'].values.astype(np.float32)[:512]
    noisy_flux = df['noisy_flux'].values.astype(np.float32)[:512]

    mean, std   = clean_flux.mean(), clean_flux.std() + 1e-8
    clean_norm  = (clean_flux - mean) / std
    noisy_norm  = (noisy_flux - mean) / std

    model.eval()
    with torch.no_grad():
        x        = torch.FloatTensor(noisy_norm).unsqueeze(0).unsqueeze(0).to(device)
        t        = torch.tensor([500], device=device)
        denoised = torch.clamp(model(x, t), -5, 5).squeeze().cpu().numpy()

    rmse = float(np.sqrt(np.mean((clean_norm - denoised[:len(clean_norm)])**2)))
    print(f"   Quick RMSE on Kepler-452 : {rmse:.4f}")
    print(f"   (Lower is better — target < 3.0)")
    _plot_test(clean_norm, noisy_norm, denoised)


def _plot_test(clean, noisy, denoised):
    fig, axes = plt.subplots(3, 1, figsize=(14, 9))
    fig.patch.set_facecolor('#050510')

    signals = [
        (noisy,    '#CC00FF', 'Noisy Input'),
        (denoised, '#00D4FF', 'AI Denoised Output'),
        (clean,    '#FF8C00', 'Clean Ground Truth'),
    ]
    for ax, (sig, col, title) in zip(axes, signals):
        ax.plot(sig, color=col, linewidth=0.9, alpha=0.9)
        ax.set_facecolor('#0A0A2E')
        ax.set_title(title, color='white', fontsize=11, pad=8)
        ax.set_ylabel('Normalized Flux', color=col, fontsize=9)
        ax.tick_params(colors='gray')
        ax.grid(True, alpha=0.12, color=col)
        for spine in ax.spines.values():
            spine.set_color('#1a1a4e')

    axes[-1].set_xlabel('Time Steps', color='gray')
    plt.tight_layout(pad=2.5)
    plt.savefig('outputs/denoising_result.png',
                dpi=150, bbox_inches='tight', facecolor='#050510')
    print(f"   Saved to outputs/denoising_result.png ✅")
    plt.close()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="AstraSense Training")
    parser.add_argument("--epochs",    type=int,   default=1000)
    parser.add_argument("--lr",        type=float, default=5e-5)
    parser.add_argument("--batch",     type=int,   default=16)
    parser.add_argument("--resume",    type=str,   default=None,
                        help="Path to checkpoint to resume/fine-tune from")
    parser.add_argument("--save-every",type=int,   default=50)
    args = parser.parse_args()

    model, scheduler, losses = train(
        csv_path      = "data/combined_lightcurves.csv",
        epochs        = args.epochs,
        batch_size    = args.batch,
        learning_rate = args.lr,
        window_size   = 512,
        save_every    = args.save_every,
        resume_from   = args.resume,
    )

    test_denoising(model, scheduler)

    print("\n" + "=" * 55)
    print("   Training Complete! 🎉")
    print("   Next: run evaluate.py to benchmark all 10 stars")
    print("=" * 55)