Name:           libdill
Version:        2.13
Release:        1%{?dist}
Summary:        Structured Concurrency for C

License:        MIT/X11
URL:            http://libdill.org
Source0:        https://github.com/sustrik/libdill/archive/%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
Structured Concurrency for C
.
This package contains the shared library.


%prep
%setup -q -n %{name}-%{version}
./autogen.sh


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_libdir}/*
%{_mandir}/*
%{_includedir}/*


%changelog
* Wed Feb 06 2019 Vincent Legoll <vincent.legoll@openio.io> - 2.13
- Initial release 2.13
