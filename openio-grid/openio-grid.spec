Name:           openio-grid

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

# Grab binaries from github
Source0:        oio-grid-%{tarversion}-linux-amd64.tar.gz

Summary:        OpenIO Grid4Apps
License:        Proprietary
URL:            http://openio.io


%description
TODO


%package client
Summary: G4A client
%description client
TODO


%package server
Summary: G4A server
%description server
TODO


%install
tar zxvf %{SOURCE0}
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_sharedstatedir}/grid/agent/docker
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_bindir}

# Install binary files
%{__install} -m 0755 oio-grid-%{tarversion}-linux-amd64/grid-agent      ${RPM_BUILD_ROOT}%{_bindir}/grid-agent
%{__install} -m 0755 oio-grid-%{tarversion}-linux-amd64/grid-apiserver  ${RPM_BUILD_ROOT}%{_bindir}/grid-apiserver
%{__install} -m 0755 oio-grid-%{tarversion}-linux-amd64/grid-controller ${RPM_BUILD_ROOT}%{_bindir}/grid-controller
%{__install} -m 0755 oio-grid-%{tarversion}-linux-amd64/grid-discovery  ${RPM_BUILD_ROOT}%{_bindir}/grid-discovery
%{__install} -m 0755 oio-grid-%{tarversion}-linux-amd64/gridctl         ${RPM_BUILD_ROOT}%{_bindir}/gridctl


%files client
%defattr(0755,root,root,0755)
%{_bindir}/gridctl


%files server
%defattr(0755,root,root,0755)

%{_sharedstatedir}/grid/agent/docker

%{_bindir}/grid-controller
%{_bindir}/grid-apiserver
%{_bindir}/grid-discovery
%{_bindir}/grid-agent


%changelog
* Wed Oct 03 2018 Vincent Legoll <vincent.legoll@openio.io> - 0.4.0-1
- Initial release
