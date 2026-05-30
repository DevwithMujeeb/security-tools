import sys
import base64
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Algorithms considered weak or dangerous
DANGEROUS_ALGORITHMS = ["none", "None", "NONE"]
WEAK_ALGORITHMS = ["HS256"]
STRONG_ALGORITHMS = ["HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]

def print_banner():
    print(Fore.GREEN + """
    ╔═══════════════════════════════════╗
    ║       🔑 JWT Analyzer             ║
    ║   github.com/DevwithMujeeb       ║
    ╚═══════════════════════════════════╝
    """ + Style.RESET_ALL)

def decode_base64(data):
    # Add padding if needed
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    try:
        decoded = base64.urlsafe_b64decode(data)
        return json.loads(decoded)
    except Exception:
        return None

def parse_token(token):
    parts = token.strip().split(".")
    if len(parts) != 3:
        print(Fore.RED + "[ERROR] Invalid JWT format. Expected 3 parts separated by dots.")
        sys.exit(1)

    header = decode_base64(parts[0])
    payload = decode_base64(parts[1])
    signature = parts[2]

    if not header or not payload:
        print(Fore.RED + "[ERROR] Could not decode token. Make sure it is a valid JWT.")
        sys.exit(1)

    return header, payload, signature

def print_section(title, data, color):
    print(color + f"\n  {'─' * 40}")
    print(color + f"  {title}")
    print(color + f"  {'─' * 40}" + Style.RESET_ALL)
    for key, value in data.items():
        print(f"  {Fore.CYAN}{key:<20}{Style.RESET_ALL}: {value}")

def analyze(token):
    print_banner()
    print(Fore.YELLOW + "-" * 50)
    print(Fore.CYAN + f"[*] Analyzing token...")
    print(Fore.YELLOW + "-" * 50)

    header, payload, signature = parse_token(token)

    # Print header
    print_section("HEADER", header, Fore.CYAN)

    # Print payload
    print_section("PAYLOAD", payload, Fore.GREEN)

    # Print signature status
    print(Fore.CYAN + f"\n  {'─' * 40}")
    print(Fore.CYAN + f"  SIGNATURE")
    print(Fore.CYAN + f"  {'─' * 40}" + Style.RESET_ALL)
    print(f"  {Fore.CYAN}{'signature':<20}{Style.RESET_ALL}: {signature[:32]}...")
    print(f"  {Fore.YELLOW}note                : signature cannot be verified without the secret key")

    print(Fore.YELLOW + "\n" + "-" * 50)
    print(Fore.CYAN + "[*] Analysis complete.")

def main():
    if len(sys.argv) < 2:
        print_banner()
        print(Fore.YELLOW + "Usage:")
        print("  python analyzer.py <jwt_token>")
        print(Fore.CYAN + "\nExamples:")
        print('  python analyzer.py eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signature')
        sys.exit(1)

    token = sys.argv[1]
    analyze(token)

if __name__ == "__main__":
    main()