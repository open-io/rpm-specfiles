#%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: High-performance coordination service for distributed applications.
Name: zookeeper
Version: 3.4.13
Release: 2%{?dist}
License: Apache License v2.0
Group: Applications/Databases
URL: http://hadoop.apache.org/zookeeper/
Source0: http://www-us.apache.org/dist/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1: zookeeper.init
Source2: zookeeper.logrotate
Source3: zoo.cfg
Source4: log4j.properties
Source5: java.env
# VL: disabled the patch
#Patch0: ZOOKEEPER-critsects.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel
BuildRequires: gcc,libtool
BuildRequires: cppunit-devel
Requires: logrotate, java
Requires(post): chkconfig initscripts
Requires(pre): chkconfig initscripts
AutoReqProv: no

%description
ZooKeeper is a distributed, open-source coordination service for distributed
applications. It exposes a simple set of primitives that distributed
applications can build upon to implement higher level services for
synchronization, configuration maintenance, and groups and naming. It is
designed to be easy to program to, and uses a data model styled after the
familiar directory tree structure of file systems. It runs in Java and has
bindings for both Java and C.

Coordination services are notoriously hard to get right. They are especially
prone to errors such as race conditions and deadlock. The motivation behind
ZooKeeper is to relieve distributed applications the responsibility of
implementing coordination services from scratch.


%prep
%setup -q -n zookeeper-%{version}
#%patch0 -p1

pushd src/c
rm -rf aclocal.m4 autom4te.cache/ config.guess config.status config.log \
    config.sub configure depcomp install-sh ltmain.sh libtool \
    Makefile Makefile.in missing stamp-h1 compile
autoheader
libtoolize --force
aclocal
automake -a
autoconf
autoreconf
popd

%build
pushd src/c
%configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc \
	--enable-shared \
	--disable-static
%{__make} %{?_smp_mflags}
popd

# Build Python interface
cd src/contrib/zkpython
python src/python/setup.py build_ext -L $PWD/../../c/.libs

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -p -d $RPM_BUILD_ROOT%{_libdir}/zookeeper  $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_datadir}/zookeeper
%{__install} bin/*.sh $RPM_BUILD_ROOT%{_bindir}/
%{__install} lib/*.jar $RPM_BUILD_ROOT%{_datadir}/zookeeper/
%{__install} -p -D -m 644 zookeeper-%{version}.jar $RPM_BUILD_ROOT%{_datadir}/zookeeper/zookeeper-%{version}.jar
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/zookeeper

# Install init script
%{__install} -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_initrddir}/zookeeper

# Install config files
%{__install} -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
%{__install} -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/zookeeper/zoo.cfg
%{__install} -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/zookeeper/log4j.properties
%{__install} -p -D -m 644 %{S:5} $RPM_BUILD_ROOT%{_sysconfdir}/zookeeper/java.env
%{__install} -p -D -m 644 conf/configuration.xsl $RPM_BUILD_ROOT%{_sysconfdir}/zookeeper/configuration.xsl

# Link scripts to human readable command
%{__install} -d $RPM_BUILD_ROOT%{_sbindir}
ln -sf %{_bindir}/zkServer.sh $RPM_BUILD_ROOT%{_sbindir}/zookeeper-server
ln -sf %{_bindir}/zkCleanup.sh $RPM_BUILD_ROOT%{_sbindir}/zookeeper-cleanup
ln -sf %{_bindir}/zkCli.sh $RPM_BUILD_ROOT%{_bindir}/zookeeper-cli

# Create var directories
%{__install} -d $RPM_BUILD_ROOT%{_localstatedir}/log/zookeeper
%{__install} -d $RPM_BUILD_ROOT%{_localstatedir}/lib/zookeeper
%{__install} -d $RPM_BUILD_ROOT%{_localstatedir}/lib/zookeeper/data
%{__install} -p -d -D -m 0755 $RPM_BUILD_ROOT%{_datadir}/zookeeper

# Install C components
%{makeinstall} -C src/c

# Kludge for ugly default path
#mv $RPM_BUILD_ROOT%{_includedir}/c-client-src $RPM_BUILD_ROOT%{_includedir}/zookeeper

# Install Python stuff
cd src/contrib/zkpython
python src/python/setup.py install --install-lib $RPM_BUILD_ROOT%{python_sitearch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc LICENSE.txt NOTICE.txt README.txt
%doc LICENSE.txt NOTICE.txt
%doc docs recipes
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper/data
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/log/zookeeper
%{_initrddir}/zookeeper
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/zookeeper
%{_sbindir}/*
%{_bindir}/*
%{_datadir}/zookeeper

# ------------------------------ libzookeeper ------------------------------

%package lib
Summary: C client interface to zookeeper server
Group: Development/Libraries
BuildRequires: gcc

%description lib
The client supports two types of APIs -- synchronous and asynchronous.
 
Asynchronous API provides non-blocking operations with completion callbacks and
relies on the application to implement event multiplexing on its behalf.
 
On the other hand, Synchronous API provides a blocking flavor of
zookeeper operations and runs its own event loop in a separate thread.
 
Sync and Async APIs can be mixed and matched within the same application.

%files lib
%defattr(-, root, root, -)
%doc src/c/README src/c/LICENSE
%{_libdir}/libzookeeper_mt.so*
%{_libdir}/libzookeeper_st.so*

# ------------------------------ libzookeeper-devel ------------------------------

%package lib-devel
Summary: Headers and static libraries for libzookeeper
Group: Development/Libraries
Requires: %{name}-lib
Requires: gcc

%description lib-devel
This package contains the libraries and header files needed for
developing with libzookeeper.

%files lib-devel
%defattr(-, root, root, -)
%{_includedir}/*
%{_libdir}/*.la

# ------------------------------ Python ------------------------------

%package -n python-ZooKeeper
Summary: Python client library for ZooKeeper
Group: Development/Libraries
Requires: python, %{name}-lib

%description -n python-ZooKeeper
Python client library for ZooKeeper.

%files -n python-ZooKeeper
%defattr(-, root, root, -)
%doc src/contrib/zkpython/README src/contrib/zkpython/src/python/zk.py
%{python_sitearch}/*


%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper >/dev/null || useradd -r -g zookeeper -d / -s /sbin/nologin zookeeper
exit 0

%post
/sbin/chkconfig --add zookeeper

%preun
if [ $1 = 0 ] ; then
    /sbin/service zookeeper stop >/dev/null 2>&1
    /sbin/chkconfig --del zookeeper
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service zookeeper condrestart >/dev/null 2>&1 || :
fi

%changelog
* Thu Oct 10 2019 Vincent Legoll <vincent.legoll@openio.io> - 3.4.13-2
- Disable the ZOOKEEPER-critsects.patch
* Fri Sep 07 2018 Vincent Legoll <vincent.legoll@openio.io> - 3.4.13-1
- Update to 3.4.13
* Mon May 21 2018 Vincent Legoll <vincent.legoll@openio.io> - 3.4.12-2
- Add ZOOKEEPER-critsects.patch for enhanced performance
* Mon May 21 2018 Vincent Legoll <vincent.legoll@openio.io> - 3.4.12-1
- Update to 3.4.12
* Mon Nov 13 2017 Romain Acciari <romain.acciari@openio.io> - 3.4.11-1
- Update to 3.4.11
* Tue Oct 24 2017 Romain Acciari <romain.acciari@openio.io> - 3.4.10-1
- Update to 3.4.10
* Wed Dec 28 2016 Romain Acciari <romain.acciari@openio.io> - 3.4.9-1
- Update to 3.4.9
- Add patch ZK#2044
* Wed Mar 16 2016 Romain Acciari <romain.acciari@openio.io> - 3.4.8-1
- Initial release
