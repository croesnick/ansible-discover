import os
import shutil

import pytest
from click.testing import CliRunner

from ansiblediscover.cli import cli


@pytest.mark.parametrize('pb_or_role, succ_or_pred, files, expected_output', [
    ('roles', 'successors', ['p0.yml'], ['r0', 'r1', 'r2', 'r3', 'r6']),
    ('roles', 'successors', ['p1.yml'], ['r0', 'r1', 'r2', 'r6']),  # GH-9 Missing roles from task includes: r4, r5
    ('roles', 'successors', ['p2.yml'], ['r0', 'r1', 'r2', 'r6']),
    ('roles', 'successors', ['roles/r0'], ['r1', 'r2', 'r6']),
    ('roles', 'successors', ['roles/r1'], []),
    ('roles', 'successors', ['roles/r2'], ['r6']),
    ('roles', 'predecessors', ['p0.yml'], []),
    ('roles', 'predecessors', ['p1.yml'], []),
    ('roles', 'predecessors', ['p2.yml'], []),
    ('roles', 'predecessors', ['roles/r0'], []),
    ('roles', 'predecessors', ['roles/r1'], ['r0']),
    ('roles', 'predecessors', ['roles/r6'], ['r0', 'r2']),
    ('playbooks', 'successors', ['p0.yml'], ['p2']),
    ('playbooks', 'successors', ['p1.yml'], ['p2']),
    ('playbooks', 'successors', ['p2.yml'], []),
    ('playbooks', 'successors', ['roles/r0'], []),
    ('playbooks', 'predecessors', ['p0.yml'], []),
    ('playbooks', 'predecessors', ['p1.yml'], []),
    ('playbooks', 'predecessors', ['p2.yml'], ['p0', 'p1']),
    ('playbooks', 'predecessors', ['roles/r0'], ['p0', 'p1', 'p2']),
    ('playbooks', 'predecessors', ['roles/r1'], ['p0', 'p1', 'p2']),
    ('playbooks', 'predecessors', ['roles/r2'], ['p0', 'p1', 'p2']),
    ('playbooks', 'predecessors', ['roles/r3'], ['p0']),
    ('playbooks', 'predecessors', ['roles/r4'], []),  # GH-9 Missing playbooks due to unhandled task includes: p1
    ('playbooks', 'predecessors', ['roles/r5'], []),  # GH-9 Missing playbooks due to unhandled task includes: p1
    ('playbooks', 'predecessors', ['roles/r6'], ['p0', 'p1', 'p2']),
])
def test_cli_role_successors(pb_or_role, succ_or_pred, files, expected_output):
    current_dir = os.path.dirname(__file__)
    fixtures_path = os.path.abspath(os.path.join(current_dir, 'fixtures'))

    runner = CliRunner()

    with runner.isolated_filesystem():
        test_path = os.path.join(os.curdir, 'fixtures')
        shutil.copytree(fixtures_path, test_path)
        os.chdir(test_path)

        result = runner.invoke(cli, args=[pb_or_role, succ_or_pred, *files], catch_exceptions=False)

    assert 0 == result.exit_code

    output = sorted(line for line in result.output.split('\n') if len(line) > 0)
    assert expected_output == output
