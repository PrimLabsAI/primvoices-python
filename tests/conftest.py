import pytest
import requests
from unittest.mock import Mock
from datetime import datetime, timezone

@pytest.fixture
def mock_session():
    """Create a mock requests session."""
    session = Mock(spec=requests.Session)
    return session

@pytest.fixture
def base_url():
    """Return a test base URL."""
    return "https://api.test.primvoices.com"

@pytest.fixture
def mock_datetime():
    """Return a mock datetime."""
    return datetime(2023, 12, 18, 22, 30, 0, tzinfo=timezone.utc)

@pytest.fixture
def mock_datetime_str(mock_datetime):
    """Return a mock datetime string."""
    return mock_datetime.isoformat()

@pytest.fixture
def sample_voice_data(mock_datetime_str):
    """Return sample voice data."""
    return {
        "id": "voice123",
        "userId": "user123",
        "name": "Test Voice",
        "sampleUrl": "https://example.com/sample.mp3",
        "previewUrl": "https://example.com/preview.mp3",
        "verified": True,
        "createdAt": mock_datetime_str,
        "updatedAt": mock_datetime_str,
        "deletedAt": None
    }

@pytest.fixture
def sample_generation_data(mock_datetime_str):
    """Return sample generation data."""
    return {
        "id": "gen123",
        "userId": "user123",
        "voiceId": "voice123",
        "text": "Test generation",
        "sourceUrl": "https://example.com/source",
        "notes": "Test notes",
        "audioUrl": "https://example.com/audio.mp3",
        "quality": "high",
        "cost": 1.0,
        "createdAt": mock_datetime_str,
        "updatedAt": mock_datetime_str,
        "deletedAt": None
    }
