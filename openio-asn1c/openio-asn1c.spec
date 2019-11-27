%define		realname asn1c

Name:		openio-%{realname}
Version:	0.9.28
Release:	1%{?dist}
Summary:	Free, Open Source ASN.1 compiler

License:	BSD
URL:		http://lionet.info/asn1c
Source0:	https://github.com/vlm/asn1c/archive/v%{version}.tar.gz
%if 0%{?suse_version}
Source1:	%{name}-rpmlintrc
%endif

BuildRequires:	autoconf,automake,libtool
#Requires:	
Provides:   asn1c

%description
Compiles ASN.1 data structures into C source structures that can be
simply marshalled to/unmarshalled from: BER, DER, CER, BASIC-XER,
CXER, EXTENDED-XER, PER.


%prep
%setup -q -n %{realname}-%{version}
autoreconf -iv


%build
%configure --docdir=%{_defaultdocdir}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%{__rm} -rf $RPM_BUILD_ROOT/%{_libdir}/*.la # Clean useless files

# --docdir option is broken
%{__mkdir_p} $RPM_BUILD_ROOT/%{_defaultdocdir}
%{__mv} $RPM_BUILD_ROOT/%{_datadir}/doc/%{realname} \
        $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}-%{version}

%files
#%doc BUGS COPYING ChangeLog FAQ README.md
#%doc TODO doc/asn1c-quick.pdf doc/asn1c-usage.pdf
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{realname}
%{_defaultdocdir}/%{name}-%{version}


%changelog
* Wed Nov 27 2019 Florent Vennetier <florent@openio.io> - 0.9.28-1
- Compile the official version again

* Sun Jan 31 2016 Florent Venntier <florent.vennetier@openio.io> - 0.9.27.1-1
- Compile custom OpenIO version

* Tue Feb 03 2015 Romain Acciari <romain.acciari@openio.io> - 0.9.27-1
- Initial release
