from datetime import datetime

import pytest

from primvoices.models import (
    VoiceResponse,
    VoiceCreateParams,
    GenerationResponse,
    GenerationCreateParams,
    PublicVoiceResponse,
    PaginationParams,
    ErrorResponse,
    APIResponse
)

def test_voice_response(sample_voice_data):
    """Test VoiceResponse model."""
    voice = VoiceResponse(**sample_voice_data)
    assert voice.id == "voice123"
    assert voice.user_id == "user123"
    assert voice.name == "Test Voice"
    assert voice.sample_url == "https://example.com/sample.mp3"
    assert voice.preview_url == "https://example.com/preview.mp3"
    assert voice.verified is True
    assert isinstance(voice.created_at, datetime)
    assert isinstance(voice.updated_at, datetime)
    assert voice.deleted_at is None

def test_voice_create_params():
    """Test VoiceCreateParams model."""
    params = VoiceCreateParams(
        name="Test Voice",
        sample_url="https://example.com/sample.mp3",
        verified=True
    )
    assert params.name == "Test Voice"
    assert params.sample_url == "https://example.com/sample.mp3"
    assert params.verified is True

    # Test that verified=False is not allowed
    with pytest.raises(ValueError):
        VoiceCreateParams(
            name="Test Voice",
            sample_url="https://example.com/sample.mp3",
            verified=False
        )

def test_generation_response(sample_generation_data):
    """Test GenerationResponse model."""
    gen = GenerationResponse(**sample_generation_data)
    assert gen.id == "gen123"
    assert gen.user_id == "user123"
    assert gen.voice_id == "voice123"
    assert gen.text == "Test generation"
    assert gen.source_url == "https://example.com/source"
    assert gen.notes == "Test notes"
    assert gen.audio_url == "https://example.com/audio.mp3"
    assert gen.quality == "high"
    assert gen.cost == 1.0
    assert isinstance(gen.created_at, datetime)
    assert isinstance(gen.updated_at, datetime)
    assert gen.deleted_at is None

def test_generation_create_params():
    """Test GenerationCreateParams model."""
    params = GenerationCreateParams(
        voice_id="voice123",
        text="Test generation",
        source_url="https://example.com/source",
        notes="Test notes",
        quality="high"
    )
    assert params.voice_id == "voice123"
    assert params.text == "Test generation"
    assert params.source_url == "https://example.com/source"
    assert params.notes == "Test notes"
    assert params.quality == "high"

    # Test optional fields
    params = GenerationCreateParams(voice_id="voice123", quality="low")
    assert params.voice_id == "voice123"
    assert params.text is None
    assert params.source_url is None
    assert params.notes is None
    assert params.quality == "low"

def test_generation_create_params_quality_validation():
    """Test quality field validation in GenerationCreateParams."""
    with pytest.raises(ValueError):
        GenerationCreateParams(voice_id="voice123", quality="invalid")

def test_public_voice_response(sample_voice_data):
    """Test PublicVoiceResponse model."""
    voice = PublicVoiceResponse(**{k: v for k, v in sample_voice_data.items() if k != "userId"})
    assert voice.id == "voice123"
    assert voice.name == "Test Voice"
    assert voice.sample_url == "https://example.com/sample.mp3"
    assert voice.preview_url == "https://example.com/preview.mp3"
    assert voice.verified is True
    assert isinstance(voice.created_at, datetime)
    assert isinstance(voice.updated_at, datetime)
    assert voice.deleted_at is None

def test_pagination_params():
    """Test PaginationParams model."""
    params = PaginationParams(limit=10, offset=20)
    assert params.limit == 10
    assert params.offset == 20

    # Test optional fields
    params = PaginationParams()
    assert params.limit is None
    assert params.offset is None

def test_error_response():
    """Test ErrorResponse model."""
    error = ErrorResponse("Test error", 400)
    assert error.error == "Test error"
    assert error.status == 400
    assert str(error) == "Test error"

def test_api_response():
    """Test APIResponse model."""
    response = APIResponse[str](data="test")
    assert response.data == "test"
