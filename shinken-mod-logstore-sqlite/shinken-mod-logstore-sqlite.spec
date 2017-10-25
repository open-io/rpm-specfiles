%define modname logstore-sqlite

Name:           shinken-mod-%{modname}
Version:        1.4.1
Release:        1%{?dist}
Summary:        Shinken module for exporting logs to a sqlite db
BuildArch:      noarch

License:        AGPL v3
URL:            https://github.com/shinken-monitoring/mod-%{modname}/
Source0:        https://github.com/shinken-monitoring/mod-%{modname}/archive/%{version}.tar.gz

#BuildRequires:  
#Requires:       

%description
Shinken module for exporting logs to a sqlite db from the Livestatus module.


%prep
%setup -q -n mod-%{modname}-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/var/lib/shinken/modules/%{modname} \
             $RPM_BUILD_ROOT/etc/shinken/modules
%{__cp} -aR module/* $RPM_BUILD_ROOT/var/lib/shinken/modules/%{modname}/
%{__cp} -aR etc/modules/* $RPM_BUILD_ROOT/etc/shinken/modules/


%files
%doc README* LICENSE
/var/lib/shinken/modules/%{modname}
/etc/shinken/modules/*


%changelog
* Mon Mar 21 2016 Romain Acciari <romain.acciari@openio.io> - 1.4.1-1
- Initial release
