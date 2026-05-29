import requests
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    print(Fore.GREEN + """
    ╔═══════════════════════════════════╗
    ║     🌐 Subdomain Enumerator       ║
    ║   github.com/DevwithMujeeb       ║
    ╚═══════════════════════════════════╝
    """ + Style.RESET_ALL)

def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[ERROR] Wordlist not found: {path}")
        sys.exit(1)

def check_subdomain(domain, subdomain, timeout=3):
    # Try HTTPS first, fall back to HTTP
    for scheme in ["https", "http"]:
        url = f"{scheme}://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return response.status_code, url
        except requests.ConnectionError:
            continue
        except requests.Timeout:
            continue
        except Exception:
            continue
    return None, f"http://{subdomain}.{domain}"

def run_enum(domain, wordlist_path, timeout=3, output_file=None):
    print_banner()

    wordlist = load_wordlist(wordlist_path)

    print(Fore.CYAN + f"[*] Target   : {domain}")
    print(Fore.CYAN + f"[*] Wordlist : {wordlist_path} ({len(wordlist)} words)")
    print(Fore.CYAN + f"[*] Timeout  : {timeout}s per request")
    if output_file:
        print(Fore.CYAN + f"[*] Output   : {output_file}")
    print(Fore.CYAN + f"[*] Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.YELLOW + "-" * 50)

    found = []

    for word in wordlist:
        status, url = check_subdomain(domain, word, timeout)

        if status is not None:
            found.append(url)
            if status == 200:
                print(Fore.GREEN + f"[+] FOUND     {url} (200 OK)")
            elif status in [301, 302]:
                print(Fore.YELLOW + f"[~] REDIRECT  {url} ({status})")
            else:
                print(Fore.CYAN + f"[~] EXISTS    {url} ({status})")
        else:
            print(Fore.RED + f"[-] NOT FOUND {word}.{domain}")

    print(Fore.YELLOW + "-" * 50)

    if found:
        print(Fore.GREEN + f"[*] Scan complete. {len(found)} subdomain(s) found.")
    else:
        print(Fore.RED + "[*] Scan complete. No subdomains found.")

    print(Fore.CYAN + f"[*] Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Save results to file if output path provided
    if output_file and found:
        with open(output_file, "w") as f:
            f.write(f"# Subdomain Enumeration Results\n")
            f.write(f"# Target: {domain}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for url in found:
                f.write(url + "\n")
        print(Fore.GREEN + f"[*] Results saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print_banner()
        print(Fore.YELLOW + "Usage:")
        print("  python enumerator.py <domain>")
        print("  python enumerator.py <domain> <wordlist>")
        print("  python enumerator.py <domain> <wordlist> <timeout>")
        print("  python enumerator.py <domain> <wordlist> <timeout> <output_file>")
        print(Fore.CYAN + "\nExamples:")
        print("  python enumerator.py google.com")
        print("  python enumerator.py google.com ../../wordlists/subdomains.txt")
        print("  python enumerator.py google.com ../../wordlists/subdomains.txt 5")
        print("  python enumerator.py google.com ../../wordlists/subdomains.txt 5 results.txt")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist = sys.argv[2] if len(sys.argv) > 2 else "../../wordlists/subdomains.txt"
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 3
    output = sys.argv[4] if len(sys.argv) > 4 else None

    run_enum(domain, wordlist, timeout, output)

if __name__ == "__main__":
    main()