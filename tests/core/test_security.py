"""Tests for src.core.security module."""

from datetime import UTC, datetime, timedelta

import jwt
import pytest

from src.core.config import settings
from src.core.security import (
    InvalidTokenTypeError,
    check_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    decode_token,
    hash_password,
)


class TestPasswordHashing:
    """Tests for hash_password and verify_password."""

    @pytest.mark.parametrize("password", ["secret123", "a", "x" * 72, "特殊字符密码"])
    def test_hash_and_verify_roundtrip(self, password: str) -> None:
        hashed = hash_password(password)
        assert check_password(password, hashed) is True

    def test_hash_produces_bcrypt_hash(self) -> None:
        hashed = hash_password("test")
        assert hashed.startswith("$2")

    def test_hash_is_different_each_time(self) -> None:
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2

    def test_verify_wrong_password_fails(self) -> None:
        hashed = hash_password("correct")
        assert check_password("wrong", hashed) is False

    def test_verify_empty_string(self) -> None:
        hashed = hash_password("")
        assert check_password("", hashed) is True


class TestAccessTokenCreation:
    """Tests for create_access_token."""

    def test_creates_valid_token_string(self) -> None:
        token = create_access_token("user-123")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contains_correct_subject(self) -> None:
        token = create_access_token("user-42")
        payload = decode_access_token(token)
        assert payload["sub"] == "user-42"

    def test_token_type_is_access(self) -> None:
        token = create_access_token("sub")
        payload = decode_access_token(token)
        assert payload["type"] == "access"

    def test_token_issuer_is_clinicore(self) -> None:
        token = create_access_token("sub")
        payload = decode_access_token(token)
        assert payload["iss"] == "clinicore-api"

    def test_token_with_int_subject(self) -> None:
        token = create_access_token(100)
        payload = decode_access_token(token)
        assert payload["sub"] == "100"

    def test_token_with_extra_data(self) -> None:
        token = create_access_token("sub", extra_data={"role": "admin"})
        payload = decode_access_token(token)
        assert payload["role"] == "admin"

    def test_token_without_extra_data(self) -> None:
        token = create_access_token("sub")
        payload = decode_access_token(token)
        assert "role" not in payload

    def test_token_expiration_in_future(self) -> None:
        token = create_access_token("sub")
        payload = decode_access_token(token)
        exp = payload["exp"]
        assert isinstance(exp, (int, float))
        assert exp > datetime.now(UTC).timestamp()

    def test_token_iat_is_recent(self) -> None:
        token = create_access_token("sub")
        payload = decode_access_token(token)
        iat = payload["iat"]
        assert isinstance(iat, (int, float))
        assert iat <= datetime.now(UTC).timestamp()


class TestRefreshTokenCreation:
    """Tests for create_refresh_token."""

    def test_creates_valid_token_string(self) -> None:
        token = create_refresh_token("user-123")
        assert isinstance(token, str)

    def test_token_contains_correct_subject(self) -> None:
        token = create_refresh_token("user-42")
        payload = decode_refresh_token(token)
        assert payload["sub"] == "user-42"

    def test_token_type_is_refresh(self) -> None:
        token = create_refresh_token("sub")
        payload = decode_refresh_token(token)
        assert payload["type"] == "refresh"

    def test_token_with_int_subject(self) -> None:
        token = create_refresh_token(99)
        payload = decode_refresh_token(token)
        assert payload["sub"] == "99"

    def test_refresh_token_cannot_be_decoded_as_access(self) -> None:
        token = create_refresh_token("sub")
        with pytest.raises(InvalidTokenTypeError):
            _ = decode_access_token(token)


class TestTokenDecoding:
    """Tests for _decode_token, decode_access_token, decode_refresh_token."""

    def test_decode_access_token_returns_dict(self) -> None:
        token = create_access_token("sub")
        result = decode_access_token(token)
        assert isinstance(result, dict)

    def test_decode_refresh_token_returns_dict(self) -> None:
        token = create_refresh_token("sub")
        result = decode_refresh_token(token)
        assert isinstance(result, dict)

    def test_decode_with_wrong_type_raises_error(self) -> None:
        token = create_access_token("sub")
        with pytest.raises(InvalidTokenTypeError):
            _ = decode_token(token, "refresh")

    def test_decode_tampered_token_raises_error(self) -> None:
        token = create_access_token("sub")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(
            (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError)
        ):
            _ = decode_access_token(tampered)

    def test_decode_expired_token(self) -> None:
        now = datetime.now(UTC)
        payload: dict[str, object] = {
            "sub": "sub",
            "type": "access",
            "iss": "clinicore-api",
            "iat": now,
            "exp": now - timedelta(hours=1),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret_key.get_secret_value(),
            algorithm=settings.jwt_algorithm,
        )
        with pytest.raises(jwt.exceptions.ExpiredSignatureError):
            _ = decode_access_token(token)

    def test_decode_with_wrong_secret(self) -> None:
        token = jwt.encode(
            {
                "sub": "sub",
                "type": "access",
                "iss": "clinicore-api",
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(hours=1),
            },
            "a-wrong-secret-key-that-is-longer-than-thirty-two-bytes",
            algorithm="HS256",
        )
        with pytest.raises(jwt.exceptions.InvalidSignatureError):
            _ = decode_access_token(token)


class TestInvalidTokenTypeError:
    """Tests for InvalidTokenTypeError exception."""

    def test_is_exception(self) -> None:
        assert issubclass(InvalidTokenTypeError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(InvalidTokenTypeError):
            raise InvalidTokenTypeError("access")
