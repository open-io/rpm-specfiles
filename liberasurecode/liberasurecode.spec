Name:           liberasurecode
Version:        1.6.1
Release:        1%{?dist}
Summary:        Erasure Code API library written in C with pluggable backends

# Main license is a 2-clause BSD with clause numbers removed for some reason.
License:        BSD and CRC32
URL:            https://bitbucket.org/tsg-/liberasurecode/
Source0:        https://github.com/openstack/liberasurecode/archive/%{version}.tar.gz
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
BuildRequires:  zlib-devel

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
%configure --disable-static --disable-mmi
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}

%check
true

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_datadir}/doc -type f -exec chmod a-x {} ';'

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

# N.B. We place .so to the main package because PyECLib insists on it.
%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_libdir}/*.so
%{_libdir}/*.so.*

%files doc
%{_datadir}/doc/liberasurecode/html/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/erasurecode-1.pc


%changelog
* Thu Jul 16 2020 Vincent Legoll <vincent.legoll@openio.io> - 1.6.1-1
- New version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Pete Zaitcev <zaitcev@redhat.com> 1.6.0-3
- Hush warnings that prevent building with our "warning-is-error" settings
- Fix liberasurecode_crc32_alt on s390x

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 21 2018 Pete Zaitcev <zaitcev@redhat.com> 1.6.0-1
- Upstream 1.6.0

* Tue Sep 11 2018 Pete Zaitcev <zaitcev@redhat.com> 1.5.0-8
- Ensure that we're using the correct checksum
- Get tests pass on s390x (a big-endian arch)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Pete Zaitcev <zaitcev@redhat.com> 1.5.0-4
- Stop using -p in scrptlets, it's dangerous (#1532872)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Pete Zaitcev <zaitcev@redhat.com> 1.5.0-1
- Upstream 1.5.0: --disable-mmi is included upstream

* Thu May 25 2017 Pete Zaitcev <zaitcev@redhat.com> 1.4.0-3
- Disable unportable optimizations, avoid crash with SIGILL (#1454543)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Pete Zaitcev <zaitcev@redhat.com> 1.4.0-1
- Upstream 1.4.0: add isa_l_rs_cauchy

* Thu Oct 20 2016 Pete Zaitcev <zaitcev@redhat.com> 1.2.0-2
- Relocate the .so from -devel to the main package, sigh (#1331977)

* Wed Oct 19 2016 Pete Zaitcev <zaitcev@redhat.com> 1.2.0-1
- Upstream 1.2.0: compatible with PyECLib 1.3.1

* Thu Mar 03 2016 Pete Zaitcev <zaitcev@redhat.com> 1.1.1-1
- Upstream 1.1.1: bugfixes for header locations and a segfault

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
