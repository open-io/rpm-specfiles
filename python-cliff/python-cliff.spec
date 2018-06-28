%if 0%{?fedora}
%global with_python3 1
%endif

%global modname cliff

Name:             python-cliff
Version:          1.13.0
Release:          2%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/cliff
Source0:          https://files.pythonhosted.org/packages/79/73/ac43a3774b313803f48af67a01ee29f184f385a3aa727bea25a7fb78f3a7/cliff-1.13.0.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-prettytable
BuildRequires:    python-cmd2 >= 0.6.7
BuildRequires:    python-stevedore
BuildRequires:    python-six >= 1.9.0

# Required for the test suite
BuildRequires:    python-nose
BuildRequires:    python-mock
BuildRequires:    bash
BuildRequires:    bash-completion

Requires:         python-setuptools
Requires:         python-prettytable
Requires:         python-cmd2 >= 0.6.7
Requires:         python-stevedore
Requires:         python-six >= 1.9.0

%if %{?rhel}%{!?rhel:0} == 6
BuildRequires:    python-argparse
Requires:         python-argparse
%endif


%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-prettytable
BuildRequires:    python3-cmd2 >= 0.6.7
BuildRequires:    python3-stevedore
BuildRequires:    python3-six
BuildRequires:    python3-nose
BuildRequires:    python3-mock
%endif

%description
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/

%if 0%{?with_python3}
%package -n python3-cliff
Summary:        Command Line Interface Formulation Framework
Group:          Development/Libraries

Requires:         python3-setuptools
Requires:         python3-prettytable
Requires:         python3-cmd2 >= 0.6.7
Requires:         python3-stevedore
Requires:         python3-six

%description -n python3-cliff
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/
%endif

%prep
%setup -q -n %{modname}-%{version}

# let RPM handle deps
rm -f requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

%check
PYTHONPATH=. nosetests

%if 0%{?with_python3}
pushd %{py3dir}
sed -i 's/nosetests/nosetests-%{python3_version}/' cliff/tests/test_help.py
PYTHONPATH=. nosetests-%{python3_version}
popd
%endif


%files
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS announce.rst CONTRIBUTING.rst
%{python_sitelib}/%{modname}
%{python_sitelib}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS announce.rst CONTRIBUTING.rst
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-%{version}-*
%endif

%changelog
* Tue Aug 25 2015 Romain Acciari <romain.acciari@openio.io> 1.13.0-2
- Add version to python-six require

* Thu Jun 25 2015 Alan Pevec <alan.pevec@redhat.com> 1.13.0-1
- Update to upstream 1.13.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Ralph Bean <rbean@redhat.com> - 1.10.0-2
- Remove setuptools dep on argparse.

* Wed Mar 04 2015 Ralph Bean <rbean@redhat.com> - 1.10.0-1
- new version
- Update list of files packages under %%doc.
- Explicitly package the license file.

* Mon Sep 22 2014 Alan Pevec <alan.pevec@redhat.com> 1.7.0-1
- Update to upstream 1.7.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Apr 17 2014 Ralph Bean <rbean@redhat.com> - 1.6.1-1
- Latest upstream.

* Tue Jan 28 2014 Ralph Bean <rbean@redhat.com> - 1.6.0-1
- Latest upstream.
- Add dep on python-pbr (python build reasonableness)
- Add dep on python-stevedore
- Add build requirements on python-nose, python-mock, and bash
- Change check to use 'nosetests' directly.
- Remove bundled egg-info

* Thu Nov 14 2013 Ralph Bean <rbean@redhat.com> - 1.4.5-1
- Latest upstream.
- Remove patch now that the latest cmd2 and pyparsing are required.

* Thu Nov 14 2013 Ralph Bean <rbean@redhat.com> - 1.4.4-2
- Enable python3 subpackage now that python3-pyparsing is available.
- Adjust patch to simplify pyparsing setuptools constraints further.

* Fri Sep 13 2013 Pádraig Brady <pbrady@redhat.com> - 1.4.4-1
- Latest upstream.

* Tue Aug 06 2013 Ralph Bean <rbean@redhat.com> - 1.4-1
- Latest upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Ralph Bean <rbean@redhat.com> - 1.3.2-1
- Latest upstream.
- Patched pyparsing version constraint for py2.
- Modernized python3 conditional.
- Temporarily disabled python3 subpackage for python3-pyparsing dep.
- Added temporary explicit dependency on python3-pyparsing>=2.0.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Ralph Bean <rbean@redhat.com> - 1.3-1
- Latest upstream.
- Enabled python3 subpackage.
- Remove requirement on python-tablib

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 06 2012 Ralph Bean <rbean@redhat.com> - 1.0-3
- Require python-argparse on epel.

* Thu Jul 05 2012 Ralph Bean <rbean@redhat.com> - 1.0-2
- Manually disable python3 support until python3-prettytable is available.

* Thu Jun 28 2012 Ralph Bean <rbean@redhat.com> - 1.0-1
- initial package for Fedora
