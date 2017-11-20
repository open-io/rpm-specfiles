Name:           openio-sds-replicator

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.4.1
Release:        1%{?dist}
%define         tarversion %{version}
%define         jarversion %{version}
Source0:        oio-replicator-%{version}.tar.gz
%define         tardir oio-replicator-%{version}
#curl -u "open-io:$TOKEN" -i https://api.github.com/repos/open-io/oio-replicator/tags
#curl -L https://api.github.com/repos/open-io/oio-replicator/tarball/%{tarversion}?access_token=$TOKEN > ./oio-replicator-%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         jarversion 0.5-SNAPSHOT
Source0:        oio-replicator-%{tag}.tar.gz
%define         tardir open-io-oio-replicator-%{tag}
Epoch:          1
%endif


Summary:        OpenIO SDS replicator service
BuildArch:      noarch
License:        OpenIO Copyright
URL:            https://github.com/open-io/oio-replicator

BuildRequires:  java-1.8.0-openjdk-devel
Requires:       java = 1:1.8.0

%description
OpenIO SDS replicator service.


%prep
%setup -q -n %{tardir}


%build
#OPENIO_API_VERSION=0.6.3 ./gradlew assemble
./gradlew assemble


%install
%{__mkdir_p} -v $RPM_BUILD_ROOT%{_javadir}/openio-sds-replicator
%{__install} -m755 build/libs/openio-sds-replicator-%{jarversion}-all.jar $RPM_BUILD_ROOT%{_javadir}/openio-sds-replicator/
pushd $RPM_BUILD_ROOT%{_javadir}/openio-sds-replicator
  %{__ln_s} openio-sds-replicator-%{jarversion}-all.jar openio-sds-replicator-all.jar
popd


%files
%doc README.md
%{_javadir}/openio-sds-replicator


%changelog
* Mon Aug 28 2017 Romain Acciari <romain.acciari@openio.io> 0.4.1-2
- New release
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-2
- Add a symlink to current version
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-1
- Update to 0.2.1
* Thu Dec 22 2016 Romain Acciari <romain.acciari@openio.io> 0.2-1
- Initial release
