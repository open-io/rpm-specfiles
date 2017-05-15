%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:		openstack-swift-plugin-swift3
Version:	1.11.1.dev35
Release:	1%{?dist}
Summary:	The swift3 plugin for Openstack Swift

License:	ASL 2.0
URL:		https://github.com/openstack/swift3
Source0:	https://tarballs.openstack.org/swift3/swift3-%{upstream_version}.tar.gz

Epoch:          1

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	openstack-swift >= 2.1.0
Requires:   python-lxml
Requires:   python-requests

%description
The swift3 plugin permits accessing Openstack Swift via the
Amazon S3 API.

%prep
%setup -q -n swift3-%{upstream_version}

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/swift3-*.egg-info/
%{python2_sitelib}/swift3/
%doc AUTHORS README.md

%changelog
* Fri Mar 17 2017 Romain Acciari <romain.acciari@openio.io> - 1.11.1.dev35-1
- OpenIO fork version
* Wed Sep 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.11.0-1
- Upstream 1.11.0

