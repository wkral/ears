import fnmatch
import json
import os
import socket
import subprocess
import sys
import threading
import Queue


def load_config_file(config_path):
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except:
        sys.stderr.write("Error parsing json config file.\n")
        sys.exit(1)

    return {}


def load_config():
    ''' Load the configuration data based on the current working directory or
        the home folders default configurations '''

    config = {}

    config.update(load_config_file(os.path.expanduser("~/.ears")))
    config.update(load_config_file('.ears'))

    if not config:
        sys.stderr.write("No config file (.ears) found in current or home "
                         "folder\n")
        sys.exit(1)

    return config


def serve(host, port, config, queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    try:
        while 1:
            conn, (client_host, client_port) = s.accept()
            filename = conn.recv(1024)  # shouldn't be more data than this
            conn.close()  # Don't make the other end wait for the results
            for extension in config['watch']:
                if fnmatch.fnmatch(filename, extension):
                    try:
                        queue.put_nowait(filename)
                    except Queue.Full:
                        pass  # Don't need to queue up too many jobs
    finally:
        s.close()


def worker(config, queue):
    args = ' '.join(sys.argv[1:])

    command = '{0} {1}'.format(config['exec'], args)

    while 1:
        filename = queue.get()
        for extension in config['watch']:
            if fnmatch.fnmatch(filename, extension):
                subprocess.call(command, shell=True)


def main():
    HOST, PORT = '', 3277

    config = load_config()

    queue = Queue.Queue(maxsize=1)

    thread = threading.Thread(target=worker, args=(config, queue))
    thread.daemon = True
    thread.start()

    try:
        serve(HOST, PORT, config, queue)
    except KeyboardInterrupt:
        print '\rGoodbye'


if __name__ == '__main__':
    main()
