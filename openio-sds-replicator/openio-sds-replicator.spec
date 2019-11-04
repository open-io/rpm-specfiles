Name:           openio-sds-replicator

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.0
Release:        1%{?dist}
%define         tarversion %{version}
%define         jarversion %{version}
%define         gradlew_args -Pbuild.type=release
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         gradlew_args -Pdummy=nothing
%define         tarversion %{tag}
%define         jarversion 0.5-SNAPSHOT
Epoch:          1
%endif

#curl -u "open-io:$TOKEN" -i https://api.github.com/repos/open-io/oio-replicator/tags
#curl -L https://api.github.com/repos/open-io/oio-replicator/tarball/%{tarversion}?access_token=$TOKEN > ./oio-replicator-%{tarversion}.tar.gz
Source0:        oio-replicator-%{tarversion}.tar.gz

Summary:        OpenIO SDS replicator service
BuildArch:      noarch
License:        OpenIO Copyright
URL:            https://github.com/open-io/oio-replicator

BuildRequires:  java-1.8.0-openjdk-devel
Requires:       java = 1:1.8.0

%description
OpenIO SDS replicator service.


%prep
%setup -q -n oio-replicator-%{version}

%build
#OPENIO_API_VERSION=0.6.3 ./gradlew %{gradlew_args} assemble
./gradlew %{gradlew_args} assemble
gradle --stop


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
* Wed Jul 17 2019 Romain Acciari <romain.acciari@openio.io> 1.0.0-1
- New release
* Fri Jun 14 2019 Vincent Legoll <vincent.legoll@openio.io> 0.5.4-1
- New release
* Thu Apr 18 2019 Vincent Legoll <vincent.legoll@openio.io> 0.5.3-1
- New release
* Fri Jan 04 2019 Vincent Legoll <vincent.legoll@openio.io> 0.5.2-1
- New release
* Fri Jan 04 2019 Vincent Legoll <vincent.legoll@openio.io> 0.5.1-1
- New release
* Mon Dec 10 2018 Vincent Legoll <vincent.legoll@openio.io> 0.5.0-1
- New release
* Fri Jan 12 2018 Vincent Legoll <vincent.legoll@openio.io> 0.4.4-1
- New release
* Tue Dec 12 2017 Vincent Legoll <vincent.legoll@openio.io> 0.4.3-1
- New release
* Mon Dec 04 2017 Vincent Legoll <vincent.legoll@openio.io> 0.4.2-1
- New release
* Mon Aug 28 2017 Romain Acciari <romain.acciari@openio.io> 0.4.1-1
- New release
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-2
- Add a symlink to current version
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-1
- Update to 0.2.1
* Thu Dec 22 2016 Romain Acciari <romain.acciari@openio.io> 0.2-1
- Initial release
