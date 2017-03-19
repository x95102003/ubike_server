#!/usr/bin/env python
# -*- coding: utf-8 -*-

class UbikeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
