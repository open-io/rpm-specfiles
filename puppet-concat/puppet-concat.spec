Name:		puppet-concat
Version:	2.1.0
Release:	1%{?dist}
Summary:	Concat puppet module for openio

Group:		openio
License:	Apache 2.0
URL:		http://www.openio.io/
Source0:	https://github.com/puppetlabs/puppetlabs-concat/archive/%{version}.tar.gz
BuildArch:	noarch

#BuildRequires:	
Requires:	puppet            >= 3.6

Provides:       puppet-concat = %{version}

%description
Concat Puppet module for OpenIO SDS solution.
The concat module lets you construct files from multiple ordered fragments of text.


%prep
%setup -q -n puppetlabs-concat-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/concat
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/puppet/modules/concat


%files
%defattr(-,root,root,-)
%{_datarootdir}/puppet/modules/concat


%changelog
* Mon Feb 15 2016 - 2.1.0-1%{?dist} - Lapierre Sebastien <sebastien.lapierre@openio.io>
- Initial release
