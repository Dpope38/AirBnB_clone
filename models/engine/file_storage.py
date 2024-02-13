"""This module defines a class to manage file storage for hbnb clone"""
import json

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    
    @classmethod
    def all(cls):
        """Returns the dictionary __ objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_obj = {}
        for key, val in self.__objects.items():
            json_obj[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(json_obj, file)
    
    def reload(self):
         """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                jfile = json.load(file)
            for key, value in jfile.items():
                self.__objects[key] = value
        except:
            pass
        
