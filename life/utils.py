"""
This module provides general purpose utility functions.

The functions provided by utils are broadly useful throughout this project
repository and beyond.

Functions:
silent_import(entity_1[, entity_2[...]][,
              noexcept=(True|False)][, warn=(True|False])
        -- import modules/packages without printing welcome or copyright text.
"""

import os
import sys


def silent_import(*entities, noexcept=False, warn=True):
    """
    Import modules/packages without printing welcome or copyright text.
    
    Use this function to import annoying packages like PyGame that print a
    welcome text to the console when imported. This saves having to modify
    environment variables arbitrarily. In order to add the modules to globals()
    as with a regular import directive, you should write something like:
    
        globals().update(utils.silent_import(package))
    
    Additionally, this function will import as many modules and packages as
    you pass to it.
    
    Parameters:
    *entities   -- strs:    the package and module names to import,
                            1 or more Required.
    noexcept    -- bool:    do not raise exceptions on failed import,
                            Default = False.
    warn        -- bool:    if noexcept, warn (on stderr) for each failed
                            import, Default = True.
    
    Returns: dict   -- entity name value pairs for each successfully imported
                       module/package, suitable to be added to globals().
    """
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        
        imported = {}
        
        for entity in entities:
            try:
                imported[entity] = __import__(entity)
            except Exception:
                if not noexcept:
                    raise
                elif warn:
                    sys.stderr.write(f"Warning: Failed to import {entity}")
        
        sys.stdout = sys.__stdout__
        
        return imported


def get_index(collection, index):
    """
    To-Do: Write docstring...
    """
    try:
        return collection[index]
    except (KeyError, IndexError):
        return None
