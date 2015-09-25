Name:		puppet-openio-sds-profile-vagrant-ext-pydio
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	Puppet manifests for Vagrant deployment

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile-vagrant-ext-pydio/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds-profile


%description
Puppet manifests to install OpenIO SDS solution using Vagrant.


%prep
%setup -q -n puppet-openiosds-profile-vagrant-ext-pydio-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-pydio
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-pydio


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles/vagrant-ext-pydio


%changelog
* Mon Sep 21 2015 - 20150921-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
