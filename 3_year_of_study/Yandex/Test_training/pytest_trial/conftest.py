# conftest.py
import pytest

from engine_class import Engine


@pytest.fixture(scope='session')
def engine():
    """Фикстура возвращает экземпляр класса двигателя."""
    return Engine()


@pytest.fixture(autouse=True)
def start_engine(engine):
    """Фикстура запускает двигатель."""
    engine.is_running = True
    yield
    engine.is_running = False
