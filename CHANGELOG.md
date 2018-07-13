# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Enable piping of file names to build dependencies for in addition to argument style

## [0.1.0] - 2018-04-09

### Added

- Recursive resolution of playbook imports
- Unified recursive handling of Ansible imports and includes
- Unified base for Ansible entities, including custom `__eq__`
- Factories and models Ansible entities; `Play`, for instance
- More unit tests
- Integration tests!

### Changed

- Improved role parsing

## [0.0.2] - 2018-03-08

### Added

- Also parse `meta/` in roles for dependencies

### Changed

- Switch from [PyYAML] to [ruamel.yaml] for parsing YAML files
- Improve logging

### Fixed

- Properly handle exceptions, prevent them to bubble up to the user

## [0.0.1] - 2018-03-06

### Added

- CLI with basic functionality for gathering dependencies and dependants for roles
- Dependency traversal for task includes in roles

[Unreleased]: https://github.com/croesnick/ansible-discover/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/croesnick/ansible-discover/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/croesnick/ansible-discover/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/croesnick/ansible-discover/compare/v0.0.1

[PyYAML]: https://pypi.python.org/pypi/PyYAML
[ruamel.yaml]: https://pypi.python.org/pypi/ruamel.yaml
