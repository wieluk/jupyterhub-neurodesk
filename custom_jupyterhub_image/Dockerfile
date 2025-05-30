# Use the official JupyterHub image as the base image
FROM jupyterhub/jupyterhub:5.3.0

# Install nativeauthenticator and dockerspawner
RUN pip install jupyterhub-nativeauthenticator
RUN pip install dockerspawner
RUN pip install jupyterhub-idle-culler
RUN pip install requests
