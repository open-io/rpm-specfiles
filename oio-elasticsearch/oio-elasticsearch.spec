%define debug_package %{nil}

Name: oio-elasticsearch
Version: 7.8.0
Release: 1%{?dist}
Summary: Distributed RESTful search engine built for the cloud
License: Elastic License
URL:     https://www.elastic.co/
Requires: java-headless
AutoReqProv: no
ExclusiveArch: x86_64

source: https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-%{version}-linux-x86_64.tar.gz

%description
Reference documentation can be found at
https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
and the 'Elasticsearch: The Definitive Guide' book can be found at
https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html

%prep
%setup -q -n elasticsearch-%{version}
%{__rm} -r logs jdk

%build

%install
%{__mkdir_p} %{buildroot}%{_datarootdir}/%{name}
%{__cp} -a * %{buildroot}%{_datarootdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_datarootdir}/%{name}

%changelog
* Wed Jun 24 2020 Jérôme Loyet <jerome@openio.io> 7.8.0-1
- Update
* Wed Jun 03 2020 Jérôme Loyet <jerome@openio.io> 7.7.1-1
- Update
* Thu May 14 2020 Jérôme Loyet <jerome@openio.io> 7.7.0-1
- Update
* Wed Apr 01 2020 Jérôme Loyet <jerome@openio.io> 7.6.2-1
- Update
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 7.6.1-1
- Initial release, version 7.6.1
