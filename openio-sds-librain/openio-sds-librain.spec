%define tarname librain

Name:		openio-sds-librain

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.0.0
Release:        1%{?dist}
%define         tarversion %{version}
Source0:        https://github.com/open-io/librain/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
Version:        test%{date}.%{tag}
Release:        0%{?dist}
%define         tarversion %{tag}
Source0:        https://github.com/open-io/librain/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Rain library for OpenIO SDS solution
License:        MIT
URL:            https://github.com/open-io/librain/
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires:  cmake
BuildRequires:  jerasure-devel

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
%setup -q -n %{tarname}-%{tarversion}
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
* Mon Mar 14 2016 - Romain Acciari <romain.acciari@openio.io> - 1.0.0-1
- New release
* Mon Feb 02 2015 - Romain Acciari <romain.acciari@openio.io> - 0.8-1
- Initial release
