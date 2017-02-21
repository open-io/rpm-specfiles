%define nanopb_version 0.3.6

Name:           grpc
Version:        1.0.1
Release:        1%{?dist}
Summary:        Implementation of the gRPC protocol

License:        BSD
URL:            http://www.grpc.io/
Source0:        https://github.com/grpc/grpc/archive/v%{version}.tar.gz
#Source1:        https://github.com/nanopb/nanopb/archive/nanopb-%{nanopb_version}.tar.gz

BuildRequires:  libtool
BuildRequires:  protobuf-devel >= 3.0.0
BuildRequires:  gperftools-devel
BuildRequires:  openssl-devel
Requires:       protobuf >= 3.0.0

%description
Remote Procedure Calls (RPCs) provide a useful abstraction for
building distributed applications and services. The libraries
in this repository provide a concrete implementation of the gRPC
protocol, layered over HTTP/2. These libraries enable communication
between clients and servers using any combination of the supported
languages.


%package devel
Summary: gRPC headers
Requires: %{name} = %{version}-%{release}

%description devel
This package contains gRPC headers


%prep
%setup -q
#tar xf %{SOURCE1} -C third_party
#rm -rf third_party/nanopb
#mv third_party/nanopb-nanopb-%{nanopb_version} third_party/nanopb
sed -r 's|^PROTOBUF_CHECK_CMD = \$\(PKG_CONFIG\) --atleast-version=[^[:space:]]+ protobuf|PROTOBUF_CHECK_CMD = $(PKG_CONFIG) --atleast-version=3.0.0 protobuf|' -i Makefile


%build
make %{?_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}


%install
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}

# Makefile fix
%{__mv} %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}


%files
%{_bindir}/*
%{_libdir}/lib*
%{_datarootdir}/%{name}
%doc CONTRIBUTING.md LICENSE PATENTS README.md

%files devel
%{_includedir}/%{name}*
%{_libdir}/pkgconfig/*


%changelog
* Thu Jan 19 2017 Romain Acciari <romain.acciari@openio.io> - 1.0.1-1
- Bugfix release
* Wed Sep 07 2016 Romain Acciari <romain.acciari@openio.io> - 1.0.0-1
- Updated to 1.0.0
* Wed Feb 24 2016 Romain Acciari <romain.acciari@openio.io> - 0.13.0-1
- New release
- Fix pkgconfig
* Fri Dec 18 2015 Romain Acciari <romain.acciari@openio.io> - 0.11.1-1
- Initial release
