#
# JBMPub Model API
#
# Structures and serves content from a git repo
#

FROM ubuntu
MAINTAINER Jesse B Miller, jesse@jessebmiller.com

RUN apt-get update
RUN apt-get install -y git python-pip python-dev
RUN pip install supervisor
RUN git clone https://github.com/jessebmiller/JBMPub.git /srv/JBMPub
