# Aegis-FIM
> A robust File Integrity Monitor (FIM) built in Python for security auditing and change detection.

## Project Purpose
Aegis-FIM is designed to monitor critical directories for unauthorized changes. In a real-world cybersecurity context, FIMs are used to ensure that system configurations, sensitive documents, and application binaries haven't been tampered with by an attacker. 

Aegis-FIM creates a **cryptographic fingerprint** (SHA-256 hash) of every 
file and compares it against a trusted "baseline" to detect unauthorized 
modifications, new files, or deletions.

---

## Features
- **Recursive Directory Scanning:** Crawls entire folder structures to ensure no file is left un-monitored
- **SHA-256 Integrity:** Uses industry-standard hashing to prevent collision attacks and ensure accurate detection
- **Persistence:** Saves and loads baselines via JSON for cross-session monitoring
- **Advanced CLI:** Fully featured command-line interface with arguments for custom paths and baseline locations
- **Intelligent Logging:** Dual-stream logging (Console + File) with timestamps and severity levels
- **Real-time Monitoring:** Watch mode provides instant change detection using filesystem events
- **Rich TUI:** Professional terminal interface with color-coded results and status indicators
- **macOS Optimization:** Automatically ignores `.DS_Store` and other system noise

---

## Getting Started

### Requirements
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jasonsoprovich/aegis-fim.git
   cd aegis-fim
   ```
2. (Recommended) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

**First-time setup (establish baseline):**
```bash
python3 main.py /path/to/monitor
```
*On first run, Aegis will create a baseline and save it to `./data/baseline.json`*

**Check for changes:**
```bash
python3 main.py /path/to/monitor
```
*Compares current state against the saved baseline*

**Update baseline after authorized changes:**
```bash
python3 main.py /path/to/monitor -u
```
*Prompts you to update the baseline if changes are detected*

**Use a custom baseline location:**
```bash
python3 main.py /path/to/monitor -b ./backups/baseline_2024.json
```

**Ignore specific files or directories:**
```bash
python3 main.py /path/to/monitor -i node_modules __pycache__ "*.tmp"
```

**Real-time monitoring mode:**
```bash
python3 main.py /path/to/monitor -w
```
*Continuously watches for changes (press Ctrl+C to stop)*

**Combine options:**
```bash
python3 main.py /path/to/monitor -b ./custom.json -i logs temp -w
```

**Preview changes without saving (Dry Run):**
```bash
python3 main.py /path/to/monitor -d
```

**See every file being processed (Verbose):**
```bash
python3 main.py /path/to/monitor -v
```

---

### Command-Line Options

| Flag | Long Form | Description |
|------|-----------|-------------|
| `-b` | `--baseline` | Specify custom baseline file path (default: `./data/baseline.json`) |
| `-u` | `--update` | Interactively update the baseline if discrepancies are identified |
| `-i` | `--ignore` | List of filenames or directory patterns to exclude from the audit |
| `-w` | `--watch` | Enable persistent real-time filesystem monitoring |
| `-d` | `--dry-run` | Preview changes without modifying the stored baseline |
| `-v` | `--verbose` | Enable detailed output, listing every file scanned during the audit |
| `-h` | `--help` | Show help message |

---

## How It Works

1. **Initial Scan:** Aegis recursively walks through the target directory and calculates SHA-256 hashes for each file
2. **Baseline Storage:** These hashes are stored in a JSON file (the "baseline")
3. **Subsequent Scans:** On future runs, Aegis compares new hashes against the baseline
4. **Change Detection:** 
   - **New files:** Present now but not in baseline
   - **Modified files:** Hash changed since baseline
   - **Deleted files:** In baseline but no longer exist
5. **Reporting:** Results are displayed in a color-coded table and logged to `./logs/audit.log`

---

## Troubleshooting

**Permission Denied Errors:**
- Aegis will skip files it can't read and log warnings
- Run with elevated privileges if monitoring system directories: `sudo python3 main.py /etc`

**Baseline file not found:**
- Ensure the `./data` directory exists (created automatically on first run)
- Check the path specified with `-b` flag

**Watch mode not working:**
- Ensure `watchdog` is installed: `pip install watchdog`
- Some network filesystems may not support file system events

---

## Roadmap & Progress

### Completed
- [x] **Core Hashing Engine:** Reliable SHA-256 generation for files.
- [x] **Recursive Crawler:** Efficient `os.walk` implementation.
- [x] **JSON Persistence:** Ability to save/load snapshots of file states.
- [x] **Comparison Brain:** Logic to identify New, Modified, and Deleted files.
- [x] **CLI Implementation:** `argparse` integration for dynamic user input.
- [x] **Logging System:** Persistent audit logs in `./logs/audit.log`.
- [x] **Exclusion Logic:** Prevent monitoring the baseline/data folder to avoid recursive loops.
- [x] **Summary Statistics:** Display total file counts and change totals at the end of a scan.
- [x] **Real-time Monitoring:** Integrate `watchdog` for instant change detection.
- [x] **TUI (Terminal User Interface):** Implement `rich` for a professional, dashboard-style interface.
- [x] **Progress Indicators:** Show progress bar during large scans
- [x] **Metadata Tracking:** Track file size, timestamps, and permissions
- [x] **Dry-Run Mode:** Preview baseline updates without applying them
- [x] **Error Summary:** Display files that couldn't be scanned with reasons
- [x] **Verbose Mode:** Optional detailed output of all scanned files

### In Progress
- [ ] **Export Results:** Save scan results to JSON for audit trails
- [ ] **Config File Support:** YAML/JSON config for easier repeated scans
- [ ] **Diff View:** Show before/after hashes for modified files

### Future Goals (V2)
- [ ] **Report Generation:** Export scan results to HTML/Markdown.
- [ ] **Alerting System:** Email or Slack notifications for critical file changes.
- [ ] **Multithreading:** Speed up hashing on large directories.
- [ ] **Checksum Algorithm Choice:** Allow MD5/SHA-1/SHA-512 selection
- [ ] **Encrypted Baselines:** Protect baseline files with encryption
- [ ] **Database Backend:** SQLite option for better performance on large datasets
- [ ] **Web Dashboard:** Simple Flask/FastAPI web interface
- [ ] **Signature Verification:** GPG signature support for critical files
- [ ] **Scheduled Scans:** Built-in cron-like scheduling
- [ ] **Cloud Storage Integration:** Store baselines in S3/Google Cloud

---

## Tech Stack
- **Language:** Python 3.x
- **Libraries:** `hashlib`, `json`, `os`, `argparse`, `logging`, `rich`, `watchdog`

## Contributing
This is a learning project, but suggestions and improvements are welcome! 
Feel free to open an issue or submit a pull request.

## License
MIT License - See LICENSE file for details

## Author
Built by Jason as a cybersecurity learning project
