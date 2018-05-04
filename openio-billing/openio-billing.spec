%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define tarname  oio-cb

Name:           openio-billing

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.0
Release:        1%{?dist}
%define         tarversion %{version}
%define         targetversion %{version}
Source0:        https://github.com/open-io/oio-cb/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         targetversion 1.0.0
Source0:        https://github.com/open-io/oio-cb/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        OpenIO Billing service
License:        Proprietary
URL:            http://www.openio.io

BuildRequires:  python-setuptools
Requires:       openio-sds-server
Requires:       python             >= 2.7
Requires:       python-simplejson  >= 2.0.9


%description
OpenIO Billing service


%prep
%if %{?_with_test:0}%{!?_with_test:1}
%setup -q -n open-io-%{tarname}-%{tarversion}
%else
%setup -q -n open-io-%{tarname}-%{tarversion}
%endif


%build
PBR_VERSION=%{targetversion} %{__python} setup.py build


%install
PBR_VERSION=%{targetversion} %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%if %{?suse_version}0
%fdupes %{buildroot}%{python_sitelib}
%endif


%files
%defattr(755,root,root,755)
/usr/bin/oio-billing-server
%defattr(644,root,root,755)
%{python_sitelib}/oio*


%post


%postun


%changelog
* Fri May 04 2018 - 1.0.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- Initial release
