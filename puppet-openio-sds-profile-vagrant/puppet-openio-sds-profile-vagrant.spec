Name:		puppet-openio-sds-profile-vagrant
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	OpenIO profile for Vagrant deployment

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-vagrant/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
OpenIO profile using Puppet to configure a Vagrant box.


%prep
%setup -q -n puppet-openiosds-profile-vagrant-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant


%changelog
* Tue Jun 30 2015 - 20150630-1 - Romain Acciari <romain.acciari@openio.io>
- Add event agent
* Wed May 27 2015 - 20150527-1 - Romain Acciari <romain.acciari@openio.io>
- Remove oioswift temporarily
* Sun Mar 29 2015 - 20150329-1 - Romain Acciari <romain.acciari@openio.io>
- Renamed to puppet-openio-sds-profile-vagrant
* Sun Mar 29 2015 - 20150329-1 - Romain Acciari <romain.acciari@openio.io>
- Fix oioswift and oioproxy namespaces
- oioswift and oioproxy now listen to 0.0.0.0
* Sun Mar 29 2015 - 20150317-3 - Romain Acciari <romain.acciari@openio.io>
- Add oioswift and oioproxy
* Tue Mar 17 2015 - 20150317-2 - Romain Acciari <romain.acciari@openio.io>
- Fix install script
* Tue Mar 17 2015 - 20150317-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
