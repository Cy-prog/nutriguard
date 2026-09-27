import urllib.request
import urllib.error
import json

BASE = "http://127.0.0.1:8001"

# 1. Health check
print("=== Health Check ===")
r = urllib.request.urlopen(f"{BASE}/health")
print(f"  Status: {r.status} | {r.read().decode()}")

# 2. Readiness check
print("\n=== Readiness Check ===")
r = urllib.request.urlopen(f"{BASE}/health/ready")
print(f"  Status: {r.status} | {r.read().decode()}")

# 3. Login
print("\n=== Login ===")
import urllib.parse
data = urllib.parse.urlencode({"username": "user@nutriguard.com", "password": "password123"}).encode()
req = urllib.request.Request(f"{BASE}/api/v1/auth/login", data=data)
try:
    r = urllib.request.urlopen(req)
    login_resp = json.loads(r.read().decode())
    token = login_resp.get("access_token", "")
    print(f"  Login OK! Token: {token[:30]}...")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"  Login failed: {e.code} {body}")
    token = None

# 4. If logged in, try fetching profile
if token:
    print("\n=== Profile ===")
    req = urllib.request.Request(f"{BASE}/api/v1/me/profile")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        r = urllib.request.urlopen(req)
        profile = json.loads(r.read().decode())
        print(f"  Name: {profile.get('name', 'N/A')}")
        print(f"  Email: {profile.get('email', 'N/A')}")
    except urllib.error.HTTPError as e:
        print(f"  Profile failed: {e.code} {e.read().decode()[:200]}")

    # 5. List meals
    print("\n=== Meals (first 3) ===")
    req = urllib.request.Request(f"{BASE}/api/v1/meals/?limit=3")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        r = urllib.request.urlopen(req)
        meals = json.loads(r.read().decode())
        if isinstance(meals, list):
            for m in meals[:3]:
                print(f"  - {m.get('name', 'N/A')} ({m.get('meal_type', '?')})")
        else:
            items = meals.get("items", meals.get("meals", []))
            for m in items[:3]:
                print(f"  - {m.get('name', 'N/A')} ({m.get('meal_type', '?')})")
    except urllib.error.HTTPError as e:
        print(f"  Meals failed: {e.code} {e.read().decode()[:200]}")

print("\n=== All checks complete ===")
