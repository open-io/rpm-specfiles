Name:		puppet-gridinit
Version:	%(date +"%Y%m%d")
Release:	1%{?dist}
Summary:	Puppet module for gridinit from OpenIO

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/open-io/puppet-gridinit/archive/master.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet >= 3.6
Requires:       puppet-stdlib >= 4.5.1

%description
Puppet module to install OpenIO SDS solution.


%prep
%setup -q -n puppet-gridinit-master


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/gridinit
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/gridinit


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/gridinit



%changelog
* Thu Jul 09 2015 - 20150709-1 - Romain Acciari <romain.acciari@openio.io>
- Require package before service
* Thu Jun 18 2015 - 20150618-1 - Romain Acciari <romain.acciari@openio.io>
- Add no_exec option
* Thu Mar 19 2015 - 20150319-2 - Romain Acciari <romain.acciari@openio.io>
- start_at_boot is enabled by default
* Thu Mar 19 2015 - 20150319-1 - Romain Acciari <romain.acciari@openio.io>
- Remove log4c
* Wed Mar 18 2015 - 20150318-1 - Romain Acciari <romain.acciari@openio.io>
- Wait 1 second before reloading to let the daemon create the socket
- Fix root user
- Fix runstatedir to /run/gridinit
* Mon Mar 09 2015 - 20150309-1 - Romain Acciari <romain.acciari@openio.io>
- Fix runstatedir to /run
* Fri Mar 06 2015 - 20150306-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
