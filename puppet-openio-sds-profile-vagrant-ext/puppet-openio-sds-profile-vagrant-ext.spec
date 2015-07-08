Name:		puppet-openio-sds-profile-vagrant-ext
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	Puppet manifests for Vagrant deployment

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-vagrant-ext/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
Puppet manifests to install OpenIO SDS solution using Vagrant.


%prep
%setup -q -n puppet-openiosds-profile-vagrant-ext-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext


%changelog
* Mon Jul 06 2015 - 20150706-1 - Romain Acciari <romain.acciari@openio.io>
- Fix for release 15.07
* Tue May 19 2015 - 20150519-1 - Romain Acciari <romain.acciari@openio.io>
- Renamed to puppet-openio-sds-profile-vagrant-ext
* Sun Mar 29 2015 - 20150329-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
