import logging
import os
from ruamel import yaml
from typing import Optional, Union

logger = logging.getLogger(__name__)


class FS:
    @staticmethod
    def load_yaml(path: str) -> Optional[Union[list, dict]]:
        if not os.path.exists(path):
            raise OSError('File does not exist: {}'.format(path))

        with open(path) as fh:
            try:
                raw_content = fh.read()
            except PermissionError:
                raise OSError('File not accessible/readable: {}'.format(path))
            else:
                try:
                    return yaml.safe_load(raw_content)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                    raise TypeError('Invalid yaml file: {}. Details: {}'.format(path, str(e)))
