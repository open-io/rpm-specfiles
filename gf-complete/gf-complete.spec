Name:           gf-complete
Version:        1
Release:        1%{?dist}
Summary:        A Comprehensive Open Source Library for Galois Field Arithmetic

Group:          Librairies
License:        BSD
URL:            http://web.eecs.utk.edu/~plank/plank/www/software.html
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  autoconf,automake,libtool
#Requires:       

%description
A Comprehensive Open Source Library for Galois Field Arithmetic.


%package	tools
Summary:	A Comprehensive Open Source Library for Galois Field Arithmetic
Group:		Tools
Requires:	gf-complete = %{version}
%description	tools
Tools for gf-complete.


%package	devel
Summary:	A Comprehensive Open Source Library for Galois Field Arithmetic
Group:		Development
Requires:	gf-complete = %{version}
%description	devel
Headers for gf-complete.


%prep
%setup -q


%build
autoreconf -i
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libgf_complete.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/lib*

%files tools
%defattr(-,root,root,-)
%{_prefix}/bin/gf_*

%files devel
%defattr(-,root,root,-)
%{_prefix}/include/gf_*


%changelog
* Mon Feb 02 2015 <romain.acciari@openio.io> - 1-1
- Initial release
