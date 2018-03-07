import logging
import os
import yaml
from typing import Optional, Union

logger = logging.getLogger(__name__)


class FS:
    @staticmethod
    def load_yaml(path: str) -> Optional[Union[list, dict]]:
        if not os.path.exists(path):
            raise FileNotFoundError('Attempted to read non-existing file: {}'.format(path))

        with open(path) as fh:
            raw_content = fh.read()
            try:
                return yaml.load(raw_content)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                raise TypeError('Failed to parse yaml file: {}. Details: {}'.format(path, str(e)))
