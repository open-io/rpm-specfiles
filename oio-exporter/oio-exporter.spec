#
# Note: to package, please add the `--enable-network` to the
# mock command line:
#
# mock -r epel-7-x86_64-openio-sds-20.04 --rebuild /home/oioops/rpmbuild/SRPMS/oio-exporter-0.0.2-1.el7.oio.src.rpm  --enable-network
#
%define debug_package %{nil}

Name: oio-exporter
Version: 0.0.4
Release: 1%{?dist}
Summary: Prometheus exporter for OpenIO services
License: OpenIO
URL:     https://github.com/open-io/oio-exporter
BuildRequires:  golang >= 1.12

source: https://github.com/open-io/oio-exporter/archive/%{version}.tar.gz

%description
Prometheus exporter for OpenIO services

%prep
if ! curl -qs github.com; then
  echo "No network available, please use --enable-network as arguement to mock" >/dev/stderr
  exit 1
fi
%setup -q -n oio-exporter-%{version}

%build
make build

%install
install -D -m755 oio-exporter ${RPM_BUILD_ROOT}%{_sbindir}/oio-exporter
for i in README.md healthchecks.yml log_patterns.yml versions.yml; do
  install -D -m644 $i ${RPM_BUILD_ROOT}%{_datadir}/oio-exporter/$i
done

%files
%defattr(-,root,root,-)
%{_sbindir}/oio-exporter
%{_datadir}/oio-exporter

%changelog
* Fri Apr 17 2020 Jérôme Loyet <jerome@openio.io> 0.0.4-1
- update
* Tue Apr 07 2020 Jérôme Loyet <jerome@openio.io> 0.0.3-1
- update
* Mon Mar 30 2020 Jérôme Loyet <jerome@openio.io> 0.0.2-1
- update
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 0.0.1-1
- Initial release, version 0.0.1
