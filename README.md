rpm-specfiles
=======

Here are the RPM spec files used by the [OpenIO](http://openio.io) project to build the packages provided in [the OpenIO repositories](http://mirror.openio.io/).
For Red Hat Enterprise Linux (RHEL) and compatibles ([CentOS](https://fedoraproject.org/wiki/EPEL) and Scientific Linux), we rely on [EPEL](https://fedoraproject.org/wiki/EPEL) packages.

They are intended to use with [Mock](https://fedoraproject.org/wiki/Mock).


Supported Platforms
--------

* Entreprise Linux 6 & 7
* Fedora 21 & 22

OpenIO SDS build
--------

To build OpenIO SDS, you'll need to build the packages in the following order:
* openio-asn1c
* gf-complete
* jerasure
* openio-sds-librain
* For EL6, you'll need compat-libevent-20
* openio-gridinit
* openio-sds
