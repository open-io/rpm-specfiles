%if 0%{?fedora}
%global with_python3 1
%endif

%global modname tablib

Name:             python-tablib
Version:          0.10.0
Release:          1%{?dist}
Summary:          Format agnostic tabular data library (XLS, JSON, YAML, CSV)

License:          MIT
URL:              http://github.com/kennethreitz/tablib
Source0:          https://pypi.python.org/packages/source/t/tablib/%{modname}-%{version}.tar.gz
BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
Requires:         PyYAML

%description
Tablib is a format-agnostic tabular dataset library, written in Python.

Output formats supported:

 - Excel (Sets + Books)
 - JSON (Sets + Books)
 - YAML (Sets + Books)
 - HTML (Sets)
 - TSV (Sets)
 - CSV (Sets)

%if 0%{?with_python3}
%package -n python3-tablib
Summary:        Format agnostic tabular data library (XLS, JSON, YAML, CSV)

BuildRequires:    python-tools
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
Requires:         python3-PyYAML

%description -n python3-tablib
Tablib is a format-agnostic tabular dataset library, written in Python.

Output formats supported:

 - Excel (Sets + Books)
 - JSON (Sets + Books)
 - YAML (Sets + Books)
 - HTML (Sets)
 - TSV (Sets)
 - CSV (Sets)

%endif

%prep
%setup -q -n %{modname}-%{version}

# Remove shebangs
for lib in $(find . -name "*.py"); do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
pushd %{py3dir}
sed -i "/\(xlwt\|odf\|xlrd\|openpyxl\|openpyxl\..*\|yaml\)'/d" setup.py
find . -name "*.py" | grep -v 3 | xargs 2to3 -w
popd
%endif

sed -i '/tablib.packages.*3/d' setup.py


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
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}


%files
%license LICENSE
%doc README.rst AUTHORS
%{python2_sitelib}/%{modname}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{modname}
%license
%doc README.rst AUTHORS
%{python3_sitelib}/%{modname}
%{python3_sitelib}/*.egg-info
%endif


%changelog
* Wed Aug 05 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.10.0-1
- Upstream 0.10.0
- Enable python3 subpackage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11.20120702git752443f-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11.20120702git752443f-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11.20120702git752443f-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11.20120702git752443f-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11.20120702git752443f-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 06 2012 Ralph Bean <rbean@redhat.com> - 0.9.11.20120702git752443f-5
- Disable python3 for now since the package is so unstable.

* Fri Jul 06 2012 Ralph Bean <rbean@redhat.com> - 0.9.11.20120702git752443f-4
- Patch to fix broken setup.py

* Wed Jul 04 2012 Ralph Bean <rbean@redhat.com> - 0.9.11.20120702git752443f-3
- Removed shebangs.

* Wed Jul 04 2012 Ralph Bean <rbean@redhat.com> - 0.9.11.20120702git752443f-2
- Added link to upstream bug for patch.

* Thu Jun 28 2012 Ralph Bean <rbean@redhat.com> - 0.9.11.20120702git752443f-1
- Initial package for Fedora
