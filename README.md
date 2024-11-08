# NeuroDesktop JupyterHub Server Deployment

This repository provides a setup to deploy a JupyterHub server that supports NeuroDesktop, offering each user a private, containerized environment. This setup leverages Docker Compose and includes features like security enhancements (`fail2ban`), user management with `NativeAuthenticator`, and Slack notifications.


### Overview

This setup is designed for research or educational institutions where users need access to data science and neuroimaging tools in isolated environments. Each user has a personal directory in `BASE_USER_DIR=/path/to/user/dir` (change this in the docker-compose.yml), enabling persistent storage across sessions. With `NativeAuthenticator`, users can self-register, though admin approval is required for access.

### Prerequisites
   Install git

   Install Docker https://docs.docker.com/engine/install

   Install docker compose https://docs.docker.com/compose/install


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
3. **Use Docker Compose**:
   ```bash
   docker compose up -d
   ```
### Configuration

#### User Directories

Open `docker-compose.yml` and ensure `BASE_USER_DIR` is set to the directory where user data is saved. This is where each user’s data will be stored persistently on the host machine.


The configuration will automatically create a new folder for each user under this directory upon login.


#### Docker Settings

1. **Images**:
   - The configuration in `jupyterhub_config.py` allows multiple versions of the NeuroDesktop image. Users can select from specific tagged versions:
     ```python
     c.DockerSpawner.allowed_images = [
         'vnmd/neurodesktop:latest',
         'vnmd/neurodesktop:2024-10-16',
         'vnmd/neurodesktop:2024-05-25',
         # Additional versions are listed in the file
     ]
     ```

2. **Resource Limits**:
   - You can set resource limits for each user’s container by uncommenting and adjusting `mem_limit` and `cpu_limit` in `jupyterhub_config.py`:
     ```python
     # c.DockerSpawner.mem_limit = '256G'
     # c.DockerSpawner.cpu_limit = 20
     ```

3. **Idle Culling**:
   - Idle containers are automatically culled after 2 weeks to free up resources.


#### Extra container (Disabled by default)

1. **Fail2Ban**:
   - The configuration includes `fail2ban` support to block repeated failed login attempts, enhancing security.
   - Failed login attempts are limited, and a cooldown period applies after consecutive failures.


2. **Slack Notifications**:
   - Slack integration allows admins to receive notifications for specific events.
   - Add your Slack webhook URL in the `.env` file if you want real-time alerts for server issues or login attempts.



