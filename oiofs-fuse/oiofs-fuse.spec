%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           oiofs-fuse

%if %{?_with_test:0}%{!?_with_test:1}
Version:        2.1.0
Release:        0%{?dist}
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

Source0:        https://vincent-legoll:%{token}@github.com/open-io/oio-fs/archive/%{tarversion}.tar.gz

Summary:        OpenIO FileSystem FUSE adapter
License:        Proprietary
URL:            http://openio.io

BuildRequires:  gcc-c++
#BuildRequires:  protobuf-devel >= 3.0
#BuildRequires:  grpc-devel >= 1.0
BuildRequires:  hiredis-devel
BuildRequires:  fuse-devel
BuildRequires:  glib2-devel
#BuildRequires:  glog-devel, gflags-devel, json-c-devel
BuildRequires:  json-c-devel
BuildRequires:  cmake >= 2.8.12
BuildRequires:  python-setuptools
BuildRequires:  libsoup-devel
BuildRequires:  libattr-devel

BuildRequires:  openio-sds-common-devel >= 4.0

Requires:       fuse-libs
Requires:       fuse >= 2.9.2
Requires:       libsoup
#Requires:       glog
#Requires:       grpc >= 1.0
#Requires:       protobuf >= 3.0

Requires:       openio-sds-common >= 4.0

%description
oiofs FUSE is a FUSE adapter that allows you to mount OpenIO SDS
containers as filesystems on Linux systems.
oiofs FUSE provides another means to access OpenIO SDS Storage.


#%package -n python-openio-oiofs-client
#Summary: Python files for OpenIO oiofs
#Requires:       python-openio-sds-client
#%description -n python-openio-oiofs-client
#Python files for OpenIO oiofs.


%prep
%setup -q -n open-io-oio-fs-%{tarversion}


%build
cmake \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DOIOSDS_INCDIR=%{_includedir} \
  -DOIOSDS_LIBDIR=%{_libdir} \
  .

#PBR_VERSION=%{version} %{__python} setup.py build

%install
%{makeinstall} DESTDIR=%{buildroot}
#PBR_VERSION=%{version} %{__python} ./setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
#%doc
%{_sbindir}/*
#%{_libdir}/*

#%files -n python-openio-oiofs-client
#%{python_sitelib}/oiofs*



%changelog
* Wed Jun 13 2018 Vincent Legoll <vincent.legoll@openio.io> - 2.1.0
- New release
* Tue Jun 05 2018 Vincent Legoll <vincent.legoll@openio.io> - 2.1.0.c1
- New release
* Tue May 15 2018 Vincent Legoll <vincent.legoll@openio.io> - 2.0.0
- New release
* Tue Mar 21 2017 Romain Acciari <romain.acciari@openio.io> - 1.0.0.c3
- New release
* Thu Oct 20 2016 Romain Acciari <romain.acciari@openio.io> - 1.0.0.c2
- Initial release
