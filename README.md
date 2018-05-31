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

Preparation
--------

    # Log on the build VM (OpenStack)
    ssh buildsys-rpm
    # Create the RPM build environment
    rpmdev-setuptree
    # Clone OpenIO's .spec files repository
    git clone https://github.com/open-io/rpm-specfiles.git
    cd ~/rpmbuild
    rmdir SPECS
    ln -s ../rpm-specfiles SPECS

Build one package
--------

    # Log on the build VM (OpenStack)
    ssh buildsys-rpm
    cd ~/rpmbuild/SPECS/openio-sds

    # Stable build
    # change "Version:" line in openio-sds.spec
    # add changelog entry (keep it in chronological order) in *.spec
    spectool -g -S *.spec
    SRCRPM=$(rpmbuild -bs --nodeps *.spec | awk '{print $2}')
    mock -r epel-7-x86_64-openio-sds-17.04 --rebuild $SRCRPM

    # Testing build
    GITTAG=3e52985ba15a4a30122ca2e64571f43860937580
    spectool -g -S -R --define '_with_test 1' --define "tag $GITTAG" *.spec
    SRCRPM=$(rpmbuild -bs --nodeps --define '_with_test 1' --define "tag $GITTAG" *.spec | awk '{print $2}')
    mock -r epel-7-x86_64-openio-sds-unstable --define '_with_test 1' --define "tag $GITTAG" --rebuild $SRCRPM

Repair the mirror / Remove a broken package
--------

    # Log on the build VM (OpenStack)
    ssh buildsys-rpm
    # Go inside the mirror (NFS mounted directory from mirror2.openio.io)
    cd /mnt/koji/mirror/pub/repo/openio/sds/17.04/el/7/x86_64
    # Remove the broken package(s)
    sudo rm -i openio-gridinit-1.7.0*
    # Re-create the metadatas
    createrepo .
    # Ask the QA team to double-check mirror2
    # Synchronize to the external mirror, if needed

    # In some rare unknown circumstances you may need to fix permissions
    sudo chmod g+w /mnt/koji/mirror/pub/repo/openio/sds/unstable/el/7/x86_64/repodata{,/*}

Bootstrap a release
--------

You'll need to build the packages in the following order:
* *openio-asn1c*
* *openio-gridinit*
* *openio-sds*
