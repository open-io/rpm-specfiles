%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define tarname oio-swift

Name:           openio-sds-swift
Version:        0.2
Release:        1%{?dist}
Summary:        Swift Gateway for OpenIO SDS

License:        Apache License v2
URL:            http://www.openio.io/
Source0:        https://github.com/open-io/oio-swift/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:	python-oiopy >= 0.3
Requires:	openstack-swift-proxy


%description
Swift Gateway for OpenIO SDS.

%prep
%setup -q -n %{tarname}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*


%changelog
* Thu Apr 23 2015 Romain Acciari <romain.acciari@openio.io>
- New release
- OpenStack Swift dependency
- License changed to Apache License v2
* Fri Mar 13 2015 Julien Kasarherou <julien.kasarherou@openio.io>
- Initial release
