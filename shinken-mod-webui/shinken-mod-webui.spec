Name:           shinken-mod-webui
Version:        2.2.1
Release:        1%{?dist}
Summary:        Shinken Web User Interface
BuildArch:      noarch

License:        AGPL v3
URL:            https://github.com/shinken-monitoring/mod-webui/
Source0:        https://github.com/shinken-monitoring/mod-webui/archive/%{version}.tar.gz

#BuildRequires:  
Requires:       python-bottle,python-requests,python-arrow,python-passlib

%description
Shinken self sufficient Web User Interface.


%prep
%setup -q -n mod-webui-%{version}


%build


%install
%{__mkdir_p} $RPM_BUILD_ROOT/var/lib/shinken/modules/webui2 \
             $RPM_BUILD_ROOT/etc/shinken/modules
%{__cp} -aR module/* $RPM_BUILD_ROOT/var/lib/shinken/modules/webui2/
%{__cp} -aR etc/modules/* $RPM_BUILD_ROOT/etc/shinken/modules/


%files
%doc README.md LICENSE
/var/lib/shinken/modules/webui2
/etc/shinken/modules/*



%changelog
* Mon Mar 21 2016 Romain Acciari <romain.acciari@openio.io> - 2.2.1-1
- Initial release
