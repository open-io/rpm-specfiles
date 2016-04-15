Name:           shinken-mod-livestatus
Version:        1.4
Release:        1%{?dist}
Summary:        Livestatus API is the modern method of interacting with Shinken
BuildArch:      noarch

License:        AGPL v3
URL:            https://github.com/shinken-monitoring/mod-livestatus/
Source0:        https://github.com/shinken-monitoring/mod-livestatus/archive/%{version}.tar.gz

#BuildRequires:  
Requires:       shinken-broker,shinken-mod-logstore-sqlite

%description
Livestatus API is the modern method of interacting with Shinken and Nagios
based systems alike.

Originally developed for Nagios, MK Livetstatus, was re-implemented in Python
for use with Shinken by professional developers. The access methods and query
languages are the same.


%prep
%setup -q -n mod-livestatus-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/var/lib/shinken/modules/livestatus \
             $RPM_BUILD_ROOT/etc/shinken/modules
%{__cp} -aR module/* $RPM_BUILD_ROOT/var/lib/shinken/modules/livestatus/
%{__cp} -aR etc/modules/* $RPM_BUILD_ROOT/etc/shinken/modules/


%files
%doc README.rst LICENSE
/var/lib/shinken/modules/livestatus
/etc/shinken/modules/*


%changelog
* Mon Mar 21 2016 Romain Acciari <romain.acciari@openio.io> - 1.4-1
- Initial release
