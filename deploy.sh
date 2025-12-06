#!/bin/bash

# Deployment script for Indian Stock Indices Dashboard on Hostinger VPS
# This script helps deploy the project in an isolated directory

set -e  # Exit on error

echo "=========================================="
echo "Indian Stock Indices Dashboard Deployment"
echo "=========================================="

# Configuration
PROJECT_NAME="stock-dashboard"
DEPLOY_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/Manideepgadi1/Right-Sector.git"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo bash deploy.sh"
    exit 1
fi

# Step 1: Create isolated project directory
echo ""
echo "[1/6] Creating project directory..."
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# Step 2: Clone repository
echo ""
echo "[2/6] Cloning repository from GitHub..."
if [ -d ".git" ]; then
    echo "Repository exists, pulling latest changes..."
    git pull origin main
else
    git clone "$REPO_URL" .
fi

# Step 3: Set proper permissions
echo ""
echo "[3/6] Setting file permissions..."
chown -R www-data:www-data "$DEPLOY_DIR"
chmod -R 755 "$DEPLOY_DIR"
chmod 644 "$DEPLOY_DIR"/*.{html,csv,json} 2>/dev/null || true

# Step 4: Create Nginx configuration
echo ""
echo "[4/6] Creating Nginx configuration..."
cat > "/etc/nginx/sites-available/$PROJECT_NAME" <<'NGINX_EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN_HERE;  # Change this to your domain or IP
    
    root /var/www/stock-dashboard;
    index dashboard.html;
    
    # Logging
    access_log /var/log/nginx/stock-dashboard-access.log;
    error_log /var/log/nginx/stock-dashboard-error.log;
    
    # Main location
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Cache control for data files
    location ~ \.(csv|json)$ {
        add_header Cache-Control "no-cache, must-revalidate";
        add_header Access-Control-Allow-Origin "*";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/csv;
    gzip_comp_level 6;
}
NGINX_EOF

# Step 5: Enable site and test configuration
echo ""
echo "[5/6] Enabling Nginx site..."
ln -sf "/etc/nginx/sites-available/$PROJECT_NAME" "/etc/nginx/sites-enabled/$PROJECT_NAME"
nginx -t

# Step 6: Reload Nginx
echo ""
echo "[6/6] Reloading Nginx..."
systemctl reload nginx

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "Project location: $DEPLOY_DIR"
echo ""
echo "⚠️  IMPORTANT: Update the domain in Nginx config:"
echo "   sudo nano /etc/nginx/sites-available/$PROJECT_NAME"
echo "   Change 'YOUR_DOMAIN_HERE' to your actual domain or IP"
echo ""
echo "Then reload Nginx:"
echo "   sudo systemctl reload nginx"
echo ""
echo "Access your dashboard at:"
echo "   http://YOUR_DOMAIN/dashboard.html"
echo ""
echo "To update the deployment later, run:"
echo "   cd $DEPLOY_DIR && sudo git pull origin main"
echo "=========================================="
