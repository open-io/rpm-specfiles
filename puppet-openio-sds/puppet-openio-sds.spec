Name:           puppet-openio-sds
Version:        1.1.0
Release:        1%{?dist}
Summary:        Puppet module for OpenIO SDS solution

License:        Apache 2.0
URL:            http://www.openio.io/
Source0:        https://github.com/open-io/puppet-openiosds/archive/%{version}.tar.gz
BuildArch:      noarch

#BuildRequires:
Requires:       puppet >= 3.6
Requires:       puppet-gridinit
Requires:       puppet-stdlib >= 4.5.1


%description
Puppet module to install OpenIO SDS solution.


%prep
%setup -q -n puppet-openiosds-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/openiosds/


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/openiosds



%changelog
* Wed Dec 02 2015 - 1.1.0-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release 1.1.0
* Wed Sep 16 2015 - 20150916-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Sep 02 2015 - 20150902-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New released pushed to Puppet Forge
* Wed Jul 22 2015 - 20150722-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Enhanced zookeeper
- Do not bootstrap by default
* Thu Jul 09 2015 - 20150709-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add default redis install to account service
* Wed Jul 01 2015 - 20150701-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix redis
* Tue Jun 30 2015 - 20150630-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix oioswift
* Wed Jun 24 2015 - 20150624-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add account service
- Add redis
* Thu Jun 18 2015 - 20150618-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add proxy option to sds.conf
- Add no_exec option to define types
- Add oioeventagent
- Fix oioswift
* Tue May 26 2015 - 20150526-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add zookeeper safe default
* Wed May 20 2015 - 20150520-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix for simple deployments
- Remove sample configuration (moved to profiles)
* Thu Apr 09 2015 - 20150409-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix for OpenIO SDS 0.3 changes
* Tue Mar 31 2015 - 20150331-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix ordering for all services
* Mon Mar 30 2015 - 20150330-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix zookeeper ordering
* Sun Mar 29 2015 - 20150329-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add oioproxy and oioswift
* Wed Mar 18 2015 - 20150318-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add "UNSAFETHREECOPES" in conscience module for standalone testing
* Tue Mar 17 2015 - 20150317-2%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix "THREECOPIES" in conscience module
* Tue Mar 17 2015 - 20150317-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add options in conscience service
* Wed Mar 11 2015 - 20150309-2%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add standalone sample configuration
* Mon Mar 09 2015 - 20150309-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix runstatedir to /run
* Fri Mar 06 2015 - 20150306-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Initial release
