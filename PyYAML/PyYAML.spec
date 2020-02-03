%global with_python3 1
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           PyYAML
Version:        3.12
Release:        2%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
BuildRequires:  python-devel, python-setuptools, libyaml-devel
BuildRequires:  Cython
BuildRequires:  libyaml-devel
Provides:       python-yaml = %{version}-%{release}
Provides:       python-yaml%{?_isa} = %{version}-%{release}
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python36-Cython
%endif
# debian patch, upstream ticket http://pyyaml.org/ticket/247 and
# https://bitbucket.org/xi/pyyaml/issue/35/test-fails-on-be-s390-x-ppc64
#Patch0: debian-big-endian-fix.patch

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if 0%{?with_python3}
%package -n python36-PyYAML
Provides: python3-PyYAML = %{version}-%{release}
Summary: YAML parser and emitter for Python
Group: Development/Libraries

%description -n python36-PyYAML
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif


%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1 -b .be
chmod a-x examples/yaml-highlight/yaml_hl.py

# remove pre-generated file
rm -rf ext/_yaml.c


%build
# regenerate ext/_yaml.c
CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build_ext

%if 0%{?with_python3}
rm -rf %{py3dir}
# ext/_yaml.c is needed
cp -a . %{py3dir}
pushd %{py3dir}
CFLAGS="${RPM_OPT_FLAGS}" %{__python3} setup.py --with-libyaml build
popd
%endif

CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif


%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES PKG-INFO README examples
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python36-PyYAML
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES PKG-INFO README examples
%{python3_sitearch}/*
%endif


%changelog
* Mon Feb 03 2020 Vincent Legoll <vincent.legoll@openio.io> - 3.12-2
- python3-PyYAML => python36-PyYAML

* Mon Oct 08 2018 Romain Acciari <romain.acciari@openio.io> - 3.12-1
- New upstream release 3.12

* Mon Sep 15 2014 Jakub Čajka <jcajka@redhat.com> - 3.11-6
- fixed typecast issues using debian patch(int->size_t)(BZ#1140189)
- spec file cleanup

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 3.11-4
- fix license handling

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 John Eckersberg <jeckersb@redhat.com> - 3.11-1
- New upstream release 3.11 (BZ#1081521)

* Thu Aug  8 2013 John Eckersberg <jeckersb@redhat.com> - 3.10-9
- Add check section and run test suite

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug  1 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-5
- remove rhel logic from with_python3 conditional

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 John Eckersberg <jeckersb@redhat.com> - 3.10-3
- Add Provides for python-yaml (BZ#740390)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 John Eckersberg <jeckersb@redhat.com> - 3.10-1
- New upstream release 3.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 John Eckersberg <jeckersb@redhat.com> - 3.09-7
- Add support to build for python 3

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.09-6
- Bump release number for upgrade path

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.09-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 3.09-1
- New upstream release 3.09

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 - John Eckersberg <jeckersb@redhat.com> - 3.08-5
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce inclusion of libyaml in build with --with-libyaml option to setup.py
- Deliver to %%{python_sitearch} instead of %%{python_sitelib} due to _yaml.so
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-4
- Correction, change libyaml to libyaml-devel in BuildRequires

* Mon Mar 2 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-3
- Add libyaml to BuildRequires

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.06-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 John Eckersberg <jeckersb@redhat.com> - 3.06-1
- New upstream release

* Wed Jan 02 2008 John Eckersberg <jeckersb@redhat.com> - 3.05-2
- Remove explicit dependency on python >= 2.3
- Remove executable on example script in docs

* Mon Dec 17 2007 John Eckersberg <jeckersb@redhat.com> - 3.05-1
- Initial packaging for Fedora
