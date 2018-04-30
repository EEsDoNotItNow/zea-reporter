
__version__ = '0.1.0'

from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=16, micro=12, releaselevel='final', serial=0)
