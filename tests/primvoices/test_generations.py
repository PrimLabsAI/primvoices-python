import pytest
from primvoices.generations import GenerationsAPI
from primvoices.models import (
    GenerationResponse,
    GenerationCreateParams,
    PaginationParams,
    ErrorResponse
)

def test_list_generations(mock_session, base_url, sample_generation_data):
    """Test listing generations."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": [sample_generation_data]}

    response = api.list()
    mock_session.get.assert_called_once_with(f"{base_url}/v1/generations", params=None)
    assert len(response.data) == 1
    assert isinstance(response.data[0], GenerationResponse)
    assert response.data[0].id == "gen123"

def test_list_generations_with_pagination(mock_session, base_url, sample_generation_data):
    """Test listing generations with pagination."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": [sample_generation_data]}

    params = PaginationParams(limit=10, offset=0)
    response = api.list(params)
    mock_session.get.assert_called_once_with(f"{base_url}/v1/generations", params={"limit": 10, "offset": 0})
    assert len(response.data) == 1

def test_retrieve_generation(mock_session, base_url, sample_generation_data):
    """Test retrieving a generation."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {"data": sample_generation_data}

    response = api.retrieve("gen123")
    mock_session.get.assert_called_once_with(f"{base_url}/v1/generations/gen123")
    assert isinstance(response.data, GenerationResponse)
    assert response.data.id == "gen123"

def test_create_generation(mock_session, base_url, sample_generation_data):
    """Test creating a generation."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.post.return_value.ok = True
    mock_session.post.return_value.json.return_value = {"data": sample_generation_data}

    params = GenerationCreateParams(
        voice_id="voice123",
        text="Test generation",
        source_url="https://example.com/source",
        notes="Test notes",
        quality="high"
    )
    response = api.create(params)
    mock_session.post.assert_called_once_with(
        f"{base_url}/v1/generations",
        json=params.model_dump(by_alias=True)
    )
    assert isinstance(response.data, GenerationResponse)
    assert response.data.id == "gen123"

def test_create_generation_minimal(mock_session, base_url, sample_generation_data):
    """Test creating a generation with minimal parameters."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.post.return_value.ok = True
    mock_session.post.return_value.json.return_value = {"data": sample_generation_data}

    params = GenerationCreateParams(voice_id="voice123", text="Test generation", quality="low")
    response = api.create(params)
    mock_session.post.assert_called_once_with(
        f"{base_url}/v1/generations",
        json=params.model_dump(by_alias=True)
    )
    assert isinstance(response.data, GenerationResponse)
    assert response.data.id == "gen123"

def test_delete_generation(mock_session, base_url):
    """Test deleting a generation."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.delete.return_value.ok = True
    mock_session.delete.return_value.json.return_value = {"data": None}

    response = api.delete("gen123")
    mock_session.delete.assert_called_once_with(f"{base_url}/v1/generations/gen123")
    assert response.data is None

def test_error_handling(mock_session, base_url):
    """Test error handling."""
    api = GenerationsAPI(mock_session, base_url)
    mock_session.get.return_value.ok = False
    error_response = {
        "error": "Not found",
        "status": 404,
    }
    mock_session.get.return_value.json.return_value = error_response

    with pytest.raises(ErrorResponse) as exc_info:
        api.retrieve("gen123")
    
    assert exc_info.value.error == error_response["error"]
    assert exc_info.value.status == error_response["status"]

def test_create_generation_invalid_quality():
    """Test creating a generation with invalid quality."""
    with pytest.raises(ValueError):
        GenerationCreateParams(voice_id="voice123", quality="invalid")
