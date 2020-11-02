%global         modname greenlet

Name:           python-%{modname}
Version:        0.4.16
Release:        1%{?dist}
Summary:        Lightweight in-process concurrent programming
License:        MIT
URL:            https://github.com/python-greenlet/greenlet
Source0:        %{pypi_source %{modname}}
BuildRequires:  gcc-c++

%global _description \
The greenlet package is a spin-off of Stackless, a version of CPython\
that supports micro-threads called "tasklets". Tasklets run\
pseudo-concurrently (typically in a single or a few OS-level threads)\
and are synchronized with data exchanges on "channels".

%description %{_description}

%package -n     python2-%{modname}
Summary:        %{summary}
Provides:       python2-%{modname}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description -n python2-%{modname} %{_description}

Python 2 version.

%package -n     python3-%{modname}
Summary:        %{summary}
Provides:       python3-%{modname}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{modname} %{_description}

Python 3 version.

%package -n     python2-%{modname}-devel
Summary:        C development headers for python2-%{modname}
Provides:       python2-%{modname}-devel
Requires:       python2-%{modname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python2-%{modname}-devel
%{summary}.

Python 2 version.

%package -n     python3-%{modname}-devel
Summary:        C development headers for python3-%{modname}
Provides:       python3-%{modname}-devel
Requires:       python3-%{modname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{modname}-devel
%{summary}.

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -p1

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install
 
%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{modname}
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%{python2_sitearch}/%{modname}-*.egg-info
%{python2_sitearch}/%{modname}.so

%files -n python2-%{modname}-devel
%{_includedir}/python%{python2_version}*/%{modname}/

%files -n python3-%{modname}
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%{python3_sitearch}/%{modname}-*.egg-info
%{python3_sitearch}/%{modname}*.so

%files -n python3-greenlet-devel
%{_includedir}/python%{python3_version}*/%{modname}/

%changelog
* Fri Jul 17 2020 Vincent Legoll <vincent.legoll@openio.io> - 0.4.16-1
- New version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Kevin Fenzi <kevin@scrye.com> - 0.4.14-1
- Update to 0.4.14.
- Drop upstreamed/no longer needed patches.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.13-4
- Add fix for Python 3.7

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.13-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.13-1
- Update to 0.4.13

* Fri Jan 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.12-1
- Update to 0.4.12

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.11-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Kevin Fenzi <kevin@scrye.com> - 0.4.11-1
- Update to 0.4.11. Fixes bug #1403514

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9
- Use %license macro
- Follow new RPM Packaging guidelines
- Cleanups in spec

* Fri Aug 21 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-2
- Re-enable tests on secondary arches. Fixes #1252899
- Applied patch to build on ppc64le. Fixes #1252900

* Fri Jun 26 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-1
- Update to 0.4.7. Fixes bug #1235896

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 29 2015 Terje Røsten <terje.rosten@ntnu.no> - 0.4.5-1
- 0.4.5
- Add python3 subpackage
- Ship license files
- Some spec clean ups
- Update fixes FTBFS issue (bz#1106779)
- Add comment about issues on ppc64, s390 & s390x

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Orion Poplawski <orion@cora.nwra.com> 0.4.2-1
- Update to 0.4.2

* Mon Aug 05 2013 Kevin Fenzi <kevin@scrye.com> 0.4.1-1
- Update to 0.4.1
- Fix FTBFS bug #993134

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Pádraig Brady <P@draigBrady.com> - 0.4.0-1
- Update to 0.4.0

* Thu Oct 11 2012 Pádraig Brady <P@draigBrady.com> - 0.3.1-11
- Add support for ppc64

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Dan Horák <dan[at]danny.cz> - 0.3.1-8
- disable tests also for s390(x)

* Thu Nov 17 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-7
- Fix %%check quoting in the previous comment which when
  left with a single percent sign, pulled in "unset DISPLAY\n"
  into the changelog

* Mon Oct 24 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-6
- cherrypick 25bf29f4d3b7 from upstream (rhbz#746771)
- exclude the %%check from ppc where the tests segfault

* Wed Oct 19 2011 David Malcolm <dmalcolm@redhat.com> - 0.3.1-5
- add a %%check section
- cherrypick 2d5b17472757 from upstream (rhbz#746771)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-2
- Splitted headers into a -devel package.

* Fri Apr 09 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-1
- Initial package version.
