%global modname eventlet
%{?python_enable_dependency_generator}

Name:           python-%{modname}
Version:        0.25.2
Release:        1%{?dist}
Summary:        Highly concurrent networking library
License:        MIT
URL:            http://eventlet.net
Source0:        %{pypi_source %{modname}}
BuildArch:      noarch

%description
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.

%package -n python2-%{modname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-dns >= 1.15.0
BuildRequires:  python2dist(enum34)
BuildRequires:  python2-greenlet >= 0.3
BuildRequires:  python2-monotonic >= 1.4
BuildRequires:  python2-six >= 1.10.0
BuildRequires:  python2-pyOpenSSL
Requires:       python-dns >= 1.15.0
Requires:       python2dist(enum34)
Requires:       python2-greenlet >= 0.3
Requires:       python2-monotonic >= 1.4
Requires:       python2-six >= 1.10.0
Requires:       python2-pyOpenSSL

%description -n python2-%{modname}
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.

%package -n python3-%{modname}
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python36-dns >= 1.15.0
BuildRequires:  python3-greenlet >= 0.3
BuildRequires:  python3-monotonic >= 1.4
BuildRequires:  python3-six >= 1.10.0
BuildRequires:  python36-pyOpenSSL
Requires:       python36-dns >= 1.15.0
Requires:       python3-greenlet >= 0.3
Requires:       python3-monotonic >= 1.4
Requires:       python3-six >= 1.10.0
Requires:       python36-pyOpenSSL

%description -n python3-%{modname}
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.

%package -n python2-%{modname}-doc
Summary:        Documentation for python2-%{modname}

%description -n python2-%{modname}-doc
%{summary}.

%package -n python3-%{modname}-doc
Summary:        Documentation for python3-%{modname}

%description -n python3-%{modname}-doc
%{summary}.

%prep
%autosetup -n %{modname}-%{version} -p1
rm -vrf *.egg-info
# Remove dependency on enum-compat from setup.py. enum-compat is installed
# as Require for python2 subpackage and it is not needed for Python 3
sed -i "/'enum-compat',/d" setup.py

%build
%py2_build
%py3_build

export PYTHONPATH=$(pwd)

%install
%py2_install
rm -vrf %{buildroot}%{python2_sitelib}/tests
# FIXME: Those files are not meant to be used with Python 2.7
# Anyway the whole module eventlet.green.http is Python 3 only
# Trying to import it will fail under Python 2.7
# https://github.com/eventlet/eventlet/issues/369
rm -rf %{buildroot}/%{python2_sitelib}/%{modname}/green/http/{cookiejar,client}.py
%py3_install
rm -vrf %{buildroot}%{python3_sitelib}/tests

%files -n python2-%{modname}
%doc README.rst AUTHORS LICENSE NEWS
%license LICENSE
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-*.egg-info/

%files -n python3-%{modname}
%doc README.rst AUTHORS LICENSE NEWS
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info/

%files -n python2-%{modname}-doc
%license LICENSE

%files -n python3-%{modname}-doc
%license LICENSE

%changelog
* Mon Jul 20 2020 Vincent Legoll <vincent.legoll@gmail.com> - 0.25.2-1
- new version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.24.1-2
- use python dependency generator

* Sun Oct 14 2018 Kevin Fenzi <kevin@scrye.com> - 0.24.1-1
- Update to 0.24.1. Fixes bug #1611023

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-1
- Update to 0.23.0 (#1575434)
- Add patch for Python 3.7 (#1594248)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.22.1-2
- Rebuilt for Python 3.7

* Sun Feb 18 2018 Kevin Fenzi <kevin@scrye.com> - 0.22.1-1
- Update to 0.22.1. Fixes bug #1546471

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-1
- Update to 0.22.0

* Tue Oct  3 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 0.21.0-3
- Fix upstream #401
- Fix compat with PyOpenSSL 17.3.0
- Cleanup BR

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Lumír Balhar <lbalhar@redhat.com> - 0.21.0-1
- Upstream 0.21.0
- Fix issue with enum-compat dependency for dependent packages
- Enable tests
- Fix tracebacks during docs generating by install python[23]-zmq

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
