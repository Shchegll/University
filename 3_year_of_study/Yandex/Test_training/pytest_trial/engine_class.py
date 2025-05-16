# engine_class.py
class Engine:
    """Класс двигателя."""

    def __init__(self):
        # При создании объекта двигателя он не запущен.
        self.is_running = False
