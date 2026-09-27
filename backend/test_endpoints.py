import urllib.request
import urllib.error
import urllib.parse
import json
import os

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

def run_smoke_test():
    # 1. Health check
    print("=== Health Check ===")
    try:
        r = urllib.request.urlopen(f"{BASE}/health")
        print(f"  Status: {r.status} | {r.read().decode()}")
    except Exception as e:
        print(f"  Health check failed: {e}")
        return

    # 2. Readiness check
    print("\n=== Readiness Check ===")
    try:
        r = urllib.request.urlopen(f"{BASE}/health/ready")
        print(f"  Status: {r.status} | {r.read().decode()}")
    except Exception as e:
        print(f"  Readiness check failed: {e}")

    # 3. Login
    print("\n=== Login ===")
    data = urllib.parse.urlencode({"username": "user@nutriguard.com", "password": "password123"}).encode()
    req = urllib.request.Request(f"{BASE}/api/v1/auth/login", data=data)
    token = None
    try:
        r = urllib.request.urlopen(req)
        login_resp = json.loads(r.read().decode())
        token = login_resp.get("access_token", "")
        print(f"  Login OK! Token: {token[:30]}...")
    except Exception as e:
        print(f"  Login failed: {e}")

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
        except Exception as e:
            print(f"  Profile failed: {e}")

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
        except Exception as e:
            print(f"  Meals failed: {e}")

    print("\n=== All checks complete ===")

if __name__ == "__main__":
    run_smoke_test()
