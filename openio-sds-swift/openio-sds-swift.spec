%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           openio-sds-swift

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.0.b3
Release:        0%{?dist}
%define         tarname oioswift
%define         tarversion %{version}
Source0:        https://github.com/open-io/oio-swift/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarname oio-swift
%define         tarversion %{tag}
Source0:        https://github.com/open-io/oio-swift/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Swift proxy for OpenIO SDS
License:        Apache License v2
URL:            http://www.openio.io/

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       openio-sds-common
Requires:       openstack-swift-proxy
Requires:       python-lxml


%description
Swift proxy for OpenIO SDS.

%prep
%setup -q -n oio-swift-%{tarversion}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*


%changelog
* Thu Apr 20 2017 - 0.8.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Mar 09 2017 - 0.8.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 06 2017 - 0.7.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Jan 05 2017 - 0.7.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Oct 20 2016 - 0.6.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Sep 20 2016 - 0.6.0-1 - Romain Acciari <romain.acciari@openio.io>
- Update
* Fri May 13 2016 - 0.5.0-2 - Romain Acciari <romain.acciari@openio.io>
- Add python-lxml require
* Tue Dec 01 2015 - 0.5.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release 0.6.0 for the 15.12 release
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
