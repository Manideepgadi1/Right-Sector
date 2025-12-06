# VPS Deployment Guide for Hostinger

## Quick Deployment Steps

### 1. Connect to Your VPS

```bash
ssh root@your-vps-ip
# or
ssh your-username@your-vps-ip
```

### 2. Upload the Deployment Script

**Option A: Using SCP (from your local machine)**
```bash
scp "D:\Right Sector\deploy.sh" root@your-vps-ip:/root/
```

**Option B: Create directly on VPS**
```bash
# On VPS, create the file
nano ~/deploy.sh

# Copy the content from deploy.sh and paste it
# Save with Ctrl+X, Y, Enter
```

### 3. Run the Deployment Script

```bash
# Make it executable
chmod +x ~/deploy.sh

# Run with sudo
sudo bash ~/deploy.sh
```

### 4. Configure Your Domain

Edit the Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/stock-dashboard
```

Change this line:
```
server_name YOUR_DOMAIN_HERE;
```

To your actual domain or IP:
```
server_name stocks.yourdomain.com;
# or just use IP
server_name 123.45.67.89;
```

Save and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Access Your Dashboard

Open browser: `http://your-domain/dashboard.html` or `http://your-ip/dashboard.html`

---

## Manual Deployment (Alternative Method)

If you prefer to deploy manually without the script:

### Step 1: Create Project Directory
```bash
sudo mkdir -p /var/www/stock-dashboard
cd /var/www/stock-dashboard
```

### Step 2: Clone Repository
```bash
sudo git clone https://github.com/Manideepgadi1/Right-Sector.git .
```

### Step 3: Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/stock-dashboard
sudo chmod -R 755 /var/www/stock-dashboard
```

### Step 4: Create Nginx Config
```bash
sudo nano /etc/nginx/sites-available/stock-dashboard
```

Paste this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/stock-dashboard;
    index dashboard.html;
    
    access_log /var/log/nginx/stock-dashboard-access.log;
    error_log /var/log/nginx/stock-dashboard-error.log;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~ \.(csv|json)$ {
        add_header Cache-Control "no-cache, must-revalidate";
    }
    
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/csv;
}
```

### Step 5: Enable and Test
```bash
sudo ln -s /etc/nginx/sites-available/stock-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Deployment to Subdirectory (If You Have Other Projects)

If you want to access it at `http://yourdomain.com/stocks/`:

**Nginx Configuration:**
```nginx
location /stocks/ {
    alias /var/www/stock-dashboard/;
    index dashboard.html;
    
    location ~ \.(csv|json)$ {
        add_header Cache-Control "no-cache, must-revalidate";
    }
}
```

**Update dashboard.html** - Add base path:
```javascript
// In loadData() function, change fetch URLs to:
const response = await fetch(`/stocks/categorized_indices_updated.csv?v=${timestamp}`);
const basketResponse = await fetch(`/stocks/basket_data.json?v=${timestamp}`);
const corrResponse = await fetch(`/stocks/correlation_matrix.json?v=${timestamp}`);
```

---

## Apache Configuration (Alternative to Nginx)

If your VPS uses Apache instead:

### Create .htaccess file
```bash
cd /var/www/stock-dashboard
sudo nano .htaccess
```

Add this content:
```apache
DirectoryIndex dashboard.html

# Cache control for data files
<FilesMatch "\.(csv|json)$">
    Header set Cache-Control "no-cache, must-revalidate"
</FilesMatch>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/css text/csv application/json application/javascript
</IfModule>

# Security headers
Header set X-Frame-Options "SAMEORIGIN"
Header set X-Content-Type-Options "nosniff"
```

### Enable required modules
```bash
sudo a2enmod headers deflate rewrite
sudo systemctl restart apache2
```

---

## SSL/HTTPS Setup (Recommended)

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate (for Nginx)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
sudo certbot renew --dry-run
```

---

## Updating Deployment

To update with new code from GitHub:

```bash
cd /var/www/stock-dashboard
sudo git pull origin main
sudo systemctl reload nginx
```

---

## File Structure on VPS

```
/var/www/stock-dashboard/
├── dashboard.html
├── categorized_indices_updated.csv
├── basket_data.json
├── correlation_matrix.json
├── data/
│   └── Latest_Indices_rawdata_14112025.csv
├── calculate_4yr_5yr_percentiles.py
├── calculate_basket_data.py
├── calculate_correlations.py
├── merge_percentiles.py
└── README.md
```

---

## Troubleshooting

### Check if Nginx is running
```bash
sudo systemctl status nginx
```

### Check Nginx error logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### Check permissions
```bash
ls -la /var/www/stock-dashboard/
```

### Test Nginx config
```bash
sudo nginx -t
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Check if port 80 is open
```bash
sudo netstat -tlnp | grep :80
```

### Check firewall
```bash
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Port Configuration

If you want to run on a different port (e.g., 8080):

**Nginx:**
```nginx
server {
    listen 8080;
    # ... rest of config
}
```

**Firewall:**
```bash
sudo ufw allow 8080/tcp
```

---

## Performance Optimization

### Enable browser caching for static files
```nginx
location ~* \.(html|css|js)$ {
    expires 1h;
    add_header Cache-Control "public, immutable";
}
```

### Enable Gzip compression
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/csv;
gzip_comp_level 6;
```

---

## Security Best Practices

1. **Keep system updated**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Configure firewall**
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

3. **Disable directory listing** (already done in config)

4. **Use HTTPS** (via Certbot as shown above)

5. **Regular backups**
```bash
# Backup script
tar -czf stock-dashboard-backup-$(date +%Y%m%d).tar.gz /var/www/stock-dashboard/
```

---

## Need Help?

- **Nginx docs**: https://nginx.org/en/docs/
- **Certbot**: https://certbot.eff.org/
- **GitHub repo**: https://github.com/Manideepgadi1/Right-Sector

---

**Quick Command Reference:**

```bash
# Deploy
sudo bash ~/deploy.sh

# Update
cd /var/www/stock-dashboard && sudo git pull

# Check logs
sudo tail -f /var/log/nginx/stock-dashboard-access.log

# Restart Nginx
sudo systemctl restart nginx

# Edit config
sudo nano /etc/nginx/sites-available/stock-dashboard
```
