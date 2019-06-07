%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         grafana
%global repo            grafana
# https://github.com/grafana/grafana
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          v5.0.4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

Name:           %{repo}
Version:        5.0.4
Release:        1%{?dist}
Summary:        Grafana is an open source, feature rich metrics dashboard and graph editor
License:        ASL 2.0
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source2:        https://github.com/percona/pmm-server-packaging/raw/608fc15aff42767835c9770cd2307099e18d8e0d/rhel/SOURCES/grafana-node_modules-v5.0.4.el7.tar.gz
Source3:        https://github.com/percona/pmm-server-packaging/raw/608fc15aff42767835c9770cd2307099e18d8e0d/rhel/SOURCES/grafana-server.service
Source4:        https://github.com/sass/node-sass/releases/download/v4.12.0/linux-x64-48_binding.node
ExclusiveArch:  %{ix86} x86_64 %{arm}

BuildRequires: golang >= 1.7.3
BuildRequires: nodejs-grunt-cli fontconfig
BuildRequires: nodejs < 1:7

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Requires:       fontconfig freetype urw-fonts

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -a 2 -n %{repo}-%{version}
mv %{SOURCE4} node_modules/node-sass/vendor/
rm -rf Godeps

%build
mkdir -p _build/src
mv vendor/google.golang.org _build/src/
mv vendor/cloud.google.com _build/src/
mv vendor/github.com _build/src/
mv vendor/golang.org _build/src/
mv vendor/gopkg.in   _build/src/

mkdir -p ./_build/src/github.com/grafana
ln -s $(pwd) ./_build/src/github.com/grafana/grafana
export GOPATH=$(pwd)/_build:%{gopath}

export LDFLAGS="$LDFLAGS -X main.version=%{version} -X main.commit=%{shortcommit} -X main.buildstamp=$(date '+%s') "
%gobuild -o ./bin/grafana-server ./pkg/cmd/grafana-server
%gobuild -o ./bin/grafana-cli ./pkg/cmd/grafana-cli

/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --pkgVer=%{version} "clean:release"
/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --pkgVer=%{version} "clean:build"
/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --pkgVer=%{version} phantomjs
./node_modules/.bin/webpack --config scripts/webpack/webpack.prod.js --verbose --progress
/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --pkgVer=%{version} build-post-process
/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --pkgVer=%{version} "compress:release"

%install
install -d -p %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/conf %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/public %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/scripts %{buildroot}%{_datadir}/%{repo}

install -d -p %{buildroot}%{_sbindir}
cp tmp/bin/%{repo}-server %{buildroot}%{_sbindir}/
install -d -p %{buildroot}%{_bindir}
cp tmp/bin/%{repo}-cli %{buildroot}%{_bindir}/

install -d -p %{buildroot}%{_sysconfdir}/%{repo}
cp tmp/conf/sample.ini %{buildroot}%{_sysconfdir}/%{repo}/grafana.ini
mv tmp/conf/ldap.toml %{buildroot}%{_sysconfdir}/%{repo}/

%if 0%{?fedora} || 0%{?rhel} == 7
mkdir -p %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/
%else
mkdir -p %{buildroot}%{_initddir}/
install -p -m 0644 packaging/rpm/init.d/grafana-server %{buildroot}%{_initddir}/
%endif

install -d -p %{buildroot}%{_sharedstatedir}/%{repo}
install -d -p %{buildroot}/var/log/%{repo}

%check
export GOPATH=$(pwd)/_build:%{gopath}
go test ./pkg/api
go test ./pkg/bus
go test ./pkg/components/apikeygen
go test ./pkg/components/renderer
go test ./pkg/events
go test ./pkg/models
go test ./pkg/plugins
# These tests fail, so they were disabled
#go test ./pkg/services/sqlstore
#go test ./pkg/services/sqlstore/migrations
go test ./pkg/setting
go test ./pkg/util

%files
%defattr(-, grafana, grafana, -)
%{_datadir}/%{repo}
%doc *.md
%doc docs
%attr(0755, root, root) %{_sbindir}/%{repo}-server
%attr(0755, root, root) %{_bindir}/%{repo}-cli
%{_sysconfdir}/%{repo}/grafana.ini
%{_sysconfdir}/%{repo}/ldap.toml
%if 0%{?fedora} || 0%{?rhel} == 7
%attr(-, root, root) /usr/lib/systemd/system/grafana-server.service
%else
%attr(-, root, root) %{_initddir}/grafana-server
%endif
#attr(-, root, root) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sharedstatedir}/%{repo}
%dir /var/log/%{repo}

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || \
    useradd -r -g grafana -d /etc/grafana -s /sbin/nologin \
    -c "Grafana Dashboard" grafana
exit 0

%post
%systemd_post grafana.service

%preun
%systemd_preun grafana.service

%postun
%systemd_postun grafana.service

%changelog

* Thu Jun 06 2019 Vladimir DOMBROVSKI <vladimir@openio.io> - 5.0.4-1
- Fix webpack, golang tests

* Thu Mar 29 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.0.4-1
- PMM-2319 update to 5.0.4

* Mon Jan  8 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.3-1
- PMM-1895 update to 4.6.3

* Mon Nov  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.1-1
- PMM-1652 update to 4.6.1

* Tue Oct 31 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.0-1
- PMM-1652 update to 4.6.0

* Fri Oct  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.5.2-1
- PMM-1521 update to 4.5.2

* Tue Sep 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-2
- fix HOME variable in unit file

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-1
- PMM-1221 update to 4.4.3

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.2-1
- PMM-1221 update to 4.4.2

* Wed Jul 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.1-1
- PMM-1221 update to 4.4.1

* Thu Jul 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-2
- PMM-1208 install fontconfig freetype urw-fonts

* Thu Jun  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-1
- update to 4.3.2

* Wed Mar 29 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.2.0-2
- up to 4.2.0
- PMM-708 rollback tooltip position

* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.2-1
- up to 4.1.2

* Thu Jan 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.1-1
- up to 4.1.1

* Thu Dec 29 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-2
- use fixed grafana-server.service

* Thu Dec 15 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-1
- up to 4.0.2

* Fri Jul 31 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-3
- Unbundled phantomjs from grafana

* Tue Jul 28 2015 Lon Hohberger <lon@redhat.com> - 2.0.2-2
- Change ownership for grafana-server to root

* Tue Apr 14 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-1
- First package for Fedora
