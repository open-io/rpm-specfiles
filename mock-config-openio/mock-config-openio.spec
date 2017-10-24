Name:           mock-config-openio
Version:        17.04.0
Release:        4%{?dist}
Summary:        Mock configuration file for building OpenIO packages

License:        Apache v2.0
URL:            http://openio.io
BuildArch:      noarch
Source0:        https://github.com/open-io/mock-config-openio/archive/%{version}.tar.gz
Source1:        http://mirror.openio.io/pub/repo/openio/RPM-GPG-KEY-OPENIO-0

#BuildRequires:
Requires:       mock

%description
Mock configuration file for building OpenIO packages for Fedora and
RHEL/CentOS distributions.


%prep
%setup -q -n %{name}-%{version}


%build


%install
%{__mkdir_p} -v %{buildroot}/etc/mock \
                %{buildroot}/usr/share/mock-config-openio \
                %{buildroot}/etc/pki/mock
%{__install} -m 0644 LICENSE README.md \
  %{buildroot}/usr/share/mock-config-openio/
%{__install} -m 0644 *.cfg \
  %{buildroot}/etc/mock/
%{__install} -m 0644 %{SOURCE1} \
  %{buildroot}/etc/pki/mock/


%files
/etc/mock/*
/usr/share/mock-config-openio/*
/etc/pki/mock/*

%changelog
* Fri Oct 20 2017 Romain Acciari <romain.acciari@openio.io> - 17.04.0-4
- Add OpenIO key to mock directory
* Thu Oct 19 2017 Vincent Legoll <vincent.legoll@openio.io> - 17.04.0-3
- Move license & readme to /usr/share, better files globbing
* Thu Oct 19 2017 Romain Acciari <romain.acciari@openio.io> - 17.04.0-2
- Fix the RPM
* Wed Aug 23 2017 Romain Acciari <romain.acciari@openio.io> - 17.04.0-1
- New release
- Adding all supported release
* Fri Jun 16 2017 Romain Acciari <romain.acciari@openio.io> - 16.10.0-1
- Updated to 16.10
* Tue Dec 29 2015 Romain Acciari <romain.acciari@openio.io> - 15.12.0-1
- Update to 15.12
* Wed Dec 02 2015 Romain Acciari <romain.acciari@openio.io> - 1.1-1
- Add Fedora 23 support
* Fri Nov 20 2015 Romain Acciari <romain.acciari@openio.io> - 1.0-1
- Initial Release
