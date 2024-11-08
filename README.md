Here's an updated `README.md` that integrates details specific to the configuration files you provided. This version highlights features such as `fail2ban`, `Slack notifications`, and other specifics related to user management and Docker settings.

---

# NeuroDesktop JupyterHub Server Deployment

This repository provides a setup to deploy a JupyterHub server that supports NeuroDesktop, offering each user a private, containerized environment. This setup leverages Docker Compose and includes features like security enhancements (`fail2ban`), user management with `NativeAuthenticator`, and Slack notifications.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [User Directories](#user-directories)
  - [Security Features](#security-features)
  - [Docker Settings](#docker-settings)
- [Starting the Server](#starting-the-server)
- [Stopping the Server](#stopping-the-server)
- [Directory Structure](#directory-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

### Overview

This setup is designed for research or educational institutions where users need access to data science and neuroimaging tools in isolated environments. Each user has a personal directory in `/storage/neurodesk/users`, enabling persistent storage across sessions. With `NativeAuthenticator`, users can self-register, though admin approval is required for access.

### Prerequisites

Ensure you have the following installed:
- **Git**: [Install Git](https://git-scm.com/)
- **Docker** and **Docker Compose**: [Install Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- **Slack Webhook URL**: Required if you enable Slack notifications for server status updates or alerts.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Docker Compose**:
   The provided `docker-compose.yml` sets up the necessary JupyterHub and support services.

### Configuration

#### User Directories

Open `jupyterhub_config.py` and ensure `base_user_dir` is set to `/storage/neurodesk/users`. This is where each user’s data will be stored persistently on the host machine.

```python
base_user_dir = '/storage/neurodesk/users'
```

The configuration will automatically create a new folder for each user under this directory upon login.

#### Security Features

1. **Fail2Ban**:
   - The configuration includes `fail2ban` support to block repeated failed login attempts, enhancing security.
   - Failed login attempts are limited, and a cooldown period applies after consecutive failures.

2. **NativeAuthenticator**:
   - The configuration uses `NativeAuthenticator` to enable self-signup with admin approval.
   - Passwords must be a minimum of 8 characters, and common passwords are automatically rejected.
   - ToS acceptance and email verification are required for new sign-ups.

3. **Slack Notifications**:
   - Slack integration allows admins to receive notifications for specific events.
   - Add your Slack webhook URL in the `docker-compose.yml` file if you want real-time alerts for server issues or login attempts.

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

3. **Volumes and Networking**:
   - User volumes are mounted to `/home/jovyan` in each container, and shared directories can be set up to `/storage`.
   - A custom network, `jupyterhub-network`, is defined to manage container communication.

4. **Idle Culling**:
   - Idle containers are automatically culled after 2 weeks to free up resources.

### Starting the Server

To deploy the server, run:
```bash
docker-compose up -d
```

This command starts the JupyterHub server with all specified configurations.

### Stopping the Server

To stop the server, run:
```bash
docker-compose down
```

### Directory Structure

- **/storage/neurodesk/users**: User data is stored persistently in this directory on the host system.
- **/srv/jupyterhub/logs**: JupyterHub logs are stored here, including logs for `fail2ban` and other services.

### Troubleshooting

- **Log Files**: View logs in `/srv/jupyterhub/logs/jupyterhub.log` for information on login attempts, authentication, and errors.
- **User Storage Permissions**: Ensure the `/storage` directory and its subdirectories have proper permissions for Docker to read and write.
- **Timeouts**: If users experience timeout issues, increase `http_timeout` and `start_timeout` in `jupyterhub_config.py`.

### License

This project is licensed under [Your License Here].

--- 

This README provides a detailed, structured guide specifically tailored to your files. Let me know if you need further adjustments or details!