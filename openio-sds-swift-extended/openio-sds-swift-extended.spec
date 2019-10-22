%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           openio-sds-swift-extended

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.9.0
Release:        1%{?dist}
%define         tarversion %{version}
%define         targetversion %{version}
Source0:        https://github.com/open-io/oio-swift-extended/archive/%{tarversion}.tar.gz
%define         tarsubdir oio-swift-extended-%{version}
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         targetversion 0.9.0
Source0:        https://github.com/open-io/oio-swift-extended/archive/%{tarversion}.tar.gz
%define         tarsubdir open-io-oio-swift-extended-%{tag}
Epoch:          1
%endif

Summary:        Swift proxy middlewares for OpenIO SDS
License:        Proprietary
URL:            http://www.openio.io/

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-pbr
Requires:       openio-sds-swift


%description
Swift proxy middlewares for OpenIO SDS.


%prep
%setup -q -n %{tarsubdir}


%build
PBR_VERSION=%{targetversion} %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
PBR_VERSION=%{targetversion} %{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%{python_sitelib}/*


%changelog
* Mon Aug 26 2019 - 0.9.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- Initial release
