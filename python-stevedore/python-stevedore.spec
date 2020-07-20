%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_python3 1

%global common_desc Manage dynamic plugins for Python applications

Name:           python-stevedore
Version:        1.32.0
Release:        1%{?dist}
Summary:        Manage dynamic plugins for Python applications

License:        ASL 2.0
URL:            https://github.com/openstack/stevedore
Source0:        https://tarballs.openstack.org/stevedore/stevedore-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-mock
BuildRequires:  python2-six
BuildRequires:  python2-testrepository
#BuildRequires:  python2-discover
#BuildRequires:  python2-oslotest

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python36-six
%endif

%description
%{common_desc}

%package -n python2-stevedore
Summary:        Manage dynamic plugins for Python applications

Requires:       python2-six
Requires:       python2-pbr

%description -n python2-stevedore
%{common_desc}

%if 0%{?with_python3}
%package -n python3-stevedore
Summary:        Manage dynamic plugins for Python applications

Requires:       python36-six
Requires:       python3-pbr

%description -n python3-stevedore
%{common_desc}
%endif

%prep
%setup -q -n stevedore-%{upstream_version}

# let RPM handle deps
rm -f requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

%check
#TODO: reenable when commented test requirements above are available
#
#PYTHONPATH=. nosetests
#
#%if 0%{?with_python3}
#pushd %{py3dir}
#PYTHONPATH=. nosetests-%{python3_version}
#popd
#%endif

%files -n python2-stevedore
%license LICENSE
%doc README.rst
%{python2_sitelib}/stevedore
%{python2_sitelib}/stevedore-*.egg-info

%if 0%{?with_python3}
%files -n python3-stevedore
%license LICENSE
%doc README.rst
%{python3_sitelib}/stevedore
%{python3_sitelib}/stevedore-*.egg-info
%endif

%changelog
* Mon Jul 20 2020 Vincent Legoll <vincent.legoll@openio.io> - 1.32.0-1
- New version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Feb 09 2018 Alfredo Moralejo <amoralej@redhat.com> 1.28.0-1
- Update to 1.28.0

