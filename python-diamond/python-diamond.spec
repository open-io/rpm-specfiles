%define         realname diamond
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-%{realname}
Version:        4.0.515
Release:        2%{?dist}
Summary:        Smart data producer for graphite graphing package

License:        MIT
URL:            https://github.com/python-diamond/Diamond
Source0:        https://files.pythonhosted.org/packages/0c/b6/4c58a8a1111c138fbed9e65dd918be706af8abd07bb5e8fe3ddfb453d899/diamond-%{version}.tar.gz

BuildRequires:  python >= 2.7
Requires:       python >= 2.7
Requires:       python-configobj

%description
Diamond is a python daemon that collects system metrics and publishes
them to Graphite (and others). It is capable of collecting cpu, memory,
network, i/o, load and disk metrics. Additionally, it features an API
for implementing custom collectors for gathering metrics from almost
any source.


%prep
%setup -q -n diamond-%{version}


%build


%install
%{__python} setup.py install -O1 \
  --root=$RPM_BUILD_ROOT \
  --record=INSTALLED_FILES

# Install default configuration
%{__mkdir_p} -v $RPM_BUILD_ROOT/etc/diamond
%{__install} -v -m644 conf/diamond.conf.example $RPM_BUILD_ROOT/etc/diamond/diamond.conf

# Install systemctl configuration file
%{__mkdir_p} -v $RPM_BUILD_ROOT/usr/lib/systemd/system
%{__install} -v -m644 rpm/systemd/diamond.service $RPM_BUILD_ROOT/usr/lib/systemd/system/diamond.service

# Remove useless init.d configuration file
%{__rm} -vrf $RPM_BUILD_ROOT/etc/init.d


%pre
getent group diamond > /dev/null || /usr/sbin/groupadd -r diamond
getent passwd diamond > /dev/null || /usr/sbin/useradd -r -g diamond \
  -d /var/lib/diamond -s /sbin/nologin diamond

%post
if [ $1 -eq 1 ] ; then
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
/bin/systemctl try-restart diamond status >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
  /bin/systemctl --no-reload disable diamond.service >/dev/null 2>&1 || :
  /bin/systemctl stop diamond.service >/dev/null 2>&1 || :
fi

%postun
if [ $1 -eq 0 ] ; then
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%files
%doc LICENSE
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_datarootdir}/*
/usr/lib/systemd/system/*
%{python_sitelib}/*
%{_localstatedir}/log/*


%changelog
* Tue Jul 04 2017 - 4.0.515-2 - Romain Acciari <romain.acciari@openio.io>
- Add python-configobj dependency
* Tue Feb 28 2017 - 4.0.515-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Jan 05 2016 - 20160105.git41a3cf0-1 - Romain Acciari <romain.acciari@openio.io>
- Add patch to support InfluxDB 0.9 (only)
* Mon Jan 04 2016 - 20160104.git41a3cf0-1 - Romain Acciari <romain.acciari@openio.io>
- Update to last git
* Thu Feb 05 2015 - 0.4-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
