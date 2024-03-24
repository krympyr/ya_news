import pytest
from engine_class import Engine

@pytest.fixture(scope='session')
def engine():
    """Фикстура возвращает экземпляр класса двигателя."""
    return Engine()


@pytest.fixture(autouse=True)
def start_engine(engine):
    """Фикстура запускает двигатель."""
    engine.is_running = True  # Запустим двигатель.
    yield  # В этот момент начинает выполняться тест.
    engine.is_running = False  # Заглушим двигатель.
