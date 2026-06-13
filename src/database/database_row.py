"""Base class for all database objects"""

from abc import ABC, abstractmethod
from sqlite3 import Cursor


class DatabaseRow(ABC):
    """Is the absolute bare minimum a database object must be"""
    def __init__(self, cursor: Cursor, obj_id: int | None = None):
        self.obj_id = obj_id
        self.cursor = cursor


    @staticmethod
    def get(cursor: Cursor, obj_id: int | None):
        """
        Grabs the record associated to this item based on fields provided.

        Accepts:
            * obj_id
            * potentially something defined in an override

        Returns:
            One object of the requested class.
        """


    @abstractmethod
    def create(self):
        """
        Creates a new record of this object in the database.

        Accepts:
            * Nuthin
        
        Returns:
            Nuthin
        """


    @abstractmethod
    def update(self):
        """
        Updates this specific object's record in the database

        Accepts:
            * Nothing

        Returns:
            * Nothing
        """


    @abstractmethod
    def delete(self):
        """
        Deletes this specific object's record in the database
        
        Accepts:
            * Nothing

        Returns:
            * Nothing
        """
