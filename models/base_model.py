#!/usr/bin/env python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class Basemodel:
    """A base class for all hbnb models"""

    def __init__(self):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Returns an updated time  with the current datetime"""
        self.updated_at = datetime.now()
        return self.updated_at

    def to_json(self):
        """Returns a dictionary containing all keys/values of  the instance"""
        new_dict = {}
        for key, value in self.__dict__items():
            if isinstance(value, datetime):
                new_dict[key] = value.isoformat()
            else:
                new_dict[key] = value
        new_dict["__class__"] = self.__class.__name
        return new_dict
