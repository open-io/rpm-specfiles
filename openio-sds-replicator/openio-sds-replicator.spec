Name:           openio-sds-replicator

%if %{?_with_test:0}%{!?_with_test:1}
Version:        0.2.1
Release:        2%{?dist}
%define         tarversion %{version}
%define         jarversion %{version}
Source0:        oio-replicator-%{version}.tar.gz
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
#Requires:       

%description
OpenIO SDS replicator service.


%prep
#%setup -q -n oio-replicator.git
%setup -q -n oio-replicator-%{version}-05ba394e23c3f37bf036051c1ee6624adbc58b16


%build
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
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-2
- Add a symlink to current version
* Fri Dec 23 2016 Romain Acciari <romain.acciari@openio.io> 0.2.1-1
- Update to 0.2.1
* Thu Dec 22 2016 Romain Acciari <romain.acciari@openio.io> 0.2-1
- Initial release
