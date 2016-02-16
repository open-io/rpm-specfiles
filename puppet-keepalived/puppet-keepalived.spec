Name:		puppet-keepalived
Version:	1.2.3
Release:	1%{?dist}
Summary:	Puppet module for keepalived by arioch

License:	Apache 2.0
URL:		http://www.puppetlabs.com/
Source0:	http://forgeapi.puppetlabs.com/v3/files/arioch-keepalived-%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet            >= 3.6
Requires:	puppet-concat     >= 2.1

Provides:       puppet-keepalived = %{version}

%description
Puppet module to install arioch keepalived


%prep
%setup -q -n arioch-keepalived-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/keepalived
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/keepalived


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/keepalived


%changelog
* Mon Feb 15 2016 - 1.2.3-1%{?dist} - Lapierre Sebastien <sebastien.lapierre@openio.io>
- Initial release
