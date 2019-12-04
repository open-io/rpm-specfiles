%global pypi_name pyperclip

%global with_python3 1

Name:           python-%{pypi_name}
Version:        1.6.4
Release:        1%{?dist}
Summary:        A cross-platform clipboard module for Python

License:        BSD
URL:            https://github.com/asweigart/pyperclip
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Fix tests suite execution
# Disable all tests requiring a display or toolkit to be available at build time
Patch001:       0001-Skip-tests-irrelevant-in-the-context-of-Fedora-packa.patch
BuildArch:      noarch

BuildRequires:  git
 
%description
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
#%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description -n python2-%{pypi_name}
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.


%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
#%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.
%endif


%package -n python-%{pypi_name}-doc
Summary:        Pyperclip documentation
BuildRequires:  python2-sphinx

%description -n python-%{pypi_name}-doc
Documentation for pyperclip


%prep
%autosetup -n %{pypi_name}-%{version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Fix ends of line encoding
sed -i 's/\r$//' README.md docs/*

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs 
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
%endif
%{__python2} setup.py test


%files -n python2-%{pypi_name}
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html

%changelog
* Wed Jul 25 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.6.4-1
- Initial package.
