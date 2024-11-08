# Use the official JupyterHub image as the base image
FROM jupyterhub/jupyterhub:5.2.1

# Install nativeauthenticator and dockerspawner
RUN pip install jupyterhub-nativeauthenticator
RUN pip install dockerspawner
RUN pip install jupyterhub-idle-culler
