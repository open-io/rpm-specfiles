Name:		puppet-openio-sds-profile-swift
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	OpenIO profile for Vagrant deployment of OpenIO's Swift

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-swift/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
OpenIO profile using Puppet to configure a Vagrant box providing OpenIO's Swift proxy.


%prep
%setup -q -n puppet-openiosds-profile-swift-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/swift
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/swift


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/swift


%changelog
* Thu Aug 20 2015 - 20150820-1 - Romain Acciari <romain.acciari@openio.io>
- Fix for puppet-openiosds
* Wed Jul 01 2015 - 20150701-1 - Romain Acciari <romain.acciari@openio.io>
- Fix ipaddresses
* Tue Jun 30 2015 - 20150630-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
