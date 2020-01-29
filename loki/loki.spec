Name:           loki
Version:        1.3.0
Release:        2%{?dist}
License:        Apache-2.0
Group:          System/Monitoring
Summary:        Set of components that can be composed into a fully featured logging stack.
Url:            https://grafana.com/loki
Source:         https://github.com/grafana/loki/archive/v%{version}.tar.gz
BuildRequires:  fdupes
BuildRequires:  systemd-devel
BuildRequires:  go >= 1.11

%define debug_package %{nil}

%description
Loki is a logging backend, optimized for users running Prometheus and Kubernetes
Loki is optimized to search, visualize and explore your logs natively in Grafana


%package -n promtail
Summary:        Logging agent for loki

%description -n promtail
Promtail is an agent which ships the contents of local logs to a private Loki
instance or Grafana Cloud. It is usually deployed to every machine that has
applications needed to be monitored. It primarily:
 * Discovers targets
 * Attaches labels to log streams
 * Pushes them to the Loki instance.

%prep
%setup -q -n loki-%{version}

%build
make loki
make logcli
make promtail

%install

install -dm755 %{buildroot}%{_sbindir}

# loki
install -Dm644 README.md %{buildroot}%{_defaultdocdir}/loki/README.md
install -Dm644 LICENSE %{buildroot}%{_defaultdocdir}/loki/LICENSE
install -Dm644 cmd/loki/loki-local-config.yaml %{buildroot}%{_defaultdocdir}/loki/loki.yaml
install -m755  cmd/loki/loki %{buildroot}%{_sbindir}/loki
install -m755  cmd/logcli/logcli %{buildroot}%{_sbindir}/logcli
# promtail
install -Dm644 README.md %{buildroot}%{_defaultdocdir}/promtail/README.md
install -Dm644 LICENSE %{buildroot}%{_defaultdocdir}/promtail/LICENSE
install -Dm644 cmd/promtail/promtail-local-config.yaml %{buildroot}%{_defaultdocdir}/promtail/promtail.yaml
install -m755  cmd/promtail/promtail %{buildroot}%{_sbindir}/promtail

%files
%defattr(-,root,root)
%{_sbindir}/loki
%{_sbindir}/logcli
%doc %{_defaultdocdir}/loki/loki.yaml
%doc %{_defaultdocdir}/loki/README.md
%doc %{_defaultdocdir}/loki/LICENSE

%files -n promtail
%defattr(-,root,root)
%{_sbindir}/promtail
%doc %{_defaultdocdir}/promtail/promtail.yaml
%doc %{_defaultdocdir}/promtail/README.md
%doc %{_defaultdocdir}/promtail/LICENSE

%changelog
* Wed Jan 29 2020 Jerome Loyet <jerome@openio.io> - 1.3.0-2
  disable the generation of the debuginfo package
* Wed Jan 29 2020 Jerome Loyet <jerome@openio.io> - 1.3.0-1
  Initial release
