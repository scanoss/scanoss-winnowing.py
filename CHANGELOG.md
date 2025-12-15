# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Upcoming changes...

## [0.7.0] - 2025-12-15
### Added
- Add `skip-headers` flag
### Modified
- Update winnowing.py to inherit from scanossbase.py for logging
  
## [0.6.0] - 2025-06-10
### Added
- Add `fh2` hash while fingerprinting mixed line ending files

## [0.5.4] - 2025-05-23
### Modified
- Update to align with scanoss.py winnowing.py implementation

## [0.5.3] - 2024-08-14
### Fixed
- Updated and fixed GH Actions dependencies

## [0.5.2] - 2024-08-09
### Added
- Added support for UTF-16 filenames

## [0.5.1] - 2024-04-17
### Added
- Added tagging workflow to aid release generation

## [0.5.0] - 2024-03-08
### Added
- Add filtering options: wfp and hpsm strip plus md5 skip.

## [0.4.1] - 2024-01-10
### Added
- Solve stability bug on HPSM.

## [0.4.0] - 2024-01-10
### Added
- Added C implementation of HPSM algorithm

## [0.3.0] - 2023-08-22
### Added
- Changed default post size limit to 32k
- Changed default size limiting to False
- Improved HPSM performance

## [0.2.0] - 2023-06-16
### Added
- Added support for HPSM, High Precision Snippet Matching

## [0.1.0] - 2023-01-01
### Added
- Added initial C implementation of winnowing algorithm

[0.1.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.0.1...v0.1.0
[0.2.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.1.1...v0.2.0
[0.3.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.2.0...v0.3.0
[0.4.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.3.0...v0.4.0
[0.4.1]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.4.0...v0.4.1
[0.5.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.4.1...v0.5.0
[0.5.1]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.5.0...v0.5.1
[0.5.2]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.5.1...v0.5.2
[0.5.3]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.5.2...v0.5.3
[0.5.4]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.5.3...v0.5.4
[0.6.0]: https://github.com/scanoss/scanoss-winnowing.py/compare/v0.5.4...v0.6.0
