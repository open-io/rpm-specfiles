#%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           openio-sds-swift-plugin-swift3
License:        ASL 2.0
Summary:        The swift3 plugin for OpenIO SDS Swift

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.12.3
Release:        1%{?dist}
URL:            https://github.com/open-io/swift3
Source0:        https://github.com/open-io/swift3/archive/%{version}-openio.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
URL:            https://github.com/open-io/swift3
Source0:        https://github.com/open-io/swift3/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       openstack-swift >= 2.1.0
Requires:       python-lxml
Requires:       python-requests
Requires:       python-redis

%description
The swift3 plugin permits accessing OpenIO Swift via the
Amazon S3 API.

%prep
%if %{?_with_test:0}%{!?_with_test:1}
%setup -q -n swift3-%{version}-openio
%else
# Testing purpose only. Do not modify.
%setup -q -n swift3-%{tarversion}
%endif

%build
PBR_VERSION=1.12.0 %{__python2} setup.py build

%install
rm -rf %{buildroot}
PBR_VERSION=1.12.0 %{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/swift3-*.egg-info/
%{python2_sitelib}/swift3/
%doc AUTHORS README.md

%changelog
* Tue May 15 2018 - 1.12.3-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Apr 18 2018 - 1.12.2-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Mar 08 2018 Romain Acciari <romain.acciari@openio.io> - 1.12.1-0
- New release
* Thu Feb 1 2018 Sebastien Lapierre <sebastien.lapierre@openio.io> - 1.12.0-1
- Add Unstable packaging 
* Thu Aug 3 2017 Sebastien Lapierre <sebastien.lapierre@openio.io> - 1.12.0-1
- Fix  BucketAlreadyExists error
* Tue Jun 27 2017 Romain Acciari <romain.acciari@openio.io> - 1.12.0-0
- New release
* Wed Sep 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.11.0-1
- Upstream 1.11.0

