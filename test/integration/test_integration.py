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
])
def test_cli_role_successors(pb_or_role, succ_or_pred, files, expected_output):
    fixtures_path = os.path.abspath(os.path.join(os.curdir, 'integration', 'fixtures'))

    runner = CliRunner()

    with runner.isolated_filesystem():
        test_path = os.path.join(os.curdir, 'fixtures')
        shutil.copytree(fixtures_path, test_path)
        os.chdir(test_path)

        result = runner.invoke(cli, args=[pb_or_role, succ_or_pred, *files], catch_exceptions=False)

    assert 0 == result.exit_code

    output = sorted(line for line in result.output.split('\n') if len(line) > 0)
    assert expected_output == output
