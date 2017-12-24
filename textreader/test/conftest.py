import os
import pytest


@pytest.fixture
def ulysses():
    print(os.curdir)
    f = open("test/testtext", encoding='utf-8-sig')
    text = f.read()
    f.close()
    return text