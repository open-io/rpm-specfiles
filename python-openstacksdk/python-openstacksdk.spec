%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

# Disable docs until bs4 package is available
%global with_doc 0

%global pypi_name openstacksdk

%global common_desc \
A collection of libraries for building applications to work with OpenStack \
clouds.

%global common_desc_tests \
A collection of libraries for building applications to work with OpenStack \
clouds - test files

Name:           python-%{pypi_name}
Version:        0.12.0
Release:        1%{?dist}
Summary:        An SDK for building applications to work with OpenStack

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-appdirs
BuildRequires:  python2-requestsexceptions
BuildRequires:  python2-munch
BuildRequires:  python2-jmespath
BuildRequires:  python2-futures
BuildRequires:  python2-jsonschema
BuildRequires:  python2-os-service-types
# Test requirements
BuildRequires:  python2-deprecation
BuildRequires:  python2-iso8601 >= 0.1.11
BuildRequires:  python2-jsonpatch >= 1.6
BuildRequires:  python2-subunit
BuildRequires:  python2-oslotest
BuildRequires:  python2-stestr
BuildRequires:  python2-mock
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-glanceclient
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-requests-mock
BuildRequires:  python2-decorator
BuildRequires:  python2-dogpile-cache
BuildRequires:  python2-ipaddress
BuildRequires:  python2-netifaces
%else
BuildRequires:  python-requests-mock
BuildRequires:  python-decorator
BuildRequires:  python-dogpile-cache
BuildRequires:  python-ipaddress
BuildRequires:  python-netifaces
%endif

Requires:       python2-deprecation
Requires:       python2-jsonpatch >= 1.16
Requires:       python2-keystoneauth1 >= 3.3.0
Requires:       python2-six
Requires:       python2-pbr >= 2.0.0
Requires:       python2-appdirs
Requires:       python2-requestsexceptions >= 1.2.0
Requires:       python2-munch
Requires:       python2-jmespath
Requires:       python2-futures
Requires:       python2-iso8601
Requires:       python2-os-service-types >= 1.1.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-decorator
Requires:       python2-dogpile-cache
Requires:       python2-ipaddress
Requires:       python2-netifaces
Requires:       python2-pyyaml
%else
Requires:       python-decorator
Requires:       python-dogpile-cache
Requires:       python-ipaddress
Requires:       python-netifaces
Requires:       PyYAML
%endif

%description -n python2-%{pypi_name}
%{common_desc}

%package -n python2-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc_tests}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-dogpile-cache
BuildRequires:  python3-appdirs
BuildRequires:  python3-requestsexceptions
BuildRequires:  python3-munch
BuildRequires:  python3-decorator
BuildRequires:  python3-jmespath
BuildRequires:  python3-netifaces
BuildRequires:  python3-jsonschema
BuildRequires:  python3-os-service-types
# Test requirements
BuildRequires:  python3-deprecation
BuildRequires:  python3-iso8601 >= 0.1.11
BuildRequires:  python3-jsonpatch >= 1.6
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-mock
BuildRequires:  python3-requests-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-glanceclient

Requires:       python3-deprecation
Requires:       python3-jsonpatch >= 1.16
Requires:       python3-keystoneauth1 >= 3.3.0
Requires:       python3-six
Requires:       python3-pbr >= 2.0.0
Requires:       python3-PyYAML
Requires:       python3-appdirs
Requires:       python3-requestsexceptions >= 1.2.0
Requires:       python3-dogpile-cache
Requires:       python3-munch
Requires:       python3-decorator
Requires:       python3-jmespath
Requires:       python3-netifaces
Requires:       python3-jsonschema
Requires:       python3-iso8601
Requires:       python3-os-service-types >= 1.1.0

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc_tests}

%endif


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation

%description -n python-%{pypi_name}-doc
A collection of libraries for building applications to work with OpenStack
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the requirements
rm -rf {,test-}requirements.txt

%build
%py2_build

%if 0%{?with_python3}
%{py3_build}
%endif

%if 0%{?with_doc}
# generate html docs 
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py2_install

%if 0%{?with_python3}
%{py3_install}
%endif


#%check
#stestr --test-path ./openstack/tests/unit run
#
#%if 0%{?with_python3}
#rm -rf .testrepository
#stestr-3 --test-path ./openstack/tests/unit run
#%endif


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/openstack-inventory
%{python2_sitelib}/openstack
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/openstack/tests

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/openstack/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/openstack
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/openstack/tests

%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/openstack/tests
%endif

%changelog
* Thu Oct 04 2018 Romain Acciari <romain.acciari@openio.io> 0.12.0-1
- Update to 0.12.0
* Sun Feb 11 2018 RDO <dev@lists.rdoproject.org> 0.11.3-1
- Update to 0.11.3

