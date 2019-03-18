%define tarname openio-netdata-plugins

Name:           openio-netdata-plugins

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.4.0
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
Source0:        %{git_repo}/archive/%{tarversion}.tar.gz

Source1:        https://github.com/go-redis/redis/archive/v6.12.0.tar.gz

Summary:        OpenIO Plugins for netdata
License:        AGPL-3.0
URL:            http://www.openio.io/

BuildRequires:  golang       >= 1.8


%description
OpenIO Plugins for netdata


%prep
%setup -q -n %{tarname}-%{tarversion}
cd ..
tar xf %{SOURCE1}
mkdir -p go/src/github.com/go-redis
cd go/src
ln -s ../../%{tarname}-%{tarversion} oionetdata
cd github.com/go-redis
ln -s ../../../../redis-* redis


%build
export GOPATH=${GOPATH:-$(go env GOPATH)}:$(pwd)/../go
go build cmd/openio.plugin/openio.plugin.go
go build cmd/zookeeper.plugin/zookeeper.plugin.go
go build cmd/container.plugin/container.plugin.go
go build cmd/command.plugin/command.plugin.go
go build cmd/fs.plugin/fs.plugin.go


%install
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_libexecdir}/netdata/plugins.d
%{__install} -m 0755 \
    openio.plugin \
    zookeeper.plugin \
    container.plugin \
    command.plugin \
    fs.plugin \
    ${RPM_BUILD_ROOT}%{_libexecdir}/netdata/plugins.d
# Looks like bare golang's `go build` don't do the required linker magic
# http://fedoraproject.org/wiki/Releases/FeatureBuildId
%undefine _missing_build_ids_terminate_build


%files
%defattr(755,root,root,755)
%{_libexecdir}/netdata/plugins.d/openio.plugin
%{_libexecdir}/netdata/plugins.d/zookeeper.plugin
%{_libexecdir}/netdata/plugins.d/command.plugin
# By default netdata will run all the plugins in plugin.d directory, which
# is not the intended behavior. The plugins below won't be set executable
# by default, and will instead be selectively activated when deploying.
%attr(644,root,root) %{_libexecdir}/netdata/plugins.d/container.plugin
%attr(644,root,root) %{_libexecdir}/netdata/plugins.d/fs.plugin


%changelog
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
