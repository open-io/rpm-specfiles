#
# Note: to package, please add the `--enable-network` to the
# mock command line:
#
# mock xxx --rebuild /path/to/xxxx.src.rpm  --enable-network
#
%define debug_package %{nil}

Summary:	Real-time performance monitoring, done right
Name:		oio-netdata
Version:	1.26.0
Release:	1%{?dist}
License:	GPLv3+
Group:		Applications/System
Source0:	https://github.com/netdata/netdata/releases/download/v%{version}/netdata-v%{version}.tar.gz
URL:		http://my-netdata.io
BuildRequires:	pkgconfig
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	libuuid-devel
BuildRequires:	libuv-devel
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  curl
Requires:	zlib
Requires:	libuuid
Requires:	libuv

Requires(post): libcap

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%prep
if ! curl -qs github.com; then
  echo "No network available, please use --enable-network as arguement to mock" >/dev/stderr
  exit 1
fi
%setup -q -n netdata-v%{version}
sed -i "/^PACKAGE_NAME=/s/netdata/%{name}/" configure
sed -i "/^PACKAGE_TARNAME=/s/netdata/%{name}/" configure
sed -i "s@/netdata@/%{name}@" configure
sed -i '/^    program_name = /s/"netdata"/"oio-netdata"/' daemon/main.c
export CFLAGS="${CFLAGS} -fPIC" && ./packaging/bundle-mosquitto.sh .
export CFLAGS="${CFLAGS} -fPIC" && ./packaging/bundle-lws.sh .

%build
%configure \
	--with-zlib \
	--with-math \
	--with-user=openio \
        --disable-cloud
%{__make} %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
%{__make} %{?_smp_mflags} DESTDIR="%{buildroot}" install

find "%{buildroot}" -name .keep -delete

mv %{buildroot}%{_datadir}/netdata %{buildroot}%{_datadir}/%{name}
./packaging/bundle-dashboard.sh . %{buildroot}%{_datadir}/%{name}/web

install -m 644 -p system/netdata.conf "%{buildroot}%{_sysconfdir}/%{name}"

install -m 644 -p collectors/charts.d.plugin/*.conf "%{buildroot}%{_sysconfdir}/%{name}/charts.d/"
install -m 644 -p collectors/python.d.plugin/*.conf "%{buildroot}%{_sysconfdir}/%{name}/python.d/"
install -m 644 -p collectors/charts.d.plugin/*.conf "%{buildroot}%{_sysconfdir}/%{name}/statsd.d/"

install -m 755 -d "%{buildroot}%{_sysconfdir}/logrotate.d"
install -m 644 -p system/netdata.logrotate "%{buildroot}%{_sysconfdir}/logrotate.d/%{name}"

install -d %{buildroot}%{_localstatedir}/cache/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}

# get rid of default healthcheck config files and edit-config script
rm -rf %{buildroot}%{_sysconfdir}/%{name}/health.d
rm -rf %{buildroot}%{_sysconfdir}/%{name}/edit-config

mv %{buildroot}%{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

mv %{buildroot}%{_sbindir}/netdata %{buildroot}%{_sbindir}/oio-netdata
mv %{buildroot}%{_sbindir}/netdatacli %{buildroot}%{_sbindir}/oio-netdatacli
rm %{buildroot}%{_sbindir}/netdata-claim.sh


%clean
rm -rf "%{buildroot}"

%files
%doc README.md
%defattr(-,root,root)

# To be eventually moved to %%_defaultdocdir
%{_libexecdir}/%{name}
%{_sbindir}/oio-netdata
%{_sbindir}/oio-netdatacli

%{_libdir}/%{name}

%caps(cap_dac_read_search,cap_sys_ptrace=ep) %attr(0550,root,openio) %{_libexecdir}/%{name}/plugins.d/apps.plugin

%attr(0770,openio,openio) %dir %{_localstatedir}/cache/%{name}
%attr(0770,openio,openio) %dir %{_localstatedir}/log/%{name}
%attr(0770,openio,openio) %dir %{_localstatedir}/lib/%{name}

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

# Enforce 0644 for files and 0755 for directories
# for the netdata web directory
%defattr(0644,root,openio,0755)
%{_datadir}/%{name}

%changelog
* Thu Oct 15 2020 Jerome Loyet <jerome@openio.io> - 1.26.0-1
  update
* Thu Oct 15 2020 Jerome Loyet <jerome@openio.io> - 1.25.0-1
  update
* Mon Aug 10 2020 Jerome Loyet <jerome@openio.io> - 1.24.0-1
  update
* Thu Jul 16 2020 Jerome Loyet <jerome@openio.io> - 1.23.2-1
  update
* Wed Jul 01 2020 Jerome Loyet <jerome@openio.io> - 1.23.1-1
  update
* Thu Jun 25 2020 Jerome Loyet <jerome@openio.io> - 1.23.0-1
  update
* Wed May 13 2020 Jerome Loyet <jerome@openio.io> - 1.22.1-1
  update
* Mon May 11 2020 Jerome Loyet <jerome@openio.io> - 1.22.0-1
  update
* Thu Apr 16 2020 Jerome Loyet <jerome@openio.io> - 1.21.1-1
  update
* Mon Apr 06 2020 Jerome Loyet <jerome@openio.io> - 1.21.0-1
  update
* Thu Mar 05 2020 Jerome Loyet <jerome@openio.io> - 1.20.0-1
  Initial release, 1.20.0
