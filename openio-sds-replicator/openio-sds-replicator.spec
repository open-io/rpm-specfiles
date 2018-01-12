Name:           openio-sds-replicator

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.4.4
Release:        1%{?dist}
%define         tarversion %{version}
%define         jarversion %{version}
Source0:        oio-replicator-%{version}.tar.gz
#curl -u 'openio-private:$TOKEN' -i https://api.github.com/repos/openio-private/oio-replicator/tags
#curl -L https://api.github.com/repos/openio-private/oio-replicator/tarball/%{version}?access_token=$TOKEN >%{version}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
%define         jarversion 0.2-SNAPSHOT
Source0:        oio-replicator-%{tag}.tar.gz
Epoch:          1
%endif


Summary:        OpenIO SDS replicator service
BuildArch:      noarch
License:        OpenIO Copyright
URL:            http://gitlab.openio.io/openio/oio-replicator/

BuildRequires:  java-1.8.0-openjdk-devel
Requires:       java = 1:1.8.0

%description
OpenIO SDS replicator service.


%prep
%setup -q -n oio-replicator-%{version}


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
* Fri Jan 12 2018 Vincent Legoll <vincent.legoll@openio.io> 0.4.4-1
- New release
* Tue Dec 12 2017 Vincent Legoll <vincent.legoll@openio.io> 0.4.3-1
- New release
* Mon Dec 04 2017 Vincent Legoll <vincent.legoll@openio.io> 0.4.2-1
- New release
* Mon Aug 28 2017 Romain Acciari <romain.acciari@openio.io> 0.4.1-2
- New release
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-2
- Add a symlink to current version
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-1
- Update to 0.2.1
* Thu Dec 22 2016 Romain Acciari <romain.acciari@openio.io> 0.2-1
- Initial release
