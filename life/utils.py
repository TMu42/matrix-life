import os
import sys


def silent_import(entity, noexcept=False):
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        
        try:
            entity = __import__(entity)
        except Exception:
            if not noexcept:
                raise
        
        sys.stdout = sys.__stdout__
        
        return entity
