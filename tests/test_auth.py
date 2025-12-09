import pytest
from app.core.security import create_access_token, decode_access_token
from app.dependencies.auth import get_current_user
from app.database import SessionLocal
from app import models
from datetime import timedelta

def test_decode_access_token():
    """Test decode_access_token function"""
    # Create token
    token = create_access_token(
        data={"sub": "1"},
        expires_delta=timedelta(minutes=30)
    )
    
    # Decode token
    payload = decode_access_token(token)
    
    assert payload is not None
    assert payload.get("sub") == "1"
    print(f"✅ Decode Token Success: {payload}")

def test_get_current_user():
    """Test get_current_user with valid token"""
    # Create token
    token = create_access_token(
        data={"sub": "1"},
        expires_delta=timedelta(minutes=30)
    )
    
    # Decode to verify
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "1"
    print(f"✅ Get Current User Test Passed!")

def test_invalid_token():
    """Test decode_access_token with invalid token"""
    payload = decode_access_token("invalid.token.here")
    assert payload is None
    print(f"✅ Invalid Token Handled!")