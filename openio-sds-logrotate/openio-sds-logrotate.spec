Name:		openio-sds-logrotate
Version:	1.1
Release:	1%{?dist}
Summary:	OpenIO SDS logrotate configuration
BuildArch:	noarch

Group:		openio
License:	GPL v3
Source0:	openio-sds-logrotate.conf

Requires:	logrotate

%description
This package contains logrotate configuration for the OpenIO SDS solution.


%prep


%build


%install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m644 %SOURCE0 %{buildroot}%{_sysconfdir}/logrotate.d/openio-sds


%files
%defattr(644,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/*


%changelog
* Mon Jan 11 2016 - 1.1-1 - Romain Acciari <romain.acciari@openio.io>
- Add proxy service support
* Thu Mar 19 2015 - 1.0-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
