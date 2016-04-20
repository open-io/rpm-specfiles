Name:		openio-sds-logrotate
Version:	1.3
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
* Wed Apr 20 2016 - 1.3-1 - Sebastien Lapierre <sebastien.lapierre@openio.io>
- Fix deleted file symptom for http-errors.log
* Fri Mar 18 2016 - 1.2-1 - Romain Acciari <romain.acciari@openio.io>
- Add event, account, rdir
* Mon Jan 11 2016 - 1.1-1 - Romain Acciari <romain.acciari@openio.io>
- Add proxy service support
* Thu Mar 19 2015 - 1.0-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
