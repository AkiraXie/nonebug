from typing import Generator

import pytest

from nonebug.helpers import clear_nonebot


@pytest.fixture
def nonebug_clear() -> Generator[None, None, None]:
    """
    Clear nonebot after test case running completed.
    Ensure every test case has a clean nonebot environment.

    By default, this fixture will be auto called by `nonebug_init`.
    """
    yield None
    clear_nonebot()


@pytest.fixture
def nonebug_init(nonebug_clear: None) -> None:
    """
    Initialize nonebot before test case running.
    And clear nonebot after test case running completed.
    """
    # ensure nonebot is clean
    clear_nonebot()

    import nonebot

    nonebot.init()


__all__ = ["nonebug_clear", "nonebug_init"]
