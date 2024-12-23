import pytest
from primvoices.voices import VoicesAPI
from primvoices.models import (
    VoiceResponse,
    VoiceCreateParams,
    PublicVoiceResponse,
    PaginationParams,
    ErrorResponse
)

def test_list_voices(mock_session, base_url, sample_voice_data):
    """Test listing voices."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": [sample_voice_data]}

    response = api.list()
    mock_session.get.assert_called_once_with(f"{base_url}/v1/voices", params=None)
    assert len(response.data) == 1
    assert isinstance(response.data[0], VoiceResponse)
    assert response.data[0].id == "voice123"

def test_list_voices_with_pagination(mock_session, base_url, sample_voice_data):
    """Test listing voices with pagination."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": [sample_voice_data]}

    params = PaginationParams(limit=10, offset=0)
    response = api.list(params)
    mock_session.get.assert_called_once_with(f"{base_url}/v1/voices", params={"limit": 10, "offset": 0})
    assert len(response.data) == 1

def test_retrieve_voice(mock_session, base_url, sample_voice_data):
    """Test retrieving a voice."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": sample_voice_data}

    response = api.retrieve("voice123")
    mock_session.get.assert_called_once_with(f"{base_url}/v1/voices/voice123")
    assert isinstance(response.data, VoiceResponse)
    assert response.data.id == "voice123"

def test_create_voice(mock_session, base_url, sample_voice_data):
    """Test creating a voice."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.post.return_value.ok = True
    mock_session.post.return_value.json.return_value = {"data": sample_voice_data}

    params = VoiceCreateParams(
        name="Test Voice",
        sample_url="https://example.com/sample.mp3",
        verified=True
    )
    response = api.create(params)
    mock_session.post.assert_called_once_with(
        f"{base_url}/v1/voices",
        json=params.model_dump(by_alias=True)
    )
    assert response.data.id == "voice123"

def test_delete_voice(mock_session, base_url):
    """Test deleting a voice."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.delete.return_value.ok = True
    mock_session.delete.return_value.json.return_value = {"data": None}

    response = api.delete("voice123")
    mock_session.delete.assert_called_once_with(f"{base_url}/v1/voices/voice123")
    assert response.data is None

def test_list_public_voices(mock_session, base_url, sample_voice_data):
    """Test listing public voices."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": [sample_voice_data]}

    response = api.list_public()
    mock_session.get.assert_called_once_with(f"{base_url}/v1/publicVoices", params=None)
    assert len(response.data) == 1
    assert isinstance(response.data[0], PublicVoiceResponse)
    assert response.data[0].id == "voice123"

def test_retrieve_public_voice(mock_session, base_url, sample_voice_data):
    """Test retrieving a public voice."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": sample_voice_data}

    response = api.retrieve_public("voice123")
    mock_session.get.assert_called_once_with(f"{base_url}/v1/publicVoices/voice123")
    assert isinstance(response.data, PublicVoiceResponse)
    assert response.data.id == "voice123"

def test_error_handling(mock_session, base_url):
    """Test error handling."""
    api = VoicesAPI(mock_session, base_url)
    mock_session.get.return_value.ok = False
    error_response = {
        "error": "Not found",
        "status": 404
    }
    mock_session.get.return_value.json.return_value = error_response

    with pytest.raises(ErrorResponse) as exc_info:
        api.retrieve("voice123")
    
    assert exc_info.value.error == error_response["error"]
    assert exc_info.value.status == error_response["status"]
