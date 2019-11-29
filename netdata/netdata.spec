%global contentdir %{_datadir}/netdata

# This is temporary and should eventually be resolved. This bypasses
# the default rhel __os_install_post which throws a python compile
# error.
%global __os_install_post %{nil}

#
# Conditional build:
%bcond_without  systemd  # systemd
%bcond_with     nfacct   # build with nfacct plugin
%bcond_with     freeipmi # build with freeipmi plugin
%bcond_with     netns    # build with netns support (cgroup-network)

%if 0%{?fedora} || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1140
%else
%undefine	with_systemd
%undefine	with_netns
%endif

%if %{with systemd}
%if 0%{?suse_version}
%global netdata_initd_buildrequires BuildRequires: systemd-rpm-macros \
%{nil}
%global netdata_initd_requires %{?systemd_requires} \
%{nil}
%global netdata_init_post %service_add_post netdata.service
%global netdata_init_preun %service_del_preun netdata.service
%global netdata_init_postun %service_del_postun netdata.service
%else
%global netdata_initd_buildrequires BuildRequires: systemd
%global netdata_initd_requires Requires(preun):  systemd-units \
Requires(postun): systemd-units \
Requires(post):   systemd-units \
%{nil}
%global netdata_init_post %systemd_post netdata.service
%global netdata_init_preun %systemd_preun netdata.service
%global netdata_init_postun %systemd_postun_with_restart netdata.service
%endif
%else
%global netdata_initd_buildrequires %{nil}
%global netdata_initd_requires Requires(post):   chkconfig \
%{nil}
%global netdata_init_post /sbin/chkconfig --add netdata \
%{nil}
%global netdata_init_preun %{nil} \
if [ $1 = 0 ]; then \
        /sbin/service netdata stop > /dev/null 2>&1 \
        /sbin/chkconfig --del netdata \
fi \
%{nil}
%global netdata_init_postun %{nil} \
if [ $1 != 0 ]; then \
        /sbin/service netdata condrestart 2>&1 > /dev/null \
fi \
%{nil}
%endif

%if 0%{?_fedora}
%global netdata_recommends Recommends:	curl \
Recommends:	iproute-tc \
Recommends:	lm_sensors \
Recommends:	nmap-ncat \
Recommends:	nodejs \
Recommends:	python \
Recommends:	PyYAML \
Recommends:	python2-PyMySQL \
Recommends:	python2-psycopg2 \
%{nil}
%else
%global netdata_recommends %{nil}
%endif

Summary:	Real-time performance monitoring, done right
Name:		netdata
Version:	1.19.0
Release:	3%{?dist}
License:	GPLv3+
Group:		Applications/System
Source0:	https://github.com/netdata/%{name}/releases/download/v%{version}/%{name}-v%{version}.tar.gz
Epoch:		1
URL:		http://my-netdata.io
BuildRequires:	pkgconfig
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	libuuid-devel
Requires:	zlib
Requires:	libuuid

# Packages can be found in the EPEL repo
%if %{with nfacct}
BuildRequires:	libmnl-devel
BuildRequires:	libnetfilter_acct-devel
Requires: libmnl
Requires: libnetfilter_acct
%endif

%if %{with freeipmi}
BuildRequires:	freeipmi-devel
Requires: freeipmi
%endif

Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(post): libcap

%{netdata_initd_buildrequires}
%{netdata_recommends}
%{netdata_initd_requires}

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%prep
%setup -q -n %{name}-v%{version}

%build
%configure \
	--with-zlib \
	--with-math \
	%{?with_nfacct:--enable-plugin-nfacct} \
	%{?with_freeipmi:--enable-plugin-freeipmi} \
	--with-user=netdata
%{__make} %{?_smp_mflags}

%install
rm -rf "${RPM_BUILD_ROOT}"
%{__make} %{?_smp_mflags} DESTDIR="${RPM_BUILD_ROOT}" install

find "${RPM_BUILD_ROOT}" -name .keep -delete

install -m 644 -p system/netdata.conf "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}"

install -m 644 -p collectors/charts.d.plugin/*.conf "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/charts.d/"
install -m 644 -p collectors/python.d.plugin/*.conf "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/python.d/"
install -m 644 -p collectors/charts.d.plugin/*.conf "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/statsd.d/"

install -m 755 -d "${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d"
install -m 644 -p system/netdata.logrotate "${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}"

# get rid of default healthcheck config files and edit-config script
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/health.d
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/edit-config

%if %{with systemd}
install -m 755 -d "${RPM_BUILD_ROOT}%{_unitdir}"
install -m 644 -p system/netdata.service "${RPM_BUILD_ROOT}%{_unitdir}/netdata.service"
%else
# install SYSV init stuff
install -d "${RPM_BUILD_ROOT}/etc/rc.d/init.d"
install -m 755 system/netdata-init-d \
        "${RPM_BUILD_ROOT}/etc/rc.d/init.d/netdata"
%endif

%pre
getent group netdata >/dev/null || groupadd -r netdata
getent group docker >/dev/null || groupadd -r docker
getent passwd netdata >/dev/null || \
  useradd -r -g netdata -G docker -s /sbin/nologin \
    -d %{contentdir} -c "netdata" netdata

%post
%{netdata_init_post}

%preun
%{netdata_init_preun}

%postun
%{netdata_init_postun}

%clean
rm -rf "${RPM_BUILD_ROOT}"

%files
%doc README.md
%defattr(-,root,root)

%dir %{_sysconfdir}/%{name}

%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/charts.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/python.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/statsd.d/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

# To be eventually moved to %%_defaultdocdir
%{_libexecdir}/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}

%caps(cap_dac_read_search,cap_sys_ptrace=ep) %attr(0550,root,netdata) %{_libexecdir}/%{name}/plugins.d/apps.plugin

%if %{with netns}
# cgroup-network detects the network interfaces of CGROUPs
# it must be able to use setns() and run cgroup-network-helper.sh as root
# the helper script reads /proc/PID/fdinfo/* files, runs virsh, etc.
%caps(cap_setuid=ep) %attr(4550,root,netdata) %{_libexecdir}/%{name}/plugins.d/cgroup-network
%attr(0550,root,root) %{_libexecdir}/%{name}/plugins.d/cgroup-network-helper.sh
%endif

%if %{with freeipmi}
%caps(cap_setuid=ep) %attr(4550,root,netdata) %{_libexecdir}/%{name}/plugins.d/freeipmi.plugin
%endif

%attr(0770,netdata,netdata) %dir %{_localstatedir}/cache/%{name}
%attr(0770,netdata,netdata) %dir %{_localstatedir}/log/%{name}
%attr(0770,netdata,netdata) %dir %{_localstatedir}/lib/%{name}

%dir %{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}/python.d
%dir %{_sysconfdir}/%{name}/charts.d
%dir %{_sysconfdir}/%{name}/node.d

%if %{with systemd}
%{_unitdir}/netdata.service
%else
%{_sysconfdir}/rc.d/init.d/netdata
%endif

# Enforce 0644 for files and 0755 for directories
# for the netdata web directory
%defattr(0644,root,netdata,0755)
%{_datadir}/%{name}/web

%changelog
* Fri Nov 29 2019 Vladimir Dombrovski <vladimir@openio.io> - 1.19.0-1
  New release
* Thu Sep 5 2019 Vladimir Dombrovski <vladimir@openio.io> - 1.9.0-3
  Remove default healthcheck provisioning
* Tue Aug 20 2019 Vladimir Dombrovski <vladimir@openio.io> - 1.9.0-2
  Set epoch to resolve conflict with epel package
* Sun Dec 17 2017 Costa Tsaousis <costa@tsaousis.gr> - 1.9.0-1
  Please check full changelog at github.
  https://github.com/firehol/netdata/releases
* Sun Sep 17 2017 Costa Tsaousis <costa@tsaousis.gr> - 1.8.0-1
  This is mainly a bugfix release.
  Please check full changelog at github.
* Sun Jul 16 2017 Costa Tsaousis <costa@tsaousis.gr> - 1.7.0-1
- netdata is now a fully featured statsd server
- new installation options
- metrics streaming and replication improvements
- backends improvements - prometheus support rewritten
- netdata now monitors ZFS (on Linux and FreeBSD)
- netdata now monitors ElasticSearch
- netdata now monitors RabbitMQ
- netdata now monitors Go applications (via expvar)
- netdata now monitors ipfw (on FreeBSD 11)
- netdata now monitors samba
- netdata now monitors squid logs
- netdata dashboard loading times have been improved significantly
- netdata alarms now support custom hooks
- dozens more improvements and bug fixes
* Mon Mar 20 2017 Costa Tsaousis <costa@tsaousis.gr> - 1.6.0-1
- central netdata
- monitoring ephemeral nodes
- monitoring ephemeral containers and VM guests
- apps.plugin ported for FreeBSD
- web_log plugin
- JSON backends
- IPMI monitoring
- several new and improved plugins
- several new and improved alarms and notifications
- dozens more improvements and bug fixes
* Sun Jan 22 2017 Costa Tsaousis <costa@tsaousis.gr> - 1.5.0-1
- FreeBSD, MacOS, FreeNAS
- Backends support
- dozens of new and improved plugins
- dozens of new and improved alarms and notification methods
* Tue Oct 4 2016 Costa Tsaousis <costa@tsaousis.gr> - 1.4.0-1
- the fastest netdata ever (with a better look too)!
- improved IoT and containers support!
- alarms improved in almost every way!
- Several more improvements, new features and bugfixes.
* Sun Aug 28 2016 Costa Tsaousis <costa@tsaousis.gr> - 1.3.0-1
- netdata now has health monitoring
- netdata now generates badges
- netdata now has python plugins
- Several more improvements, new features and bugfixes.
* Tue Jul 26 2016 Jason Barnett <J@sonBarnett.com> - 1.2.0-2
- Added support for EL6
- Corrected several Requires statements
- Changed default to build without nfacct
- Removed --docdir from configure
* Mon May 16 2016 Costa Tsaousis <costa@tsaousis.gr> - 1.2.0-1
- netdata is now 30% faster.
- netdata now has a registry (my-netdata menu on the dashboard).
- netdata now monitors Linux containers.
- Several more improvements, new features and bugfixes.
* Wed Apr 20 2016 Costa Tsaousis <costa@tsaousis.gr> - 1.1.0-1
- Several new features (IPv6, SYNPROXY, Users, Users Groups).
- A lot of bug fixes and optimizations.
* Tue Mar 22 2016 Costa Tsaousis <costa@tsaousis.gr> - 1.0.0-1
- First public release.
* Sun Nov 15 2015 Alon Bar-Lev <alonbl@redhat.com> - 0.0.0-1
- Initial add.
