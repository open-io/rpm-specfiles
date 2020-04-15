# __python2 macro doesn't exist for el6
%if 0%{?rhel} == 6
  %global __python2 %{__python}
  %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if 0%{?epel} > 7
  # Do not build python2 package for EPEL7+ since it's included in RHEL
  %global with_python2 0
  # Rename source package so it doesn't conflict with RHEL source package
  %global srpm_py_suffix 3
%else
  %global with_python2 1

  # Rename to python2-dns after Fedora 23
  %if 0%{?fedora} > 23 || 0%{?rhel} > 7
    %global with_p2subpkg 1
    %global python2_pkgversion 2
  %else
    %global python2_pkgversion %{nil}
  %endif
%endif

# Build python3 package for Fedora and EPEL7+
%if 0%{?fedora} > 12 || 0%{?epel} > 6 || 0%{?rhel} > 7
  %global with_python3 1
  %{!?python3_pkgversion: %global python3_pkgversion 3}
%endif

Name:           python%{?srpm_py_suffix}-dns
Version:        1.15.0
Release:        10%{?dist}
Summary:        DNS toolkit for Python

License:        MIT
URL:            http://www.dnspython.org/

Source0: http://www.dnspython.org/kits/%{version}/dnspython-%{version}.tar.gz

BuildArch:      noarch
Patch0:         test_fails_on_missing_file.patch

%if 0%{?rhel} == 6
BuildRequires:  python-unittest2
%endif

# If python2-package
%if 0%{?with_p2subpkg}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-crypto
# If python2 but no python2-package
%else
%if 0%{?with_python2}
Provides:       python2-dns = %{version}-%{release}
Requires:       python-crypto
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-crypto
%endif
%endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-crypto
%endif

%description
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.

%if 0%{?with_p2subpkg}
%package -n python2-dns
Summary:        DNS toolkit for Python 2
%{?python_provide:%python_provide python2-dns}
Requires:       python2-crypto

%description -n python2-dns
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.
%endif

%if 0%{?with_python3}
%package     -n python%{python3_pkgversion}-dns
Summary:        DNS toolkit for Python 3
%{?python_provide:%python_provide python%{python3_pkgversion}-dns}
Requires:       python%{python3_pkgversion}-crypto

%description -n python%{python3_pkgversion}-dns
dnspython3 is a DNS toolkit for Python 3. It supports almost all
record types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython3 provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.
%endif

%prep
%setup -q -n dnspython-%{version}
%patch0 -p1

# strip exec permissions so that we don't pick up dependencies from docs
find examples -type f | xargs chmod a-x

%build
%if 0%{?with_python2}
  %py2_build
%endif

%if 0%{?with_python3}
  %py3_build
%endif

%install
%if 0%{?with_python2}
  %py2_install
%endif

%if 0%{?with_python3}
  %py3_install
%endif

%check
%if 0%{?with_python2}
%{__python2} setup.py test
%endif

%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%if 0%{?with_python2}
%if 0%{?with_p2subpkg}
%files -n python2-dns
%else
%files
%endif
# Add README.* when it is included with the source (commit a906279)
%doc {ChangeLog,LICENSE,examples}
%{python2_sitelib}/*egg-info
%{python2_sitelib}/dns
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-dns
# Add README.* when it is included with the source (commit a906279)
%doc {ChangeLog,LICENSE,examples}
%{python3_sitelib}/*egg-info
%{python3_sitelib}/dns
%endif

%changelog
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Paul Wouters <pwouters@redhat.com> - 1.15.0-8
- Resolves: rhbz#1600418 - NVR of python-dns is lower in rawhide than in f28

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-7
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.15.0-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-2
- Rebuild for Python 3.6

* Tue Oct 04 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.15.0-1
- Latest Release

* Wed Jun 15 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.14.0-1
- Latest Release

* Sun Mar 27 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT99fd864-1
- Latest Snapshot
- Fixed SRPM naming for EPEL7+

* Fri Feb 12 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GITa4774ee-1
- Latest Snapshot
- Drop EPEL5 from master spec
- Patch to support EL6
- Disable python2 package for EPEL7+

* Mon Feb 01 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT465785f-4
- Changed Python2 package name to python2-dns for Fedora 24+

* Fri Jan 22 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT465785f-3
- Using python3_pkgversion to support python34 package in el7
- Build Python3 package for el7+

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0GIT465785f-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep 11 2015 Petr Spacek <pspacek@redhat.com> - 1.12.0GIT465785f
- Rebase to GIT snapshots 465785f85f87508209117264c677080e901e957c (Python 2)
  and 1b0c15086f0e5f6eacc06d77a119280c31731b3c (Python 3)
  to pull in latest fixes

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 18 2014 Paul Wouters <pwouters@redhat.com> - 1.11.1-2
- Added LOC and ECDSA fixes from git (rhbz#1059594)

* Thu Sep  5 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.1-1
- New since 1.11.0:
-
-         Nothing
-
- Bugs fixed since 1.11.1:
-
-         dns.resolver.Resolver erroneously referred to 'retry_servfail'
-         instead of 'self.retry_servfail'.
-
-         dns.tsigkeyring.to_text() would fail trying to convert the
-         keyname to text.
-
-         Multi-message TSIGs were broken for algorithms other than
-         HMAC-MD5 because we weren't passing the right digest module to
-         the HMAC code.
-
-         dns.dnssec._find_candidate_keys() tried to extract the key
-         from the wrong variable name.
-
-         $GENERATE tests were not backward compatible with python 2.4.
-
-         APL RR trailing zero suppression didn't work due to insufficient
-         python 3 porting.   [dnspython3 only]

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.0-2
- Integrate Python 2.6 packaging, EPEL5, EPEL6 support

* Sun Jul  7 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.0-1
- New since 1.10.0:
-
-         $GENERATE support
-
-         TLSA RR support
-
-         Added set_flags() method to dns.resolver.Resolver
-
- Bugs fixed since 1.10.0:
-
-         Names with offsets >= 2^14 are no longer added to the
-         compression table.
-
-         The "::" syntax is not used to shorten a single 16-bit section
-         of the text form an IPv6 address.
-
-         Caches are now locked.
-
-         YXDOMAIN is raised if seen by the resolver.
-
-         Empty rdatasets are not printed.
-
-         DNSKEY key tags are no longer assumed to be unique.

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.10.0-3
- add python3-dns subpackage (rhbz#911933)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Paul Wouters <pwouters@redhat.com> - 1.10.0-1
- Updated to 1.10.0
- Patch to support TLSA RRtype

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 28 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.4-1
-
- dnspython 1.9.4 has been released and is available at
- http://www.dnspython.org/kits/1.9.4/
-
- There is no new functionality in this release; just a few bug fixes
- in RRSIG and SIG code.
-
- I will be eliminating legacy code for earlier versions of DNSSEC in a
- future release of dnspython.

* Fri Mar 25 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.3-1
-
- New since 1.9.2:
-
-     A boolean parameter, 'raise_on_no_answer', has been added to
- the query() methods.  In no-error, no-data situations, this
- parameter determines whether NoAnswer should be raised or not.
- If True, NoAnswer is raised.  If False, then an Answer()
- object with a None rrset will be returned.
-
- Resolver Answer() objects now have a canonical_name field.
-
- Rdata now have a __hash__ method.
-
- Bugs fixed since 1.9.2:
-
-        Dnspython was erroneously doing case-insensitive comparisons
- of the names in NSEC and RRSIG RRs.
-
- We now use "is" and not "==" when testing what section an RR
- is in.
-
- The resolver now disallows metaqueries.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.2-2
- Build Python 2.6 subpackage for EPEL 5

* Tue Nov 23 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.2-1
- It's brown paper bag time :) The fix for the import problems was
- actually bad, but didn't show up in testing because the test suite's
- conditional importing code hid the problem.
-
- Any, 1.9.2 is out.
-
- Sorry for the churn!

* Mon Nov 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.1-1
- New since 1.9.0:
-
-        Nothing.
-
- Bugs fixed since 1.9.0
-
-        The dns.dnssec module didn't work with DSA due to namespace
-        contamination from a "from"-style import.
-
- New since 1.8.0:
-
-        dnspython now uses poll() instead of select() when available.
-
-        Basic DNSSEC validation can be done using dns.dnsec.validate()
-        and dns.dnssec.validate_rrsig() if you have PyCrypto 2.3 or
-        later installed.  Complete secure resolution is not yet
-        available.
-
-        Added key_id() to the DNSSEC module, which computes the DNSSEC
-        key id of a DNSKEY rdata.
-
-        Added make_ds() to the DNSSEC module, which returns the DS RR
-        for a given DNSKEY rdata.
-
-        dnspython now raises an exception if HMAC-SHA284 or
-        HMAC-SHA512 are used with a Python older than 2.5.2.  (Older
-        Pythons do not compute the correct value.)
-
-        Symbolic constants are now available for TSIG algorithm names.
-
- Bugs fixed since 1.8.0
-
-        dns.resolver.zone_for_name() didn't handle a query response
-        with a CNAME or DNAME correctly in some cases.
-
-        When specifying rdata types and classes as text, Unicode
-        strings may now be used.
-
-        Hashlib compatibility issues have been fixed.
-
-        dns.message now imports dns.edns.
-
-        The TSIG algorithm value was passed incorrectly to use_tsig()
-        in some cases.

* Fri Aug 13 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-3
- Add a patch from upstream to fix a Python 2.7 issue.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.8.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 27 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-1.1
- Fix error

* Wed Jan 27 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-1
- New since 1.7.1:
-
-  Support for hmac-sha1, hmac-sha224, hmac-sha256, hmac-sha384 and
-  hmac-sha512 has been contributed by Kevin Chen.
-
-  The tokenizer's tokens are now Token objects instead of (type,
-  value) tuples.
-
- Bugs fixed since 1.7.1:
-
-  Escapes in masterfiles now work correctly.  Previously they were
-  only working correctly when the text involved was part of a domain
-  name.
-
-  When constructing a DDNS update, if the present() method was used
-  with a single rdata, a zero TTL was not added.
-
-  The entropy pool needed locking to be thread safe.
-
-  The entropy pool's reading of /dev/random could cause dnspython to
-  block.
-
-  The entropy pool did buffered reads, potentially consuming more
-  randomness than we needed.
-
-  The entropy pool did not seed with high quality randomness on
-  Windows.
-
-  SRV records were compared incorrectly.
-
-  In the e164 query function, the resolver parameter was not used.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- New since 1.7.0:
-
-        Nothing
-
- Bugs fixed since 1.7.0:
-
-        The 1.7.0 kitting process inadventently omitted the code for the
-        DLV RR.
-
-        Negative DDNS prerequisites are now handled correctly.

* Fri Jun 19 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.0-1
- New since 1.6.0:
-
-        Rdatas now have a to_digestable() method, which returns the
-        DNSSEC canonical form of the rdata, suitable for use in
-        signature computations.
-
-        The NSEC3, NSEC3PARAM, DLV, and HIP RR types are now supported.
-
-        An entropy module has been added and is used to randomize query ids.
-
-        EDNS0 options are now supported.
-
-        UDP IXFR is now supported.
-
-        The wire format parser now has a 'one_rr_per_rrset' mode, which
-        suppresses the usual coalescing of all RRs of a given type into a
-        single RRset.
-
-        Various helpful DNSSEC-related constants are now defined.
-
-        The resolver's query() method now has an optional 'source' parameter,
-        allowing the source IP address to be specified.
-
- Bugs fixed since 1.6.0:
-
-        On Windows, the resolver set the domain incorrectly.
-
-        DS RR parsing only allowed one Base64 chunk.
-
-        TSIG validation didn't always use absolute names.
-
-        NSEC.to_text() only printed the last window.
-
-        We did not canonicalize IPv6 addresses before comparing them; we
-        would thus treat equivalent but different textual forms, e.g.
-        "1:00::1" and "1::1" as being non-equivalent.
-
-        If the peer set a TSIG error, we didn't raise an exception.
-
-        Some EDNS bugs in the message code have been fixed (see the ChangeLog
-        for details).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-3
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-2
- fix license tag

* Tue Dec  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-1
- Update to 1.6.0

* Tue Oct  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-2
- Follow new Python egg packaging specs

* Thu Jan 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-1
- Update to 1.5.0

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-3
- Bump release for rebuild with Python 2.5

* Mon Aug 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-2
- No longer ghost *.pyo files, thus further simplifying the files section.

* Sat Aug  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-1
- Update to 1.4.0
- Remove unneeded python-abi requires
- Remove unneeded python_sitearch macro

* Fri May 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.5-1
- First version for Fedora Extras

