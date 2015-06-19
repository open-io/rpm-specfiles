%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define tarname oiopy

Name:           python-oiopy
Version:        0.3
Release:        2%{?dist}
Summary:        Python API for OpenIO SDS

License:        LGPL v3
URL:            http://www.openio.io/
Source0:        https://github.com/open-io/oiopy/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       python-eventlet >= 0.15.2
Requires:	python-urllib3

Obsoletes:	python-openio-sds-client

%description
Python API for OpenIO SDS

%prep
%setup -q -n %{tarname}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*


%changelog
* Thu Apr 23 2015 0.3-2 Romain Acciari <romain.acciari@openio.io>
- Package renamed
* Mon Apr 20 2015 0.3-1 Romain Acciari <romain.acciari@openio.io>
- Jka proxyd pool
* Fri Apr 10 2015 0.2-1 Romain Acciari <romain.acciari@openio.io>
- New release to fit with OpenIO SDS 0.3
* Fri Feb 13 2015 0.1-1 Julien Kasarherou <julien.kasarherou@openio.io>
- Initial release
