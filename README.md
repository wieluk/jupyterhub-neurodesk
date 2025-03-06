# NeuroDesktop JupyterHub Server Deployment

This repository provides a setup to deploy a JupyterHub server that supports NeuroDesktop, offering each user a private, containerized environment. This setup leverages Docker Compose and includes features like security enhancements (`fail2ban`), user management with `NativeAuthenticator`, and Slack notifications.

### Overview

This setup is designed for research or educational institutions where users need access to data science and neuroimaging tools in isolated environments. Each user has a personal directory in `BASE_USER_DIR=/path/to/user/dir` (change this in the .env), enabling persistent storage across sessions. With `NativeAuthenticator`, users can self-register, though admin approval is required for access.

### Prerequisites

   1. Install git

   2. Install Docker https://docs.docker.com/engine/install

   3. Install docker compose https://docs.docker.com/compose/install

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/wieluk/jupyterhub-neurodesk.git
   cd jupyterhub-neurodesk
   ```

2. **Create docker network**
   
   ```bash
   docker network create jupyterhub-network
   ```
   
3. **Edit .env**
Open `.env` and ensure `BASE_USER_DIR` is set to the directory where you want to save user data. This is where each user’s data will be stored persistently on the host machine.

4. **Use Docker Compose**:
   
   ```bash
   docker compose up -d
   ```

4. **Create Admin User**
   
   Go to `localhost:8000` or `serverip:port_you_choose` in your browser and sign up as `admin`.


**Note** The first start of neurodesk will take some time. The docker image needs to be downloaded.

### Configuration

#### jupyterhub_config.py

1. **Images**:  
   - The configuration dynamically fetches all available versions of the NeuroDesktop image from Docker Hub.

2. **Resource Limits**:
   - You can set resource limits for each user’s container by uncommenting and adjusting `mem_limit` and `cpu_limit` in `jupyterhub_config.py`:
     ```python
     # c.DockerSpawner.mem_limit = '8G'
     # c.DockerSpawner.cpu_limit = 4
     ```

3. **Idle Culling**:
   - Idle containers are automatically culled after 2 weeks to free up resources.

#### Extra container (Disabled by default)

1. **Fail2Ban**:
   - The configuration includes `fail2ban` support to block repeated failed login attempts, enhancing security.
   - Failed login attempts are limited, and a cooldown period applies after consecutive failures.

2. **Slack Notifications**:
   - Only uncomment if jupyterhub.sqlite already exists in jupyterhub_config folder
   - Slack integration allows admins to receive notifications for specific events.
   - Add your Slack webhook URL in the `.env` file if you want real-time alerts for server issues or login attempts.
