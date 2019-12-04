# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%{!?_licensedir:%global license %%doc}

%global pypi_name eventlet

%global with_python3 1

Name:           python-%{pypi_name}
Version:        0.20.1
Release:        6%{?dist}
Epoch:          1
Summary:        Highly concurrent networking library
License:        MIT
URL:            http://eventlet.net
Source0:        https://pypi.io/packages/source/e/eventlet/eventlet-%{version}.tar.gz
Patch1:         0001-dns-hosts-file-was-consulted-after-nameservers.patch
Patch2:         0002-greendns-don-t-contact-nameservers-if-one-entry-is-r.patch
Patch3:         0001-Fix-bad-ipv6-comparison.patch
Patch4:         0002-greendns-udp-Fix-infinite-loop-when-source-address-m.patch
Patch5:         0003-tests-Add-ipv6-tests-for-greendns-udp-function.patch
Patch6:         0004-tests-Add-ipv4-udp-tests-for-greendns.patch
Patch7:         0001-greendns-Treat-etc-hosts-entries-case-insensitive.patch
Patch8:         0005-case-insensitive-hundred-continue.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-greenlet

Requires:       python-greenlet

%description
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.


%package -n python2-%{pypi_name}
Summary:        Highly concurrent networking library

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-greenlet

#%{?python_provide:%python_provide python2-%{pypi_name}}
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name} = %{version}-%{release}
Obsoletes:  python-%{pypi_name} < 0.17.4-3

%description -n python2-%{pypi_name}
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.


%if 0%{?with_python3}
%package -n python3-eventlet
Summary:        Highly concurrent networking library
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-greenlet

Requires:       python3-greenlet

#%{?python_provide:%python_provide python3-eventlet}

%description -n python3-eventlet
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.
%endif


%package -n python2-%{pypi_name}-doc
Summary:        Documentation for %{name}
BuildRequires:  python-sphinx

%{?python_provide:%python_provide python2-%{pypi_name}-doc}
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name}-doc = %{version}-%{release}
Obsoletes:  python-%{pypi_name}-doc < 0.17.4-3

%description -n python2-%{pypi_name}-doc
Documentation for the python-eventlet package.

%if 0%{?with_python3}
%package -n python3-eventlet-doc
Summary: Documentation for python3-eventlet-doc
BuildRequires:  python3-sphinx

%description -n python3-eventlet-doc
Documentation for the python-eventlet package.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf *.egg-info
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
popd

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
popd
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}/%{python3_sitelib}/tests
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}/%{python2_sitelib}/tests
# FIXME: Those files are not meant to be used with Python 2.7
# Anyway the whole module eventlet.green.http is Python 3 only
# Trying to import it will fail under Python 2.7
# https://github.com/eventlet/eventlet/issues/369
rm -rf %{buildroot}/%{python2_sitelib}/%{pypi_name}/green/http/{cookiejar,client}.py


%files -n python2-%{pypi_name}
%doc README.rst AUTHORS LICENSE NEWS
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst AUTHORS LICENSE NEWS
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python2-%{pypi_name}-doc
%license LICENSE
%doc doc/_build/html

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc doc/_build/html
%endif

%changelog
* Tue Sep 03 2019 Vincent Legoll <vincent.legoll@openio.io> 0.20.1-6
- repackaged for OpenIO
- Added patch for case-insensitive "100-continue" header
- Epoch set to 1

* Fri Aug 10 2018 Lon Hohberger <lon@redhat.com> 0.20.1-6
- Add ipv4 tests for bz1607967
- Treat names as case-insensitive (rhbz#1612541)

* Wed Aug 08 2018 Lon Hohberger <lon@redhat.com> 0.20.1-5
- Fix ipv6 address handling (rhbz#1607967)

* Mon Aug 06 2018 Daniel Alvarez <dalvarez@redhat.com> - 0.20.1-3
- Don't contact nameservers if there's at least one entry in /etc/hosts, lp#1785615

* Fri Jun 09 2017 Ihar Hrachyshka <ihrachys@redhat.com> - 0.20.1-2
- Consult /etc/hosts before resolving with DNS, lp#1696094

* Tue Apr 25 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 0.20.1-1
- Upstream 0.20.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.18.4-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 25 2016 Kevin Fenzi <kevin@scrye.com> - 0.18.4-1
- Update to 0.18.4. Fixes bug #1329993

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Oct 19 2015 Jon Schlueter <jschluet@redhat.com> 0.17.4-4
- greenio: send() was running empty loop on ENOTCONN rhbz#1268351

* Thu Sep 03 2015 Pádraig Brady <pbrady@redhat.com> - 0.17.4-3
- Tighten up Provides: and Obsoletes: for previous change

* Tue Sep 01 2015 Chandan Kumar <chkumar246@gmail.com> - 0.17.4-2
- Added python3 support

* Wed Jul 22 2015 Pádraig Brady <pbrady@redhat.com> - 0.17.4-1
- Latest upstream

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Pádraig Brady <pbrady@redhat.com> - 0.17.3-1
- Latest upstream

* Tue Mar 31 2015 Pádraig Brady <pbrady@redhat.com> - 0.17.1-1
- Latest upstream

* Tue Sep 02 2014 Pádraig Brady <pbrady@redhat.com> - 0.15.2-1
- Latest upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Alan Pevec <apevec@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Pádraig Brady <P@draigBrady.com - 0.12.0-1
- Update to 0.12.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Pádraig Brady <P@draigBrady.com - 0.9.17-2
- fix waitpid() override to not return immediately

* Fri Aug 03 2012 Pádraig Brady <P@draigBrady.com - 0.9.17-1
- Update to 0.9.17

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Pádraig Brady <P@draigBrady.com - 0.9.16-6
- Update patch to avoid leak of _DummyThread objects

* Mon Mar  5 2012 Pádraig Brady <P@draigBrady.com - 0.9.16-5
- Fix patch to avoid leak of _DummyThread objects

* Wed Feb 29 2012 Pádraig Brady <P@draigBrady.com - 0.9.16-4
- Apply a patch to avoid leak of _DummyThread objects

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Pádraig Brady <P@draigBrady.com - 0.9.16-2
- Apply a patch to support subprocess.Popen implementations
  that accept the timeout parameter, which is the case on RHEL >= 6.1

* Sat Aug 27 2011 Kevin Fenzi <kevin@scrye.com> - 0.9.16-1
- Update to 0.9.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.12-1
- Updated to version 0.9.12.

* Wed Jul 28 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.9-1
- Updated to version 0.9.9.

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.7-1
- Initial package version.
