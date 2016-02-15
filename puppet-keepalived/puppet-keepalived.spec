Name:		puppet-gridinit
Version:	1.2.3
Release:	1%{?dist}
Summary:	Puppet module for keepalived by arioch for OpenIO SDS

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	http://forgeapi.puppetlabs.com/v3/files/arioch-keepalived-%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet            >= 3.6
Requires:       puppetlabs-stdlib >= 4.6.0

%description
Puppet module to install arioch keepalived for OpenIO SDS solution.


%prep
%setup -q -n puppet-keepalived-%{version}


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
