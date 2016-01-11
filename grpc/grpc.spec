Name:           grpc
Version:        0.11.1
Release:        1%{?dist}
Summary:        Implementation of the gRPC protocol

License:        BSD
URL:            http://www.grpc.io/
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  libtool
BuildRequires:  protobuf-devel = 3.0.0_beta_1
Requires:       protobuf = 3.0.0_beta_1

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


%build
make %{?_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}


%install
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}

# Makefile fix
%{__mv} %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}


%files
%{_bindir}/*
%{_libdir}/lib*
%{_libdir}/pkgconfig/*
%{_datarootdir}/%{name}
%doc CONTRIBUTING.md LICENSE PATENTS README.md

%files devel
%{_includedir}/%{name}*


%changelog
* Fri Dec 18 2015 Romain Acciari <romain.acciari@openio.io> - 0.11.1-1%{?dist}
- Initial release
