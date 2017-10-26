Name:           gf-complete
Version:        1.03
Release:        1%{?dist}
Summary:        A Comprehensive Open Source Library for Galois Field Arithmetic

Group:          Librairies
License:        BSD
URL:            http://lab.jerasure.org/jerasure/gf-complete/
Source0:        http://lab.jerasure.org/jerasure/gf-complete/repository/archive.tar.gz?ref=363da207236617b1d50f04bb191a14f0de364303
Patch0:         do-not-use-sse-ac-ext.patch

BuildRequires:  autoconf,automake,libtool
#Requires:       

%description
A Comprehensive Open Source Library for Galois Field Arithmetic.


%package        tools
Summary:        A Comprehensive Open Source Library for Galois Field Arithmetic
Group:          Tools
Requires:       gf-complete = %{version}
%description    tools
Tools for gf-complete.


%package        devel
Summary:        A Comprehensive Open Source Library for Galois Field Arithmetic
Group:          Development
Requires:       gf-complete = %{version}
%description    devel
Headers for gf-complete.


%prep
%setup -q -n %{name}-master
%patch0 -p1


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
* Thu Dec 03 2015 <romain.acciari@openio.io> - 1.03-1%{?dist}
- New old release 1.03
- Add patch to build on Fedora 23
- New URL and Source (Issue open-io/rpm-specfiles#2)
* Mon Feb 02 2015 <romain.acciari@openio.io> - 1-1%{?dist}
- Initial release
