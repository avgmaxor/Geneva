# Simple client to client multiplayer
# One player hosts, the other joins with the host's IP
# Messages are newline separated JSON over a single TCP connection
import socket, threading, json

PORT = 5555

def localIp():
    # No packets are sent, this just asks the OS which interface it would use
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()

class Peer():
    def __init__(self):
        self.sock = None
        self.session = 0
        self.reset()

    def reset(self):
        self.connected = False
        self.started = False
        self.peerrnd = 1
        self.status = ''

    def host(self, port=PORT):
        self.close()
        self.status = 'Waiting for player... your IP: ' + localIp()
        threading.Thread(target=self._host, args=(self.session, port), daemon=True).start()

    def join(self, ip, port=PORT):
        self.close()
        self.status = 'Connecting to ' + ip + '...'
        threading.Thread(target=self._join, args=(self.session, ip, port), daemon=True).start()

    def send(self, **msg):
        if not self.connected:
            return
        try:
            self.sock.sendall((json.dumps(msg) + '\n').encode())
        except OSError:
            self.connected = False

    def close(self):
        # Bumping the session makes any old threads stop touching our state
        self.session += 1
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.sock.close()
            self.sock = None
        self.reset()

    def _host(self, session, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(0.5)
        try:
            server.bind(('', port))
            server.listen(1)
            while session == self.session:
                try:
                    conn, addr = server.accept()
                except socket.timeout:
                    continue
                if session != self.session:
                    conn.close()
                    return
                self.status = 'Player connected from ' + addr[0]
                self._listen(session, conn)
                return
        except OSError as e:
            if session == self.session:
                self.status = 'Could not host: ' + str(e)
        finally:
            server.close()

    def _join(self, session, ip, port):
        try:
            conn = socket.create_connection((ip, port), timeout=5)
        except OSError as e:
            if session == self.session:
                self.status = 'Could not connect: ' + str(e)
            return
        if session != self.session:
            conn.close()
            return
        self.status = 'Connected! waiting for host to start'
        self._listen(session, conn)

    def _listen(self, session, conn):
        conn.settimeout(None)
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock = conn
        self.connected = True
        buf = b''
        try:
            while session == self.session:
                data = conn.recv(1024)
                if not data:
                    break
                buf += data
                while b'\n' in buf:
                    line, buf = buf.split(b'\n', 1)
                    self._handle(json.loads(line))
        except (OSError, ValueError):
            pass
        if session == self.session:
            self.connected = False
            self.status = 'Opponent disconnected'

    def _handle(self, msg):
        if msg.get('type') == 'start':
            self.started = True
        if msg.get('type') == 'rnd':
            self.peerrnd = int(msg['value'])
