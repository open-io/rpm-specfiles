%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define tarname  oio-diag

Name:           openio-diag

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.0.b1
Release:        1%{?dist}
%define         tarversion %{version}
Source0:        https://github.com/open-io/oio-diag/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         targetversion 4.0.0
Source0:        https://github.com/open-io/oio-diag/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        OpenIO diagnostic CLI tool
License:        AGPL
URL:            http://www.openio.io/
BuildRequires:  python-setuptools
Requires:       openio-sds-server
Requires:       python             >= 2.7
Requires:       python-simplejson  >= 2.0.9


%description
Here we are!


%prep
%setup -q -n %{tarname}-%{tarversion}


%build
# Build python
%if %{?_with_test:0}%{!?_with_test:1}
PBR_VERSION=%{version} %{__python} setup.py build
%else
PBR_VERSION=%{targetversion} %{__python} setup.py build
%endif


%install
# Install python
%if %{?_with_test:0}%{!?_with_test:1}
PBR_VERSION=%{version} %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%else
PBR_VERSION=%{targetversion} %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%endif
%if %{?suse_version}0
%fdupes %{buildroot}%{python_sitelib}
%endif


%files
%defattr(755,root,root,755)
%{_bindir}/oio-diag
%defattr(644,root,root,755)
%{python_sitelib}/oio*


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%changelog
* Fri Sep 22 2017 - 1.0.0.b1-1 - Jean-Francois Smigielski <jf.smigielski@gmail.com>
- Initial release
