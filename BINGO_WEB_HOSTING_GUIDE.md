# 🌐 BINGO Web Hosting Guide

This guide will help you host your BINGO game on a Linux server so others can watch the game live via a web browser!

## 📋 Requirements

- Linux Server (Ubuntu, CentOS, Debian, etc.)
- Python 3.6 or higher
- Web server (Nginx, Apache, or Python's built-in server)

## 🚀 Quick Setup

### Method 1: Using Python's Built-in HTTP Server (Easiest!)

1. **Upload your game to the server:**
```bash
# On your local machine
scp Lets_Play_BINGO.py user@your-server-ip:/home/user/bingo/
```

2. **Connect to your server:**
```bash
ssh user@your-server-ip
cd /home/user/bingo/
```

3. **Start the game with HTML output enabled:**
```bash
python3 Lets_Play_BINGO.py
```
- Choose number of players
- When asked "Enable HTML output?", type: **y**
- Use default filename: **bingo_game.html**

4. **In a separate terminal (or use `screen`/`tmux`), start the web server:**
```bash
# Navigate to the directory containing bingo_game.html
cd /home/user/bingo/

# Start Python HTTP server on port 8000
python3 -m http.server 8000
```

5. **Share the URL with your group:**
```
http://your-server-ip:8000/bingo_game.html
```

### Method 2: Using Nginx (For Production)

1. **Install Nginx:**
```bash
sudo apt update
sudo apt install nginx -y
```

2. **Create directory for your game:**
```bash
sudo mkdir -p /var/www/bingo
sudo chown $USER:$USER /var/www/bingo
```

3. **Copy/move your files:**
```bash
cp Lets_Play_BINGO.py /var/www/bingo/
cd /var/www/bingo/
```

4. **Run the game (with HTML enabled):**
```bash
python3 Lets_Play_BINGO.py
```
- Enable HTML output: **y**
- Filename: **bingo_game.html**

5. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/bingo
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your server IP

    root /var/www/bingo;
    index bingo_game.html;

    location / {
        try_files $uri $uri/ =404;
        # Disable caching for live updates
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }
}
```

6. **Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/bingo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Share the URL:**
```
http://your-server-ip/bingo_game.html
```

### Method 3: Using Apache

1. **Install Apache:**
```bash
sudo apt update
sudo apt install apache2 -y
```

2. **Setup directory:**
```bash
sudo mkdir -p /var/www/html/bingo
sudo chown $USER:$USER /var/www/html/bingo
cp Lets_Play_BINGO.py /var/www/html/bingo/
cd /var/www/html/bingo/
```

3. **Run the game:**
```bash
python3 Lets_Play_BINGO.py
```
- Enable HTML output: **y**

4. **Configure Apache (optional - for no-cache headers):**
```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Add inside `<VirtualHost>`:
```apache
<Directory /var/www/html/bingo>
    Header set Cache-Control "no-cache, no-store, must-revalidate"
    Header set Pragma "no-cache"
    Header set Expires "0"
</Directory>
```

5. **Enable headers module and restart:**
```bash
sudo a2enmod headers
sudo systemctl restart apache2
```

6. **Share the URL:**
```
http://your-server-ip/bingo/bingo_game.html
```

## 🎮 Running Game in Background

To keep the game running even after you disconnect:

### Using `screen`:
```bash
# Install screen
sudo apt install screen -y

# Start a new screen session
screen -S bingo

# Run your game
python3 Lets_Play_BINGO.py

# Detach from screen: Press Ctrl+A, then D

# Re-attach later
screen -r bingo
```

### Using `tmux`:
```bash
# Install tmux
sudo apt install tmux -y

# Start a new tmux session
tmux new -s bingo

# Run your game
python3 Lets_Play_BINGO.py

# Detach from tmux: Press Ctrl+B, then D

# Re-attach later
tmux attach -t bingo
```

## 🔧 Firewall Configuration

If your server has a firewall, open the necessary ports:

```bash
# For Python HTTP server (port 8000)
sudo ufw allow 8000/tcp

# For Nginx/Apache (port 80)
sudo ufw allow 80/tcp

# For HTTPS (port 443)
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## 📱 Features of the Web View

- **Auto-refresh every 3 seconds** - No manual refresh needed!
- **Beautiful gradient design** - Purple theme with animations
- **Live game stats** - Round number, players, winners
- **All player cards** - See everyone's BINGO cards in real-time
- **Called numbers** - Last 15 numbers displayed
- **Funny commentary** - Each number's funny comment shown
- **Winner highlights** - Winners' cards glow in gold!
- **Mobile responsive** - Works on phones, tablets, and desktops

## 🌍 Sharing with Group

Once set up, share the link in your group chat:

**Format:**
```
🎲 BINGO Game Live!
Watch here: http://your-server-ip:8000/bingo_game.html
📱 Auto-updates every 3 seconds!
```

## 🔒 Security Tips (Optional)

For production environments:

1. **Use HTTPS with SSL certificate:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

2. **Restrict access by IP (if needed):**
In Nginx config:
```nginx
location / {
    allow 192.168.1.0/24;  # Your network
    deny all;
}
```

3. **Add password protection:**
```bash
sudo apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd bingo_user
```

Add to Nginx config:
```nginx
location / {
    auth_basic "BINGO Game";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

## 🐛 Troubleshooting

**Problem:** HTML file not updating
- **Solution:** Make sure the game is running and you're calling numbers

**Problem:** Can't access from other devices
- **Solution:** Check firewall rules, ensure web server is running, use server's public IP

**Problem:** Page shows old data
- **Solution:** Hard refresh (Ctrl+F5 or Cmd+Shift+R), check cache headers

**Problem:** Permission denied errors
- **Solution:** Check file permissions: `chmod 644 bingo_game.html`

## 📞 Quick Reference Commands

```bash
# Check if web server is running
sudo systemctl status nginx    # For Nginx
sudo systemctl status apache2  # For Apache

# Check which ports are open
sudo netstat -tulpn | grep LISTEN

# Check if HTML file exists and is readable
ls -la bingo_game.html

# Monitor HTML file updates in real-time
watch -n 1 cat bingo_game.html

# See last modification time
stat bingo_game.html
```

## 🎉 That's It!

Your BINGO game is now live on the web! Players can watch the game progress in real-time from any device with a web browser!

Enjoy your game! 🎲🍀

