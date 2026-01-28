import os
import sys
from remdesk_project.wsgi import application

# GoDaddy/Passenger configuration
# This helps the server find your django project using the correct python interpreter
sys.path.insert(0, os.path.dirname(__file__))

# On some GoDaddy setups, they require the 'application' object to be directly available here
# The import above handles this by importing the fully configured Django app
