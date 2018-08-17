import logging
import os
from typing import Optional, Union

from ruamel import yaml


# Handle tags like !vault: https://stackoverflow.com/a/13281292
def default_ctor(_loader, tag_suffix, node):
    return tag_suffix + ' ' + node.value


yaml.add_multi_constructor('', default_ctor)

logger = logging.getLogger(__name__)


class FS:
    @staticmethod
    def load_yaml(path: str) -> Optional[Union[list, dict]]:
        if not os.path.exists(path):
            raise OSError('File does not exist: {}'.format(path))

        with open(path) as fh:
            raw_content = fh.read()
            try:
                return yaml.load(raw_content, Loader=yaml.Loader)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                raise TypeError('Invalid yaml file: {}. Details: {}'.format(path, str(e)))
