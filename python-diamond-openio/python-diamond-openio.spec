Name:           python-diamond-openio
Version:        0.2
Release:        1%{?dist}
Summary:        Diamond collector for OpenIO SDS

License:        Apache v2
URL:            http://openio.io
Source0:        openiosds.py

#BuildRequires:  
Requires:       python-diamond,python-oiopy,python-urllib3

%description
Diamond collector for OpenIO SDS object storage solution.


%prep
#%setup -q


%build


%install
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datarootdir}/diamond/collectors/openiosds
%{__install} -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_datarootdir}/diamond/collectors/openiosds/openiosds.py


%files
%{_datarootdir}/diamond/collectors/openiosds


%changelog
* Wed Mar 02 2016 Romain Acciari <romain.acciari@openio.io> - 0.2-1%{?dist}
- New release
* Fri Jan 29 2016 Romain Acciari <romain.acciari@openio.io> - 0.1-1%{?dist}
- Initial release
