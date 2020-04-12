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

COPY ./requirements.txt /requirements.txt
# we need to copy our requirements.txt file to
#requirements.txt
#What this does is it says copy from the directory adjacent
#to the Docker file, copy the requirements
#file that we're going to create here and copy it on the Docker image to /requirements.txt

RUN pip3 install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# it creates a empty folder on our docket in the edge called forward slash at this location
#and then it switches to that as the default directory.

RUN adduser -D user
# create a user that is going to run our application using docker
# -D: create a user that is going to be used for running applications only.
# Not for basically having a home directory and that someone will log in to it's
# going to be used simply to run our processes from our project.
USER user
# switch to user
## Security reasons ##

#terminal: docker build .
#it says build which ever dock a file is in the root of our project that we're currently in.

# And it should be fairly quick because we using the Alpine image and the Alpine image is a very lightweight
#and minimal image that runs python.