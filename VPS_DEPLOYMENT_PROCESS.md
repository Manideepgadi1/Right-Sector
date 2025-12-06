# VPS Deployment Process - Quick Reference

## Server Details
- **VPS IP**: 82.25.105.18
- **Web Server**: Nginx
- **SSH Access**: `ssh root@82.25.105.18`
- **Main Config File**: `/etc/nginx/sites-available/combined`

---

## Standard Deployment Steps for New Projects

### 1. Prepare Local Code
```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### 2. Connect to VPS
```bash
ssh root@82.25.105.18
```

---

### 3. Create Project Directory
```bash
# Choose a unique project name (lowercase, use hyphens)
PROJECT_NAME="your-project-name"

# Create directory
mkdir -p /var/www/$PROJECT_NAME
cd /var/www/$PROJECT_NAME

# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Set permissions
chown -R www-data:www-data /var/www/$PROJECT_NAME
chmod -R 755 /var/www/$PROJECT_NAME
```

---

### 4. Configure Nginx (Add to Existing Config)

**Edit the combined config:**
```bash
nano /etc/nginx/sites-available/combined
```

**Add BEFORE the last `}` of the server block:**

```nginx
    # Your Project Name
    location /your-project-name {
        alias /var/www/your-project-name/;
        index index.html;  # or dashboard.html or whatever your main file is
        try_files $uri /index.html =404;
    }
    
    # Static files for your project (CSS, JS, JSON, CSV, images)
    location ~ ^/your-project-name/(.+\.(css|js|json|csv|png|jpg|jpeg|gif|svg|ico))$ {
        alias /var/www/your-project-name/$1;
        add_header Cache-Control "no-cache, must-revalidate";
        add_header Access-Control-Allow-Origin "*";
    }
```

**Important Notes:**
- Replace `your-project-name` with your actual project name
- Replace `index.html` with your main HTML file name
- Make sure there's a `/` after the alias path
- Keep all closing braces `}` intact

---

### 5. Test and Reload Nginx

```bash
# Test configuration syntax
nginx -t

# If syntax is OK, reload
systemctl reload nginx

# If there are errors, check the config file again
nano /etc/nginx/sites-available/combined
```

---

### 6. Access Your Project

**URL Format:**
```
http://82.25.105.18/your-project-name
```

**Clear browser cache if you see old content:**
- Press `Ctrl + Shift + R` (hard refresh)
- Or open in incognito/private mode

---

## Updating Existing Projects

When you push new code to GitHub:

```bash
# SSH into VPS
ssh root@82.25.105.18

# Navigate to project
cd /var/www/your-project-name

# Pull latest changes
git pull origin main

# Reload Nginx (optional, usually not needed for static files)
systemctl reload nginx
```

---

## Common Issues & Solutions

### Issue 1: 404 Not Found
**Solution:**
```bash
# Check if files exist
ls -la /var/www/your-project-name/

# Verify Nginx config paths match
cat /etc/nginx/sites-available/combined | grep -A 5 "your-project-name"

# Check Nginx error logs
tail -50 /var/log/nginx/error.log
```

### Issue 2: Data Files Not Loading (CSV/JSON)
**Solution:**
- Add the static files location block (see step 4)
- Make sure the regex pattern captures the file extension
- Check file permissions: `chmod 644 /var/www/your-project-name/*.json`

### Issue 3: Old Content Showing
**Solution:**
- Hard refresh browser: `Ctrl + Shift + R`
- Open in incognito mode
- Add cache-busting in your code: `file.json?v=${Date.now()}`

### Issue 4: Nginx Syntax Error
**Solution:**
```bash
# Check syntax with line numbers
nginx -t

# Common causes:
# - Missing semicolon ;
# - Missing closing brace }
# - Wrong path (missing leading / in alias)
# - Duplicate location blocks

# Edit and fix
nano /etc/nginx/sites-available/combined
```

### Issue 5: Files Not Found Despite Correct Config
**Solution:**
```bash
# Check file permissions
ls -la /var/www/your-project-name/

# Fix permissions if needed
chown -R www-data:www-data /var/www/your-project-name/
chmod -R 755 /var/www/your-project-name/
chmod 644 /var/www/your-project-name/*.html
chmod 644 /var/www/your-project-name/*.json
chmod 644 /var/www/your-project-name/*.csv
```

---

## Project Structure Best Practices

```
/var/www/your-project-name/
├── index.html (or dashboard.html)
├── styles.css
├── script.js
├── data/
│   ├── file1.json
│   ├── file2.csv
├── images/
│   ├── logo.png
└── README.md
```

---

## Multiple Projects on Same VPS

**Current Setup:**
- Heatmap Dashboard: `http://82.25.105.18/` (root)
- Right Sector: `http://82.25.105.18/right-sector`
- Your Next Project: `http://82.25.105.18/your-project-name`

**All projects share the same Nginx config file:**
`/etc/nginx/sites-available/combined`

**Each project gets its own location block in that file.**

---

## Quick Commands Reference

```bash
# SSH Connect
ssh root@82.25.105.18

# Check Nginx Status
systemctl status nginx

# Test Nginx Config
nginx -t

# Reload Nginx (after config changes)
systemctl reload nginx

# Restart Nginx (if reload doesn't work)
systemctl restart nginx

# View Error Logs
tail -f /var/log/nginx/error.log

# View Access Logs
tail -f /var/log/nginx/access.log

# List All Projects
ls -la /var/www/

# Check Disk Space
df -h

# Check Memory Usage
free -h

# View Running Processes
htop
# or
top
```

---

## Template for ChatGPT/AI Assistance

**Copy this when asking for help:**

```
I need to deploy a new project to my VPS. Here are the details:

VPS IP: 82.25.105.18
Web Server: Nginx
Config File: /etc/nginx/sites-available/combined
Current Projects: 
  - Heatmap Dashboard at /
  - Right Sector at /right-sector

New Project Details:
- GitHub Repo: [YOUR_REPO_URL]
- Project Name: [your-project-name]
- Main HTML File: [index.html or dashboard.html]
- Additional Files: [list any special files: JSON, CSV, Python scripts, etc.]

I want to deploy it at: http://82.25.105.18/[your-project-name]

Please provide:
1. Exact commands to clone and set up the project
2. Nginx configuration to add to /etc/nginx/sites-available/combined
3. Any special considerations for file types or server-side code

The Nginx config should be added to the existing combined file WITHOUT breaking current projects.
```

---

## Security Notes

1. **Always backup before editing Nginx config:**
   ```bash
   cp /etc/nginx/sites-available/combined /etc/nginx/sites-available/combined.backup
   ```

2. **Keep your VPS updated:**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Consider adding SSL/HTTPS** (free with Let's Encrypt):
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   ```

4. **Monitor disk space regularly:**
   ```bash
   df -h
   ```

---

## Contact/Notes

- VPS Provider: Hostinger
- Server Location: [Your server location]
- Setup Date: December 6, 2025
- Projects Deployed:
  1. Financial Heatmap Dashboard (root)
  2. Right Sector - Indian Indices Dashboard (/right-sector)
  3. [Future projects go here]

---

**Last Updated:** December 6, 2025
