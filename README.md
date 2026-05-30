# 🛠️ Security Tools

A collection of Python CLI security tools built as part of my 90-day open-source challenge.

## Tools

| Tool                    | Description                                                 | Status  |
| ----------------------- | ----------------------------------------------------------- | ------- |
| 🔍 Port Scanner         | TCP port scanner with service detection                     | ✅ Done |
| 🌐 Subdomain Enumerator | Wordlist-based subdomain discovery with HTTPS + export      | ✅ Done |
| 🔑 JWT Analyzer         | CLI tool to decode, inspect and security-analyze JWT tokens | ✅ Done |

## Usage

### 🔍 Port Scanner

```bash
cd tools/port_scanner
python scanner.py <target>
python scanner.py <target> <port>
python scanner.py <target> <start_port> <end_port>
python scanner.py <target> <start_port> <end_port> <timeout>
```

Examples:

```bash
python scanner.py localhost
python scanner.py localhost 80
python scanner.py localhost 1 1000
python scanner.py localhost 1 1000 0.5
```

### 🌐 Subdomain Enumerator

```bash
cd tools/subdomain_enum
python enumerator.py <domain>
python enumerator.py <domain> <wordlist>
python enumerator.py <domain> <wordlist> <timeout>
python enumerator.py <domain> <wordlist> <timeout> <output_file>
```

Examples:

```bash
python enumerator.py google.com
python enumerator.py google.com ../../wordlists/subdomains.txt
python enumerator.py google.com ../../wordlists/subdomains.txt 5
python enumerator.py google.com ../../wordlists/subdomains.txt 5 results.txt
```

### 🔑 JWT Analyzer

```bash
cd tools/jwt_analyzer
python analyzer.py <jwt_token>
```

Example:

```bash
python analyzer.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMyIsInJvbGUiOiJhZG1pbiJ9.signature
```

What it checks:

- Decodes header, payload and signature
- Checks token expiry and time remaining
- Flags dangerous algorithms (none)
- Flags weak algorithms (HS256)
- Shows issued at and expires at timestamps

## Requirements

```bash
pip install requests colorama
```

## Part of the 90-Day Build Challenge

| Project                                                                   | Status      |
| ------------------------------------------------------------------------- | ----------- |
| [Secure Auth API](https://github.com/DevwithMujeeb/secure-auth-api)       | ✅ Shipped  |
| [Vulnerable Web Lab](https://github.com/DevwithMujeeb/vulnerable-web-lab) | ✅ Shipped  |
| Security Tools (this repo)                                                | 🔜 Building |
