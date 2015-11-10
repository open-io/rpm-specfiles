%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define tarname oiopy

Name:           python-oiopy

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.5.3
Release:        1%{?dist}
%define         tarversion %{version}
Source0:        https://pypi.python.org/packages/source/o/oiopy/oiopy-%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
Version:        test%{date}.%{tag}
Release:        0%{?dist}
%define         tarversion %{tag}
Source0:        https://github.com/open-io/oiopy/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Python API for OpenIO SDS
License:        LGPLv3
URL:            http://www.openio.io/

BuildArch:      noarch
BuildRequires:  python-setuptools
#BuildRequires:  python-pbr
Requires:       python-eventlet >= 0.15.2
Requires:       python-requests
Requires:       python-cliff-tablib
Requires:       python-cliff >= 1.13
Requires:	python-tablib
Requires:	python-pbr >= 0.11
#Requires:       python-pbr

Obsoletes:	python-openio-sds-client

%description
Python API for OpenIO SDS

%prep
%setup -q -n %{tarname}-%{tarversion}


%build


%install
rm -rf $RPM_BUILD_ROOT
%if %{?_with_test:0}%{!?_with_test:1}
%{__python} setup.py install --root $RPM_BUILD_ROOT
%else
PBR_VERSION=0.5.2 %{__python} setup.py install --root $RPM_BUILD_ROOT
%endif

%files
%{_bindir}/*
%{python_sitelib}/*


%changelog
* Wed Sep 16 2015 Romain Acciari <romain.acciari@openio.io> - 0.5.3-1%{?dist}
- New release
* Mon Sep 14 2015 Romain Acciari <romain.acciari@openio.io> - 0.5.2-1%{?dist}
- New release
* Thu Sep 03 2015 Romain Acciari <romain.acciari@openio.io> - 0.5.1-2%{?dist}
- Update dependencies
* Wed Sep 02 2015 Romain Acciari <romain.acciari@openio.io> - 0.5.1-1%{?dist}
- New release
* Fri Aug 28 2015 Romain Acciari <romain.acciari@openio.io> - 0.5.0-1%{?dist}
- New release
* Mon Jun 29 2015 Romain Acciari <romain.acciari@openio.io> - 0.4.0-1%{?dist}
- Account support
* Thu Apr 23 2015 Romain Acciari <romain.acciari@openio.io> - 0.3-2%{?dist}
- Package renamed
* Mon Apr 20 2015 Romain Acciari <romain.acciari@openio.io> - 0.3-1%{?dist}
- Jka proxyd pool
* Fri Apr 10 2015 Romain Acciari <romain.acciari@openio.io> - 0.2-1%{?dist}
- New release to fit with OpenIO SDS 0.3
* Fri Feb 13 2015 Julien Kasarherou <julien.kasarherou@openio.io> - 0.1-1%{?dist}
- Initial release
