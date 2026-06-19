import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# ============================================
#   ASTRASENSE — 1D U-Net + DDPM (Week 2)
# ============================================


class DoubleConv1D(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.GELU(),
            nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.GELU()
        )

    def forward(self, x):
        return self.block(x)


class TimeEmbedding(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        self.embed_dim = embed_dim
        self.linear = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Linear(embed_dim * 4, embed_dim)
        )

    def forward(self, t):
        half = self.embed_dim // 2
        freqs = torch.exp(
            -np.log(10000) * torch.arange(half, device=t.device) / half
        ).float()
        args = t[:, None].float() * freqs[None]
        embedding = torch.cat([torch.sin(args), torch.cos(args)], dim=-1)
        return self.linear(embedding)


class UNet1D(nn.Module):
    def __init__(self, in_channels=1, base_channels=64, time_embed_dim=128):
        super().__init__()

        self.time_embed = TimeEmbedding(time_embed_dim)

        # ---- ENCODER ----
        self.enc1 = DoubleConv1D(in_channels, base_channels)
        self.enc2 = DoubleConv1D(base_channels, base_channels * 2)
        self.enc3 = DoubleConv1D(base_channels * 2, base_channels * 4)

        self.down1 = nn.MaxPool1d(2)
        self.down2 = nn.MaxPool1d(2)
        self.down3 = nn.MaxPool1d(2)

        # ---- BOTTLENECK ----
        self.bottleneck = DoubleConv1D(base_channels * 4, base_channels * 8)

        # ---- DECODER ----
        self.up1 = nn.ConvTranspose1d(base_channels * 8, base_channels * 4, kernel_size=2, stride=2)
        self.dec1 = DoubleConv1D(base_channels * 8, base_channels * 4)

        self.up2 = nn.ConvTranspose1d(base_channels * 4, base_channels * 2, kernel_size=2, stride=2)
        self.dec2 = DoubleConv1D(base_channels * 4, base_channels * 2)

        self.up3 = nn.ConvTranspose1d(base_channels * 2, base_channels, kernel_size=2, stride=2)
        self.dec3 = DoubleConv1D(base_channels * 2, base_channels)

        self.out_conv = nn.Conv1d(base_channels, in_channels, kernel_size=1)

        self.time_proj1 = nn.Linear(time_embed_dim, base_channels)
        self.time_proj2 = nn.Linear(time_embed_dim, base_channels * 2)
        self.time_proj3 = nn.Linear(time_embed_dim, base_channels * 4)

    def forward(self, x, t):
        t_emb = self.time_embed(t)

        e1 = self.enc1(x)
        e1 = e1 + self.time_proj1(t_emb).unsqueeze(-1)

        e2 = self.enc2(self.down1(e1))
        e2 = e2 + self.time_proj2(t_emb).unsqueeze(-1)

        e3 = self.enc3(self.down2(e2))
        e3 = e3 + self.time_proj3(t_emb).unsqueeze(-1)

        b = self.bottleneck(self.down3(e3))

        d1 = self.up1(b)
        if d1.shape[-1] != e3.shape[-1]:
            d1 = F.pad(d1, (0, e3.shape[-1] - d1.shape[-1]))
        d1 = torch.cat([d1, e3], dim=1)
        d1 = self.dec1(d1)

        d2 = self.up2(d1)
        if d2.shape[-1] != e2.shape[-1]:
            d2 = F.pad(d2, (0, e2.shape[-1] - d2.shape[-1]))
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)

        d3 = self.up3(d2)
        if d3.shape[-1] != e1.shape[-1]:
            d3 = F.pad(d3, (0, e1.shape[-1] - d3.shape[-1]))
        d3 = torch.cat([d3, e1], dim=1)
        d3 = self.dec3(d3)

        return self.out_conv(d3)


class DDPMScheduler:
    def __init__(self, num_timesteps=1000, beta_start=0.0001, beta_end=0.02, device='cpu'):
        self.num_timesteps = num_timesteps
        self.device = device

        self.betas = torch.linspace(beta_start, beta_end, num_timesteps).to(device)
        self.alphas = (1.0 - self.betas).to(device)
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0).to(device)
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod).to(device)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - self.alphas_cumprod).to(device)

    def add_noise(self, clean_signal, noise, timestep):
        sqrt_alpha = self.sqrt_alphas_cumprod[timestep]
        sqrt_one_minus = self.sqrt_one_minus_alphas_cumprod[timestep]
        sqrt_alpha = sqrt_alpha.view(-1, 1, 1)
        sqrt_one_minus = sqrt_one_minus.view(-1, 1, 1)
        return sqrt_alpha * clean_signal + sqrt_one_minus * noise

    def get_loss(self, model, clean_signal, device):
        """
        Train U-Net to predict CLEAN signal directly
        from noisy input — much better for signal denoising
        """
        batch_size = clean_signal.shape[0]
        t = torch.randint(0, self.num_timesteps, (batch_size,), device=device)
        noise = torch.randn_like(clean_signal)
        noisy_signal = self.add_noise(clean_signal, noise, t)

        # Predict clean signal directly
        predicted_clean = model(noisy_signal, t)

        # Loss = how close to clean signal
        return F.mse_loss(predicted_clean, clean_signal)

    def direct_denoise(self, model, noisy_signal, device):
        """
        Direct denoising — one forward pass through U-Net
        Clean, fast, and much better than reverse diffusion
        for signal denoising tasks
        """
        model.eval()
        with torch.no_grad():
            x = torch.FloatTensor(noisy_signal).unsqueeze(0).unsqueeze(0).to(device)
            # Use timestep 500 — middle of noise schedule
            t = torch.tensor([500], device=device)
            denoised = model(x, t)
            denoised = torch.clamp(denoised, -5, 5)
            return denoised.squeeze().cpu().numpy()


if __name__ == "__main__":
    print("=" * 50)
    print("   ASTRASENSE — Testing Model Architecture")
    print("=" * 50)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n💻 Device: {device}")

    model = UNet1D(in_channels=1, base_channels=64, time_embed_dim=128).to(device)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"🧠 Total model parameters: {total_params:,}")

    batch_size = 4
    signal_length = 512
    x = torch.randn(batch_size, 1, signal_length).to(device)
    t = torch.randint(0, 1000, (batch_size,)).to(device)

    print(f"\n📡 Input shape  : {x.shape}")
    output = model(x, t)
    print(f"📡 Output shape : {output.shape}")

    scheduler = DDPMScheduler(num_timesteps=1000, device=str(device))
    loss = scheduler.get_loss(model, x, device)
    print(f"\n📉 Test loss    : {loss.item():.6f}")
    print(f"\n✅ U-Net + DDPM architecture working perfectly!")
    print("=" * 50)