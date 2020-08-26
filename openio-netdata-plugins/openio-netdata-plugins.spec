%global debug_package %{nil}
%define tarname openio-netdata-plugins

Name:           openio-netdata-plugins

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.5.8
Release:        1%{?dist}
%define         tarversion %{version}
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
Epoch:          1
%endif

%define         git_repo https://github.com/open-io/%{tarname}
Source:        %{git_repo}/archive/%{tarversion}.tar.gz


Summary:        OpenIO Plugins for netdata
License:        AGPL-3.0
URL:            http://www.openio.io/

BuildRequires:  curl


%description
OpenIO Plugins for netdata


%prep
if ! curl -qs github.com; then
  echo "No network available, please use --enable-network as arguement to mock" >/dev/stderr
  exit 1
fi
%setup -q -n %{tarname}-%{tarversion}
curl -Lqsko - https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz | tar -xzf - go/{bin,pkg,src}

%build
PATH=./go/bin:${PATH} make build


%install
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_libexecdir}/netdata/plugins.d
%{__install} -m 0755 \
    openio.plugin \
    zookeeper.plugin \
    container.plugin \
    command.plugin \
    fs.plugin \
    s3roundtrip.plugin \
    ${RPM_BUILD_ROOT}%{_libexecdir}/netdata/plugins.d


%files
%defattr(755,root,root,755)
%{_libexecdir}/netdata/plugins.d/openio.plugin
%{_libexecdir}/netdata/plugins.d/zookeeper.plugin
%{_libexecdir}/netdata/plugins.d/command.plugin
%{_libexecdir}/netdata/plugins.d/fs.plugin
%{_libexecdir}/netdata/plugins.d/container.plugin
%{_libexecdir}/netdata/plugins.d/s3roundtrip.plugin


%changelog
* Wed Aug 26 2020 - 0.5.8-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Tue Aug 25 2020 - 0.5.7-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Wed Jul 15 2020 - 0.5.6-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Fri May 24 2019 - 0.5.0-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Mon Mar 18 2019 - 0.4.0-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Wed Oct 31 2018 - 0.3.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Aug 28 2018 - 0.2.17-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Jul 09 2018 - 0.2.16-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Jun 26 2018 - 0.2.14-1 - Vincent Legoll <vincent.legoll@openio.io>
- Initial release
