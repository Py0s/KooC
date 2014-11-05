#!/usr/bin/env python3

class KoocException(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)