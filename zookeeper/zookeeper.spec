#
# spec file for package zookeeper
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define realname apache-zookeeper
%define srcext   tar.gz
%define so_ver   2

Name:           zookeeper
Version:        3.5.6
Release:        0
License:        Apache-2.0
Summary:        A high-performance coordination service for distributed applications
Group:          Development/Libraries/Java
Url:            http://zookeeper.apache.org/
Vendor:         Apache Software Foundation
Source0:        http://www.apache.org/dist/zookeeper/%{name}-%{version}/%{realname}-%{version}-bin.%{srcext}
Source1:        %{name}.service
Source2:        http://www.apache.org/dist/zookeeper/%{name}-%{version}/%{realname}-%{version}.%{srcext}
Patch0:         zkEnv.patch
Patch1:         01-zkpython-setup.patch
Patch2:         02-zkpython-module-init-return-value.patch
Patch3:         ftbfs-with-gcc-8.patch
BuildRequires:  autoconf automake libtool
BuildRequires:  cppunit-devel
%if 0%{?centos_ver} > 0
# CentOS
BuildRequires:  pkgconfig
%else
%if  0%{?suse_version}%{?fedora:9999} < 1550
# Old Opensuse
BuildRequires:  pkg-config
%else
# Opensuse Tumbleweed and Fedora
BuildRequires:  pkgconf-pkg-config
%endif
%endif
BuildRequires:  python-devel python-setuptools
BuildRequires:  python3-devel python3-setuptools
%if 0%{?suse_version} >= 1210
BuildRequires:  systemd-rpm-macros
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%{?systemd_requires}
Requires: java

%description
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services. All of these kinds of services are used in
some form or another by distributed applications. Each time they are
implemented there is a lot of work that goes into fixing the bugs and
race conditions that are inevitable. Because of the difficulty of
implementing these kinds of services, applications initially usually
skimp on them ,which make them brittle in the presence of change and
difficult to manage. Even when done correctly, different
implementations of these services lead to management complexity when
the applications are deployed.

%package -n libzookeeper%{so_ver}
Group:         System/Libraries
Summary:       C interface to ZooKeeper

Provides:      libzookeeper_mt%{so_ver} = %{version}-%{release}
Provides:      libzookeeper_st%{so_ver} = %{version}-%{release}
# CentOS compatibility
Provides:      zookeeper-lib = %{version}-%{release}
Obsoletes:     zookeeper-lib < 3.5

%description -n libzookeeper%{so_ver}
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services.

This package provides C interface library to ZooKeeper.

%package devel
Group:         Development/Libraries/C and C++
Summary:       Development files for C interface to ZooKeeper

Provides:      libzookeeper%{so_ver}-devel
Provides:      libzookeeper-devel
Provides:      libzookeeper_mt%{so_ver}-devel
Provides:      libzookeeper_st%{so_ver}-devel
Provides:      libzookeeper_mt-devel
Provides:      libzookeeper_st-devel
Requires:      libzookeeper%{so_ver} = %{version}-%{release}
# CentOS compatibility
Provides:      zookeeper-lib-devel = %{version}-%{release}
Obsoletes:     zookeeper-lib-devel < 3.5

%description devel
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services.

This package provides development stuff to build software against ZooKeeper.

%package -n python2-zookeeper
Summary:       Python client library for ZooKeeper
Group:         Development/Libraries/Python
Requires:      python2
Requires:      libzookeeper%{so_ver} = %{version}-%{release}
Provides:      python-ZooKeeper
Obsoletes:     python-ZooKeeper < 3.5

%description -n python2-zookeeper
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services.

This package provides the Python3 client library for ZooKeeper.

%package -n python3-zookeeper
Summary:       Python client library for ZooKeeper
Group:         Development/Libraries/Python
Requires:      python3
Requires:      libzookeeper%{so_ver} = %{version}-%{release}
Provides:      python-ZooKeeper
Obsoletes:     python-ZooKeeper < 3.5

%description -n python3-zookeeper
ZooKeeper is a centralized service for maintaining configuration
information, naming, providing distributed synchronization, and
providing group services.

This package provides the Python3 client library for ZooKeeper.

%prep
%setup -q -b 2 -n %{realname}-%{version}-bin
%patch0
sed -i 's/^dataDir=.*$/dataDir=\/var\/lib\/zookeeper\/data/' conf/zoo_sample.cfg
sed -i 's,^#!/usr/bin/env bash,#!/bin/bash,' bin/*.sh

# Prepare C and Python APIs
cd ../%{realname}-%{version}
# VL: This patch is obsolete, starting from version 3.5.6
#%patch1
%patch2
%patch3

# C API
cd zookeeper-client/zookeeper-client-c
test -x configure || autoreconf --install
cd ../..

# Python API
cd zookeeper-contrib/zookeeper-contrib-zkpython
sed -E -e 's,(version = ")[^"]+,\1%{version},' -i src/python/setup.py
cd ../..

%build
cd ../%{realname}-%{version}
_CFLAGS='%{optflags} %{?gcc_lto}'
_LDFLAGS='-Wl,--as-needed -Wl,--strip-all %{?gcc_lto}'
cd zookeeper-client/zookeeper-client-c
%configure \
 --disable-static \
 --without-cppunit \
 \
 CFLAGS="$_CFLAGS -Wno-error=nonnull -Wno-error=unused-but-set-variable" \
 LDFLAGS="$_LDFLAGS"
%{__make} %{?_smp_mflags}

cd ../..

# Build python bindings
cd zookeeper-contrib/zookeeper-contrib-zkpython
PBR_VERSION=%{version} %{__python2} src/python/setup.py build_ext
PBR_VERSION=%{version} %{__python3} src/python/setup.py build_ext
cd ../..


%install
# Precompiled Java libraries and dependencies
mkdir -p %{buildroot}%{_javadir}
mkdir -p %{buildroot}%{_javadir}/%{name}
cp -r lib/* %{buildroot}%{_javadir}/%{name}
(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*.jar; do ln -sf ${jar} `echo $jar| sed -e "s|-%{version}||g"`; done)

# Scripts
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/zkCleanup.sh %{buildroot}%{_bindir}
install -p -m 755 bin/zkCli.sh %{buildroot}%{_bindir}
install -p -m 755 bin/zkEnv.sh %{buildroot}%{_bindir}
install -p -m 755 bin/zkServer.sh %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
install -p -m 0640 conf/log4j.properties %{buildroot}%{_sysconfdir}/zookeeper
install -p -m 0640 conf/zoo_sample.cfg %{buildroot}%{_sysconfdir}/zookeeper
install -p -m 0640 conf/zoo_sample.cfg %{buildroot}%{_sysconfdir}/zookeeper/zoo.cfg

mkdir -p %{buildroot}/var/lib/zookeeper/data
# This file must contain a valid numeric ID
echo 0 > %{buildroot}/var/lib/zookeeper/data/myid

mkdir -p %{buildroot}/var/log/zookeeper

install -D -m 644 %{S:1} %{buildroot}%{_unitdir}/%{name}.service
mkdir -p %{buildroot}%{_sbindir}
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rc%{name}

# C API library
cd ../%{realname}-%{version}
%{__make} -C zookeeper-client/zookeeper-client-c install DESTDIR=%{buildroot}

# Python libraries
cd zookeeper-contrib/zookeeper-contrib-zkpython
PBR_VERSION=%{version} %{__python2} src/python/setup.py install \
    -O1 --skip-build --root $RPM_BUILD_ROOT
PBR_VERSION=%{version} %{__python3} src/python/setup.py install \
    -O1 --skip-build --root $RPM_BUILD_ROOT
cd ../..

%pre
groupadd --system zookeeper 2>/dev/null || :
useradd -g zookeeper -r -d /var/lib/zookeeper -s /bin/false \
        -c "ZooKeeper service account" zookeeper 2>/dev/null || :
%if 0%{?suse_version} >= 1210
%service_add_pre %{name}.service
%endif

%post
ZK_CLASSPATH=%{_javadir}/%{name}.jar:$(find %{_javadir}/%{name} -name "*.jar" -printf %p:)
echo "CLASSPATH=$ZK_CLASSPATH" > %{_sysconfdir}/zookeeper/java.env
/sbin/ldconfig > /dev/null 2>&1
%if 0%{?rhel_version} || 0%{?centos_version}
%systemd_post %{name}.service
%else
%service_add_post %{name}.service
%endif

%preun
%if 0%{?rhel_version} || 0%{?centos_version}
%systemd_preun %{name}.service
%else
%service_del_preun %{name}.service
%endif

%postun
/sbin/ldconfig > /dev/null 2>&1
%if 0%{?rhel_version} || 0%{?centos_version}
%systemd_postun %{name}.service
%else
%service_del_postun %{name}.service
%endif

%post   -n libzookeeper%{so_ver} -p /sbin/ldconfig
%postun -n libzookeeper%{so_ver} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.md
%{_bindir}/*.sh
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*
%attr(0750,zookeeper,zookeeper) %dir /var/lib/zookeeper
%attr(0750,zookeeper,zookeeper) %dir /var/lib/zookeeper/data
%attr(0640,zookeeper,zookeeper) /var/lib/zookeeper/data/myid
%attr(0755,zookeeper,zookeeper) %dir /var/log/zookeeper
%attr(0755,root,root) %dir %{_sysconfdir}/zookeeper
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/zookeeper/zoo.cfg
%config %attr(0644,root,root) %{_sysconfdir}/zookeeper/zoo_sample.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/zookeeper/log4j.properties
%{_unitdir}/%{name}.service
%{_sbindir}/rc%{name}

# Development stuff
%files devel
%defattr(-,root,root)
%{_includedir}/zookeeper/
%{_libdir}/*.so
%exclude %{_libdir}/*.la

%files -n libzookeeper%{so_ver}
%defattr(-,root,root)
%doc ../%{realname}-%{version}/zookeeper-client/zookeeper-client-c/{LICENSE,NOTICE.txt,README}
%{_bindir}/cli*
%{_bindir}/load_gen
%{_libdir}/libzookeeper_mt.so.%{so_ver}*
%{_libdir}/libzookeeper_st.so.%{so_ver}*

%files -n python2-zookeeper
%defattr(-, root, root, -)
%doc ../%{realname}-%{version}/zookeeper-contrib/zookeeper-contrib-zkpython/README
%doc ../%{realname}-%{version}/zookeeper-contrib/zookeeper-contrib-zkpython/src/python/zk.py
%if 0%{?centos_ver} > 0
%{python_sitearch}/*
%else
%{python2_sitearch}/*
%endif

%files -n python3-zookeeper
%defattr(-, root, root, -)
%doc ../%{realname}-%{version}/zookeeper-contrib/zookeeper-contrib-zkpython/README
%doc ../%{realname}-%{version}/zookeeper-contrib/zookeeper-contrib-zkpython/src/python/zk.py
%{python3_sitearch}/*

%changelog
