# Dockerfile
# https://medium.com/@parth_24073/configure-docker-with-django-postgresql-pg-admin-elasticsearch-b8711420cdf5

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install Supervisor.
RUN mkdir -p /var/log/celery 
RUN apt-get update&&apt-get upgrade -y
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor

# Set work directory
RUN mkdir /code/
WORKDIR /code/

# install dependencies
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Copy supervisor configs
RUN \
    cp configs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
    cp configs/conf.d/*.conf /etc/supervisor/conf.d/

# https://github.com/pm990320/docker-flask-celery/blob/master/Dockerfile

# expose port 80 of the container (HTTP port, change to 443 for HTTPS)
EXPOSE 80

# needs to be set else Celery gives an error (because docker runs commands inside container as root)
ENV C_FORCE_ROOT=1

# run supervisord
CMD ["/usr/bin/supervisord"]

