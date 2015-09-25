%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           openio-sds-swift

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.4.1
Release:        1%{?dist}
%define         tarname oioswift
%define         tarversion %{version}
Source0:        https://pypi.python.org/packages/source/o/oioswift/oioswift-%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
Version:        test%{date}.%{tag}
Release:        0%{?dist}
%define         tarname oio-swift
%define         tarversion %{tag}
Source0:        https://github.com/open-io/oio-swift/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Swift Gateway for OpenIO SDS
License:        Apache License v2
URL:            http://www.openio.io/

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:	python-oiopy >= 0.5.2
Requires:	openstack-swift-proxy


%description
Swift Gateway for OpenIO SDS.

%prep
%setup -q -n %{tarname}-%{tarversion}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*


%changelog
* Mon Sep 14 2015 - 0.4.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Sep 04 2015 - 0.4.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Update requires
* Mon Jun 29 2015 - 0.3.0-1 - Romain Acciari <romain.acciari@openio.io>
- account autocreate on account POST
* Mon Jun 29 2015 - 0.3.0-1 - Romain Acciari <romain.acciari@openio.io>
- Account support
* Thu Apr 23 2015 - 0.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- OpenStack Swift dependency
- License changed to Apache License v2
* Fri Mar 13 2015 - 0.1-1 - Julien Kasarherou <julien.kasarherou@openio.io>
- Initial release
