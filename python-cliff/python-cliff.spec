# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global modname cliff

%global common_desc \
cliff is a framework for building command line programs. It uses setuptools \
entry points to provide subcommands, output formatters, and other \
extensions. \
\
Documentation for cliff is hosted on readthedocs.org at \
http://readthedocs.org/docs/cliff/en/latest/

%global common_desc_tests This package contains tests for the python cliff library.

Name:             python-%{modname}
Version:          3.3.0
Release:          1%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://pypi.io/pypi/cliff
Source0:          https://files.pythonhosted.org/packages/c7/c4/38ea8a52809dd2fd7b6282d21bb17a5f3d13d79df57b53b96dddb41dc2b6/cliff-3.3.0.tar.gz

BuildArch:        noarch

%package -n python%{pyver}-%{modname}
Summary:          Command Line Interface Formulation Framework

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-prettytable
BuildRequires:    python%{pyver}-stevedore
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-pyparsing
# FIXME (jcapitao): As soon as CentOS8 is out, bump version of python-cmd2 to 0.8.3
BuildRequires:    python%{pyver}-cmd2 >= 0.6.7

Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-six
Requires:         python%{pyver}-cmd2 >= 0.6.7
Requires:         python%{pyver}-pyparsing
# Handle python2 exception
%if %{pyver} == 2
Requires:         PyYAML
Requires:         python%{pyver}-unicodecsv
%else
Requires:         python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{modname}
%{common_desc}

%description
%{common_desc}

%prep
%setup -q -n %{modname}-%{upstream_version}
rm -rf {test-,}requirements.txt

# Remove bundled egg info
rm -rf *.egg-info

%build
%{pyver_build}

%install
%{pyver_install}

%files -n python%{pyver}-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{pyver_sitelib}/%{modname}
%{pyver_sitelib}/%{modname}-*.egg-info
%exclude %{pyver_sitelib}/%{modname}/tests


%changelog
* Tue Jul 21 2020 Vincent Legoll <vincent.legoll@openio.io> - 3.3.0-1
- new version

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 2.16.0-2
- Update to upstream version 2.16.0

* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 2.16.0-1
- Update to 2.16.0. Fixes bug #1749959

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.15.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.15.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Kevin Fenzi <kevin@scrye.com> - 2.15.0-1
- Update to 2.15.0. Fixed bug #1686683

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 2.14.1-1
- Update to 2.14.1

