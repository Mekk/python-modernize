# -*- coding: utf-8 -*-

"""
Tests for config file parsing and interpretation, plus proper default handling.
"""

from mekk.calibre.config import Config

def test_existing():

    try:
        cfg = Config(tf.name)
    finally:
        print tf.name
        #os.remove(tf.name)
