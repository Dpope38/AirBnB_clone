#!/usr/bin/env python3
"""initialize the models package"""
from engine import file_storage

storage = file_storage.FileStorage()
storage.reload()
