%define         realname gridinit

Name:           openio-%{realname}
%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.6
Release:        3%{?dist}
%define         tarversion %{version}
Source0:        https://github.com/open-io/gridinit/archive/v%{version}.tar.gz
%else
%define         date %(date +"%Y%m%d%H%M")
Version:        test%{date}.%{tag}
Release:        0%{?dist}
%define         tarversion %{tag}
Source0:        https://github.com/open-io/gridinit/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

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
BuildRequires:  autoconf,automake,libtool
BuildRequires:  git,bison,flex,cmake
BuildRequires:  glib2-devel    >= 2.28.8
BuildRequires:  libevent-devel >= 2.0
%if 0%{?suse_version}
BuildRequires:  systemd
BuildRequires:  rsyslog
%endif

Requires:       glib2         >= 2.28.8
Requires:       libevent      >= 2.0
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-utils  = %{version}
%else
Requires:       %{name}-utils  = 1:%{version}
%endif
# SuSe requires
%if 0%{?suse_version}
Requires:  systemd
%endif


%description
Init program used by the OpenIO Open Source Project. It forks processes
and respawns them as soon as they die. It also provides a simple management
interface through a UNIX socket. Services can be started/stopped/monitored.
OpenIO gridinit is a fork of Redcurrant gridinit, from Worldline by Atos.


%package        utils
Summary:        Grid Init utilities libraries
License:        AGPL-3.0+
Requires:       glib2 >= 2.28.8
%description    utils
C code library with children processes management features. This library is
internally used by the gridinit process.

%package        devel
Summary:        Grid Init devel headers
License:        AGPL-3.0+
%if %{?_with_test:0}%{!?_with_test:1}
Requires:       %{name}-utils  = %{version}
%else
Requires:       %{name}-utils  = 1:%{version}
%endif
%description    devel
Devel files for OpenIO gridinit.


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

# Default config file
%{__mkdir_p} -m755 %{buildroot}%{_sysconfdir}/%{realname}
%{__install} -m644 gridinit.conf.default %{buildroot}%{_sysconfdir}/%{realname}/gridinit.conf

# Install init script
%{__mkdir_p} -m755 %{buildroot}%{_libdir}/systemd/system
%{__install} -m644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/gridinit.service

# Install tmpfiles
%{__mkdir_p} -m755 -v ${RPM_BUILD_ROOT}%{_prefix}/lib/tmpfiles.d
%{__install} -m644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/lib/tmpfiles.d/gridinit.conf

# Install rsyslog configuration
%{__mkdir_p} -m755 -v ${RPM_BUILD_ROOT}/etc/rsyslog.d
%{__install} -m644 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rsyslog.d/gridinit.conf

# Install logrotate configuration
%{__mkdir_p} -m755 -v ${RPM_BUILD_ROOT}/etc/logrotate.d
%{__install} -m644 %{SOURCE4} ${RPM_BUILD_ROOT}/etc/logrotate.d/gridinit.conf

# Install /run directory
%{__mkdir_p} -m755 -v %{buildroot}/run/%{realname}

# Remove dirty .la
%{__rm} -vf %{buildroot}%{_libdir}/gridinit/*.la


%files
%defattr(-,root,root,-)
%{_libdir}/systemd/system/gridinit.service
%{_bindir}/*
%dir %{_sysconfdir}/%{realname}
%config(noreplace) %{_sysconfdir}/%{realname}/*
%{_prefix}/lib/tmpfiles.d/*
%ghost /run/%{realname}
%config %{_sysconfdir}/rsyslog.d/*
%config %{_sysconfdir}/logrotate.d/*

%files utils
%defattr(-,root,root,-)
%{_libdir}/libgridinit-utils.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libgridinit-utils.so


%post
if [ $1 -eq 1 ] ; then 
  # Initial installation 
  /usr/bin/systemctl preset gridinit.service >/dev/null 2>&1 || : 
else
  /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || : 
fi
/usr/bin/systemctl reload-or-restart rsyslog.service || : 
%if 0%{?suse_version}
  %tmpfiles_create %_tmpfilesdir/gridinit.conf
%endif
%preun
if [ $1 -eq 0 ] ; then 
  # Package removal, not upgrade 
  /usr/bin/systemctl --no-reload disable gridinit.service > /dev/null 2>&1 || : 
  /usr/bin/systemctl stop gridinit.service > /dev/null 2>&1 || : 
fi
%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || : 
if [ $1 -ge 1 ] ; then 
  # Package upgrade, not uninstall 
  /usr/bin/systemctl try-restart gridinit.service >/dev/null 2>&1 || : 
fi
/usr/bin/systemctl reload-or-restart rsyslog.service || : 

%post utils
/sbin/ldconfig
%postun utils
/sbin/ldconfig


%changelog
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
