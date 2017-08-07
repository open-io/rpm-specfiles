#%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           openio-sds-swift-plugin-swift3
Version:        1.12.0.b1
Release:        1%{?dist}
Summary:        The swift3 plugin for OpenIO SDS Swift

License:        ASL 2.0
URL:            https://github.com/open-io/swift3
Source0:        https://github.com/open-io/swift3/archive/%{version}-openio.tar.gz

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
%setup -q -n swift3-%{version}-openio

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
* Tue Aug 3 2017 Sebastien Lapierre <sebastien.lapierre@openio.io> - 1.12.0-1
- Fix  BucketAlreadyExists error
* Tue Jun 27 2017 Romain Acciari <romain.acciari@openio.io> - 1.12.0-0
- New release
* Wed Sep 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.11.0-1
- Upstream 1.11.0

