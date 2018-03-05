import logging
import sys
from typing import Callable, List, Set

import click

from ansiblediscover.entity.entities import Entities
from ansiblediscover.graph.dependencies import Dependencies
from ansiblediscover.graph.node import Node
from ansiblediscover.graph.traversal import Traversal

LOG_LEVEL_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

logger = logging.getLogger('ansiblediscover')


def _configure_logger(do_log: bool, log_level: str):
    logger.setLevel(LOG_LEVEL_MAP.get(log_level.lower(), 'info'))
    logger.handlers = []

    if do_log:
        log_handler = logging.StreamHandler(sys.stderr)
        log_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(name)s] %(message)s'))
        log_handler.setLevel(logging.NOTSET)
        logger.addHandler(log_handler)
    else:
        log_handler = logging.NullHandler()
        logger.addHandler(log_handler)


def _print_successors(entities: List[str], limit: str, for_type: str, succ_fun: Callable[[Node], Set[Node]]):
    if len(entities) == 0:
        logger.info('No entity files given, thus nothing to do. Bye!')
        return

    dependency_map = Dependencies.discover()

    # {'playbook': [...], 'role': [...]}
    types_n_entities = Entities.from_paths(entities)
    # ['playbook:playbook1', ..., 'role:role1', ...]
    entity_identifiers = [Node.build_identifier(entity_name, entity_type)
                          for (entity_type, entity_list) in types_n_entities.items()
                          for entity_name in entity_list]
    filtered_entities = [dependency_map[identifier]
                         for identifier in entity_identifiers if identifier in dependency_map]

    collector_func = getattr(Traversal, limit)
    successors = collector_func(filtered_entities, succ_fun)

    for succ in successors:
        if succ.node_type == for_type:
            print(succ.name)


@click.group()
@click.option('--log/--no-log', default=False)
@click.option('--log-level', type=click.Choice(LOG_LEVEL_MAP.keys()), default='info')
def cli(log: bool, log_level: str):
    _configure_logger(log, log_level)


@cli.group('roles')
def roles():
    pass


@roles.command('successors')
@click.argument('entities', type=click.Path(exists=True), nargs=-1)
@click.option('--limit', '-l', type=click.Choice(['direct', 'leafs', 'all']), default='all')
def roles_successors(entities: List[str], limit: str):
    _print_successors(entities, limit, 'role', (lambda n: n.successors))


@roles.command('predecessors')
@click.argument('entities', type=click.Path(exists=True), nargs=-1)
@click.option('--limit', '-l', type=click.Choice(['direct', 'leafs', 'all']), default='all')
def roles_successors(entities: List[str], limit: str):
    _print_successors(entities, limit, 'role', (lambda n: n.predecessors))


if __name__ == '__main__':
    cli()
