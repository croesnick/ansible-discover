import logging
import os
from typing import Optional, Union

from ruamel import yaml

logger = logging.getLogger(__name__)


class FS:
    @staticmethod
    def load_yaml(path: str) -> Optional[Union[list, dict]]:
        if not os.path.exists(path):
            raise OSError('File does not exist: {}'.format(path))

        with open(path) as fh:
            raw_content = fh.read()
            try:
                return yaml.safe_load(raw_content)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                raise TypeError('Invalid yaml file: {}. Details: {}'.format(path, str(e)))
