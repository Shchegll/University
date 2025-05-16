import pytest

from engine_class import Engine


def test_engine_is_running(engine):
    """Тест проверяет, работает ли двигатель."""
    assert engine.is_running


def test_check_engine_class(engine):
    """Тест проверяет класс объекта."""
    assert isinstance(engine, Engine)
