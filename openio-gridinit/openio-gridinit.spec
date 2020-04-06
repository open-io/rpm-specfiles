%define         realname gridinit

Name:           openio-%{realname}
%if %{?_with_test:0}%{!?_with_test:1}
Version:        2.1.0
Release:        1%{?dist}
%define         tarversion %{version}
%else
%define         date %(date +"%Y%m%d%H%M")
Version:        test%{date}.%{tag}
Release:        0%{?dist}
%define         tarversion %{tag}
Epoch:          1
%endif
Source0:        https://github.com/open-io/gridinit/archive/%{tarversion}.tar.gz

Summary:        OpenIO gridinit daemon
License:        AGPL-3.0+
#URL:
Source1:        %{name}-systemd.service
Source2:        %{name}-tmpfiles.conf
Source3:        %{name}-rsyslog.conf
Source4:        %{name}-logrotate.conf
%if 0%{?suse_version}
Source5:        %{name}-rpmlintrc
%endif

# Requires
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  git
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  glib2-devel    >= 2.52.0
BuildRequires:  systemd
%if 0%{?suse_version}
BuildRequires:  rsyslog
%endif

Requires:       glib2         >= 2.52
Requires:       python36-setproctitle
# SuSe requires
%if 0%{?suse_version}
Requires:  systemd
%{?systemd_requires}
Recommends:     logrotate
%endif


%description
Init program used by the OpenIO Open Source Project. It forks processes
and respawns them as soon as they die. It also provides a simple management
interface through a UNIX socket. Services can be started/stopped/monitored.
OpenIO gridinit is a fork of Redcurrant gridinit, from Worldline by Atos.


%prep
%setup -q -n %{realname}-%{tarversion}


%build
cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DGRIDINIT_SOCK_PATH="/run/%{realname}/%{realname}.sock" \
  .

make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

# Default config file & services directory
%{__mkdir_p} -m755 -v %{buildroot}%{_sysconfdir}/gridinit.d
%{__install} -m644 gridinit.conf %{buildroot}%{_sysconfdir}/gridinit.conf

# Install systemd unit file
%{__mkdir_p} -m755 -v %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE1} %{buildroot}%{_unitdir}/gridinit.service

# Install tmpfiles
%{__mkdir_p} -m755 -v %{buildroot}%{_tmpfilesdir}
%{__install} -m644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/gridinit.conf

# Install rsyslog configuration
%{__mkdir_p} -m755 -v %{buildroot}%{_sysconfdir}/rsyslog.d
%{__install} -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.d/gridinit.conf

# Install logrotate configuration
%{__mkdir_p} -m755 -v %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/gridinit.conf

# Install /run directory
%{__mkdir_p} -m755 -v %{buildroot}/run/%{realname}

# Remove dirty .la
%{__rm} -vf %{buildroot}%{_libdir}/gridinit/*.la

%{__install} -m755 tools/gridinit-syslog-logger %{buildroot}%{_bindir}/gridinit-syslog-logger


%files
%defattr(-,root,root,-)
%{_unitdir}/gridinit.service
%{_bindir}/*
%dir %{_sysconfdir}/gridinit.d
%config(noreplace) %{_sysconfdir}/gridinit.conf
%{_tmpfilesdir}/gridinit.conf
%ghost /run/%{realname}
%config %{_sysconfdir}/rsyslog.d/*
%config %{_sysconfdir}/logrotate.d/*


%pre
%if 0%{?suse_version}
%service_add_pre gridinit.service
%endif


%post
if [ $1 -eq 1 ] ; then
  # Initial installation
  /usr/bin/systemctl preset gridinit.service >/dev/null 2>&1 || :
else
  /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
/usr/bin/systemctl reload-or-restart rsyslog.service || :
%tmpfiles_create %{_tmpfilesdir}/gridinit.conf
%if 0%{?suse_version}
  %service_add_post gridinit.service
%endif


%preun
if [ $1 -eq 0 ] ; then
  # Package removal, not upgrade
  /usr/bin/systemctl --no-reload disable gridinit.service > /dev/null 2>&1 || :
  /usr/bin/systemctl stop gridinit.service > /dev/null 2>&1 || :
fi


%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/usr/bin/systemctl reload-or-restart rsyslog.service || :


%changelog
* Mon Apr 06 2020 - 2.1.0-1 - Jerome Loyet <jerome@openio.io>
- New release
* Tue May 28 2019 - 2.0.2-4 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Apr 26 2019 - 2.0.2-3 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Jan 04 2019 - 2.0.2-2 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Oct 15 2018 - 2.0.2-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Oct 10 2018 - 2.0.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- Remove the gridinit-utils library subpackage
- Remove the gridinit-devel subpackage
- Update glib2 requirement to 2.52
- Remove libevent dependencies
* Wed Jul 11 2018 - 1.7.0-2 - Vincent Legoll <vincent.legoll@openio.io>
- Remove the restart gridinit when upgrading
* Wed Jun 27 2018 - 1.7.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Oct 27 2016 - 1.6-3 - Romain Acciari <romain.acciari@openio.io>
- Add tmpfiles_create at %%post for OpenSuSe
* Sun Apr 17 2016 - 1.6-2 - Romain Acciari <romain.acciari@openio.io>
- /run files are created at package install now
* Mon Feb 29 2016 - 1.6-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Nov 25 2015 - 1.5-1 - Romain Acciari <romain.acciari@openio.io>
- Fix GCC version detection
- Fix default socket path
* Thu Jun 04 2015 - 1.4-3 - Romain Acciari <romain.acciari@openio.io>
- Fix tmpfiles
* Thu Apr 09 2015 - 1.4-1 - Romain Acciari <romain.acciari@openio.io>
- New release to come with OpenIO SDS 0.3
* Thu Mar 19 2015 - 1.3.1-2 - Romain Acciari <romain.acciari@openio.io>
- Fix systemd reload on update
* Thu Mar 19 2015 - 1.3.1-1 - Romain Acciari <romain.acciari@openio.io>
- Fix PREFIX in spec file
- Fix socket path
- Add rsyslog support
- Add logrotate rule
* Wed Mar 18 2015 - 20150310-2 - Romain Acciari <romain.acciari@openio.io>
- Add tmpfiles
- Cleaned spec file
- Moved from /run to /run/gridinit
* Tue Mar 10 2015 - 20150310-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Mar 06 2015 - 20150309-1 - Romain Acciari <romain.acciari@openio.io>
- Fix socket path
- Remove runstatedir (using /run)
* Fri Mar 06 2015 - 20150203-2 - Romain Acciari <romain.acciari@openio.io>
- Fix for systemd
* Tue Feb 03 2015 - 20150203-1 - Romain Acciari <romain.acciari@openio.io>
- Inital release
