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


def serve(host, port, queues):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    try:
        while 1:
            conn, (client_host, client_port) = s.accept()
            filename = conn.recv(1024)  # shouldn't be more data than this
            conn.close()  # Don't make the other end wait for the results
            for queue in queues:
                try:
                    queue.put_nowait(filename)
                except Queue.Full:
                    pass  # Don't need to queue up too many jobs
    finally:
        s.close()


def worker(job, queue):
    while 1:
        filename = queue.get()
        if not filename.startswith(job['cwd']):
            continue
        for extension in job['watch']:
            if fnmatch.fnmatch(filename, extension):
                output = None if job.get('output', True) else subprocess.PIPE
                subprocess.call(job['exec'], shell=True, stdout=output,
                                stderr=output)


def main():
    HOST, PORT = '', 3277

    config = load_config()

    queues = []
    cwd = os.getcwd()

    for job in config['jobs']:
        queue = Queue.Queue(maxsize=1)
        job['cwd'] = cwd

        thread = threading.Thread(target=worker, args=(job, queue))
        thread.daemon = True
        thread.start()
        queues.append(queue)

    try:
        serve(HOST, PORT, queues)
    except KeyboardInterrupt:
        print '\rGoodbye'


if __name__ == '__main__':
    main()
