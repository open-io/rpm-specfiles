Name:		openio-sds-rsyslog
Version:	1.2
Release:	1%{?dist}
Summary:	OpenIO SDS rsyslog configuration
BuildArch:	noarch

Group:		openio
License:	GPL v3
Source0:	openio-sds-rsyslog.conf

Requires:	rsyslog >= 3.20
Requires:	openio-sds-server

%description
OpenIO SDS rsyslog configuration.


%prep


%build


%install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rsyslog.d
%{__install} -m644 %{SOURCE0} %{buildroot}%{_sysconfdir}/rsyslog.d/openio-sds.conf


%post
# Add a rsyslog configuration directory (if not present)
/bin/grep -q '^$IncludeConfig /etc/rsyslog.d/\*.conf' /etc/rsyslog.conf
if [ $? -ne 0 ] ; then
  echo "Adding /etc/rsyslog.d to your config file directory in /etc/rsyslog.conf"
  echo '# Proceeding custom config files first' >/etc/rsyslog.conf.tmp
  echo '$IncludeConfig /etc/rsyslog.d/*.conf' >>/etc/rsyslog.conf.tmp
  echo >>%{_sysconfdir}/rsyslog.conf.tmp
  /bin/cat %{_sysconfdir}/rsyslog.conf >>%{_sysconfdir}/rsyslog.conf.tmp
  /bin/mv -f %{_sysconfdir}/rsyslog.conf.tmp %{_sysconfdir}/rsyslog.conf
fi
/usr/bin/systemctl reload-or-restart rsyslog.service

%postun
/usr/bin/systemctl reload-or-restart rsyslog.service


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rsyslog.d/openio-sds.conf


%changelog
* Fri Mar 06 2015 - 1.2-1 - Romain Acciari <romain.acciari@openio.io>
- Fixes directories and filenames
* Tue Feb 17 2015 - 1.1-1 - Romain Acciari <romain.acciari@openio.io>
- Fix syslogtag
* Fri Feb 13 2015 - 1.0-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
