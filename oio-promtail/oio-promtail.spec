%define debug_package %{nil}

Name:    oio-promtail
Version: 1.3.0
Release: 1%{?dist}
Summary: Logging agent for loki
License: Apache-2.0
URL:     https://grafana.com/oss/loki/
ExclusiveArch: x86_64

Source: https://github.com/grafana/loki/releases/download/v%{version}/promtail-linux-amd64.zip

%description
Promtail is an agent which ships the contents of local logs to a private Loki
instance or Grafana Cloud. It is usually deployed to every machine that has
applications needed to be monitored. It primarily:
 * Discovers targets
 * Attaches labels to log streams
 * Pushes them to the Loki instance.

%prep
%setup -q -c promtail 

%build
/bin/true

%install
install -D -m 755 promtail-linux-amd64 %{buildroot}%{_sbindir}/oio-promtail

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-promtail

%changelog
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 1.3.0-1
- Initial release, version 1.3.0
