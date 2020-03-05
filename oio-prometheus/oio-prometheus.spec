%define debug_package %{nil}

Name:    oio-prometheus
Version: 2.16.0
Release: 1%{?dist}
Summary: The Prometheus 2.x monitoring system and time series database.
License: ASL 2.0
URL:     https://prometheus.io
ExclusiveArch: x86_64

Source: https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz

%description
Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -q -n prometheus-%{version}.linux-amd64

%build

%install
install -D -m 755 prometheus %{buildroot}%{_sbindir}/oio-prometheus
install -D -m 755 promtool %{buildroot}%{_bindir}/oio-promtool
install -D -m 644 prometheus.yml %{buildroot}%{_datadir}/%{name}/config/prometheus.yml
install -D -m 644 NOTICE %{buildroot}%{_datadir}/%{name}/NOTICE

for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -D -m 644 ${file} %{buildroot}%{_datarootdir}/%{name}/${file}
  done
done

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-prometheus
%{_bindir}/oio-promtool
%{_datarootdir}/%{name}

%changelog
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 2.16.0-1
- Initial release, version 2.16.0
