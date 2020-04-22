from cryptography import x509
import cryptography
from cryptography.hazmat.backends import default_backend
import time
import ssl
import socket


def get_certificate(host, port, timeout=3, retry_attempts: int = 3, retry_rate: int = 2,
                    current_attempt: int = 0):
    socket.setdefaulttimeout(timeout)  # Set Socket Timeout

    try:
        print(f"Fetching seednode {host}:{port} TLS certificate")
        seednode_certificate = ssl.get_server_certificate(addr=(host, port))

    except socket.timeout:
        if current_attempt == retry_attempts:
            message = f"No Response from seednode {host}:{port} after {retry_attempts} attempts"
            print(message)
            raise ConnectionRefusedError("No response from {}:{}".format(host, port))
        print("No Response from seednode {host}:{port}. Retrying in {retry_rate} seconds...")
        time.sleep(retry_rate)
        return get_certificate(host, port, timeout, retry_attempts, retry_rate, current_attempt + 1)

    except OSError:
        raise  # TODO: #1835

    else:
        certificate = x509.load_pem_x509_certificate(seednode_certificate.encode(),
                                                     backend=default_backend())
        return certificate


print(get_certificate("188.165.23.19", 443))