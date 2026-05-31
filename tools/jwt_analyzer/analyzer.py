import sys
import base64
import json
from datetime import datetime, timezone
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

def check_expiry(payload):
    exp = payload.get("exp")
    iat = payload.get("iat")
    now = datetime.now(timezone.utc).timestamp()

    print(Fore.CYAN + f"\n  {'─' * 40}")
    print(Fore.CYAN + f"  EXPIRY CHECK")
    print(Fore.CYAN + f"  {'─' * 40}" + Style.RESET_ALL)

    if exp:
        exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)
        if now > exp:
            print(f"  {Fore.RED}status              : ❌ EXPIRED")
            print(f"  {Fore.RED}expired at          : {exp_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        else:
            remaining = exp - now
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            print(f"  {Fore.GREEN}status              : ✅ VALID")
            print(f"  {Fore.GREEN}expires at          : {exp_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"  {Fore.GREEN}time remaining      : {minutes}m {seconds}s")
    else:
        print(f"  {Fore.RED}status              : ❌ NO EXPIRY SET — token never expires")

    if iat:
        iat_time = datetime.fromtimestamp(iat, tz=timezone.utc)
        print(f"  {Fore.CYAN}issued at           : {iat_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")

def check_security(header):
    alg = header.get("alg", "unknown")

    print(Fore.CYAN + f"\n  {'─' * 40}")
    print(Fore.CYAN + f"  SECURITY ANALYSIS")
    print(Fore.CYAN + f"  {'─' * 40}" + Style.RESET_ALL)

    if alg in DANGEROUS_ALGORITHMS:
        print(f"  {Fore.RED}algorithm           : ❌ DANGEROUS — '{alg}'")
        print(f"  {Fore.RED}risk                : No signature verification. Anyone can forge this token.")
        print(f"  {Fore.RED}recommendation      : Never use 'none' algorithm in production.")

    elif alg in WEAK_ALGORITHMS:
        print(f"  {Fore.YELLOW}algorithm           : ⚠️  WEAK — '{alg}'")
        print(f"  {Fore.YELLOW}risk                : Vulnerable to brute-force if secret is short or common.")
        print(f"  {Fore.YELLOW}recommendation      : Use RS256 or HS512 with a strong secret (32+ chars).")

    elif alg in STRONG_ALGORITHMS:
        print(f"  {Fore.GREEN}algorithm           : ✅ STRONG — '{alg}'")
        print(f"  {Fore.GREEN}recommendation      : Good algorithm choice.")

    else:
        print(f"  {Fore.YELLOW}algorithm           : ⚠️  UNKNOWN — '{alg}'")
        print(f"  {Fore.YELLOW}recommendation      : Verify this algorithm is secure and supported.")

    # Check for sensitive data in payload
    typ = header.get("typ", "")
    if typ.upper() == "JWT":
        print(f"  {Fore.CYAN}type                : JWT ✅")

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

    # Expiry check
    check_expiry(payload)

    # Security analysis
    check_security(header)

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