# Aegis-FIM
> A robust File Integrity Monitor (FIM) built in Python for security auditing and change detection.

## Project Purpose
Aegis-FIM is designed to monitor critical directories for unauthorized changes. In a real-world cybersecurity context, FIMs are used to ensure that system configurations, sensitive documents, and application binaries haven't been tampered with by an attacker. 

By utilizing **SHA-256 hashing**, Aegis-FIM creates a digital fingerprint of every file in a directory and compares it against a known "baseline" to detect modifications, additions, or deletions.

---

## Features
- **Recursive Directory Scanning:** Crawls entire folder structures to ensure no file is left un-monitored.
- **SHA-256 Integrity:** Uses industry-standard hashing to prevent collision attacks and ensure accurate detection.
- **Persistence:** Saves and loads baselines via JSON for cross-session monitoring.
- **Advanced CLI:** Fully featured command-line interface with arguments for custom paths and baseline locations.
- **Intelligent Logging:** Dual-stream logging (Console + File) with timestamps and severity levels (INFO/WARNING).
- **Apple macOS Optimization:** Automatically ignores `.DS_Store` noise.

---

## Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jasonsoprovich/aegis-fim.git
   cd aegis-fim
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

### Usage
**Generate an initial baseline:**
```bash
python3 main.py /path/to/monitor -b ./data/my_baseline.json
```

**Audit for changes:**
```bash
python3 main.py /path/to/monitor -b ./data/my_baseline.json
```

**Audit and prompt for baseline update:**
```bash
python3 main.py /path/to/monitor -b ./data/my_baseline.json -u
```

---

## Roadmap & Progress

### Completed
- [x] **Core Hashing Engine:** Reliable SHA-256 generation for files.
- [x] **Recursive Crawler:** Efficient `os.walk` implementation.
- [x] **JSON Persistence:** Ability to save/load snapshots of file states.
- [x] **Comparison Brain:** Logic to identify New, Modified, and Deleted files.
- [x] **CLI Implementation:** `argparse` integration for dynamic user input.
- [x] **Logging System:** Persistent audit logs in `./logs/audit.log`.

### In Progress
- [ ] **Exclusion Logic:** Prevent monitoring the baseline/data folder to avoid recursive loops.
- [ ] **Summary Statistics:** Display total file counts and change totals at the end of a scan.
- [ ] **Real-time Monitoring:** Integrate `watchdog` for instant change detection.
- [ ] **TUI (Terminal User Interface):** Implement `rich` for a professional, dashboard-style interface.

### Future Goals (V2)
- [ ] **Report Generation:** Export scan results to HTML/Markdown.
- [ ] **Alerting System:** Email or Slack notifications for critical file changes.
- [ ] **Multithreading:** Speed up hashing on large directories.

---

## Tech Stack
- **Language:** Python 3.x
- **Libraries:** `hashlib`, `json`, `os`, `argparse`, `logging`
- **Upcoming Libraries:** `watchdog`, `rich`
