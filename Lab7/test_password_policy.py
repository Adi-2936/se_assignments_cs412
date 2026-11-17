from hypothesis import given, settings, strategies as st
from password_policy import first_character_type, split_credentials, digit_ratio

FUZZ_INPUTS = st.text() | st.none()


@given(FUZZ_INPUTS)
@settings(max_examples=100, deadline=None)
def test_first_character_type_no_crash(s):
    result = first_character_type(s)
    assert result in {"digit", "letter", "symbol", "invalid"}
    if not isinstance(s, str) or not s:
        assert result == "invalid"


@given(FUZZ_INPUTS)
@settings(max_examples=100, deadline=None)
def test_split_credentials_no_crash(s):
    result = split_credentials(s)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(part, str) for part in result)
    if not isinstance(s, str) or ":" not in s:
        assert result == ("", "")


@given(FUZZ_INPUTS)
@settings(max_examples=100, deadline=None)
def test_digit_ratio_no_crash(s):
    result = digit_ratio(s)
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0
    if not isinstance(s, str) or not s:
        assert result == 0.0


def test_valid_first_character_type():
    assert first_character_type("7abc") == "digit"
    assert first_character_type("Alpha1!") == "letter"
    assert first_character_type("!Alpha1") == "symbol"


def test_valid_split_credentials():
    assert split_credentials(" alice : Secret1! ") == ("alice", "Secret1!")


def test_valid_digit_ratio():
    assert digit_ratio("Abc123!") == 3 / 7
