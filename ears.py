import fnmatch
import json
import os
import socket
import subprocess
import sys


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


def serve(host, port, handler, handler_args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    try:
        while 1:
            conn, (client_host, client_port) = s.accept()
            if client_host == '127.0.0.1':
                handler(conn, *handler_args)
            conn.close()
    finally:
        s.close()


def handle(sock, config, args):
    command = '{0} {1}'.format(config['exec'], args)

    filename = sock.recv(1024)  # shouldn't be more data than this
    print filename

    for extension in config['watch']:
        if fnmatch.fnmatch(filename, extension):
            subprocess.call(command, shell=True)


def main():
    HOST, PORT = '127.0.0.1', 3277

    config = load_config()
    args = ' '.join(sys.argv[1:])
    try:
        serve(HOST, PORT, handle, [config, args])
    except KeyboardInterrupt:
        print '\nGoodbye'


if __name__ == '__main__':
    main()
