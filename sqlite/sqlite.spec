%define realver 3320200
%define rpmver 3.32.2

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{rpmver}
Release: 2%{?dist}
License: Public Domain
Group: Applications/Databases
URL: http://www.sqlite.org/
Source0: https://www.sqlite.org/2020/sqlite-autoconf-%{realver}.tar.gz

BuildRequires: ncurses-devel readline-devel glibc-devel
BuildRequires: autoconf
BuildRoot: %{_tmppath}/%{name}-root

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package analyzer
Summary: Additional tools for the sqlite3 embeddable SQL database engine
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description analyzer
This package contains the sqlite3_analyzer tool: read an SQLite database
file and analyze its space utilization.

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation 
for %{name}. If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%prep
%setup -q -n %{name}-autoconf-%{realver}
autoconf # Rerun with new autoconf to add support for aarm64

%build
export CFLAGS="$RPM_OPT_FLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -Wall -fno-strict-aliasing"
%configure --disable-tcl \
           --enable-threadsafe \
           --enable-threads-override-locks \
           --enable-load-extension

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
make %{?_smp_mflags} sqlite3_analyzer

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1
install -m0755 sqlite3_analyzer $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/sqlite3
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files analyzer
%defattr(-, root, root)
%{_bindir}/sqlite3_analyzer

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Dec 1 2020 - Florent Vennetier <florent.vennetier@ovhcloud.com> 3.32.2-2
- create a subpackage for sqlite3_analyzer
* Wed Jun 10 2020 - Jerome Loyet <jerome@openio.io> 3.32.2-1
- update
