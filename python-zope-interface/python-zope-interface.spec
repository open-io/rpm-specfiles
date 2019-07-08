# Filter private shared library provides
%filter_provides_in %{python_sitearch}/zope/interface/.*\.so$
%filter_setup

%if 0%{?fedora} > 12
%global with_python3 1
%{!?py3ver: %global py3ver %(%{?__python3} -c 'import sys; print(sys.version[0:3])' 2>/dev/null)}
%endif


Name:		python-zope-interface
Version:	4.0.5
Release:	4%{?dist}
Summary:	Zope 3 Interface Infrastructure
Group:		Development/Libraries
License:	ZPLv2.1
URL:		http://pypi.python.org/pypi/zope.interface
Source0:	https://pypi.python.org/packages/source/z/zope.interface/zope.interface-%{version}.zip
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python-nose
# since F14
Obsoletes:	python-zope-filesystem <= 1-8

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
%endif

%description
Interfaces are a mechanism for labeling objects as conforming to a given API
or contract.

This is a separate distribution of the zope.interface package used in Zope 3.

%if 0%{?with_python3}
%package -n python3-zope-interface
Summary:	Zope 3 Interface Infrastructure
Group:		Development/Libraries

%description -n python3-zope-interface
Interfaces are a mechanism for labeling objects as conforming to a given API
or contract.

This is a separate distribution of the zope.interface package used in Zope 3.
%endif

%prep
%setup -n zope.interface-%{version} -q

rm -rf %{modname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif


%install
# python3 block
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# Will put docs in %%{_docdir} instead
%{__rm} -f %{buildroot}%{python3_sitearch}/zope/interface/{,tests/}*.txt

# C files don't need to be packaged
%{__rm} -f %{buildroot}%{python3_sitearch}/zope/interface/_zope_interface_coptimizations.c
popd
%endif

# do it again for python2
%{__python} setup.py install -O1 --skip-build --root  %{buildroot}

# Will put docs in %%{_docdir} instead
%{__rm} -f %{buildroot}%{python_sitearch}/zope/interface/{,tests/}*.txt

# C files don't need to be packaged
%{__rm} -f %{buildroot}%{python_sitearch}/zope/interface/_zope_interface_coptimizations.c

%check
PYTHONPATH=$(pwd) nosetests

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd) nosetests-%{py3ver}
popd
%endif

%files
%defattr(-,root,root,-)
%doc README.rst LICENSE.txt CHANGES.rst COPYRIGHT.txt docs/
%{python_sitearch}/zope/interface/
# Co-own %%{python_sitearch}/zope/
%dir %{python_sitearch}/zope/
%exclude %{python_sitearch}/zope/interface/tests/
%exclude %{python_sitearch}/zope/interface/common/tests/
%{python_sitearch}/zope.interface-*.egg-info
%{python_sitearch}/zope.interface-*-nspkg.pth

%if 0%{?with_python3}
%files -n python3-zope-interface
%doc README.rst LICENSE.txt CHANGES.rst COPYRIGHT.txt docs/
%{python3_sitearch}/zope/interface/
# Co-own %%{python3_sitearch}/zope/
%dir %{python3_sitearch}/zope/
%exclude %{python3_sitearch}/zope/interface/tests/
%exclude %{python3_sitearch}/zope/interface/common/tests/
%{python3_sitearch}/zope.interface-*.egg-info
%{python3_sitearch}/zope.interface-*-nspkg.pth
%endif

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.0.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.0.5-3
- Mass rebuild 2013-12-27

* Fri May 17 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 4.0.5-2
- Remove the python-zope-event soft dependency.

* Thu Apr 11 2013 Luke Macken <lmacken@redhat.com> - 4.0.5-1
- Update to 4.0.5 (#891046)
- Run the unit tests with nose

* Tue Mar 26 2013 David Malcolm <dmalcolm@redhat.com> - 4.0.4-2
- remove rhel clause from python3 guard

* Mon Feb 25 2013 Ralph Bean <rbean@redhat.com> - 4.0.4-1
- Latest upstream
- README and CHANGES moved from .txt to .rst.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Ralph Bean <rbean@redhat.com> - 4.0.2-4
- Wrap files section in a python3 conditional.

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 4.0.2-3
- Typofix to python-zope-event requirement.

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 4.0.2-2
- Added dependency on python-zope-event.

* Wed Nov 28 2012 Ralph Bean <rbean@redhat.com> - 4.0.2-1
- Latest upstream release.
- Python3 subpackage.
- Rearrange the way we package docs.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan  7 2012 Robin Lee <cheeselee@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0 (ZTK 1.1.3)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct  4 2010 Robin Lee <cheeselee@fedoraproject.org> - 3.6.1-7
- Obsoletes python-zope-filesystem

* Wed Sep 29 2010 jkeating - 3.6.1-6
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-5
- Move the texts files to %%doc
- Exclude the tests from installation
- Filter private shared library provides

* Wed Sep 15 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-4
- Run the test suite
- Don't move the text files

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-3
- Remove python-zope-filesystem from requirements
- Own %%{python_sitearch}/zope/
- BR: python-setuptools-devel renamed to python-setuptools
- Spec cleaned up

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 22 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-1
- update to 3.6.1
- License provided in the source package
- include the tests

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.2-1
- update to 3.5.2

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> 3.5.1-3
- Add python-setuptools-devel to the BuildRequires, so we generate egg-info

* Sun Apr 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.1-2
- use correct source filename (upstream switched from zip to tar.gz)

* Sun Apr 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.1-1
- update to 3.5.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.5.0-3
- Make compatible with the new python-zope-filesystem.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.5.0-2
- Rebuild for Python 2.6

* Sat Nov 15 2008 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.0-1
- update to 3.5.0

* Mon Mar 31 2008 Paul Howarth <paul@city-fan.org> 3.4.1-1
- update to 3.4.1
- incorporate suggestions from Felix Schwarz:
  - new summary and description
  - new upstream URL (old one out of date)
  - don't package test files
  - include more documentation

* Mon Mar 31 2008 Paul Howarth <paul@city-fan.org> 3.3.0-1
- update to 3.3.0
- update source URL to include versioned directory and new tarball name
- drop the gcc 4.x compatibility patch, no longer needed
- don't run the test suite as it now depends on zope.testing
- exclude _zope_interface_coptimizations.c source from the binary package

* Thu Feb 14 2008 Paul Howarth <paul@city-fan.org> 3.0.1-10
- rebuild with gcc 4.3.0 for Fedora 9

* Fri Jan  4 2008 Paul Howarth <paul@city-fan.org> 3.0.1-9
- tweak %%files list to pull in egg info file when necessary
- fix permissions on shared objects (silence rpmlint)

* Wed Aug 29 2007 Paul Howarth <paul@city-fan.org> 3.0.1-8
- update license tag to ZPLv2.1 in anticipation of this tag being approved

* Sat Dec  9 2006 Paul Howarth <paul@city-fan.org> 3.0.1-7
- rebuild against python 2.5 for Rawhide

* Tue Oct 31 2006 Paul Howarth <paul@city-fan.org> 3.0.1-6
- add %%check section

* Wed Sep 20 2006 Paul Howarth <paul@city-fan.org> 3.0.1-5
- dispense with %%{pybasever} macro and python-abi dependency, not needed from
  FC4 onwards
- include ZPL 2.1 license text
- add reference in %%description to origin of patch
- change License: tag from "ZPL 2.1" to "Zope Public License" to shut rpmlint up

* Thu Aug 31 2006 Paul Howarth <paul@city-fan.org> 3.0.1-4
- files list simplified as .pyo files are no longer %%ghost-ed

* Tue May  9 2006 Paul Howarth <paul@city-fan.org> 3.0.1-3
- import from PyVault Repository
- rewrite in Fedora Extras style

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 3.0.1-2
- add bug fix for gcc 4

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 3.0.1-1
- new rpm

