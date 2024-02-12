#!/usr/bin/python3
''' Defines unittests for models/base_model.py. '''

import os
import unittest
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_init(unittest.TestCase):
    '''Unittests for the __init__ method of the BaseModel class.'''

    def test_no_args(self):
        '''Test create an instance with no arguments.'''
        self.assertEqual(type(BaseModel()), BaseModel)

    def test_None_args(self):
        '''Test __init__method with None as an argument.'''
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_id_is_str(self):
        '''Test that ``id`` is a public string attribute.'''
        self.assertEqual(type(BaseModel().id), str)

    def test_unique_ids(self):
        '''Test that two instances of BaseModel have unique ids.'''
        i1 = BaseModel()
        i2 = BaseModel()
        self.assertNotEqual(i1.id, i2.id)

    def test_created_at_is_datetime(self):
        '''Test that ``created_at`` is a publis attribute of type datettime.'''
        self.assertEqual(type(BaseModel().created_at), datetime)

    def test_created_at_right_time(self):
        '''Test that two models created at separate times,
                            have different ``created_at``.'''
        i1 = BaseModel()
        sleep(1)
        i2 = BaseModel()
        self.assertNotEqual(i1.created_at, i2.created_at)
        self.assertLess(i1.created_at, i2.created_at)

    def test_updated_at_is_datetime(self):
        '''Test that ``updated_at`` is a publis attribute of type datettime.'''
        self.assertEqual(type(BaseModel().updated_at), datetime)

    def test_updated_at_right_time(self):
        '''Test that two models created at separate times,
                            have different ``updated_at``.'''
        i1 = BaseModel()
        sleep(1)
        i2 = BaseModel()
        self.assertNotEqual(i1.updated_at, i2.updated_at)
        self.assertLess(i1.updated_at, i2.updated_at)

    def test_init_with_kwargs(self):
        '''Create an instance of BaseModel with **kwargs.'''
        dt = datetime.now()
        dt_isoformat = dt.isoformat()
        bm = BaseModel(id='123', created_at=dt_isoformat,
                       updated_at=dt_isoformat)
        self.assertEqual(bm.id, '123')
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_datetime_attributes(self):
        '''Test that the created_at and updated_at are datetime attributes
                        when init with **kwargs.'''
        dt = datetime.now()
        dt_isoformat = dt.isoformat()
        bm = BaseModel(id='123', created_at=dt_isoformat,
                       updated_at=dt_isoformat)
        self.assertEqual(type(bm.created_at), datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_init_excludes_class_attributes(self):
        '''Tests that '__class__' key from kwargs
            is not added as an attribute.'''
        dt = datetime.now()
        dt_isoformat = dt.isoformat()
        bm = BaseModel(id='123', created_at=dt_isoformat,
                       updated_at=dt_isoformat, __class__='BaseModel')
        self.assertNotEqual(bm.__class__, 'BaseModel')

    def test_init_with_None_kwargs(self):
        '''Test __init__ methods with kwargs whose values are None.'''
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_args_and_kwargs(self):
        '''Create an instance of BaseModel with args and kwargs arguments.'''
        dt = datetime.now()
        dt_isoformat = dt.isoformat()
        bm = BaseModel('1234', id='123', created_at=dt_isoformat,
                       updated_at=dt_isoformat)
        self.assertEqual(bm.id, '123')
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)
        self.assertNotIn('1234', bm.__dict__.values())


class TestBaseModel_str(unittest.TestCase):
    '''Unittests for the __str__ method of the BaseModel class.'''

    def test_str_method(self):
        '''Test the __str__ public string method.'''
        dt = datetime.now()
        bm = BaseModel()
        bm.id = '1234567890'
        bm.created_at = dt
        bm.updated_at = dt
        expected_str = '[BaseModel] (1234567890) ' + str(bm.__dict__)
        output_str = bm.__str__()
        self.assertEqual(expected_str, output_str)


class TestBaseModel_save(unittest.TestCase):
    '''Unittests for the __save__ method of the BaseModel class.'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        '''Test if save updates the updated_at time'''
        bm = BaseModel()
        initial_updated_at = bm.updated_at
        sleep(1)
        bm.save()
        self.assertNotEqual(initial_updated_at, bm.updated_at)
        self.assertLess(initial_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        '''Test calling the save method with an argument.'''
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save('an_argument')

    def test_save_with_None_arg(self):
        '''Test calling the save method with None argument.'''
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(self):
        '''Test that the save method updates the JSON file with object.'''
        bm = BaseModel()
        bm.save()
        id = 'BaseModel.' + bm.id
        with open('file.json', 'r', encoding='utf-8') as f:
            self.assertIn(id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    '''Unittests for the __to_dict__ method of the BaseModel class.'''

    def test_to_dict(self):
        '''Tests if to_dict returns a dictionary'''
        bm = BaseModel()
        self.assertEqual(type(bm.to_dict()), dict)

    def test_to_dict_contains_all_keys(self):
        '''Test to_dict returns a dictionary with all the expected keys.'''
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm_dict)
        self.assertIn("updated_at", bm_dict)
        self.assertIn("__class__", bm_dict)
        self.assertEqual(bm_dict['__class__'], 'BaseModel')

    def test_to_dict_includes_extra_attributes(self):
        '''Test that the to_dict method includes any added attributes.'''
        bm = BaseModel()
        bm.name = 'Aishah'
        bm.age = 17
        bm_dict = bm.to_dict()
        self.assertIn('name', bm_dict)
        self.assertEqual(bm_dict['name'], 'Aishah')
        self.assertIn('age', bm_dict)
        self.assertEqual(bm_dict['age'], 17)

    def test_to_dict_correct_output(self):
        '''Test that to_dict method returns the correct dictionary.'''
        dt = datetime.now()
        bm = BaseModel()
        bm.id = '1234567890'
        bm.created_at = bm.updated_at = dt
        expected_dict = {
                'id': '1234567890',
                'created_at': dt.isoformat(),
                'updated_at': dt.isoformat(),
                '__class__': 'BaseModel'
        }
        self.assertDictEqual(bm.to_dict(), expected_dict)

    def test_datetime_attribute_value_type(self):
        '''Tests if created_at and updated_at values  are strings.'''
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(type(bm_dict['created_at']), str)
        self.assertEqual(type(bm_dict['updated_at']), str)

    def test_to_dict_updates(self):
        '''Tests that to_dict reflects updated value'''
        bm = BaseModel()
        bm.id = '1234567890'
        initial_dict = bm.to_dict()
        bm.id = '0987654321'
        updated_dict = bm.to_dict()
        self.assertNotEqual(initial_dict['id'], updated_dict['id'])
        self.assertEqual(updated_dict['id'], "0987654321")

    def test_to_dict_ISO(self):
        '''Tests that created_at and updated_at are in ISO format'''
        dt = datetime.now()
        bm = BaseModel()
        bm.id = '1234567890'
        bm.created_at = dt
        bm.updated_at = dt
        bm_dict = bm.to_dict()
        iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.assertTrue(datetime.strptime(bm_dict['created_at'], iso_format))
        self.assertTrue(datetime.strptime(bm_dict['updated_at'], iso_format))

    def test_only_instance_attributes(self):
        '''Tests that to_dict returns only instance attributes set'''
        dt = datetime.now()
        bm = BaseModel()
        bm.id = '1234567890'
        bm.created_at = dt
        bm_dict = bm.to_dict()
        self.assertEqual(bm_dict['id'], '1234567890')
        self.assertEqual(bm_dict['created_at'], dt.isoformat())
        self.assertNotIn('mass', bm_dict)

    def test_to_dict_not__dict__(self):
        '''Test that to_dict method is not the same as the special __dict__.'''
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        '''Test the to_dict method with an argument.'''
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict('an_argument')

    def test_to_dict_with_None_arg(self):
        ''''Test the to_dict method with None argument.'''
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
