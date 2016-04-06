%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           beanstalkc

Version:        0.4.0
Release:        1%{?dist}
Source0:        https://pypi.python.org/packages/source/b/beanstalkc/beanstalkc-%{version}.tar.gz

Summary:        A simple beanstalkd client library
License:        Apache 2.0
URL:            http://github.com/earl/beanstalkc

BuildArch:      noarch
BuildRequires:  python-setuptools


%description
Beanstalkc is a simple beanstalkd client library for Python.
Beanstalkd is a fast, distributed, in-memory workqueue service.


%prep
%setup -q


%build


%install
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc LICENSE README.mkd TUTORIAL.mkd
%{python_sitelib}/*


%changelog
* Mon Apr 04 2016 Romain Acciari <romain.acciari@openio.io> - 0.4.0-1
- Initial release
