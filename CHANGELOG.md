# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). (or tries to...)

## [v0.7.2] 2020-12-16

### Added

- Added pre-commit hook support to enforce code style (black, isort)
- Added unittest for defusedxml to fix billionlaugh and external entities security issues
- Added extra_requires for plugins deps and defusedxml
- Added banner_dict support + unittest (Merge edited PR from @cfoulds)
- Added black, isort in tox environment
- Added more unit tests in several modules to improve code collaboration and automated tested
- Added GitHub action pipeline to run pytests, black and isort checks
- Added GitHub action pipeline to publish pypi package

### Changed

- Code linted and styled with black and isort
- Changed Licence from CC-BY to Apache 2.0, considering that CC is [not appropriate for code licensing](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software)
- Changelog now using [Keep-a-changelog](https://keepachangelog.com/en/1.0.0/) specs

### Removed

- Removed travis build in favor of GitHub Actions pipelines

### Fixed

- Fix empty nmap outputs due to subprocess race condition (Merge PR#79 from @Shouren)
- Add extra_requires for plugins deps and defusedxml
- Removed code duplication in sudo_run and sudo_run_background from process.py

### Security

- Fix for security issue on XXE (XML External Entities) - CVE-2019-1010017

## [v0.7.0] - 28/02/2016

### Fixed

- Fix of endless loop in Nmap.Process. Fix provided by @rcarrillo, many thanks!

## [v0.6.3] - 18/08/2015

### Added

- Merged pull requests for automatic pypi upload, thanks @bmx0r

## [v0.6.2] -  03/01/2015

### Added

- Added cpe_list method
- Added elasticsearch example code

### Fixed

- Fixed issues: 37, 41, 42, 43, 44, 46

## [v0.6.1] - 29/06/2014

### Added

- Added full support for python 3.X: python now supports python 2.6, 2.7, 3.3, 3.4

## [v0.5.1] - 26/05/2014

### Added

- Basic API for class CPE interface similar to python-cpe for more advanced usage of CPE, I strongly recommend you to use python-cpe.

## [v0.5.0] - 17/05/2014

### Added

- Added NmapTask class
- Added NmapProcess.current_task
- Added NmapProcess.tasks list
- Use of semaphore to not consume CPU while looping

### Fixed

- Removed Threads to read stdout/stderr
- Fixed bug in NmapProcess.state

## [v0.4.9] - 14/05/2014

### Added

- Added [code samples](examples/)

### Fixed

- Fix for issue 28

## [v0.4.8] - 05/05/2014

### Changed

- Changes in OS fingerprint data API
- NmapHost now holds its OS fingerprint data in NmapHost.os (NmapOSFingerpring object)
- fingerprint is now a property which means you have to call it without (); e.g.: NmapHost.os.fingerprint
- NmapHost.os.fingerprints return an array of os fingerprints (strings)
- NmapHost.os.fingerprint return a concatenated string of all fingerprints
- Fingerprints data are now accessible via NmapHost.os.osmatches which returns a list of NmapOSMatch objects
- NmapOSMatch objects might contain a list of NmapOSClass objects matching with it
- NmapOSClass objects might contain a list of CPE object related to the os class (CPE class will be improved and API enriched)

## [v0.4.7] - 03/05/2014

### Added

- added support for <owner> if present in <port>: accessible via NmapService.owner

### Fixed

- Minor fix for issue25
- Fixed exception when optional service tag is not present in <port> tag


## [v0.4.6] - 06/04/2014

### Added

- Added support to run scan in background with sudo support
- Added NmapProcess.sudo_run_background()

### Fixed

- Corrected missing incomplete parameter on parse_fromfile and parse_fromstring
- Fixed issue with run() blocking when an error triggered during the scan

## [v0.4.5] - 06/04/2014

### Added

- Added "incomplete" argument in NmapReport.parse() in order to enable parsing of incomplete or interrupted nmap scans. Could be useful to use with a background scan to parse incomplete data blocks from callback function (thanks @Sibwara for the idea).
- Added NmapReport.endtimestr
- Added and tested cElementTree support (performance)

### Fixed 

- Fixed bug when NmapReport.summary is empty

## [v0.4.4] - 04/04/2014

### Added
- Added support for tunnel attribute from <service> tag
- Added support for servicefp (service fingerprint) in attributes from <port><service> tag
- Added support for reasons attributes from <port> tag
- Added support for extraports/extrareasons tags

### Fixed

- corrected bug in serialization: missing extra data (pull request from @DougRoyal)

## [v0.4.3] - 14/03/2014

### Changed

- API change for NmapService.scripts_results:
  - NmapHost.address property returns the IPv4 or IPv6 or MAC in that preference order. Use specific calls for determinists results
  - NmapService.scripts_results is now a property
  - NmapService.scripts_results return an array of scripts results

### Added

- Added new properties in hosts object API:
  - NmapHost.ipv4
  - NmapHost.ipv6
  - NmapHost.mac

### Fixed

- Fix issue#14: better scripts parsing
- Fix issue#9 address field not correcly parsed: MAC Address would erase an ipv4 address type.
- Fix API issue#10: os_ports_used

## [v0.4.2] - 26/12/2013

### Fixed

- Fixed #issue8: There is no guarantee that "finished" or "runstats" will be received by event parser of process.py.
- Summary functions are now flagged as deprecated. To use data from scan summary of numbers of hosts up, the user of the lib will have to use NmapParser.parse() and the appropriate accessors.

## [v0.4.1] - 26/12/2013

### Fixed

- Fixed issue#6: Infinite loop while launching several nmap scans in background

## [v0.4.0] - 28/10/2013

### Added

- Added stop() to terminate nmap scan running in background

### Fixed 

- Bug corrected in missing data from nmap scan output
                      
## [v0.3.1] - 17/06/2013

### Changed

- Refactory of objects to isolate each nmap object in a separate file

## [v0.3.0] - 17/06/2013

### Added

- Added fingerprint class
- Added NmapOSFingerprint class to provide better API to fingerprint data
- Added unit tests for basic NmapHost API check
- Added unit test for basic NmapOSFingerprint class

## [v0.2.9] - 17/06/2013

### Added

- Add S3 plugin, allow to store nmapreport object to aws S3 compatible object storage backend (via boto)

## [v0.2.8] - 11/06/2013

### Added

- Prepare packaging for pypi

## [v0.2.1] - 17/05/2013

### Added
- Code Docstring and added support for additional data
- Added support for scripts in NmapService
- Added support for hosts extra data in NmapHost (uptime, distance,...)
- Added support for OS fingerprint data in NmapHost
- Added python docstrings for all modules
- Added sphinx documentation

### Fixed

- Reviewed API for libnmap objects
- Fixed errors with hash() in diff
- Fixed errors/exceptions in NmapParser

## [v0.2.0] - 18/04/2013

### Added

- Added Serialization and Plugin support
- Added serialization encoders and decoders for NmapReport
- Added basic plugin capability to NmapReport
- Added basic mongodb plugin to validate plugin setup

## [v0.1.5] - 08/04/2013

### Changed

Refactory of NmapDiff system
- Rework of NmapHost and NmapService API
- Added __hash__, id and get_dict() for common Nmap Objects
- Added NmapDiff class
- Full rework of unittests
- NmapParser now supports parsing from file
- NmapParser is able to handle nmap XML portions
- Added import in reports

## [v0.1.4] - 05/04/2013 -- Bug Fixes and improvements

### Added

- Added unittest for diff on NmapHost
- Added unittest for diff on NmapService

### Fixed

- Fixed: __eq__ in NmapService: protocol not honoured
- Fixed: sudo_run hardened and added exception handling

## [v0.1.3] - 04/04/2013

### Added

- Full refactory of NmapParser with static method
- Added support for diffing NmapHost and NmapService
- Added NmapParserException class
- Added NmapReport class
- Added unittest for report api
- Added unittest for parser

### Fixed

- Corrected en hardened code for NmapParser

## [v0.1.2] - 13/03/2013

### Added

- Added scaninfo parsing

### Fixed

- Corrected unused variables and wrong unittests
- Parse() method reviewed to call "independent" XML bloc parsers

## [v0.1.1] - 12/03/2013

### Added

- Complete refactory of code to isolate NMAP objects.

## [v0.1.0] - 11/03/2013

### Added

- First developement release packaged for Project Ninaval
