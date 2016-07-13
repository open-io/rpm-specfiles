Name:           liberasurecode
Version:        1.1.0
Release:        2%{?dist}
Summary:        Erasure Code API library written in C with pluggable backends

# Main license is a 2-clause BSD with clause numbers removed for some reason.
License:        BSD and CRC32
URL:            https://bitbucket.org/tsg-/liberasurecode/
# Bitbucket's web export naming is like the old github (== awful), so we pull
# the tag using git CLI. Save the current command for Source0 below.
#  git archive -o ../liberasurecode-1.1.0.tar.gz --prefix=liberasurecode-1.1.0/ v1.1.0
Source0:        %{name}-%{version}.tar.gz
Patch2:         liberasurecode-1.0.5-docs.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  doxygen
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  sed

%description
An API library for Erasure Code, written in C. It provides a number
of pluggable backends, such as Intel ISA-L library.

%package doc
Summary:        Documentation for %{name}

%description doc
The documentation for %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch2 -p1

%build
autoreconf -i -v
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}

%check
make test

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_datadir}/doc -type f -exec chmod a-x {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_libdir}/*.so*

%files doc
%{_datadir}/doc/liberasurecode/html/*

%files devel
%{_includedir}/*


%changelog
* Tue Jul 12 2016 Romain Acciari <romain.acciari@openio.io> 1.1.0-2
- Move .so files into main package

* Fri Oct 23 2015 Pete Zaitcev <zaitcev@redhat.com> 1.1.0-1
- Upstream 1.1.0: better built-in reference implementation
- Enable build-time tests

* Tue Sep 22 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.9-3
- Address final review comments (#1208695)

* Tue Sep 15 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.9-2
- Address review comments (#1208695)

* Fri Sep 11 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.9-1
- Release 1.0.9: true plug-in architecture

* Fri Jul 31 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.8-1
- Release 1.0.8: build and distribution fixes
- Drop the patch for CFLAGS that was merged upstream

* Fri Apr 17 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.7-2
- Add a patch to obey CFLAGS from the build system
- Require doxygen, else -doc package fails to install

* Wed Apr 15 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.7-1
- Release 1.0.7: needed by PyECLib 1.0.7
- Fetch with "git archive": no more tsg--liberasurecode-4e1290ea61e5.tar.bz2
- Drop patch for -ldl that upstream accepted

* Sun Mar 29 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.5-1
- Initial release
