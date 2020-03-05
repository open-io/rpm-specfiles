%define debug_package %{nil}

Name: oio-kibana
Version: 7.6.1
Release: 1%{?dist}
Summary: Explore and visualize your Elasticsearch data
License: Elastic License
URL:     https://www.elastic.co/
AutoReqProv: no
ExclusiveArch: x86_64

source: https://artifacts.elastic.co/downloads/kibana/kibana-%{version}-linux-x86_64.tar.gz

%description
Explore and visualize your Elasticsearch data

%prep
%setup -q -n kibana-%{version}-linux-x86_64

%build

%install
%{__mkdir_p} %{buildroot}%{_datarootdir}/%{name}
%{__cp} -a * %{buildroot}%{_datarootdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_datarootdir}/%{name}

%changelog
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 7.6.1-1
- Initial release, version 7.6.1
