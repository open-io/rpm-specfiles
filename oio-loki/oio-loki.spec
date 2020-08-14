%define debug_package %{nil}

Name:    oio-loki
Version: 1.6.0
Release: 1%{?dist}
Summary: Set of components that can be composed into a fully featured logging stack.
License: Apache-2.0
URL:     https://grafana.com/oss/loki/
ExclusiveArch: x86_64

source: https://github.com/grafana/loki/releases/download/v%{version}/loki-linux-amd64.zip
source1: https://github.com/grafana/loki/releases/download/v%{version}/logcli-linux-amd64.zip

%description
Loki is a logging backend, optimized for users running Prometheus and Kubernetes
Loki is optimized to search, visualize and explore your logs natively in Grafana

%prep
%setup -c -a 1

%build
/bin/true

%install
install -D -m 755 loki-linux-amd64 %{buildroot}%{_sbindir}/oio-loki
install -D -m 755 logcli-linux-amd64 %{buildroot}%{_bindir}/oio-logcli

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-loki
%{_bindir}/oio-logcli

%changelog
* Fri Aug 14 2020 Jérôme Loyet <jerome@openio.io> 1.6.0-1
- update
* Wed May 20 2020 Jérôme Loyet <jerome@openio.io> 1.5.0-1
- update
* Wed Apr 01 2020 Jérôme Loyet <jerome@openio.io> 1.4.0-1
- update
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 1.3.0-1
- Initial release, version 1.3.0
