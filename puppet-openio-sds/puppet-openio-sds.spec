Name:           puppet-openio-sds
Version:        1.1.41
Release:        1%{?dist}
Summary:        Puppet module for OpenIO SDS solution

License:        Apache 2.0
URL:            http://www.openio.io/
Source0:        https://github.com/open-io/puppet-openiosds/archive/%{version}.tar.gz
BuildArch:      noarch

#BuildRequires:
Requires:       puppet            >= 3.6
Requires:       puppet-gridinit
Requires:       puppetlabs-stdlib >= 4.6.0


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
* Fri May 13 2016 - 1.1.41-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Apr 26 2016 - 1.1.39-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Apr 15 2016 - 1.1.38-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Mar 25 2016 - 1.1.26-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 21 2016 - 1.1.26-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Mar 08 2016 - 1.1.24-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 07 2016 - 1.1.22-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Mar 04 2016 - 1.1.21-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Feb 29 2016 - 1.1.20-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Feb 23 2016 - 1.1.19-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Feb 22 2016 - 1.1.17-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Feb 15 2016 - 1.1.11-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Feb 11 2016 - 1.1.10-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Feb 08 2016 - 1.1.9-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Jan 29 2016 - 1.1.8-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Jan 22 2016 - 1.1.4-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Dec 16 2015 - 1.1.2-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Dec 02 2015 - 1.1.1-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release 1.1.1
- Update puppetlabs-stdlib dependency
* Wed Dec 02 2015 - 1.1.0-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release 1.1.0
