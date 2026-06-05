# Deployment Guide

## Architecture

We run the app on a VM (home computer, VPS, or cloud instance) and expose it securely to the internet using **Cloudflare Tunnel**. This gives us:

- **HTTPS for free** — Cloudflare terminates TLS at their edge
- **No open ports** — The tunnel creates an outbound connection, no port forwarding needed
- **No static IP** — Works behind NAT (home router)
- **$0 cost** — Cloudflare Tunnel is free

```
[Interviewer Browser]
         │
         ▼
[Cloudflare Edge]  ←── HTTPS (TLS 1.3)
         │
         ▼
[cloudflared daemon]  ←── Runs on your VM
         │
         ▼
[Docker Compose stack]
  ├── API (FastAPI) on port 8000
  └── Postgres on port 5432
```

---

## Prerequisites

- A VM or computer with Docker + Docker Compose installed
- A domain name (we use `hr.garfias.dev` as the example)
- Cloudflare account with your domain's DNS managed by Cloudflare

---

## 1. Clone & Start the App Locally

```bash
# SSH into your VM (or open a terminal on the host)
git clone <your-repo-url>
cd HappyRobot

# Create environment file
cp .env.example .env
# Edit .env with real values:
#   API_KEY=your-secret-key
#   FMCSA_API_KEY=cdc33e44d693a3a58451898d4ec9df862c65b954
#   CORS_ORIGINS=https://hr.garfias.dev

# Start everything
docker compose up --build -d
```

Verify locally:
```bash
curl http://localhost:8000/health
curl -H "Authorization: Bearer <API_KEY>" -H "client: happy-robot" http://localhost:8000/loads
```

The dashboard is available at `http://localhost:8000` (served by FastAPI static files).

### 1.1 Seed Demo Data (One-Time)

The API starts with empty tables. Apply the demo loads once so the voice agent has freight to pitch:

```bash
# After `docker compose up`, apply seed data
docker exec -i hr-postgres psql -U happyrobot -d happyrobot < seed_data.sql
```

Verify the loads were inserted:
```bash
curl -H "Authorization: Bearer <API_KEY>" -H "client: happy-robot" http://localhost:8000/loads
curl -H "Authorization: Bearer <API_KEY>" -H "client: happy-robot" "http://localhost:8000/loads?origin=Houston&destination=New%20Orleans&equipment_type=Dry%20Van"
```

> **Important:** Only run `seed_data.sql` once. The data persists in the Postgres volume across container restarts.

To stop:
```bash
docker compose down
```

To view logs:
```bash
docker compose logs -f api
```

---

## 2. Expose to the Internet via Cloudflare Tunnel

### 2.1 Install `cloudflared`

```bash
# Debian/Ubuntu
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Or using the official repo
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared
```

### 2.2 Authenticate

```bash
cloudflared tunnel login
```
This opens a browser. Select the zone for `garfias.dev`.

### 2.3 Create the Tunnel

```bash
cloudflared tunnel create hr-carrier-sales
```
Save the **Tunnel ID** printed in the output.

### 2.4 Configure the Tunnel

Create `~/.cloudflared/config.yml`:
```yaml
tunnel: <TUNNEL_ID>
credentials-file: /home/<user>/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: hr.garfias.dev
    service: http://localhost:8000
  - service: http_status:404
```

### 2.5 Route DNS

```bash
cloudflared tunnel route dns hr-carrier-sales hr.garfias.dev
```

### 2.6 Run the Tunnel

**For testing (foreground):**
```bash
cloudflared tunnel run hr-carrier-sales
```

**For production (systemd service):**
```bash
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

### 2.7 Verify

```bash
curl https://hr.garfias.dev/health
curl -H "Authorization: Bearer <API_KEY>" https://hr.garfias.dev/loads
```

You should see your API responding over HTTPS.

---

## 3. HTTPS — How It Works

**You do not configure HTTPS in the app.** The stack runs on plain HTTP inside the VM (port 8000), which is fine because it never faces the public internet directly.

**Cloudflare handles HTTPS entirely:**
1. The browser connects to `https://hr.garfias.dev`
2. Cloudflare's edge provides the TLS certificate (auto-managed)
3. Cloudflare decrypts the request and sends it through the tunnel to your VM
4. `cloudflared` forwards the request to `http://localhost:8000`
5. Your app responds over plain HTTP back through the tunnel
6. Cloudflare re-encrypts and sends the response to the browser

This is secure because:
- The tunnel itself is authenticated and encrypted (Cloudflare → your VM)
- The domain DNS is controlled by Cloudflare
- No inbound ports are open on your VM or router

---

## 4. Reproducing the Deployment

Everything needed to reproduce is in this repo:

```bash
# 1. Clone
git clone <repo-url>
cd HappyRobot

# 2. Configure environment
cp .env.example .env
# Edit .env

# 3. Start the stack
docker compose up --build -d

# 4. Set up Cloudflare Tunnel (one-time)
cloudflared tunnel login
cloudflared tunnel create hr-carrier-sales
cloudflared tunnel route dns hr-carrier-sales hr.garfias.dev
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

---

## 5. On-Premises Considerations

- **Updates**: `git pull && docker compose up --build -d`
- **Logs**: `docker compose logs -f`
- **Database backups**: `docker compose exec postgres pg_dump -U happyrobot happyrobot > backup.sql`
- **Monitoring**: The health endpoint (`/health`) can be used by any monitoring tool
- **Restart on boot**: `docker compose up -d` in crontab `@reboot` or systemd service

---

## 6. Security Checklist

- [ ] `.env` is in `.gitignore` and never committed
- [ ] `API_KEY` is rotated and strong
- [ ] `FMCSA_API_KEY` is set via `.env`, not hardcoded
- [ ] The VM firewall blocks port 8000 from external access (only Cloudflare Tunnel reaches it)
- [ ] `CORS_ORIGINS` is restricted to production domains
- [ ] Health endpoint (`/health`) is public for monitoring
