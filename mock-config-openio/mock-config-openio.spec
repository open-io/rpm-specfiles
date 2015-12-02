Name:           mock-config-openio
Version:        1.1
Release:        1%{?dist}
Summary:        Mock configuration file for building OpenIO packages

License:        Apache v2
URL:            http://openio.io
BuildArch:      noarch
Source0:        epel-7-x86_64-openio.cfg       
Source1:        fedora-21-x86_64-openio.cfg
Source2:        fedora-22-x86_64-openio.cfg
Source3:        fedora-23-x86_64-openio.cfg

#BuildRequires: 
Requires:       mock

%description
Mock configuration file for building OpenIO packages for Fedora and
RHEL/CentOS distributions.


%prep


%build


%install
%{__mkdir_p} -v %{buildroot}/etc/mock
%{__install} %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
  %{buildroot}/etc/mock/


%files
/etc/mock/*


%changelog
* Wed Dec 02 2015 Romain Acciari <romain.acciari@openio.io> - 1.1-1%{?dist}
- Add Fedora 23 support
* Fri Nov 20 2015 Romain Acciari <romain.acciari@openio.io> - 1.0-1%{?dist}
- Initial Release
