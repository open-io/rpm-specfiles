Name:		puppet-stdlib
Version:	4.15.0
Release:	1%{?dist}
Summary:	Puppet module for PuppetLabs stdlib

License:	Apache 2.0
URL:		http://www.puppetlabs.com/
Source0:	https://github.com/puppetlabs/puppetlabs-stdlib/archive/%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:       puppet >= 3.6

Provides:       puppetlabs-stdlib = %{version}

%description
Puppet module to install PuppetLabs stdlib.
This module provides a standard library of resources for the development of
Puppet modules. Puppet modules make heavy use of this standard library.
The stdlib module adds the following resources to Puppet:
. Stages
. Facts
. Functions
. Defined resource types
. Types
. Providers


%prep
%setup -q -n puppetlabs-stdlib-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/stdlib
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/stdlib


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/stdlib



%changelog
* Tue Feb 21 2017 - 4.15.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Sat Dec 05 2015 - 4.9.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Add provides puppetlabs-stdlib
* Fri Mar 06 2015 - 4.5.1-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
