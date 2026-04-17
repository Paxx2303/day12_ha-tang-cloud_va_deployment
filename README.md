# Day 12 Lab - Deploy AI Agent to Production

> **Grading Instructions** | VinUniversity 2026

---

## Quick Deploy (5 min)

### Deploy to Render
1. Go to: https://render.com
2. Connect GitHub: `Paxx2303/day12_ha-tang-cloud_va_deployment`
3. Create new **Docker** service (name: `ai-agent`)
4. Add Environment Variables:
   ```
   AGENT_API_KEY=dev-key-change-me
   ENVIRONMENT=production
   RATE_LIMIT_PER_MINUTE=10
   ```
5. Deploy

### Test
```bash
# Health (should return 200)
curl https://<app>.onrender.com/health

# With auth (should return 200)
curl -X POST https://<app>.onrender.com/ask \
  -H "X-API-Key: dev-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

---

## Auto Grading (Recommended)

Run the grading script:

```bash
python grade.py
# or with custom URL/API key:
python grade.py https://your-app.onrender.com your-api-key
```

Expected output:
```
============================================================
DAY 12 LAB - AUTO GRADING
============================================================
[PASS] Agent responds correctly: 10/10
[PASS] Error handling: 5/5
[PASS] Response metadata: 5/5
[PASS] Multi-stage Dockerfile: 5/5
[PASS] docker-compose.yml: 4/4
[PASS] Environment config: 3/3
[PASS] No hardcoded config: 3/3
[PASS] Auth required (no key): 5/5
[PASS] Auth with valid key: 5/5
[PASS] Rate limiting: 5/5
[PASS] No hardcoded secrets: 5/5
[PASS] /health endpoint: 3/3
[PASS] /ready endpoint: 3/3
[PASS] Graceful shutdown: 4/4
[PASS] Stateless design: 5/5
[PASS] Public URL works: 5/5
[PASS] Config files exist: 3/3
[PASS] Environment set: 2/2
============================================================
TOTAL: 75/80
============================================================
PASSED (>= 70%)
```

---

## Manual Test Commands

### Using Python (Recommended)

```python
import requests

BASE_URL = "https://day12-ha-tang-cloud-va-deployment-2.onrender.com"
API_KEY = "dev-key-change-me"

# 1. Health - should return 200
r = requests.get(f"{BASE_URL}/health")
print(f"Health: {r.status_code}")  # Expect: 200

# 2. Readiness - should return 200
r = requests.get(f"{BASE_URL}/ready")
print(f"Ready: {r.status_code}")  # Expect: 200

# 3. No auth - should return 401
r = requests.post(f"{BASE_URL}/ask", json={"question": "test"})
print(f"No auth: {r.status_code}")  # Expect: 401

# 4. With auth - should return 200
headers = {"X-API-Key": API_KEY}
r = requests.post(f"{BASE_URL}/ask", json={"question": "test"}, headers=headers)
print(f"With auth: {r.status_code}")  # Expect: 200

# 5. Rate limit - should return 429 after ~10 requests
for i in range(15):
    r = requests.post(f"{BASE_URL}/ask", json={"question": "test"}, headers=headers)
    if r.status_code == 429:
        print(f"Rate limited at request {i+1}")  # Expect: 429
        break
```

---

## Grading Criteria (Based on INSTRUCTOR_GUIDE.md)

| Category | Points | Test |
|----------|-------|------|
| **Functionality** | **20** | |
| - Agent responds | 10 | `/ask` returns 200 with answer |
| - Error handling | 5 | Invalid input returns 4xx |
| - Response metadata | 5 | Has model/timestamp |
| **Docker** | **15** | |
| - Multi-stage Dockerfile | 5 | Manual check |
| - docker-compose.yml | 4 | Manual check |
| - Environment config | 3 | Config from env vars |
| - No hardcoded config | 3 | Manual check |
| **Security** | **20** | |
| - Auth required | 5 | No key = 401 |
| - Auth works | 5 | Valid key = 200 |
| - Rate limiting | 5 | Too many requests = 429 |
| - No hardcoded secrets | 5 | Manual check |
| **Reliability** | **15** | |
| - Health endpoint | 3 | `/health` = 200 |
| - Readiness endpoint | 3 | `/ready` = 200 |
| - Graceful shutdown | 4 | Manual check |
| - Stateless design | 5 | Manual check |
| **Deployment** | **10** | |
| - Public URL works | 5 | URL returns 200 |
| - Config files exist | 3 | Manual check |
| - Environment set | 2 | Has env var |
| **Total** | **80** | **Pass: >= 56 (70%)** |

---

## Files in Project

- `Dockerfile` - Multi-stage, < 500MB
- `docker-compose.yml` - Agent + Redis
- `app/main.py` - FastAPI agent
- `app/config.py` - 12-factor config
- `requirements.txt` - Dependencies
- `grade.py` - Auto grading
- `test_checklist.py` - Quick test

---

## Live URL for Testing

```
https://day12-ha-tang-cloud-va-deployment-2.onrender.com
```

API Key: `dev-key-change-me`