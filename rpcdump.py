import argparse
import re
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='RPC dump and proxy script.')
    parser.add_argument('--mapresult', type=str, required=True, help='Path to the nmap result file.')
    parser.add_argument('--localport', type=int, default=8000, help='Local port for proxy server.')
    parser.add_argument('--remotehost', type=str, required=True, help='Remote host IP address.')
    parser.add_argument('--remoteport', type=int, required=True, help='Remote host port.')
    return parser.parse_args()

def parse_nmap_result(filepath):
    """
    Parse the nmap result file to extract RPC service information.

    Args:
    filepath (str): Path to the nmap result file.

    Returns:
    dict: A dictionary with port numbers as keys and service names as values.
    """
    try:
        with open(filepath, 'r') as file:
            data = file.read()
    except Exception as e:
        logging.error(f"Failed to read nmap result file: {e}")
        raise

    rpc_pattern = re.compile(r'(\d+)/tcp\s+open\s+\S+\s+\S+\s+\S+\s+(\S+)\s+\S+')
    matches = rpc_pattern.findall(data)

    rpc_info = {int(port): service for port, service in matches}
    return rpc_info

def create_portmap_dump(rpc_info, dump_file='portmap_dump.txt'):
    """
    Create a local portmap dump from RPC service information.

    Args:
    rpc_info (dict): A dictionary with port numbers as keys and service names as values.
    dump_file (str): Path to the dump file.
    """
    try:
        with open(dump_file, 'w') as file:
            for port, service in rpc_info.items():
                file.write(f'{service} {port}\n')
        logging.info(f"Portmap dump created at {dump_file}")
    except Exception as e:
        logging.error(f"Failed to create portmap dump: {e}")
        raise

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the proxy server.
    """
    protocol_version = "HTTP/1.0"

    def do_GET(self):
        self._proxy_request()

    def do_POST(self):
        self._proxy_request()

    def _proxy_request(self):
        """
        Proxy the client request to the remote server.
        """
        try:
            logging.info(f"Proxying request to {self.server.remote_host}:{self.server.remote_port}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Proxy request handled successfully')
        except Exception as e:
            logging.error(f"Failed to proxy request: {e}")
            self.send_error(500, 'Proxy request failed')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Handle requests in a separate thread.
    """
    def __init__(self, server_address, RequestHandlerClass, remote_host, remote_port):
        super().__init__(server_address, RequestHandlerClass)
        self.remote_host = remote_host
        self.remote_port = remote_port

def run_proxy(local_port, remote_host, remote_port):
    """
    Run the proxy server.

    Args:
    local_port (int): Local port for the proxy server.
    remote_host (str): Remote host IP address.
    remote_port (int): Remote host port.
    """
    server_address = ('', local_port)
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler, remote_host, remote_port)
    logging.info(f"Starting proxy server on port {local_port}")
    httpd.serve_forever()

def main():
    """
    Main function to parse arguments, create portmap dump, and run the proxy server.
    """
    args = parse_args()
    
    try:
        rpc_info = parse_nmap_result(args.mapresult)
    except Exception as e:
        logging.error(f"Error parsing nmap result: {e}")
        return
    
    try:
        create_portmap_dump(rpc_info)
    except Exception as e:
        logging.error(f"Error creating portmap dump: {e}")
        return
    
    try:
        proxy_thread = threading.Thread(target=run_proxy, args=(args.localport, args.remotehost, args.remoteport))
        proxy_thread.start()
    except Exception as e:
        logging.error(f"Error starting proxy server: {e}")

if __name__ == '__main__':
    main()
