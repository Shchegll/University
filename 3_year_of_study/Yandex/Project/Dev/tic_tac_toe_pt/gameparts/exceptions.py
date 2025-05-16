class FieldIndexError(IndexError):

    def __str__(self):
        return 'Введено значение за границами игрового поля'


class CellOccupiedError(Exception):

    def __str__(self):
        return 'Попытка изменить занятую ячейку'
