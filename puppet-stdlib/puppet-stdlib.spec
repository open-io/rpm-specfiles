Name:		puppet-stdlib
Version:	4.5.1
Release:	1%{?dist}
Summary:	Puppet module for PuppetLabs stdlib

License:	Apache 2.0
URL:		http://www.puppetlabs.com/
Source0:	https://forgeapi.puppetlabs.com/v3/files/puppetlabs-stdlib-%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:       puppet >= 3.6


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
* Fri Mar 06 2015 - 4.5.1-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
