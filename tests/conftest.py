import time
from collections.abc import Generator

import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def wait_for_api():
    """Attend que l'API réponde 200 sur /health avant de lancer les tests."""
    url = f"{BASE_URL}/health"
    timeout = 30
    start = time.time()

    print("\n[Test] Waiting for API...")
    while time.time() - start < timeout:
        try:
            res = httpx.get(url, timeout=1.0)
            if res.status_code == 200:
                print("API Ready")
                return
        except httpx.RequestError:
            time.sleep(1)

    pytest.fail("API unreachable. Docker is likely down.")


@pytest.fixture(scope="session")
def api_client(wait_for_api) -> Generator[httpx.Client, None, None]:
    """Client HTTP pré-configuré pour les tests d'intégration."""
    with httpx.Client(base_url=f"{BASE_URL}/api/v1", timeout=10.0) as client:
        yield client
