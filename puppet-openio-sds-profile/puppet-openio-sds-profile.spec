Name:		puppet-openio-sds-profile
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	OpenIO minimal profile

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-openiosds-profile/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet-openio-sds
Obsoletes:      puppet-openio-sds-profile-docker


%description
Puppet manifests to install OpenIO SDS solution.


%prep
%setup -q -n puppet-openiosds-profile-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/profiles/


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds/profiles


%changelog
* Fri Aug 18 2017 - 20170818-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Mar 07 2017 - 20170307-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Feb 28 2017 - 20170228-1 - Romain Acciari <romain.acciari@openio.io>
- New release (remove vagrant)
* Mon Feb 20 2017 - 20170220-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Sun Feb 19 2017 - 20170219-1 - Romain Acciari <romain.acciari@openio.io>
- Now integrates vagrant and docker profiles
* Sun Apr 17 2016 - 20160417-1 - Romain Acciari <romain.acciari@openio.io>
- Prepare for 16.04 release
* Tue Dec 08 2015 - 20151208-1 - Romain Acciari <romain.acciari@openio.io>
- Fixes for Fedora 23
- Update minimal profile
* Wed Sep 02 2015 - 20150902-1 - Romain Acciari <romain.acciari@openio.io>
- New release for Docker
* Thu Aug 20 2015 - 20150820-1 - Romain Acciari <romain.acciari@openio.io>
- Fix for puppet-openiosds
* Mon Jul 06 2015 - 20150706-1 - Romain Acciari <romain.acciari@openio.io>
- Permit additionnal parameters
* Wed May 20 2015 - 20150520-1 - Romain Acciari <romain.acciari@openio.io>
- Fix minimal profile to wait for meta1 to register.
* Tue May 19 2015 - 20150519-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
