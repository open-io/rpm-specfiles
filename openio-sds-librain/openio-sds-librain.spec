Name:		openio-sds-librain
Version:	0.8
Release:	1%{?dist}
Summary:	Rain library for OpenIO SDS solution

Group:		openio
License:	MIT
URL:		https://mirrors.atosworldline.com/external/
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires: cmake
BuildRequires: jerasure-devel

%description
A Library in C/C++ Facilitating Erasure Coding for Storage Applications.


%package devel
Summary: Include files for RAIN library
Group: openio
Requires: %{name} = %{version}
Provides: librain-devel
%description devel
Header files for OpenIO SDS RAIN library.


%prep
%setup -q
sed -i -e "s@jerasure/jerasure.h@jerasure.h@g" librain.c


%build
cmake \
  -DPREFIX=%{_prefix} \
  -DJERASURE_INCDIR=%{_includedir}/jerasure \
  .
%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/librain.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/librain.h


%changelog
* Mon Feb 02 2015 - 0.8-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
