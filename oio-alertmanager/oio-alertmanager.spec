%define debug_package %{nil}

Name:    oio-alertmanager
Version: 0.20.0
Release: 1%{?dist}
Summary: Prometheus Alertmanager.
License: ASL 2.0
URL:     https://prometheus.io
ExclusiveArch: x86_64

Source: https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz

%description
The Alertmanager handles alerts sent by client applications such as the
Prometheus server. It takes care of deduplicating, grouping, and routing them to
the correct receiver integration such as email, PagerDuty, or OpsGenie. It also
takes care of silencing and inhibition of alerts.

%prep
%setup -q -n alertmanager-%{version}.linux-amd64

%build

%install
install -D -m 755 alertmanager %{buildroot}%{_sbindir}/oio-alertmanager
install -D -m 755 amtool %{buildroot}%{_bindir}/oio-amtool
install -D -m 644 NOTICE %{buildroot}%{_datadir}/%{name}/NOTICE
install -D -m 644 alertmanager.yml %{buildroot}%{_datadir}/%{name}/alertmanager.yml

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-alertmanager
%{_bindir}/oio-amtool
%{_datadir}/%{name}

%changelog
* Thu Mar 05 2020 Jérôme Loyet <jerome@openio.io> 0.20.0-1
- Initial release, version 0.20.0
