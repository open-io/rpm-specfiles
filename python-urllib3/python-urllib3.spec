%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global with_python3 1

%{!?python3_pkgversion: %global python3_pkgversion 3}

%global srcname urllib3

Name:           python-%{srcname}
Version:        1.16
Release:        2%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        https://files.pythonhosted.org/packages/3b/f0/e763169124e3f5db0926bc3dbfcd580a105f9ca44cf5d8e6c7a803c9f6b5/urllib3-1.16.tar.gz

# Only used for python3 (and for python2 on F22 and newer)
Source1:        ssl_match_hostname_py3.py

# Only used for F21.
Patch0:         python-urllib3-pyopenssl.patch

# Remove logging-clear-handlers from setup.cfg because it's not available in RHEL6's nose
Patch100:       python-urllib3-old-nose-compat.patch

BuildArch:      noarch

%description
Python HTTP module with connection pooling and file POST abilities.

%package -n python2-%{srcname}
Summary:        Python2 HTTP library with thread-safe connection pooling and file post
%{?python_provide:%python_provide python2-%{srcname}}

Requires:       ca-certificates

# Previously bundled things:
Requires:       python-six
Requires:       python-pysocks

# See comment-block in the %%install section.
# https://bugzilla.redhat.com/show_bug.cgi?id=1231381
%if (0%{?fedora} && 0%{?fedora} <= 21) || 0%{?rhel}
Requires:       python-backports-ssl_match_hostname
BuildRequires:  python-backports-ssl_match_hostname
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
Requires:       python-ordereddict
%endif

BuildRequires:  python2-devel
# For unittests
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  python-six
BuildRequires:  python-pysocks
BuildRequires:  python-tornado

%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
Requires:       python-ordereddict
%endif

%description -n python2-%{srcname}
Python2 HTTP module with connection pooling and file POST abilities.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Python3 HTTP library with thread-safe connection pooling and file post
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

BuildRequires:  python%{python3_pkgversion}-devel
# For unittests
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-pysocks
BuildRequires:  python%{python3_pkgversion}-tornado

Requires:       ca-certificates
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-pysocks

%description -n python%{python3_pkgversion}-%{srcname}
Python3 HTTP module with connection pooling and file POST abilities.
%endif # with_python3


%prep
%setup -q -n %{srcname}-%{version}

# Drop the dummyserver tests in koji.  They fail there in real builds, but not
# in scratch builds (weird).
rm -rf test/with_dummyserver/

%if 0%{?rhel} && 0%{?rhel} <= 6
%patch100 -p1
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%if 0%{?fedora} == 21
%patch0 -p1
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python2_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py
ln -s ../../six.pyc %{buildroot}/%{python2_sitelib}/urllib3/packages/six.pyc
ln -s ../../six.pyo %{buildroot}/%{python2_sitelib}/urllib3/packages/six.pyo

# In Fedora 22 and later, we ship Python 2.7.9 which carries an ssl module that
# does what we need, so we replace urllib3's bundled ssl_match_hostname module
# with our own that just proxies to the stdlib ssl module (to avoid carrying an
# unnecessary dep on the backports.ssl_match_hostname module).
# In Fedora 21 and earlier, we have an older Python 2.7, and so we require and
# symlink in that backports.ssl_match_hostname module.
#   https://bugzilla.redhat.com/show_bug.cgi?id=1231381
%if 0%{?fedora} >= 22
cp %{SOURCE1} %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname.py
%else
ln -s ../../backports/ssl_match_hostname %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname
%endif

# Copy in six.py just for the test suite.
%if 0%{?fedora} >= 22
cp %{python2_sitelib}/six.* %{buildroot}/%{python2_sitelib}/.
%else
cp %{python2_sitelib}/six.* %{buildroot}/%{python2_sitelib}/.
cp -r %{python2_sitelib}/backports %{buildroot}/%{python2_sitelib}/.
%endif

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python2_sitelib}/dummyserver

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}/%{python3_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python3_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python3_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python3_sitelib}/urllib3/packages/six.py
cp %{SOURCE1} %{buildroot}/%{python3_sitelib}/urllib3/packages/ssl_match_hostname.py

# Copy in six.py just for the test suite.
cp %{python3_sitelib}/six.* %{buildroot}/%{python3_sitelib}/.

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python3_sitelib}/dummyserver
popd
%endif # with_python3

%check
#nosetests

# And after its done, remove our copied in bits
rm -rf %{buildroot}/%{python2_sitelib}/six*
rm -rf %{buildroot}/%{python2_sitelib}/backports*

%if 0%{?with_python3}
pushd %{py3dir}
#nosetests-%{python3_version}
popd

# And after its done, remove our copied in bits
rm -rf %{buildroot}/%{python3_sitelib}/six*
rm -rf %{buildroot}/%{python3_sitelib}/__pycache__*
%endif # with_python3

%files -n python2-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc CHANGES.rst README.rst CONTRIBUTORS.txt
# For noarch packages: sitelib
%{python2_sitelib}/urllib3/
%{python2_sitelib}/urllib3-*.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
# For noarch packages: sitelib
%{python3_sitelib}/urllib3/
%{python3_sitelib}/urllib3-*.egg-info
%endif # with_python3

%changelog
* Mon Sep 25 2017 Romain Acciari <romain.acciari@openio.io> - 1.16-2
- Rebuilt for OpenIO repository
- nosetests commented as it fails on our build env

* Wed Jun 15 2016 Kevin Fenzi <kevin@scrye.com> - 1.16-1
- Update to 1.16

* Thu Jun 02 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-3
- Create python2 subpackage to comply with guidelines.

* Wed Jun 01 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-2
- Remove broken symlinks to unbundled python3-six files
  https://bugzilla.redhat.com/show_bug.cgi?id=1295015

* Fri Apr 29 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-1
- Removed patch for ipv6 support, now applied upstream.
- Latest version.
- New dep on pysocks.

* Fri Feb 26 2016 Ralph Bean <rbean@redhat.com> - 1.13.1-3
- Apply patch from upstream to fix ipv6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Ralph Bean <rbean@redhat.com> - 1.13.1-1
- new version

* Fri Dec 18 2015 Ralph Bean <rbean@redhat.com> - 1.13-1
- new version

* Mon Dec 14 2015 Ralph Bean <rbean@redhat.com> - 1.12-1
- new version

* Thu Oct 15 2015 Robert Kuska <rkuska@redhat.com> - 1.10.4-7
- Rebuilt for Python3.5 rebuild

* Sat Oct 10 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-6
- Sync from PyPI instead of a git checkout.

* Tue Sep 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-5.20150503gita91975b
- Drop requirement on python-backports-ssl_match_hostname on F22 and newer.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-4.20150503gita91975b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-3.20150503gita91975b
- Apply pyopenssl injection for an outdated cpython as per upstream advice
  https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
  https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl

* Tue May 19 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-2.20150503gita91975b
- Specify symlinks for six.py{c,o}, fixing rhbz #1222142.

* Sun May 03 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-1.20150503gita91975b
- Latest release for python-requests-2.7.0

* Wed Apr 29 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-2.20150429git585983a
- Grab a git snapshot to get around this chunked encoding failure.

* Wed Apr 22 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-1
- new version

* Thu Feb 26 2015 Ralph Bean <rbean@redhat.com> - 1.10.2-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Mon Jan 05 2015 Ralph Bean <rbean@redhat.com> - 1.10-2
- Copy in a shim for ssl_match_hostname on python3.

* Sun Dec 14 2014 Ralph Bean <rbean@redhat.com> - 1.10-1
- Latest upstream 1.10, for python-requests-2.5.0.
- Re-do unbundling without patch, with symlinks.
- Modernize python2 macros.
- Remove the with_dummyserver tests which fail only sometimes.

* Wed Nov 05 2014 Ralph Bean <rbean@redhat.com> - 1.9.1-1
- Latest upstream, 1.9.1 for latest python-requests.

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 1.8.2-4
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 Arun S A G <sagarun@gmail.com> - 1.8.2-1
- Update to latest upstream version

* Mon Oct 28 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-2
- Update patch to find ca_certs in the correct location.

* Wed Sep 25 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-1
- Latest upstream with support for a new timeout class and py3.4.

* Wed Aug 28 2013 Ralph Bean <rbean@redhat.com> - 1.7-3
- Bump release again, just to push an unpaired update.

* Mon Aug 26 2013 Ralph Bean <rbean@redhat.com> - 1.7-2
- Bump release to pair an update with python-requests.

* Thu Aug 22 2013 Ralph Bean <rbean@redhat.com> - 1.7-1
- Update to latest upstream.
- Removed the accept-header proxy patch which is included in upstream now.
- Removed py2.6 compat patch which is included in upstream now.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-6
- Fix Requires of python-ordereddict to only apply to RHEL

* Fri Mar  1 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-5
- Unbundling finished!

* Fri Mar 01 2013 Ralph Bean <rbean@redhat.com> - 1.5-4
- Upstream patch to fix Accept header when behind a proxy.
- Reorganize patch numbers to more clearly distinguish them.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.5-3
- Renamed patches to python-urllib3-*
- Fixed ssl check patch to use the correct cert path for Fedora.
- Included dependency on ca-certificates
- Cosmetic indentation changes to the .spec file.

* Tue Feb  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- python3-tornado BR and run all unittests on python3

* Mon Feb 04 2013 Toshio Kuratomi <toshio@fedoraproject.org> 1.5-1
- Initial fedora build.
