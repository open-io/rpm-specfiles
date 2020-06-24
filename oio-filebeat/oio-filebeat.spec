%define debug_package %{nil}

Name: oio-filebeat
Version: 7.8.0
Release: 1%{?dist}
Summary: Filebeat sends log files to Logstash or directly to Elasticsearch.
License: Elastic License
URL:     https://www.elastic.co/

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
%{__mkdir_p} %{buildroot}%{_datarootdir}/oio-filebeat
%{__cp} -a * %{buildroot}%{_datarootdir}/oio-filebeat/

%files
%defattr(-,root,root,-)
%{_datarootdir}/oio-filebeat

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
