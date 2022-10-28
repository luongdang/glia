from collections import Counter
from urllib.parse import quote

import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_jumble_1():
    """Calling jumble on "aaa" always return "aaa"."""

    response = client.get("/jumble/aaa")
    assert response.ok
    assert response.text == "aaa"


@pytest.mark.parametrize("word", ["hello world", "aaa", "lorem ipsum"])
def test_jumble_2(word: str):
    """
    The original and jumbled text should have the same number of characters
    appearing the same number of times. Space and punctuations are counted as
    characters.
    """
    response = client.get(f"/jumble/{quote(word)}")
    assert response.ok

    expected_counter = Counter(word)
    actual_counter = Counter(response.text)
    assert actual_counter == expected_counter
