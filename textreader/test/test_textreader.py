"""
Tests for `textreader` module.
"""
import pytest
from textreader import textreader


def test_lambda_simple_call():
    # GIVEN
    # WHEN
    result = textreader.lambda_handler({},{})


    # THEN
    assert "text" in result
    assert "T" in result["text"]

