Name:		openio-sds-meta-rebuilder
Version:	1.0
Release:	1%{?dist}
Summary:	OpenIO SDS metadata rebuilder
BuildArch:	noarch

Group:		openio
License:	GPL v3
Source0:	oio-meta1-rebuilder.sh
Source1:	oio-meta2-rebuilder.sh

%description
This package contains rebuilder scripts for meta1 and meta2 databases.


%prep


%build


%install
#%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_sharedstatedir}/oio/sds
%{__install} -m744 %SOURCE0 %{buildroot}%{_sharedstatedir}/oio/sds/oio-meta1-rebuilder.sh
%{__install} -m744 %SOURCE0 %{buildroot}%{_sharedstatedir}/oio/sds/oio-meta1-rebuilder.sh



%files
%defattr(644,root,root)
%config(noreplace) %{_sharedstatedir}/oio/sds/*


%changelog
* Mon Apr 24 2017 - 1.0-1 - sebastien  Lapierre <sebastien.lapierre@openio.io>
- Initial release
