from app import app
import pytest
from fastapi.testclient import TestClient
from time import sleep

client = TestClient(app)


def test_audit_1():
    """Calling /audit should return 10 most recent requests"""

    urls = [f"/jumble/{w}" for w in "lorem ipsum dolor sit amet".split(" ")]

    # Make 5 calls to the jumble API
    [client.get(u) for u in urls]

    # Make 5 more calls to the Audit API
    [client.get("/audit?n=1") for _ in range(5)]

    response = client.get("/audit")
    assert response.ok
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    # Assert that a default Audit call returns last 10 requests
    assert len(data) == 10
    # Assert that the most-recent 5 calls are to Audit
    assert set([d["path"] for d in data[:5]]) == {"/audit"}
    # Assert that the next most-recent calls are to Jumble
    assert set([d["path"] for d in data[5:]]) == set(urls)


def test_audit_2():
    """Calling /audit?n=XXX will return XXX most recent requests"""

    # Make n calls to the jumble API
    urls = [f"/jumble/{w}" for w in "lorem ipsum dolor sit amet".split(" ")]
    for url in urls:
        client.get(url)
        sleep(0.5)

    # Get audit log of the last n calls
    response = client.get(f"/audit?n={len(urls)}")
    assert response.ok
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    assert len(data) == len(urls)

    # Assert that the audit logs came out in order
    for d, url in zip(data, reversed(urls)):
        assert d["path"] == url


def test_audit_3():
    """
    Calling /audit?n=XXX with absurdly huge XXX will return *at most* XXX
    requests and won't blow up the application.
    """

    n = 1_000_000_000
    response = client.get(f"/audit?n={n}")
    assert response.ok
    assert len(response.json()) <= n