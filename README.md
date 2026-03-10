# Python DevOps Toolkit

Python automation toolkit for DevOps workflows — REST API testing, system monitoring, and deployment helpers.

## Contents

| File | Description |
|---|---|
| `tests/test_api.py` | PyTest REST API validation framework covering 90+ endpoints |
| `tests/conftest.py` | Shared test fixtures and configuration |
| `scripts/sys_monitor.py` | System health monitor — CPU, memory, disk, service checks |

## Usage

### Run API Tests
```bash
export API_BASE_URL=http://your-api.com
export API_TOKEN=your-token
pytest tests/ -v --tb=short
```

### System Monitor
```bash
python3 scripts/sys_monitor.py
```

## Stack

`Python` `PyTest` `Requests` `REST APIs` `Linux` `Bash`
