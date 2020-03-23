%define debug_package %{nil}

Name: oio-grafana
Version: 6.7.1
Release: 1%{?dist}
Summary: Grafana is an open source, feature rich metrics dashboard and graph editor
License: ASL 2.0
URL:     https://grafana.com
AutoReqProv: no
ExclusiveArch: x86_64

source: https://dl.grafana.com/oss/release/grafana-%{version}.linux-amd64.tar.gz

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -n grafana-%{version}

%build

%install
%{__mkdir_p} %{buildroot}%{_datarootdir}/%{name}
%{__cp} -a * %{buildroot}%{_datarootdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_datarootdir}/%{name}

%changelog
* Mon Mar 23 2020 Jérôme Loyet <jerome@openio.io> 6.7.1-1
- update to version 6.7.1
* Fri Mar 20 2020 Jérôme Loyet <jerome@openio.io> 6.7.0-1
- update to version 6.7.0
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 6.6.2-1
- Initial release, version 6.6.2
