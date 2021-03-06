FROM python:3.7-alpine
# This image what it is is basically a lightweight version of Docker.
# That's what the Alpine means and it runs Python 3.7.
# the tag name 3.7-alpine
MAINTAINER Goldie App Developer Ltd

ENV PYTHONUNBUFFERED 1
# What this does is it tells Python to run in unbuffered mode which
# is recommended when running Python within Docker containers.
# The reason for this is that it doesn't allow Python to buffer the outputs.
# It just prints them directly.

# Install dependencies
COPY ./requirements.txt /requirements.txt
# we need to copy our requirements.txt file to
# requirements.txt
# What this does is it says copy from the directory adjacent
# to the Docker file, copy the requirements
# file that we're going to create here and copy it on the Docker image to /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
# it uses the package manager that comes with Alpine
# and it says this is the name of the package
# this is the dependencies that we add that we don't
# remove after we've installed the requirements
# jpeg-dev this adds the JPEG dev binaries to our docker file

# this update means update theregistry before we add
# it but this no cache means don't store the registry index on our docker file.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# it sets up an alias for our
# dependencies that we can use to easily remove all those dependencies later.
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
# deletes the temporary requirements

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# it creates a empty folder on our docket in the edge called forward slash at this location
# and then it switches to that as the default directory.

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# this is so we have a place where we can store the static
# and media files within our container without getting any permission errors
# -p: make all of the sub directories including the directory

RUN adduser -D user
# create a user that is going to run our application using docker
# -D: create a user that is going to be used for running applications only.
# Not for basically having a home directory and that someone will log in to it's
# going to be used simply to run our processes from our project.

RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
# change the ownership of these files (in vol directory) to the user
# R: recursive

USER user
# switch to user
# Security reasons

# terminal: docker build .
# it says build which ever dock a file is in the root of our project that we're currently in.

# And it should be fairly quick because we using the Alpine image and the Alpine
# image is a very lightweight and minimal image that runs python.