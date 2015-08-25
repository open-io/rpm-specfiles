Name:		puppet-openio-sds-profile-cyrus
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	OpenIO profile for Vagrant deployment of Cyrus with OpenIO

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-cyrus/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
OpenIO profile using Puppet to configure a Vagrant box providing OpenIO implementation in Cyrus.


%prep
%setup -q -n puppet-openiosds-profile-cyrus-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/cyrus
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/cyrus


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/cyrus


%changelog
* Thu Aug 20 2015 - 20150820-1 - Romain Acciari <romain.acciari@openio.io>
- Fix for puppet-openiosds
* Fri Jul 17 2015 - 20150717-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
