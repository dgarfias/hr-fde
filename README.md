# HappyRobot Inbound Carrier Sales

## Technologies

- FastAPI
- React + TypeScript + Vite
- Tailwind CSS
- PostgreSQL
- Docker Compose
- Cloudflare Tunnel

## How To Deploy

### 1. Create the containers

Clone the repo, create your env file, and start the stack:

```bash
cp .env.example .env
# Edit .env and fill in your values (API keys, passwords, etc.)

docker compose up --build -d
```

The main app is served at `http://localhost:8000`.

If you want to stop the stack:

```bash
docker compose down
```

### 2. Upload dummy data to the database

Seed the demo loads after the containers are running:

```bash
docker compose exec -T postgres psql -U happyrobot -d happyrobot < seed_data.sql
```

You can verify the data with:

```bash
docker compose exec postgres psql -U happyrobot -d happyrobot -c "SELECT load_id, origin, destination, equipment_type, loadboard_rate FROM loads ORDER BY created_at;"
```

### 3. Start the Cloudflare Tunnel

Install and authenticate `cloudflared` on the machine running Docker:

```bash
cloudflared tunnel login
cloudflared tunnel create hr-carrier-sales
cloudflared tunnel route dns hr-carrier-sales your-subdomain.yourdomain.com
```

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: <TUNNEL_ID>
credentials-file: /home/<user>/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: your-subdomain.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

Run the tunnel:

```bash
cloudflared tunnel run hr-carrier-sales
```

Or install it as a persistent service (requires root):

```bash
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

After that, your app is available over HTTPS at your Cloudflare hostname, while the app itself continues running locally on `http://localhost:8000`.

### 4. Verify

```bash
# Local health check
curl http://localhost:8000/health

# Public health check (replace with your hostname)
curl https://your-subdomain.yourdomain.com/health
```
