from dockerspawner import DockerSpawner
import os
import nativeauthenticator
#import pwd
#import grp
import sys
import logging
import requests

base_user_dir = os.getenv('BASE_USER_DIR')

c.JupyterHub.log_level = logging.INFO
c.Spawner.debug = False
c.JupyterHub.extra_log_file = '/srv/jupyterhub/logs/jupyterhub.log'


# Set the authenticator class to NativeAuthenticator
c.JupyterHub.authenticator_class = 'native'
c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

# If you want to have a checkbox with Terms of service on Signup
#c.NativeAuthenticator.tos = 'Add your TOS here'

c.NativeAuthenticator.minimum_password_length = 8
c.NativeAuthenticator.check_common_password = True
c.NativeAuthenticator.allowed_failed_logins = 5
c.NativeAuthenticator.seconds_before_next_try = 300
c.NativeAuthenticator.ask_email_on_signup = True
c.Authenticator.allow_all = True
#c.NativeAuthenticator.allow_2fa = True

# Enable self-signup
c.NativeAuthenticator.enable_signup = True
# Require admin approval for new users
c.NativeAuthenticator.open_signup = False


def get_neurodesktop_tags():
    repo_name = "vnmd/neurodesktop"
    base_url = f"https://hub.docker.com/v2/repositories/{repo_name}/tags"
    
    fixed_top_tags = ["vnmd/neurodesktop:latest"]
    tags = set()
    url = base_url

    try:
        while url:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                for tag_info in data.get('results', []):
                    tag_name = tag_info['name']
                    if tag_name.lower() != "latest": 
                        tags.add(f"{repo_name}:{tag_name}")
                url = data.get('next')
            else:
                break
    except Exception:
        pass

    sorted_tags = sorted(tags, reverse=True)
    return fixed_top_tags + sorted_tags

# Configure DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

# Dynamically fetch available images (with a fallback)
c.DockerSpawner.allowed_images = get_neurodesktop_tags()

c.DockerSpawner.remove = True
c.DockerSpawner.notebook_dir = '/home/jovyan'

### Per user limits:
#c.DockerSpawner.mem_limit = '8G'
#c.DockerSpawner.cpu_limit = 4

### Timeout increase to download images
c.Spawner.http_timeout = 180
c.Spawner.start_timeout = 300

### Customize container name template
c.DockerSpawner.name_template = 'jupyterhub-{username}'
#c.DockerSpawner.name_template = 'Hub-{username}-{imagename}'


def create_user_directory(spawner):
    username = spawner.user.name
    user_dir = os.path.join(base_user_dir, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, mode=0o755)
    
    spawner.volumes = {
        user_dir: '/home/jovyan',
    }


### If you want to pass server users to jupyterhub and give them permissions like on the server.

#storage_dir='/storage' # Users wanted to acces whole /storage
#shared_dir='/storage/neurodesk/shared' # Shared dir for users that exist on server and neurodesk
#import pwd

# def create_user_directory(spawner):
#     username = spawner.user.name
#     user_dir = os.path.join(base_user_dir, username)

#     try:
#         system_user = pwd.getpwnam(username)
#         uid = system_user.pw_uid
#         gid = system_user.pw_gid
#     except KeyError:
#         uid = 1010  # Default UID
#         gid = 1010  # Default GID
#     if not os.path.exists(user_dir):
#         os.makedirs(user_dir, mode=0o755)
#         os.chown(user_dir, uid, gid)

#     if uid != 1010:
#         spawner.volumes = {
#             user_dir: '/home/jovyan',
#             storage_dir: '/storage',
#             shared_dir: '/shared',
#         }
#     else:
#         spawner.volumes = {
#             user_dir: '/home/jovyan',
#         }
#     spawner.environment.update({
#         'NB_UID': uid,
#         'NB_GID': gid,
#     })


c.DockerSpawner.pre_spawn_hook = create_user_directory

c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.extra_create_kwargs.update({'user': 'root'})

### Add required capabilities and security options
c.DockerSpawner.extra_host_config = {
    'privileged': True,
    'shm_size': '2g',
}

### Configure connect ip for internal Docker network
c.JupyterHub.hub_connect_ip = 'jupyterhub'

### Configure HTTPS
# c.JupyterHub.ssl_key = '/etc/letsencrypt/privkey.pem'
# c.JupyterHub.ssl_cert = '/etc/letsencrypt/fullchain.pem'


c.Authenticator.admin_users = {'admin'}

### Culler stops unused spawned containers after 2 Weeks 
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=1209600",
        ],
        # "admin": True,
    }
]
