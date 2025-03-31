# VEIC Interview Demo App

This is a Flask-based web application for viewing projects and associated measures. It uses SQLite and SQLAlchemy on the backend, with Bootstrap and DataTables on the frontend. The app is configured for production-level deployment behind Nginx using Gunicorn.

<p align="left">
  <img src="https://github.com/user-attachments/assets/54c29fe3-0fa4-4436-9d4b-59f0cdaf50c5" width="700"/>
  <br>
  <em>Figure 1. Default view of the Projects and Measures Dashboard</em>
</p>

---

## Features

- View and filter projects by status
- View and add measures tied to each project
- Input custom measure types

---

## Local Development

### 1. Clone the Repo

`git clone https://github.com/vcaristo/energy_modeling_software_interview.git`   
`cd VEIC_interview`

### 2. Setup Python environment
With conda:

`conda env create -f environment.yml`  
`conda activate veic-interview`

### 3. Run the app

`python app.py`  

Then visit http://localhost:5000/veic-interview/

## Deploying on EC2 with Gunicorn and Nginx

### 1. SSH into EC2 instance and clone this repository:

`ssh ec2-user@your-ec2-ip`    
`git clone https://github.com/vcaristo/energy_modeling_software_interview.git`    
`cd VEIC_interview`    

### 2. Setup Python environment
With conda:

`conda env create -f environment.yml`    
`conda activate veic-interview`  

### 3. Start Gunicorn

`nohup gunicorn -w 4 -b 127.0.0.1:8001 app:app > gunicorn.log 2>&1 &`  

This command does the following:
- Runs Gunicorn with 4 workers on port 8002.  
- Keeps running after logout.
- Writes stdout and stderr to gunicorn.log.

### 4. Configure Nginx to handle reverse proxy requests

Create a file at /etc/nginx/conf.d/veic.conf:

    server {
        listen 80;
        server_name vincecaristo.com;

        location /veic-interview/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

To add basic security hardening features, add any of the following inside the server block in veic.conf:

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy no-referrer-when-downgrade;
    add_header Permissions-Policy "geolocation=(), microphone=()";

    # Limit abusive requests
    limit_req zone=req_limit_per_ip burst=20 nodelay;

    # Block unwanted bots
    if ($http_user_agent ~* (bot|crawl|spider|wget|curl)) {
        return 403;
    }

    # Deny access to dotfiles
    location ~ /\.(?!well-known).* {
        deny all;
    }

Note, if rate limiting requests from individual IP addresses ("limit abusive requests"), you may 
need to add the following line to the the http block of your nginx.conf files (typically, at folder /etc/nginx/):

    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=10r/s;

### 5. Reload Nginx

`sudo nginx -t`    
`sudo systemctl reload nginx`    

Then visit http://\<your-domain\>/veic-interview/
