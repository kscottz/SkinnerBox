import json
import inspect, os, argparse, signal, sys
#import numpy as np
from bottle import get, post, run, request, static_file, route

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=imgPath)

@get('/')
def captureTopImg():
    return """<html>

    <link href="bootstrap.min.css" rel="stylesheet" media="screen">
    <script src="http://d3js.org/d3.v2.js"></script>  
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="bootstrap.min.js"></script>
    
    <body><center><h1>
    <div class="container">
        Top camera not connected.
    </div>
        </html></body></center></h1>
        """
@route('/derp/')
def derp():
    return "No top camera attached."

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='The Tempo CV Server')
    # #parser.add_argument('--settings', metavar='S',  nargs='+',
    # #                    help='Settings json file')
    # parser.add_argument('--no-camera', action='store_true',
    #                     help='Start the server with no cameras attached')
    signal.signal(signal.SIGINT, signal_handler)

    run(host='localhost', port=8080)
    exit(0)
