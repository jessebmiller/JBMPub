# JBMPub

Publishing Stack for the personal website of Jesse B Miller.

## JesseBMiller.com Design Objectives

- To participate in the marketplace of ideas
- To challenge conventional thinking
- To show my expertise
- To increase awareness of myself
- To generate interest in my projects and ideas

## Install Requirements

    pip install pyzmq werkzeug
    
## Start all the services

start all the services from their respective folders

- /bartok/server.py
- /logic/api/logic_server.py
- /model/api/model_server.py
- /view/api/view_server.py

then start the werkzeug wsgi server

    python server.py localhost
    
