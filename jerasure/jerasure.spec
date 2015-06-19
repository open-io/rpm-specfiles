Name:           jerasure
Version:        2
Release:        1%{?dist}
Summary:        A Library in C Facilitating Erasure Coding for Storage Applications

Group:          Libraries
License:        BSD
URL:            https://bitbucket.org/jimplank/jerasure
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  gf-complete-devel
Requires:       gf-complete

%description
A Library in C Facilitating Erasure Coding for Storage Applications.


%package	tools
Summary:        A Library in C Facilitating Erasure Coding for Storage Applications
Group:          Libraries
Requires:	jerasure = %{version}
%description	tools
Tools for jerasure library.


%package	devel
Summary:        A Library in C Facilitating Erasure Coding for Storage Applications
Group:          Libraries
Requires:	jerasure = %{version}
Requires:	gf-complete-devel
%description	devel
Headers for jerasure library.

%prep
%setup -q


%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/libJerasure.la


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libJerasure.so*

%files tools
%defattr(-,root,root,-)
%{_prefix}/bin/*

%files devel
%defattr(-,root,root,-)
%{_prefix}/include/*
#%{_prefix}/include/jerasure


%changelog
* Mon Feb 02 2015 - 2-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
