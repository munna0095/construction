#!/bin/bash

# SIDDHI CONSTRUCTION - AUTOMATED DEPLOYMENT SCRIPT
# This script deploys the website to DigitalOcean server and sets up Nginx

echo "================================"
echo "SIDDHI CONSTRUCTION - DEPLOYMENT"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Update system
echo -e "${BLUE}[1/7] Updating system...${NC}"
apt update && apt upgrade -y

# Step 2: Install Nginx
echo -e "${BLUE}[2/7] Installing Nginx...${NC}"
apt install nginx curl wget git -y

# Step 3: Create website directory
echo -e "${BLUE}[3/7] Creating website directory...${NC}"
mkdir -p /var/www/siddhi-construction
cd /var/www/siddhi-construction

# Step 4: Clone or pull from Git
echo -e "${BLUE}[4/7] Cloning from GitHub...${NC}"
if [ -d ".git" ]; then
    echo "Repository exists, pulling latest..."
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/munna0095/construction.git .
fi

# Step 5: Set permissions
echo -e "${BLUE}[5/7] Setting permissions...${NC}"
chmod 755 /var/www/siddhi-construction
chmod 644 /var/www/siddhi-construction/*
chmod 755 /var/www/siddhi-construction/*.sh 2>/dev/null || true

# Step 6: Configure Nginx
echo -e "${BLUE}[6/7] Configuring Nginx...${NC}"
cat > /etc/nginx/sites-available/siddhi-construction << 'NGINX_CONFIG'
server {
    listen 80;
    server_name 168.144.30.73;
    
    root /var/www/siddhi-construction;
    index index.html;
    
    # Serve static files
    location / {
        try_files $uri $uri/ =404;
        expires 30d;
    }
    
    # Cache images
    location ~* \.(jpg|jpeg|png|gif|ico|svg|avif)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }
    
    # Log files
    access_log /var/log/nginx/siddhi-construction.log;
    error_log /var/log/nginx/siddhi-construction-error.log;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/javascript application/javascript;
}
NGINX_CONFIG

# Remove default config if exists
rm -f /etc/nginx/sites-enabled/default

# Enable our config
ln -sf /etc/nginx/sites-available/siddhi-construction /etc/nginx/sites-enabled/

# Step 7: Start Nginx
echo -e "${BLUE}[7/7] Starting Nginx...${NC}"
nginx -t
systemctl restart nginx
systemctl enable nginx

echo ""
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo ""
echo "Website is now live at: http://168.144.30.73"
echo ""
echo "To view logs:"
echo "  tail -f /var/log/nginx/siddhi-construction.log"
echo ""
echo "To restart Nginx:"
echo "  systemctl restart nginx"
echo ""
