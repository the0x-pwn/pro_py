إليك ملف **README احترافي كامل** جاهز للنشر على GitHub لأداتك:

---

# GhostDir

**GhostDir** is a high-performance directory and file discovery tool written in Python, designed for fast and flexible web content enumeration using multi-threading and advanced filtering options.

It supports proxy routing (Burp Suite compatible), status filtering, response size filtering, and multiple operational modes for speed or debugging.

---

## 🚀 Features

* ⚡ Multi-threaded scanning using `ThreadPoolExecutor`
* 🔥 Fast mode for high-speed brute forcing
* 🐢 Burp mode for controlled debugging and traffic inspection
* 🎯 Status code filtering (`-fc`)
* 📦 Response size filtering (`-fs`)
* 🌐 Proxy support (Burp Suite / custom proxies)
* ⏱ Adjustable timeout handling
* 🧾 Custom HTTP headers support
* 📊 Live request monitoring (requests sent / errors / timeout tracking)
* 🧠 Smart response validation (filters false positives)

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/GhostDir.git
cd GhostDir
pip install -r requirements.txt
```

### Requirements

```txt
requests
urllib3
```

---

## ⚙️ Usage

### Basic Usage

```bash
python ghostdir.py -u https://example.com -w wordlist.txt
```

---

## 🧩 Arguments

| Flag               | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `-u`, `--url`      | Target URL (required)                                         |
| `-w`, `--wordlist` | Path to wordlist file (required)                              |
| `--timeout`        | Request timeout (default: 10s)                                |
| `-t`, `--threads`  | Number of threads (default: 30)                               |
| `-fc`              | Filter HTTP status codes (e.g. 404,403)                       |
| `-fs`              | Filter response sizes (e.g. 1024,2048)                        |
| `-H`               | Custom HTTP headers (e.g. `User-Agent:xxx,Authorization:yyy`) |
| `--proxy`          | Proxy support (e.g. Burp Suite `http://127.0.0.1:8080`)       |
| `--mode`           | Execution mode: `fast` or `burp`                              |

---

## ⚡ Modes

### 🔥 Fast Mode (Default)

Optimized for maximum speed:

```bash
python ghostdir.py -u https://example.com -w wordlist.txt --mode fast
```

* Higher thread count (up to 50)
* Minimal delay
* Best for large wordlists

---

### 🐢 Burp Mode

Optimized for traffic analysis in Burp Suite:

```bash
python ghostdir.py -u https://example.com -w wordlist.txt --mode burp --proxy http://127.0.0.1:8080
```

* Reduced threads (3)
* Added delay between requests
* Enhanced visibility in proxy tools

---

## 🔍 Filtering Examples

### Filter Status Codes

Ignore 404 and 403 responses:

```bash
python ghostdir.py -u https://example.com -w wordlist.txt -fc 404,403
```

---

### Filter Response Sizes

Ignore responses of specific sizes:

```bash
python ghostdir.py -u https://example.com -w wordlist.txt -fs 0,1254
```

---

## 🧪 Custom Headers

```bash
python ghostdir.py -u https://example.com -w wordlist.txt -H "User-Agent:Mozilla/5.0,Authorization:Bearer TOKEN"
```

---

## 🌐 Proxy Support (Burp Suite)

```bash
python ghostdir.py -u https://example.com -w wordlist.txt --proxy http://127.0.0.1:8080
```

---

## 📊 Output Example

```
[+] admin [Status: 200] [Size: 5321 B]
[+] backup [Status: 301] [Size: 0 B]
[+] login [Status: 200] [Size: 2210 B]
```

---

## 📈 Live Statistics

During execution, GhostDir displays:

* Total requests sent
* Timeout errors
* Connection errors
* Found paths count

---

## ⚠️ Disclaimer

This tool is intended for:

* Security research
* Penetration testing (with authorization)
* Educational purposes

❗ Unauthorized scanning of systems you do not own or have permission to test is illegal. The developer is not responsible for any misuse of this tool.

---

## 🧠 How It Works

GhostDir performs:

1. Reads wordlist entries
2. Appends each word to target URL
3. Sends HTTP GET requests using multi-threading
4. Filters responses based on:

   * Status code
   * Response size
5. Displays valid endpoints in real time

---

## 🛠 Example Workflow

```bash
python ghostdir.py \
-u https://target.com \
-w wordlist.txt \
-t 30 \
--timeout 10 \
-fc 404 \
--mode fast
```

---

## 🔥 Performance Tips

* Use `fast` mode for large wordlists
* Use `burp` mode for debugging requests
* Combine `-fc 404` to reduce noise
* Use proxy only when needed (it slows requests)

---

## 📌 Author

**Ali Waled**
