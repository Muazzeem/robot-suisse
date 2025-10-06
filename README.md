# Nginx Configuration and SSL Setup Guide

This guide walks you through setting up Nginx with SSL certificates for your web projects using Let's Encrypt.

## Prerequisites

- Ubuntu/Debian server with sudo access
- Nginx installed
- Certbot installed for Let's Encrypt certificates
- Domain pointing to your server IP
- Project running on a Unix socket

## Step-by-Step Configuration

### Step 1: Create Nginx Site Configuration

Create a new Nginx configuration file for your project:

```bash
sudo nano /etc/nginx/sites-available/<project_name>

upstream <project_name> {
    server unix:/www/service_web/<project_name>/server/socket/SERVER.sock fail_timeout=0;
}

server {
    server_name <project_name>.marketize.biz;

    gzip            on;
    gzip_types      text/plain application/xml text/css application/javascript;
    gzip_min_length 1000;
    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /www/service_web/<project_name>/logs/nginx-access.log;
    error_log /www/service_web/<project_name>/logs/nginx-error.log;

    location /static/ {
        alias /www/service_web/<project_name>/server/static/;
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    location /media/ {
        alias /www/service_web/<project_name>/server/media/;
        access_log off;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://<project_name>;
    }
}
```

### Step 2: Create a Symlink to the Nginx Site Configuration

Create a symbolic link to the Nginx site configuration in the `sites-enabled` folder:

```bash
sudo ln -s /etc/nginx/sites-available/<project_name> /etc/nginx/sites-enabled/<project_name>
```

### Step 3: Request the Certificate from Let's Encrypt

Request a Let's Encrypt certificate for your domain:

```bash
sudo certbot --nginx -d <project_name>.marketize.biz
```

### Step 4: Reload Nginx

Reload Nginx to apply the changes:

```bash
sudo systemctl reload nginx
```

### Step 5: Restart Nginx

Restart Nginx to apply the changes:

```bash
sudo systemctl restart nginx
```

### Step 6: Check the Status of the Project

Check the status of the project:

```bash
sudo systemctl status nginx
```

## Conclusion

Congratulations! You have successfully set up Nginx with SSL certificates for your web projects using Let's Encrypt.
