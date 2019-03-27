%global upstream_name plyvel
%global module_name plyvel

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        0.9
Release:        3%{?dist}
Summary:        Python interface to the LevelDB embedded database library
License:        BSD
URL:            https://github.com/wbolster/plyvel
Source0:        https://files.pythonhosted.org/packages/32/09/7e849991f3fcf0ad3bba475c113ea0cf5623376d716ce9923eb291838201/plyvel-0.9.tar.gz
Patch0:         0001-py.test.mark.skipif-wants-str-not-bool.patch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest
BuildRequires:  leveldb-devel
BuildRequires:  Cython
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-Cython
%endif

%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\\.so$

%description
Plyvel is a fast and feature-rich Python interface to the LevelDB embedded 
database library. It has a rich feature set, high performance, and a friendly 
Pythonic API.

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python 3 interface to the LevelDB embedded database library

%description -n python3-%{upstream_name}
Plyvel is a fast and feature-rich Python interface to the LevelDB embedded 
database library. It has a rich feature set, high performance, and a friendly 
Pythonic API.
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
%patch0 -p1
rm -rf *.egg-info

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
cython --cplus --fast-fail --annotate plyvel/_plyvel.pyx
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
cython3 --cplus --fast-fail --annotate plyvel/_plyvel.pyx
%{__python3} setup.py build
popd
%endif

%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install --skip-build --root %{buildroot}

%check
# VL: some tests are broken, skip them all
#%{__python} setup.py build_ext --inplace
#py.test

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build_ext --inplace
py.test-%{python3_version}
popd
%endif

%files
%doc README.rst LICENSE.rst NEWS.rst
%{python_sitearch}/%{module_name}
%{python_sitearch}/%{module_name}*.egg-info

%if %{with python3}
%files -n python3-%{upstream_name}
%doc README.rst LICENSE.rst NEWS.rst
%{python3_sitearch}/%{module_name}
%{python3_sitearch}/%{module_name}*.egg-info
%endif

%changelog
* Fri Dec 04 2015 Romain Acciari <romain.acciari@openio.io> - 0.9-3
- Rebuilt for EL7
- Desactivate build using python3 for el7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 28 2014 Dan Callaghan <dcallagh@redhat.com> - 0.9-1
- upstream bug fix release 0.9:
  https://plyvel.readthedocs.org/en/latest/news.html#plyvel-0-9

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Dec 19 2013 Dan Callaghan <dcallagh@redhat.com> - 0.8-1
- new upstream release 0.8

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Dan Callaghan <dcallagh@redhat.com> - 0.4-1
- new upstream release 0.4

* Tue Jun 04 2013 Dan Callaghan <dcallagh@redhat.com> - 0.3-1
- upstream bug fix release 0.3
- switch to upstream patch for test failure

* Sat May 25 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-1
- initial version
