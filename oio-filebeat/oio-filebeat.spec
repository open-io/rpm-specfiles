%define debug_package %{nil}

Name: oio-filebeat
Version: 7.6.1
Release: 1%{?dist}
Summary: Filebeat sends log files to Logstash or directly to Elasticsearch.
License: Elastic License
URL:     https://www.elastic.co/
AutoReqProv: no
ExclusiveArch: x86_64

source: https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-%{version}-linux-x86_64.tar.gz

%description
Filebeat sends log files to Logstash or directly to Elasticsearch.

%prep
%setup -q -n filebeat-%{version}-linux-x86_64
%{__mkdir} config bin
%{__mv} filebeat bin/
%{__mv} *.yml modules.d config/

%build

%install
%{__mkdir_p} %{buildroot}%{_datarootdir}/%{name}
%{__cp} -a * %{buildroot}%{_datarootdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_datarootdir}/%{name}

%changelog
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 7-6.1-1
- Initial release, version 7.6.1
