#!/usr/bin/env python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from . import storage



class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.now().isoformat()
            else:
                self.created_at = datetime.now().isoformat()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.now().isoformat()
            else:
                self.updated_at = datetime.now().isoformat()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            self.new = storage.new()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Returns an updated time  with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()
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
