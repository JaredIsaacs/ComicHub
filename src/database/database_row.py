from abc import ABC, abstractmethod
from sqlite3 import Cursor


class DatabaseRow(ABC):
    def __init__(self, cursor: Cursor, id: int | None = None):
        self.id = id
        self.cursor = cursor


    @staticmethod
    def get(cursor: Cursor, id: int | None):
        pass


    @abstractmethod
    def create(self):
        pass


    @abstractmethod
    def update(self):
        pass


    @abstractmethod
    def delete(self):
        pass