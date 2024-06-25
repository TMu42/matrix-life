import os
import sys


def silent_import(*entities, noexcept=False, warn=True):
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
