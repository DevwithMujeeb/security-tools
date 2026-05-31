# 🛠️ Security Tools

A collection of Python CLI security tools built as part of my 90-day open-source build challenge. Each tool is standalone, documented, and runs from the command line.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> ⚠️ These tools are for educational and authorized testing only. Never use against systems you don't own.

---

## 🔧 Tools

| Tool                    | Description                                                 | Status  |
| ----------------------- | ----------------------------------------------------------- | ------- |
| 🔍 Port Scanner         | TCP port scanner with service detection                     | ✅ Done |
| 🌐 Subdomain Enumerator | Wordlist-based subdomain discovery with HTTPS + export      | ✅ Done |
| 🔑 JWT Analyzer         | CLI tool to decode, inspect and security-analyze JWT tokens | ✅ Done |

---

## 🚀 Installation

```bash
git clone https://github.com/DevwithMujeeb/security-tools.git
cd security-tools
pip install -r requirements.txt
```

---

## 📖 Usage

### 🔍 Port Scanner

Scans a target for open TCP ports and identifies running services.

```bash
cd tools/port_scanner
python scanner.py <target>
python scanner.py <target> <port>
python scanner.py <target> <start_port> <end_port>
python scanner.py <target> <start_port> <end_port> <timeout>
```

**Examples:**

```bash
python scanner.py localhost
python scanner.py localhost 80
python scanner.py localhost 1 1000
python scanner.py localhost 1 1000 0.5
```

**Output:**

```
[+] Port 22     OPEN   SSH
[+] Port 80     OPEN   HTTP
[+] Port 443    OPEN   HTTPS
```

---

### 🌐 Subdomain Enumerator

Discovers subdomains using a wordlist. Tries HTTPS first, falls back to HTTP. Optionally saves results to a file.

```bash
cd tools/subdomain_enum
python enumerator.py <domain>
python enumerator.py <domain> <wordlist>
python enumerator.py <domain> <wordlist> <timeout>
python enumerator.py <domain> <wordlist> <timeout> <output_file>
```

**Examples:**

```bash
python enumerator.py google.com
python enumerator.py google.com ../../wordlists/subdomains.txt
python enumerator.py google.com ../../wordlists/subdomains.txt 5
python enumerator.py google.com ../../wordlists/subdomains.txt 5 results.txt
```

**Output:**

```
[+] FOUND     https://www.google.com (200 OK)
[~] REDIRECT  https://mail.google.com (301)
[-] NOT FOUND ftp.google.com
```

---

### 🔑 JWT Analyzer

Decodes and security-analyzes JWT tokens from the command line. Checks expiry, flags weak algorithms, and shows all claims.

```bash
cd tools/jwt_analyzer
python analyzer.py <jwt_token>
```

**Example:**

```bash
python analyzer.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMyIsInJvbGUiOiJhZG1pbiJ9.signature
```

**What it checks:**

- Decodes header, payload, and signature
- Token expiry status and time remaining
- Flags dangerous algorithms (`none`) — forgeable tokens
- Flags weak algorithms (`HS256`) — brute-force risk
- Shows issued at and expires at timestamps

**Output:**

```
  HEADER
  algorithm           : HS256
  type                : JWT

  PAYLOAD
  id                  : 123
  role                : admin
  iat                 : 1234567890
  exp                 : 1234568790

  EXPIRY CHECK
  status              : ✅ VALID
  expires at          : 2026-05-15 17:45:48 UTC
  time remaining      : 14m 32s

  SECURITY ANALYSIS
  algorithm           : ⚠️ WEAK — 'HS256'
  risk                : Vulnerable to brute-force if secret is short or common.
  recommendation      : Use RS256 or HS512 with a strong secret (32+ chars).
```

---

## 📁 Project Structure

```
security-tools/
├── tools/
│   ├── port_scanner/
│   │   └── scanner.py
│   ├── subdomain_enum/
│   │   └── enumerator.py
│   └── jwt_analyzer/
│       └── analyzer.py
├── wordlists/
│   └── subdomains.txt
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗺️ Part of the 90-Day Build Challenge

| Project                                                                   | Description                         | Status      |
| ------------------------------------------------------------------------- | ----------------------------------- | ----------- |
| [Secure Auth API](https://github.com/DevwithMujeeb/secure-auth-api)       | Production-grade JWT auth with RBAC | ✅ Shipped  |
| [Vulnerable Web Lab](https://github.com/DevwithMujeeb/vulnerable-web-lab) | OWASP Top 10 exploit and patch lab  | ✅ Shipped  |
| Security Tools (this repo)                                                | Python CLI security tools           | ✅ Shipped  |
| Secure Fullstack App                                                      | React + Node.js with security layer | 🔜 Building |

---

## 👨‍💻 Author

**Abdulmujeeb Uthman**

- GitHub: [@DevwithMujeeb](https://github.com/DevwithMujeeb)
- X: [@JeebExplains](https://x.com/JeebExplains)
- LinkedIn: [Abdulmujeeb Uthman](https://linkedin.com/in/abdulmujeeb-uthman)

---

## 📄 License

MIT License — use these tools however you want for learning and authorized testing.
