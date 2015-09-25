%global pypi_name pbr

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?fedora} > 19
# we don't have the necessary br's, yet
%global do_test 0
%endif

Name:           python-%{pypi_name}
Version:        1.6.0
Release:        1%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        http://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel

%if 0%{?do_test} == 1
BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg
%endif


%if 0%{?rhel}==6
BuildRequires: python-sphinx10
%else
BuildRequires: python-sphinx >= 1.1.3
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
PBR is a library that injects some useful and sensible default behaviors into 
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18 
different projects each with at least 3 active branches, it seems like a good 
time to make that code into a proper re-usable library.

%if 0%{?with_python3}
%package -n python3-pbr
Summary:        Python Build Reasonableness

%description -n python3-pbr
Manage dynamic plugins for Python applications
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
export SKIP_PIP_INSTALL=1
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

# generate html docs 
%if 0%{?rhel}==6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pbr/tests

%if 0%{?do_test} 
%check
%{__python} setup.py test
%endif

%files
%license LICENSE
%doc html README.rst
%{_bindir}/pbr
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{pypi_name}

%if 0%{?with_python3}
%files -n python3-pbr
%license LICENSE
%doc html README.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog
* Mon Aug 31 2015 Matthias Runge <mrunge@redhat.com> - 1.6.0-1
- update to upstream 1.6.0 (rhbz#1249840)

* Sat Aug 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.5.0-1
- Update to upstream 1.5.0

* Wed Jul 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.3.0-1
- Update to upstream 1.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Alan Pevec <apevec@redhat.com> - 0.11.0-1
- update to 0.11.0

* Fri Mar 20 2015 Alan Pevec <apevec@redhat.com> - 0.10.8-1
- update to 0.10.8

* Mon Dec 29 2014 Alan Pevec <apevec@redhat.com> - 0.10.7-1
- update to 0.10.7

* Tue Nov 25 2014 Matthias Runge <mrunge@redhat.com> - 0.10.0-1
- update to 0.10.0 (rhbz#1191232)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 30 2014 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0 (rhbz#1078761)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-2
- Added python3 subpackage.
- slight modification of Ralph Beans proposal

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-1
- update to 0.7.0 (rhbz#1078761)

* Tue Feb 11 2014 Matthias Runge <mrunge@redhat.com> - 0.6.0-1
- update to 0.6.0 (rhbz#1061124)

* Fri Nov 01 2013 Matthias Runge <mrunge@redhat.com> - 0.5.23-1
- update to 0.5.23 (rhbz#1023926)

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-2
- add requirement python-pip (rhbz#996192)
- remove requirements.txt

* Thu Aug 08 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-1
- update to 0.5.21 (rhbz#990008)

* Fri Jul 26 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-2
- remove one buildrequires: python-sphinx

* Mon Jul 22 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-1
- update to python-pbr-0.5.19 (rhbz#983008)

* Mon Jun 24 2013 Matthias Runge <mrunge@redhat.com> - 0.5.17-1
- update to python-pbr-0.5.17 (rhbz#976026)

* Wed Jun 12 2013 Matthias Runge <mrunge@redhat.com> - 0.5.16-1
- update to 0.5.16 (rhbz#973553)

* Tue Jun 11 2013 Matthias Runge <mrunge@redhat.com> - 0.5.14-1
- update to 0.5.14 (rhbz#971736)

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-2
- remove requirement setuptools_git
- fix docs build under rhel

* Fri May 17 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-1
- update to 0.5.11 (rhbz#962132)
- disable tests, as requirements can not be fulfilled right now

* Thu Apr 25 2013 Matthias Runge <mrunge@redhat.com> - 0.5.8-1
- Initial package.
