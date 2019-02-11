%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define cli_name oio
%define tarname  oio-sds

%if %{?suse_version}0
%define _sharedstatedir /var/lib
%endif

Name:           openio-sds

%if %{?_with_test:0}%{!?_with_test:1}
Version:        4.2.2
Release:        2%{?dist}
%define         tarversion %{version}
%define         targetversion %{version}
Source0:        https://github.com/open-io/oio-sds/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         targetversion 4.2.0
%define         git_repo https://github.com/open-io/oio-sds
Source0:        %{git_repo}/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        OpenIO Cloud Storage Solution
License:        AGPL-3.0
URL:            http://www.openio.io/
Source1:        openio-sds.tmpfiles

# golang deps
Source2:        https://github.com/tylerb/graceful/archive/v1.2.15.tar.gz
Source3:        https://github.com/go-ini/ini/archive/v1.38.2.tar.gz

Obsoletes:      openio-sds-client,openio-sds-client-devel

BuildRequires:  glib2-devel              >= 2.52.0
BuildRequires:  leveldb-devel
%if %{?fedora}%{?suse_version}0
BuildRequires:  python-pbr
BuildRequires:  zookeeper-devel          >= 3.3.4
%else
BuildRequires:  python2-pbr
BuildRequires:  zookeeper-lib-devel      >= 3.3.4
%endif
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  libcurl-devel
%if %{?suse_version}0
BuildRequires:  libapr1-devel            >= 1.2
BuildRequires:  apache2-devel            >= 2.2
BuildRequires:  libjson-c-devel          >= 0.12
BuildRequires:  libdb-6_0-devel
BuildRequires:  zeromq-devel

BuildRequires:  fdupes
%else
BuildRequires:  apr-devel                >= 1.2
BuildRequires:  httpd-devel              >= 2.2
BuildRequires:  json-c                   >= 0.12
BuildRequires:  json-c-devel             >= 0.12
BuildRequires:  libdb-devel
BuildRequires:  zeromq3-devel
%endif
BuildRequires:  sqlite-devel             >= 3.7.11
BuildRequires:  libattr-devel            >= 2.4.32
%if %{?el6}0
BuildRequires:  compat-libevent-20-devel >= 2.0
%else
BuildRequires:  libevent-devel           >= 2.0
%endif
BuildRequires:  lzo-devel                >= 2.0
BuildRequires:  zlib-devel
BuildRequires:  openio-asn1c             >= 0.9.27
BuildRequires:  cmake,bison,flex
BuildRequires:  golang


%description
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.


%package common
Summary: Common files for OpenIO Cloud Storage Solution
Requires:       expat
Requires:       glib2         >= 2.52
Requires:       openio-asn1c  >= 0.9.27
Requires:       zlib
%if %{?suse_version}0
Requires:       (libjson-c3 or libjson-c2>=0.12)
%else
Requires:       json-c        >= 0.12
%endif
%if %{?fedora}%{?suse_version}0
BuildRequires:  zookeeper     >= 3.3.4
%else
BuildRequires:  zookeeper-lib >= 3.3.4
%endif
%description common
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains common files used by other OpenIO SDS packages.


%package server
Summary: Server files for OpenIO Cloud Storage Solution
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-common = %{version}
%else
Requires:       %{name}-common = 1:%{version}
%endif
%if %{?fedora}%{?suse_version}0
BuildRequires:  zookeeper          >= 3.3.4
Requires:       python-zookeeper
%else
BuildRequires:  zookeeper-lib      >= 3.3.4
Requires:       python-ZooKeeper
%endif
Requires:       python             >= 2.7
%if %{?suse_version}0
Requires:       libapr1            >= 1.2
%else
Requires:       apr                >= 1.2
%endif
Requires:       sqlite             >= 3.7.11
Requires:       libattr            >= 2.4.32
%if %{?el6}0
Requires:       compat-libevent-20 >= 2.0
%else
BuildRequires:  libevent           >= 2.0
%endif
Requires:       leveldb
Requires:       lzo                >= 2.0
Requires:       openio-asn1c       >= 0.9.27
Requires:       python-gunicorn    >= 19.4.5
Requires:       python-eventlet
Requires:       python-zmq
Requires:       python-redis
Requires:       PyYAML
Requires:       python-futures
Requires:       pyxattr            >= 0.4
Requires:       python-simplejson  >= 2.0.9
Requires:       python-cliff       >= 1.13
Requires:       python-pyeclib     >= 1.2.0
Requires:       python-urllib3     >= 1.12
Requires:       python-werkzeug
# Needed for backblaze connector
Requires:       python-requests    >= 2.6.0

Provides:       python-oiopy


%description server
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains all needed server files to run OpenIO SDS
solution.


%package common-devel
Summary: Header files for OpenIO Cloud Storage Solution
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-common = %{version}
%else
Requires:       %{name}-common = 1:%{version}
%endif
%description common-devel
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains header files for OpenIO SDS solution client.


%package mod-httpd
Summary: Apache HTTPd module for OpenIO Cloud Storage Solution
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-server  = %{version}
%else
Requires:       %{name}-server  = 1:%{version}
%endif
%if %{?suse_version}0
Requires:       apache2        >= 2.2
Requires:       libdb-6_0
%else
Requires:       httpd          >= 2.2
Requires:       libdb
%endif
%description mod-httpd
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains Apache HTTPd module for OpenIO SDS solution.


%package tools
Summary: Side tools for OpenIO Cloud Storage Solution
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-server = %{version}
%else
Requires:       %{name}-server = 1:%{version}
%endif
%description tools
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains side tools for OpenIO SDS solution.



%prep
%setup -q -n %{tarname}-%{tarversion}

# Golang dependencies
cd ..
tar xf %{SOURCE2}
tar xf %{SOURCE3}

mkdir -p /builddir/go/src/gopkg.in/tylerb
cd /builddir/go/src/gopkg.in/tylerb
ln -s /builddir/build/BUILD/graceful-* graceful.v1
cd -

mkdir -p /builddir/go/src/gopkg.in/go-ini
cd /builddir/go/src/gopkg.in
ln -s /builddir/build/BUILD/ini-* ini.v1
cd -


%build
#VL: Workaround: "ERROR: No build ID note found in ..."
%undefine _missing_build_ids_terminate_build
cmake \
  -DCMAKE_BUILD_TYPE="Release" \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DEXE_PREFIX="%{cli_name}" \
  -DZK_LIBDIR="%{_libdir}" \
  -DZK_INCDIR="%{_includedir}/zookeeper" \
  -DLZO_INCDIR="%{_includedir}/lzo" \
  -DSOCKET_OPTIMIZED=1 \
  -DOIOSDS_RELEASE=%{version} \
%if %{?suse_version}0
  -DAPACHE2_INCDIR="%{_includedir}/apache2" \
  -DAPACHE2_LIBDIR="%{_libdir}/apache2" \
  -DAPACHE2_MODDIR="%{_libdir}/apache2" \
%endif
  "-DGCLUSTER_AGENT_SOCK_PATH=\"/run/oio/sds/sds-agent-0.sock\"" \
  .

make %{?_smp_mflags}

# Build python
PBR_VERSION=%{targetversion} %{__python} setup.py build


%install
%if %{?suse_version}0
%{__sed} -i -e 's,#!/usr/bin/env python,#!/usr/bin/python2,g' tools/*.py
%{__sed} -i -e 's,#!/usr/bin/env bash,#!/bin/bash,g' tools/*.sh
%endif

make DESTDIR=$RPM_BUILD_ROOT install

# Install python
PBR_VERSION=%{targetversion} %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%if %{?suse_version}0
%fdupes %{buildroot}%{python_sitelib}
%endif

# Install OpenIO SDS directories
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_localstatedir}/log/oio/sds \
  ${RPM_BUILD_ROOT}%{_sharedstatedir}/oio/sds \
  ${RPM_BUILD_ROOT}%{_sysconfdir}/oio/sds \
  ${RPM_BUILD_ROOT}%{_datarootdir}/%{name}-%{version}

# Install tmpfiles
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_tmpfilesdir} ${RPM_BUILD_ROOT}/run/oio/sds
%{__install} -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_tmpfilesdir}/openio-sds.conf

# Remove unwanted debug tool
rm -f ${RPM_BUILD_ROOT}%{_bindir}/%{cli_name}-dump-buried-events.py
rm -f ${RPM_BUILD_ROOT}%{_bindir}/%{cli_name}-webhook-test.py


%files common
%defattr(755,root,root,755)
%{_libdir}/libgridcluster.so*
%{_libdir}/libhcresolve.so*
%{_libdir}/libmeta0utils.so*
%{_libdir}/libmetautils.so*
%{_libdir}/libmeta0remote.so*
%{_libdir}/libmeta1remote.so*
%{_libdir}/liboio*
# TODO find why libserver is necessary in common
%{_libdir}/libserver.so*
# TODO find why libsqliterepo is necessary in common
%{_libdir}/libsqliterepo.so*
%{_libdir}/libsqlitereporemote.so*
%{_libdir}/libsqlxsrv.so*
%{_libdir}/libmeta2v2utils.so*
%{_libdir}/libsqliteutils.so*
%{_bindir}/%{cli_name}-daemon
%defattr(0644,openio,openio,0755)
%{_sysconfdir}/oio
%{_localstatedir}/log/oio
%defattr(0640,openio,openio,0750)
%{_sharedstatedir}/oio
%dir %{_datarootdir}/%{name}-%{version}

%files server
%defattr(755,root,root,755)
%{_libdir}/libmeta0v2.so*
%{_libdir}/libmeta1v2.so*
%{_libdir}/libmeta2v2.so*
%{_libdir}/librawx.so*
%{_bindir}/%{cli_name}-account-server
%{_bindir}/%{cli_name}-blob-auditor
%{_bindir}/%{cli_name}-blob-converter
%{_bindir}/%{cli_name}-blob-indexer
%{_bindir}/%{cli_name}-blob-mover
%{_bindir}/%{cli_name}-blob-rebuilder
%{_bindir}/%{cli_name}-blob-improver
%{_bindir}/%{cli_name}-conscience-agent
%{_bindir}/%{cli_name}-cluster
%{_bindir}/%{cli_name}-crawler-storage-tierer
%{_bindir}/%{cli_name}-event-agent
%{_bindir}/%{cli_name}-meta0-client
%{_bindir}/%{cli_name}-meta0-server
%{_bindir}/%{cli_name}-meta1-server
%{_bindir}/%{cli_name}-meta2-server
%{_bindir}/%{cli_name}-meta1-rebuilder
%{_bindir}/%{cli_name}-meta2-rebuilder
%{_bindir}/%{cli_name}-meta1-client
%{_bindir}/%{cli_name}-meta2-indexer
%{_bindir}/%{cli_name}-meta2-mover
%{_bindir}/%{cli_name}-rawx-compress
%{_bindir}/%{cli_name}-rawx-uncompress
%{_bindir}/%{cli_name}-rawx
%{_bindir}/%{cli_name}-rdir-server
%{_bindir}/%{cli_name}-sqlx
%{_bindir}/%{cli_name}-sqlx-server
%{_bindir}/%{cli_name}-tool
%{_bindir}/%{cli_name}-proxy
%{_bindir}/zk-bootstrap.py*
%{_bindir}/oio-gdb.py*
%{_bindir}/openio
%defattr(644,root,root,755)
%{python_sitelib}/oio*
/usr/lib/tmpfiles.d/openio-sds.conf
%if %{?suse_version}0
%ghost /run/oio
%else
/run/oio
%endif

%files common-devel
%defattr(644,root,root,755)
%{_prefix}/include/*
%{_libdir}/pkgconfig/oio-sds.pc

%files mod-httpd
%defattr(755,root,root,755)
%if %{?suse_version}0
%{_libdir}/apache2/mod_dav_rawx.so*
%else
%{_libdir}/httpd/modules/mod_dav_rawx.so*
%endif

%files tools
%defattr(755,root,root,755)
%{_bindir}/%{cli_name}-check-services
%{_bindir}/%{cli_name}-bootstrap.py
%{_bindir}/%{cli_name}-reset.sh
%{_bindir}/zk-reset.py
%{_bindir}/%{cli_name}-unlock-all.sh
%{_bindir}/%{cli_name}-wait-scored.sh
%{_bindir}/%{cli_name}-test-config.py
%{_bindir}/%{cli_name}-flush-all.sh
%{_bindir}/%{cli_name}-election-dump.py
%{_bindir}/%{cli_name}-election-reset.py
%{_bindir}/%{cli_name}-election-smudge.py
%{_bindir}/%{cli_name}-crawler-integrity
%{_bindir}/%{cli_name}-blob-registrator
%{_bindir}/%{cli_name}-election-stat.py
%{_bindir}/%{cli_name}-check-directory
%{_bindir}/%{cli_name}-check-master
%{_bindir}/%{cli_name}-file-tool

%pre common
# Add user and group "openio" if not exists
getent group openio >/dev/null || groupadd -g 220 openio
if ! getent passwd openio >/dev/null; then
  useradd -M -d /var/lib/oio -s /bin/bash -u 120 -g openio -c "OpenIO services" openio
fi

%post common
/sbin/ldconfig
%post server
/sbin/ldconfig
%tmpfiles_create %{_tmpfilesdir}/openio-sds.conf
%post mod-httpd
/sbin/ldconfig

%postun common
/sbin/ldconfig
%postun server
/sbin/ldconfig
%postun mod-httpd
/sbin/ldconfig

%changelog
* Wed Sep 26 2018 - 4.2.2-2 - Vincent Legoll <vincent.legoll@openio.io>
- Bump glib2 dependency to at least 2.52.0
* Wed Sep 26 2018 - 4.2.2-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Sep 11 2018 - 4.2.1.2-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Sep 07 2018 - 4.2.1.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Jul 16 2018 - 4.2.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Jul 12 2018 - 4.2.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Jun 20 2018 - 4.1.26-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Jun 13 2018 - 4.1.25-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Jun 04 2018 - 4.1.24-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon May 28 2018 - 4.1.23-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Apr 24 2018 - 4.1.22-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Apr 03 2018 - 4.1.21-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Mar 30 2018 - 4.1.20-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Mar 28 2018 - 4.1.19-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Mar 27 2018 - 4.1.18-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Mar 22 2018 - 4.1.17-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Mar 19 2018 - 4.1.16-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Fix pbr for CentOS and SuSe
* Tue Mar 06 2018 - 4.1.14-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Feb 28 2018 - 4.1.13-2 - Florent Vennetier <florent@fridu.net>
- Fix compilation on opensuse
* Wed Feb 21 2018 - 4.1.13-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Jan 23 2018 - 4.1.12-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Dec 12 2017 - 4.1.11-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Dec 11 2017 - 4.1.10-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Nov 27 2017 - 4.1.9-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Nov 24 2017 - 4.1.8-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Nov 21 2017 - 4.1.7-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Nov 06 2017 - 4.1.6-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Oct 27 2017 - 4.1.5-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Oct 04 2017 - 4.1.4-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Sep 19 2017 - 4.1.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Sep 18 2017 - 4.1.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Sep 12 2017 - 4.1.0-2 - Romain Acciari <romain.acciari@openio.io>
- Update python-urllib3 requirement
* Mon Sep 11 2017 - 4.1.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Jun 30 2017 - 4.0.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Jun 16 2017 - 3.3.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri May 12 2017 - 3.3.0-1 - Sebastien Lapierre <sebastien.lapierre@openio.io>
- New realease
- Rdir from python to C
* Tue May 09 2017 - 3.2.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Apr 20 2017 - 3.2.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Mar 28 2017 - 3.2.1-1 - Florent Vennetier <florent@fridu.net>
- Update to 3.2.1
- Fix compilation on opensuse
* Tue Feb 21 2017 - 3.2.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Feb 10 2017 - 3.2.0-0.c0 - Romain Acciari <romain.acciari@openio.io>
- Release Candidate 3.2.0.c0
* Fri Feb 03 2017 - 3.1.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Add python-futures
* Fri Dec 23 2016 - 3.1.2-1 - Romain Acciari <romain.acciari@openio.io>
- Update to 3.1.2 (Kraken released)
* Tue Nov 01 2016 - 3.1.0-0.beta0 - Sebastien Lapierre <sebastien.lapierre@openio.io>
- Update to 3.1.0.b0
* Mon Oct 31 2016 - 3.0.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Oct 21 2016 - 3.0.0-2 - Romain Acciari <romain.acciari@openio.io>
- Add obsoletes to remove old packages
* Thu Oct 20 2016 - 3.0.0-1 - Romain Acciari <romain.acciari@openio.io>
- Update to 3.0.0
* Thu Sep 15 2016 - 3.0.0-0.4 - Romain Acciari <romain.acciari@openio.io>
- Update to 3.0.0.b3
* Fri Jun 17 2016 - 2.1.0.-1 - Romain Acciari <romain.acciari@openio.io>
- Python API (python-oiopy) is now part of the core
* Tue May 17 2016 - 2.1.0.c0-2 - Romain Acciari <romain.acciari@openio.io>
- Recompile with CMAKE_BUILD_TYPE="RelWithDebInfo"
* Mon May 09 2016 - 2.1.0.c0-1 - Romain Acciari <romain.acciari@openio.io>
- Testing new release 2.1.0.c0
* Tue Apr 19 2016 - 2.0.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Apr 15 2016 - 2.0.0.c3-1 - Romain Acciari <romain.acciari@openio.io>
- New release candidate
* Wed Mar 16 2016 - 2.0.0.c2-1 - Romain Acciari <romain.acciari@openio.io>
- New release candidate
- Fix %%defattr warnings
- Add files
* Thu Mar 03 2016 - 2.0.0.c1-1 - Romain Acciari <romain.acciari@openio.io>
- New release candidate (change major version)
* Thu Feb 25 2016 - 1.1.rc0-1 - Romain Acciari <romain.acciari@openio.io>
- New release cadidate
* Mon Dec 14 2015 - 1.0.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Renamed package client-devel to common-devel
* Tue Dec 01 2015 - 1.0.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release 1.0.0
* Wed Sep 16 2015 - 0.8.3-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Mon Sep 14 2015 - 0.8.2-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Thu Sep 10 2015 - 0.8.1-2 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Wed Sep 02 2015 - 0.8.1-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Fri Aug 28 2015 - 0.8.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Remove Net-SNMP package
* Fri Jul 03 2015 - 0.7.6-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Tue Jun 30 2015 - 0.7.5-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Tue Jun 30 2015 - 0.7.4-2 - Romain Acciari <romain.acciari@openio.io>
- Remove integrityloop package
* Mon Jun 29 2015 - 0.7.4-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Mon Jun 22 2015 - 0.7.3-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Wed Jun 17 2015 - 0.7.2-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Wed Jun 17 2015 - 0.7.1-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Tue Jun 09 2015 - 0.7-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Removed useless BuildRequires
- Add python dependencies in server
* Thu May 28 2015 - 0.6.6-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Tue May 26 2015 - 0.6.5-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Sun May 17 2015 - 0.6.4-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Fri May 15 2015 - 0.6.3-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Wed May 13 2015 - 0.6.2-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Tue May 12 2015 - 0.6.1-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Mon May 11 2015 - 0.6-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Apr 24 2015 - 0.5-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Apr 09 2015 - 0.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Mar 25 2015 - 0.2.2-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Thu Mar 19 2015 - 0.2.1-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
