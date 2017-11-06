Name:           python-diamond-openio

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.1
Release:        1%{?dist}
%define         tarversion %{version}
Source0:        https://github.com/open-io/python-diamond-openio/archive/%{version}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         git_repo https://github.com/open-io/python-diamond-openio
Source0:        %{git_repo}/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Diamond collector for OpenIO SDS
License:        Apache v2
URL:            http://openio.io

#BuildRequires:  
Requires:       python-diamond,python-urllib3
Requires:       openio-sds-server

%description
Diamond collector for OpenIO SDS object storage solution.


%prep
%setup -q -n %{name}-%{tarversion}


%build


%install
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datarootdir}/diamond/collectors \
             ${RPM_BUILD_ROOT}%{_sysconfdir}/diamond/collectors
%{__cp} -a collectors/* ${RPM_BUILD_ROOT}%{_datarootdir}/diamond/collectors/
%{__cp} -a conf/* ${RPM_BUILD_ROOT}%{_sysconfdir}/diamond/collectors/


%files
%{_sysconfdir}/diamond/collectors/*
%{_datarootdir}/diamond/collectors/*


%changelog
* Thu Mar 09 2017 Romain Acciari <romain.acciari@openio.io> - 1.0.1-1
- New release
* Tue Feb 21 2017 Romain Acciari <romain.acciari@openio.io> - 1.0.0-1
- New release
* Tue Aug 30 2016 Romain Acciari <romain.acciari@openio.io> - 16.04.1-1
- New release
* Thu May 26 2016 Romain Acciari <romain.acciari@openio.io> - 0.4-1
- New release updated by Vladimir Dombrovski
* Thu May 26 2016 Romain Acciari <romain.acciari@openio.io> - 0.3-1
- New release updated by Florent Vennetier
* Wed Mar 02 2016 Romain Acciari <romain.acciari@openio.io> - 0.2-1
- New release
* Fri Jan 29 2016 Romain Acciari <romain.acciari@openio.io> - 0.1-1%{?dist}
- Initial release
