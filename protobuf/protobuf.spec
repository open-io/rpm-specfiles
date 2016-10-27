# Build -python subpackage
%bcond_without python
# Build -java subpackage for fedora
%if 0%{?fedora}
%bcond_without java
%else
%bcond_with java
%endif
# Don't require gtest
%bcond_with gtest

%global emacs_version %(pkg-config emacs --modversion)
%global emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%global emacs_startdir %(pkg-config emacs --variable sitestartdir)

Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
Version:        3.0.2
Release:        1%{?dist}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/google/protobuf/archive/v%{version}.tar.gz
Source1:        ftdetect-proto.vim
Source2:        protobuf-init.el
Patch0:         protobuf-2.5.0-emacs-24.4.patch
Patch1:         protobuf-2.5.0-fedora-gtest.patch
URL:            https://github.com/google/protobuf
BuildRequires:  automake autoconf libtool pkgconfig zlib-devel
BuildRequires:  emacs(bin)
BuildRequires:  emacs-el >= 24.1
BuildRequires:  gmock-devel
%if %{with gtest}
BuildRequires:  gtest-devel
%endif
%if %{with java}
BuildRequires:  mvn(org.easymock:easymock)
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary: Protocol Buffers C++ headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%package lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary: Protocol Buffers LITE_RUNTIME development libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with python}
%package python
Summary: Python bindings for Google Protocol Buffers
Group: Development/Languages
BuildRequires: python-devel
BuildRequires: python-setuptools
# For tests
BuildRequires: python-google-apputils
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description python
This package contains Python libraries for Google Protocol Buffers
%endif

%package vim
Summary: Vim syntax highlighting for Google Protocol Buffers descriptions
Group: Development/Libraries
Requires: vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor

%package emacs
Summary: Emacs mode for Google Protocol Buffers descriptions
Group: Applications/Editors
Requires: emacs(bin) >= 0%{emacs_version}

%description emacs
This package contains syntax highlighting for Google Protocol Buffers
descriptions in the Emacs editor.

%package emacs-el
Summary: Elisp source files for Google protobuf Emacs mode
Group: Applications/Editors
Requires: protobuf-emacs = %{version}

%description emacs-el
This package contains the elisp source files for %{pkgname}-emacs
under GNU Emacs. You do not need to install this package to use
%{pkgname}-emacs.


%if %{with java}
%package java
Summary: Java Protocol Buffers runtime library
Group:   Development/Languages
BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.apache.maven.plugins:maven-antrun-plugin)
Conflicts:        %{name}-compiler > %{version}
Conflicts:        %{name}-compiler < %{version}

%description java
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}-java
Group:   Documentation
Requires: %{name}-java = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}-java.

%endif

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .emacs
%if %{with gtest}
rm -rf gtest
%patch1 -p1 -b .gtest
%endif
chmod 644 examples/*
%if %{with java}
%pom_remove_parent java/pom.xml
%pom_remove_dep org.easymock:easymockclassextension java/pom.xml
rm -rf java/src/test
%endif

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
#./autogen.sh
autoreconf -f -i -Wall,no-obsolete
%configure

make %{?_smp_mflags}

%if %{with python}
pushd python
python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with java}
pushd java
%mvn_file : %{name}
%mvn_build
popd
%endif

emacs -batch -f batch-byte-compile editors/protobuf-mode.el

%check
# Tets is segfaulting on arm
# https://github.com/google/protobuf/issues/298
#%ifnarch %{arm}
#make %{?_smp_mflags} check
#%else
#make %{?_smp_mflags} check || :
#%endif

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;

%if %{with python}
pushd python
python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
pushd java
%mvn_install
popd
%endif

mkdir -p $RPM_BUILD_ROOT%{emacs_lispdir}
mkdir -p $RPM_BUILD_ROOT%{emacs_startdir}
install -p -m 0644 editors/protobuf-mode.el $RPM_BUILD_ROOT%{emacs_lispdir}
install -p -m 0644 editors/protobuf-mode.elc $RPM_BUILD_ROOT%{emacs_lispdir}
install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{emacs_startdir}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%files
%{_libdir}/libprotobuf.so.*
%doc CHANGES.txt CONTRIBUTORS.txt README.md
%license LICENSE

%files compiler
%{_bindir}/protoc
%{_libdir}/libprotoc.so.*
%doc README.md
%license LICENSE

%files devel
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files static
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files lite
%{_libdir}/libprotobuf-lite.so.*

%files lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files lite-static
%{_libdir}/libprotobuf-lite.a

%if %{with python}
%files python
%dir %{python_sitelib}/google
%{python_sitelib}/google/protobuf/
%{python_sitelib}/protobuf-*-py2.?.egg-info/
%{python_sitelib}/protobuf-*-py2.?-nspkg.pth
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files vim
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%files emacs
%{emacs_startdir}/protobuf-init.el
%{emacs_lispdir}/protobuf-mode.elc

%files emacs-el
%{emacs_lispdir}/protobuf-mode.el

%if %{with java}
%files java -f java/.mfiles
%doc examples/AddPerson.java examples/ListPeople.java

%files javadoc -f java/.mfiles-javadoc
%endif

%changelog
* Thu Oct 20 2016 Romain Acciari <romain.acciari@openio.io> - 3.0.2-1
- Update to 3.0.2 stable release

* Tue Sep 06 2016 Romain Acciari <romain.acciari@openio.io> - 3.0.0-1
- Update to 3.0.0 stable release

* Fri Dec 18 2015 Romain Acciari <romain.acciari@openio.io> - 3.0.0_beta_2-1
- Update to 3.0.0-beta-2

* Fri Dec 18 2015 Romain Acciari <romain.acciari@openio.io> - 3.0.0_beta1_1-1
- Update to 3.0.0-beta1-1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-1
- Update to 2.6.1
- New URL
- Cleanup spec
- Add patch to fix emacs compilation with emacs 24.4
- Drop java-fixes patch, use pom macros instead
- Add BR on python-google-apputils and mvn(org.easymock:easymock)
- Run make check
- Make -static require -devel (bug #1067475)

* Thu Mar 26 2015 Kalev Lember <kalevlember@gmail.com> - 2.6.0-4
- Rebuilt for GCC 5 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.6.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 17 2014 Peter Lemenkov <lemenkov@gmail.com> - 2.6.0-2
- Added missing Requires zlib-devel to protobuf-devel (see rhbz #1173343). See
  also rhbz #732087.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.6.0-1
- Bump to upstream release 2.6.0 (rh# 1154474).
- Rebase 'java fixes' patch on 2.6.0 pom.xml.
- Drop patch #3 (fall back to generic GCC atomics if no specialized atomics
  exist, e.g. AArch64 GCC); this has been upstreamed.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-11
- protobuf-emacs requires emacs(bin), not emacs (rh# 1154456)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-9
- Update to current Java packaging guidelines

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-7
- Use Requires: java-headless rebuild (#1067528)

* Thu Dec 12 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-6
- BR python-setuptools-devel -> python-setuptools

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Dan Horák <dan[at]danny.cz> - 2.5.0-4
- export the new generic atomics header (rh #926374)

* Mon May 6 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-3
- Add support for generic gcc atomic operations (rh #926374)

* Sat Apr 27 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-2
- Remove changelog history from before 2010
- This spec already runs autoreconf -fi during %%build, but bump build for
  rhbz #926374

* Sat Mar 9 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-1
- Bump to latest upstream (#883822)
- Rebase gtest, maven patches on 2.5.0

* Tue Feb 26 2013 Conrad Meyer <cemeyer@uw.edu> - 2.4.1-12
- Nuke BR on maven-doxia, maven-doxia-sitetools (#915620)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jan 20 2013 Conrad Meyer <konrad@tylerc.org> - 2.4.1-9
- Fix packaging bug, -emacs-el subpackage should depend on -emacs subpackage of
  the same version (%%version), not the emacs version number...

* Thu Jan 17 2013 Tim Niemueller <tim@niemueller.de> - 2.4.1-8
- Added sub-package for Emacs editing mode

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-6
- disable test-suite until g++ 4.7 issues are resolved

* Mon Mar 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.1-5
- Update to latest java packaging guidelines

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.4.1-2
- Adding zlib-devel as BR (rhbz: #732087)

* Thu Jun 09 2011 BJ Dierkes <wdierkes@rackspace.com> - 2.4.1-1
- Latest sources from upstream.
- Rewrote Patch2 as protobuf-2.4.1-java-fixes.patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-6
- Fix java subpackage bugs #669345 and #669346
- Use new maven plugin names
- Use mavenpomdir macro for pom installation

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-5
- generalize hardcoded reference to 2.6 in python subpackage %%files manifest

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 James Laska <jlaska@redhat.com> - 2.3.0-3
- Correct use of %bcond macros

* Wed Jul 14 2010 James Laska <jlaska@redhat.com> - 2.3.0-2
- Enable python and java sub-packages

* Tue May 4 2010 Conrad Meyer <konrad@tylerc.org> - 2.3.0-1
- bump to 2.3.0
