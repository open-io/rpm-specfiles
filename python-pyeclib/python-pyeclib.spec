%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-pyeclib
Version:        1.4.0
Release:        3%{?dist}
Summary:        Python interface to erasure codes

License:        BSD
URL:            https://bitbucket.org/kmgreen2/pyeclib/
# We pull the tag using git CLI. Save the current command for Source0 below.
#  git archive -o ../pyeclib-1.4.0.tar.gz --prefix=pyeclib-1.4.0/ 1.4.0
Source0:        pyeclib-%{version}.tar.gz

BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif
BuildRequires:  python-setuptools
BuildRequires:  liberasurecode-devel >= 1.4.0

Requires:       liberasurecode >= 1.4.0

%description
This library provides a simple Python interface for implementing erasure
codes. A number of back-end implementations is supported either directly
or through the C interface liberasurecode.

%if 0%{?with_python3}
%package -n python3-pyeclib
Summary:        Python 3 interface to erasure codes

%description -n python3-pyeclib
This library provides a simple Python 3 interface for implementing erasure
codes. A number of back-end implementations is supported either directly
or through the C interface liberasurecode.
%endif

%prep
%setup -q -n pyeclib-%{version}

%if 0%{?with_python3}
# The {py3dir} is a convenience built-in that Fedora provides in F13
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%license License.txt
%doc README.rst
%{_libdir}/python2*/site-packages/*
# There is no __python2_sitearch on F21
#{__python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-pyeclib
%license License.txt
%doc README.rst
%{_libdir}/python3*/site-packages/*
# There is no __python3_sitearch on F21
#{__python3_sitearch}/*
%endif

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-2
- Rebuild for Python 3.6

* Thu Dec 08 2016 Pete Zaitcev <zaitcev@redhat.com> 1.4.0-1
- Upstream 1.4.0, companion with liberasurecode 1.4.0

* Wed Oct 19 2016 Pete Zaitcev <zaitcev@redhat.com> 1.3.1-1
- Update to upstream 1.3.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 03 2016 Pete Zaitcev <zaitcev@redhat.com> 1.2.0-1
- Update to upstream 1.2.0: drop built-in liberasurecode

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 23 2015 Pete Zaitcev <zaitcev@redhat.com> 1.1.0-1
- Update to upstream 1.1.0

* Sun Oct 11 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.9-1
- Update to upstream 1.0.9
- Make py3 conditional for old system releases

* Tue Apr 21 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.7-2
- Correct the reported version from 1.0.5 to 1.0.7
- Address Haikel's comments (#1212148)
- Add BuildRequires: python-setuptools

* Wed Apr 15 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.7-1
- Update to upstream 1.0.7 (asked by Swift with EC and follow-up fixups)

* Thu Apr 02 2015 Pete Zaitcev <zaitcev@redhat.com> 1.0.6-1
- Initial release
