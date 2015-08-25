Name:		puppet-openio-sds-profile-vagrant-ext-swift
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	Puppet manifests for Vagrant deployment

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-vagrant-ext-swift/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
Puppet manifests to install OpenIO SDS solution using Vagrant.


%prep
%setup -q -n puppet-openiosds-profile-vagrant-ext-swift-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-swift
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-swift


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-swift


%changelog
* Thu Aug 20 2015 - 20150820-1 - Romain Acciari <romain.acciari@openio.io>
- Fix for puppet-openiosds
* Wed Jul 08 2015 - 20150708-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
