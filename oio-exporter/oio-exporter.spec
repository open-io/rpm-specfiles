#
# Note: to package, please add the `--enable-network` to the
# mock command line:
#
# mock -r epel-7-x86_64-openio-sds-20.04 --rebuild /home/oioops/rpmbuild/SRPMS/oio-exporter-0.0.2-1.el7.oio.src.rpm  --enable-network
#
%define debug_package %{nil}

Name: oio-exporter
Version: 0.0.12
Release: 1%{?dist}
Summary: Prometheus exporter for OpenIO services
License: OpenIO
URL:     https://github.com/open-io/oio-exporter
BuildRequires:  curl

source: https://github.com/open-io/oio-exporter/archive/%{version}.tar.gz

%description
Prometheus exporter for OpenIO services

%prep
if ! curl -qs github.com; then
  echo "No network available, please use --enable-network as arguement to mock" >/dev/stderr
  exit 1
fi
%setup -q -n oio-exporter-%{version}
curl -Lqsko - https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz | tar -xzf - go/{bin,pkg,src}

%build
PATH=./go/bin:${PATH} make build

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
* Thu Jun 11 2020 Jérôme Loyet <jerome@openio.io> 0.0.12-1
- update
* Mon Jun 08 2020 Jérôme Loyet <jerome@openio.io> 0.0.11-1
- update
* Wed May 20 2020 Jérôme Loyet <jerome@openio.io> 0.0.10-1
- update
* Mon May 18 2020 Jérôme Loyet <jerome@openio.io> 0.0.9-1
- update
* Tue May 12 2020 Jérôme Loyet <jerome@openio.io> 0.0.8-1
- update
* Thu May 07 2020 Jérôme Loyet <jerome@openio.io> 0.0.7-1
- update
* Mon May 04 2020 Jérôme Loyet <jerome@openio.io> 0.0.6-1
- update
* Fri Apr 17 2020 Jérôme Loyet <jerome@openio.io> 0.0.5-1
- update
* Fri Apr 17 2020 Jérôme Loyet <jerome@openio.io> 0.0.4-2
- stop using golang package from distro, but version from golang
* Fri Apr 17 2020 Jérôme Loyet <jerome@openio.io> 0.0.4-1
- update
* Tue Apr 07 2020 Jérôme Loyet <jerome@openio.io> 0.0.3-1
- update
* Mon Mar 30 2020 Jérôme Loyet <jerome@openio.io> 0.0.2-1
- update
* Wed Mar 04 2020 Jérôme Loyet <jerome@openio.io> 0.0.1-1
- Initial release, version 0.0.1
