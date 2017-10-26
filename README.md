rpm-specfiles
=======

Here are the RPM spec files used by the [OpenIO](http://openio.io) project to build the packages provided in the [OpenIO repositories](http://mirror.openio.io).
For [Red Hat Enterprise Linux (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) and compatibles ([CentOS](https://www.centos.org) and [Scientific Linux](https://www.scientificlinux.org)), we rely on [EPEL](https://fedoraproject.org/wiki/EPEL) packages.

They are intended to be used with [Mock](https://fedoraproject.org/wiki/Mock).

Supported Platforms
--------

* CentOS 7 (tested)
* Scientific Linux 7 (untested)
* Red Hat Entreprise Linux 7 (untested)
* Fedora (untested)

How to build OpenIO SDS
--------

You'll need to build the packages in the following order:
* *openio-asn1c*
* *openio-gridinit*
* *openio-sds*
