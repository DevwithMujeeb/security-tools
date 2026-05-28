import socket
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Common ports and their services
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def print_banner():
    print(Fore.GREEN + """
    ╔═══════════════════════════════════╗
    ║        🔍 Port Scanner            ║
    ║   github.com/DevwithMujeeb       ║
    ╚═══════════════════════════════════╝
    """ + Style.RESET_ALL)

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(Fore.RED + f"[ERROR] Could not resolve host: {target}")
        sys.exit(1)

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def get_service(port):
    return COMMON_SERVICES.get(port, "Unknown")

def scan(target, start_port, end_port):
    print_banner()

    ip = resolve_target(target)

    print(Fore.CYAN + f"[*] Target   : {target} ({ip})")
    print(Fore.CYAN + f"[*] Ports    : {start_port} - {end_port}")
    print(Fore.CYAN + f"[*] Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.YELLOW + "-" * 45)

    open_ports = []

    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            service = get_service(port)
            open_ports.append(port)
            print(Fore.GREEN + f"[+] Port {port:<6} OPEN   {service}")

    print(Fore.YELLOW + "-" * 45)

    if open_ports:
        print(Fore.GREEN + f"[*] Scan complete. {len(open_ports)} open port(s) found.")
    else:
        print(Fore.RED + "[*] Scan complete. No open ports found.")

    print(Fore.CYAN + f"[*] Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    if len(sys.argv) < 2:
        print(Fore.YELLOW + "Usage:")
        print("  python scanner.py <target>")
        print("  python scanner.py <target> <port>")
        print("  python scanner.py <target> <start_port> <end_port>")
        print(Fore.CYAN + "\nExamples:")
        print("  python scanner.py localhost")
        print("  python scanner.py localhost 80")
        print("  python scanner.py localhost 1 1000")
        sys.exit(1)

    target = sys.argv[1]

    # Single port
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        scan(target, port, port)

    # Port range
    elif len(sys.argv) == 4:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
        scan(target, start_port, end_port)

    # Default — scan common ports
    else:
        scan(target, 1, 1024)

if __name__ == "__main__":
    main()