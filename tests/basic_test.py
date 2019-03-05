import os
import re
import threading
try:
    import http.server as http
    import socketserver
except ImportError:
    import SimpleHTTPServer as http
    import SocketServer as socketserver
import subprocess


if __name__ == '__main__':
    # Start webserver
    socketserver.TCPServer.allow_reuse_address = True

    class Handler(http.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Testing'.encode('utf-8'))
    server = socketserver.TCPServer(('127.0.0.1', 50422), Handler)

    def serve():
        server.serve_forever()
    threading.Thread(target=serve).start()

    # Run spider
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        if 'PYTHONPATH' in os.environ:
            env['PYTHONPATH'] += ':' + os.environ['PYTHONPATH']
        scrapy = subprocess.Popen([
            'scrapy', 'runspider', 'tests/test_spider.py'
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = scrapy.communicate()[0].decode('utf-8')
        if scrapy.returncode != 0:
            print(log)
            raise RuntimeError('Errors running test_spider')
    finally:
        # Cleanup
        server.shutdown()
    errors = re.search('log_count/ERROR.: (?P<c>\\d+),', log, re.S)
    if errors:
        errors = errors.group('c')
    if errors:
        errors = int(errors)
    if errors:
        print(log)
        raise RuntimeError('Errors running test_spider')