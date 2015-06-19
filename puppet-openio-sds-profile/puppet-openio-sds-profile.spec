Name:		puppet-openio-sds-profile
Version:	20150520
Release:	1%{?dist}
Summary:	OpenIO minimal profile

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	http://www.openio.io/%{name}-%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds


%description
Puppet manifests to install OpenIO SDS solution using Vagrant.


%prep
%setup -q


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles


%changelog
* Wed May 20 2015 - 20150520-1 - Romain Acciari <romain.acciari@openio.io>
- Fix minimal profile to wait for meta1 to register.
* Tue May 19 2015 - 20150519-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
