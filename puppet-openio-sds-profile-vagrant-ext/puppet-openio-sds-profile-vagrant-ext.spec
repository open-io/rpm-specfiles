Name:		puppet-openio-sds-profile-vagrant-ext
Version:	20150519
Release:	1%{?dist}
Summary:	Puppet manifests for Vagrant deployment

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	http://www.openio.io/%{name}-%{version}.tar.bz2
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
Puppet manifests to install OpenIO SDS solution using Vagrant.


%prep
%setup -q


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext


%changelog
* Tue May 19 2015 - 20150519-1 - Romain Acciari <romain.acciari@openio.io>
- Renamed to puppet-openio-sds-profile-vagrant-ext
* Sun Mar 29 2015 - 20150329-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
