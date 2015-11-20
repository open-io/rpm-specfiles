%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define cli_name oio
%define tarname  oio-sds

Name:		openio-sds

%if %{?_with_test:0}%{!?_with_test:1}
Version:	0.8.3
Release:	1%{?dist}
%define		tarversion %{version}
Source0:	https://github.com/open-io/oio-sds/archive/v%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define		date %(date +"%Y%m%d%H%M")
Version:	test%{date}.%{tag}
Release:	0%{?dist}
%define		tarversion %{tag}
Source0:	https://github.com/open-io/oio-sds/archive/%{tarversion}.tar.gz
Epoch:		1
%endif

Summary:	OpenIO Cloud Storage Solution
Group:		openio
License:	AGPL
URL:		http://www.openio.io/
Source1:        openio-sds.tmpfiles


BuildRequires:	glib2-devel              >= 2.28.8
%if %{?fedora}0
BuildRequires:  zookeeper-devel          >= 3.3.4
%else
BuildRequires:  zookeeper-lib-devel      >= 3.3.4
%endif
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:  zeromq3-devel
BuildRequires:	libcurl-devel
BuildRequires:	apr-devel                >= 1.2
BuildRequires:	sqlite-devel             >= 3.7.11
BuildRequires:	libattr-devel            >= 2.4.32
%if %{?el6}0
BuildRequires:	compat-libevent-20-devel >= 2.0
%else
BuildRequires:	libevent-devel           >= 2.0
%endif
BuildRequires:	httpd-devel              >= 2.2
BuildRequires:	lzo-devel                >= 2.0
BuildRequires:	openio-gridinit-devel
BuildRequires:	openio-asn1c             >= 0.9.27
BuildRequires:	cmake,bison,flex
BuildRequires:	librain-devel
BuildRequires:	libdb-devel
BuildRequires:	json-c                   >= 0.12
BuildRequires:	json-c-devel             >= 0.12


%description
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.


%package common
Summary: common files for OpenIO Cloud Storage Solution
Group: openio
Requires:	expat
Requires:	glib2         >= 2.28
Requires:	openio-asn1c  >= 0.9.27
Requires:	zlib
Requires:	json-c        >= 0.12
%if %{?fedora}0
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
Group: openio
%if %{?_with_test:0}%{!?_with_test:1}
Requires:	%{name}-common = %{version}
%else
Requires:	%{name}-common = 1:%{version}
%endif
%if %{?fedora}0
BuildRequires:  zookeeper          >= 3.3.4
Requires:       python-zookeeper
%else
BuildRequires:  zookeeper-lib      >= 3.3.4
Requires:       python-ZooKeeper
%endif
Requires:	python             >= 2.7
Requires:	apr                >= 1.2
Requires:	sqlite             >= 3.7.11
Requires:	libattr            >= 2.4.32
%if %{?el6}0
Requires:	compat-libevent-20 >= 2.0
%else
BuildRequires:	libevent           >= 2.0
%endif
Requires:	lzo                >= 2.0
Requires:	openio-gridinit-utils
Requires:	openio-asn1c       >= 0.9.27
Requires:	python-gunicorn    >= 19.0
Requires:	python-flask,python-eventlet,python-zmq,python-redis,python-requests
Requires:	pyxattr            >= 0.4
Requires:	python-simplejson  >= 2.0.9
%description server
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains all needed server files to run OpenIO SDS
solution.


%package client-devel
Summary: Header files for OpenIO Cloud Storage Solution client
Group: openio
%if %{?_with_test:0}%{!?_with_test:1}
Requires:	%{name}-client = %{version}
%else
Requires:	%{name}-client = 1:%{version}
%endif
%description client-devel
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains header files for OpenIO SDS solution client.


%package mod-httpd
Summary: Apache HTTPd module for OpenIO Cloud Storage Solution
Group: openio
%if %{?_with_test:0}%{!?_with_test:1}
Requires:	%{name}-server  = %{version}
%else
Requires:	%{name}-server  = 1:%{version}
%endif
Requires:	httpd          >= 2.2
Requires:	libdb
%description mod-httpd
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains Apache HTTPd module for OpenIO SDS solution.


%package mod-httpd-rainx
Summary: Apache HTTPd module for OpenIO Cloud Storage Solution
Group: openio
%if %{?_with_test:0}%{!?_with_test:1}
Requires:	%{name}-server  = %{version}
%else
Requires:	%{name}-server  = 1:%{version}
%endif
Requires:	httpd          >= 2.2
Requires:       librain
%description mod-httpd-rainx
OpenIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains Apache HTTPd module for OpenIO SDS solution.


%package tools
Summary: Side tools for OpenIO Cloud Storage Solution
Group: openio
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-server = %{version}
%else
Requires:       %{name}-server = 1:%{version}
%endif
%description tools
penIO software storage solution is designed to handle PETA-bytes of
data in a distributed way, data such as: images, videos, documents, emails,
and any other personal unstructured data.
OpenIO is a fork of Redcurrant, from Worldline by Atos.
This package contains side tools for OpenIO SDS solution.



%prep
%setup -q -n %{tarname}-%{tarversion}


%build
cmake \
  -DCMAKE_BUILD_TYPE="Debug" \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DEXE_PREFIX="%{cli_name}" \
  -DZK_LIBDIR="%{_libdir}" \
  -DZK_INCDIR="%{_includedir}/zookeeper" \
  -DLZO_INCDIR="%{_includedir}/lzo" \
  -DMOCKS=1 \
  -DSOCKET_OPTIMIZED=1 \
  -DSTACK_PROTECTOR=1 \
  "-DGCLUSTER_AGENT_SOCK_PATH=\"/run/oio/sds/sds-agent-0.sock\"" \
  .

make %{?_smp_mflags}

# Build python
(cd python; PBR_VERSION=0.0.1 %{__python} setup.py build)


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Install python
(cd python; PBR_VERSION=0.0.1 %{__python} ./setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT)


# Install OpenIO SDS directories
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_localstatedir}/log/oio/sds \
                ${RPM_BUILD_ROOT}%{_sharedstatedir}/oio/sds \
                ${RPM_BUILD_ROOT}%{_sysconfdir}/oio/sds \
		${RPM_BUILD_ROOT}%{_datarootdir}/%{name}-%{version}

# Install tmpfiles
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_tmpfilesdir} ${RPM_BUILD_ROOT}/run/oio/sds
%{__install} -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_tmpfilesdir}/openio-sds.conf


%files common
#%defattr(-,root,root,-)
%defattr(755,root,root,-)
%{_libdir}/libgridcluster-conscience.so*
%{_libdir}/libgridcluster.so*
%{_libdir}/libhcresolve.so*
%{_libdir}/libmeta0utils.so*
%{_libdir}/libmetautils.so*
%{_libdir}/libmeta0remote.so*
%{_libdir}/libmeta1remote.so*
%{_libdir}/libmeta2v2remote.so*
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
/run/oio
%dir %{_datarootdir}/%{name}-%{version}

%files server
%defattr(-,root,root,-)
%defattr(755,root,root,-)
%{_libdir}/grid/msg_conscience.so*
%{_libdir}/grid/msg_fallback.so*
%{_libdir}/grid/msg_ping.so*
%{_libdir}/grid/msg_stats.so*
%{_libdir}/libmeta0v2.so*
%{_libdir}/libmeta1v2.so*
%{_libdir}/libmeta2v2.so*
%{_libdir}/libmeta2v2utils.so*
%{_libdir}/librawx.so*
%{_libdir}/libserver.so*
%{_libdir}/libsqliterepo.so*
%{_libdir}/libsqliteutils.so*
%{_bindir}/%{cli_name}-account-server
%{_bindir}/%{cli_name}-blob-auditor
%{_bindir}/%{cli_name}-blob-mover
%{_bindir}/%{cli_name}-conscience-agent
%{_bindir}/%{cli_name}-cluster
%{_bindir}/%{cli_name}-cluster-agent
%{_bindir}/%{cli_name}-echo-server
%{_bindir}/%{cli_name}-event-agent
%{_bindir}/%{cli_name}-meta0-init
%{_bindir}/%{cli_name}-meta0-client
%{_bindir}/%{cli_name}-meta0-server
%{_bindir}/%{cli_name}-meta1-server
%{_bindir}/%{cli_name}-meta2-server
%{_bindir}/%{cli_name}-meta1-client
%{_bindir}/%{cli_name}-proxy-monitor.py
%{_bindir}/%{cli_name}-rawx-compress
%{_bindir}/%{cli_name}-rawx-uncompress
%{_bindir}/%{cli_name}-redis-monitor.py
%{_bindir}/%{cli_name}-sqlx
%{_bindir}/%{cli_name}-sqlx-server
%{_bindir}/%{cli_name}-svc-monitor
%{_bindir}/%{cli_name}-tool
%{_bindir}/%{cli_name}-proxy
%{_bindir}/zk-bootstrap.py*
%{python_sitelib}/oio*
/usr/lib/tmpfiles.d/openio-sds.conf
%{_bindir}/%{cli_name}-account-monitor.py

%files client-devel
%defattr(-,root,root,-)
%{_prefix}/include/*

%files mod-httpd
%defattr(755,root,root,-)
%{_libdir}/httpd/modules/mod_dav_rawx.so*
%{_bindir}/%{cli_name}-rawx-monitor.py

%files mod-httpd-rainx
%defattr(755,root,root,-)
%{_libdir}/httpd/modules/mod_dav_rainx.so*
%{_bindir}/%{cli_name}-rainx-monitor.py

%files tools
%defattr(755,root,root,-)
%{_bindir}/%{cli_name}-bootstrap.py
%{_bindir}/%{cli_name}-reset.sh
%{_bindir}/zk-reset.py


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
%post mod-httpd
/sbin/ldconfig
%post mod-httpd-rainx
/sbin/ldconfig

%postun common
/sbin/ldconfig
%postun server
/sbin/ldconfig
%postun mod-httpd
/sbin/ldconfig

%changelog
* Wed Sep 16 2015 - 0.8.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Sep 14 2015 - 0.8.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Sep 10 2015 - 0.8.1-2 - Romain Acciari <romain.acciari@openio.io>
- Add STACK_PROTECTOR flag
- Require json-c >= 0.12
* Wed Sep 02 2015 - 0.8.1-1 - Romain Acciari <romain.acciari@openio.io>
- Bugfix release
* Fri Aug 28 2015 - 0.8.0-1 - Romain Acciari <romain.acciari@openio.io>
- Remove Net-SNMP package
- Add new files
* Fri Jul 03 2015 - 0.7.6-1 - Romain Acciari <romain.acciari@openio.io>
- Accounts autocreation
- Various minor fixes and improvements (debug traces, error reporting)
* Tue Jun 30 2015 - 0.7.5-1 - Romain Acciari <romain.acciari@openio.io>
- proxy: fixed flag detection
- svc-monitor: lighter traces
- cmake: SDK_ONLY directive
* Tue Jun 30 2015 - 0.7.4-2 - Romain Acciari <romain.acciari@openio.io>
- Obsoletes intregrityloop
* Mon Jun 29 2015 - 0.7.4-1 - Romain Acciari <romain.acciari@openio.io>
- event-agent improvements
- proxy evolution for more adaptation with the future Swift interop.
- SDK fixes
- server fixes
* Mon Jun 22 2015 - 0.7.3-1 - Romain Acciari <romain.acciari@openio.io>
- proxy: fixed listing of containers: the delimiter behavior was broken
- gridagent: Fixed timeout management: uses monotonic clock with millisecond precision
- sdk: improved
* Wed Jun 17 2015 - 0.7.2-1 - Romain Acciari <romain.acciari@openio.io>
- Merge pull request #55 from jkasarherou/master
* Wed Jun 17 2015 - 0.7.1-1 - Romain Acciari <romain.acciari@openio.io>
- Merge pull request #53 from jfsmig/master
- SDK improvements, better access logs, svc-monitor fixed.
* Tue Jun 09 2015 - 0.7-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Removed useless BuildRequires
- Add python dependencies in server
* Thu May 28 2015 - 0.6.6-1 - Romain Acciari <romain.acciari@openio.io>
- Fixed logging
* Tue May 26 2015 - 0.6.5-1 - Romain Acciari <romain.acciari@openio.io>
- Minor changes destined to help integrate OIO SDS's C client in external applications.
* Sun May 17 2015 - 0.6.4-1 - Romain Acciari <romain.acciari@openio.io>
- metautils: fixed memory leaks when extracting message bodies.
* Fri May 15 2015 - 0.6.3-1 - Romain Acciari <romain.acciari@openio.io>
- Memleaks fixed in: oio-proxy,oio-meta1-server
* Wed May 13 2015 - 0.6.2-1 - Romain Acciari <romain.acciari@openio.io>
- The memleaks concerned every sqliterepo-based services : meta0, meta1, meta2, sqlx.
* Tue May 12 2015 - 0.6.1-1 - Romain Acciari <romain.acciari@openio.io>
- M2V2 felt when deleting content properties (while setting a property with an empty value)
* Mon May 11 2015 - 0.6-1 - Romain Acciari <romain.acciari@openio.io>
- Bump to 0.6
* Fri Apr 24 2015 - 0.5-1 - Romain Acciari <romain.acciari@openio.io>
- Merge pull request #14 from jfsmig/master
- m2v2: uses ZMQ 3.X instead of ZMQ 4.X
* Thu Apr 09 2015 - 0.3-1 - Romain Acciari <romain.acciari@openio.io>
- Update to 0.3
* Wed Mar 25 2015 - 0.2.2-1 - Romain Acciari <romain.acciari@openio.io>
- m2v2: disables checks upon PUT and UPDATE
* Thu Mar 19 2015 - 0.2.1-1 - Romain Acciari <romain.acciari@openio.io>
- Fix meta1 error
* Wed Mar 18 2015 - 20150318-1 - Romain Acciari <romain.acciari@openio.io>
- Cleaned the spec
- Add tmpfiles
* Fri Mar 13 2015 - 20150313-1 - Romain Acciari <romain.acciari@openio.io>
- Daily update
* Thu Mar 12 2015 - 20150312-1 - Romain Acciari <romain.acciari@openio.io>
- Just another daily release
* Wed Mar 11 2015 - 20150311-1 - Romain Acciari <romain.acciari@openio.io>
- Fix other hardcoded paths
- Fix tools permissions
* Tue Mar 10 2015 - 20150310-1 - Romain Acciari <romain.acciari@openio.io>
- Fix agent sock path
- Many other fixes
* Fri Mar 06 2015 - 20150306-2 - Romain Acciari <romain.acciari@openio.io>
- Fix directories, user and group in spec file
* Fri Mar 06 2015 - 20150306-1 - Romain Acciari <romain.acciari@openio.io>
- Fix meta1 replication
- Update to current development
* Mon Feb 02 2015 - 20150202-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
