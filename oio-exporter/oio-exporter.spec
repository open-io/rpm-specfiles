#
# Note: to package, please add the `--enable-network` to the
# mock command line:
#
# mock -r epel-7-x86_64-openio-sds-20.04 --rebuild /home/oioops/rpmbuild/SRPMS/oio-exporter-0.0.2-1.el7.oio.src.rpm  --enable-network
#
%define debug_package %{nil}

Name: oio-exporter
Version: 0.0.2
Release: 1%{?dist}
Summary: Prometheus exporter for OpenIO services
License: OpenIO
URL:     https://github.com/open-io/oio-exporter
BuildRequires:  golang >= 1.12

source: https://github.com/open-io/oio-exporter/archive/%{version}.tar.gz

%description
Prometheus exporter for OpenIO services

%prep
%setup -q -n oio-exporter-%{version}

%build
go build -ldflags="-X 'main.HEALTHCHECKS=$(base64 -w0 ./healthchecks.yml)' -X 'main.LOGPATTERNS=$(base64 -w0 ./log_patterns.yml)'" oio-exporter.go

%install
install -D -m755 oio-exporter ${RPM_BUILD_ROOT}%{_sbindir}/oio-exporter

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-exporter

%changelog
* Mon Mar 30 2020 Jérôme Loyet <jerome@openio.io> 0.0.2-1
- update
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 0.0.1-1
- Initial release, version 0.0.1
