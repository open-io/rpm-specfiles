%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           openio-sds-swift

%if %{?_with_test:0}%{!?_with_test:1}
Version:        1.11.0
Release:        1%{?dist}
%define         tarversion %{version}
Source0:        https://github.com/open-io/oio-swift/archive/%{tarversion}.tar.gz
%else
# Testing purpose only. Do not modify.
%define         date %(date +"%Y%m%d%H%M")
%global         shortcommit %(c=%{tag}; echo ${c:0:7})
Version:        test%{date}.git%{shortcommit}
Release:        0%{?dist}
%define         tarversion %{tag}
Source0:        https://github.com/open-io/oio-swift/archive/%{tarversion}.tar.gz
Epoch:          1
%endif

Summary:        Swift proxy for OpenIO SDS
License:        Apache License v2
URL:            http://www.openio.io/

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       openio-sds-common
Requires:       openstack-swift-proxy
Requires:       python-lxml


%description
Swift proxy for OpenIO SDS.

%prep
%setup -q -n oio-swift-%{tarversion}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*
%{_bindir}/oioswift-*


%changelog
* Tue Nov 12 2019 - 1.11.0-1 - Florent Vennetier <florent@openio.io>
- New release: 1.11.0
- Include oioswift-proxy-server binary
- Build with -O1 flag
* Fri Aug 16 2019 - 1.9.3-1 - Vladimir Dombrovski <vladimir@openio.io>
- New release
* Wed Mar 27 2019 - 1.7.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Feb 05 2019 - 1.6.5.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Jan 18 2019 - 1.6.5-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Jan 11 2019 - 1.6.4-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Jan 11 2019 - 1.6.3-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Dec 21 2018 - 1.6.2-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Dec 18 2018 - 1.6.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Nov 21 2018 - 1.6.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Nov 15 2018 - 1.5.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Oct 29 2018 - 1.5.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Sep 26 2018 - 1.4.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Jul 26 2018 - 1.4.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Jun 06 2018 - 1.3.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon May 28 2018 - 1.2.12-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Tue Apr 24 2018 - 1.2.11-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Apr 11 2018 - 1.2.10-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Fri Mar 30 2018 - 1.2.9-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Mar 28 2018 - 1.2.8-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Thu Mar 22 2018 - 1.2.7-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Mar 21 2018 - 1.2.6-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Mar 19 2018 - 1.2.5-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 12 2018 - 1.2.4-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 12 2018 - 1.2.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Mar 08 2018 - 1.2.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Mar 06 2018 - 1.2.1-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Wed Feb 28 2018 - 1.2.0-1 - Vincent Legoll <vincent.legoll@openio.io>
- New release
* Mon Sep 11 2017 - 1.0.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Sep 08 2017 - 1.0.0-0.b6 - Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Aug 23 2017 - 1.0.0-0.b5 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Jul 21 2017 - 1.0.0-0.b4 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Apr 20 2017 - 0.8.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Mar 09 2017 - 0.8.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Mon Mar 06 2017 - 0.7.3-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Jan 05 2017 - 0.7.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Thu Oct 20 2016 - 0.6.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Sep 20 2016 - 0.6.0-1 - Romain Acciari <romain.acciari@openio.io>
- Update
* Fri May 13 2016 - 0.5.0-2 - Romain Acciari <romain.acciari@openio.io>
- Add python-lxml require
* Tue Dec 01 2015 - 0.5.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release 0.6.0 for the 15.12 release
* Mon Sep 14 2015 - 0.4.1-1 - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Sep 04 2015 - 0.4.0-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- Update requires
* Mon Jun 29 2015 - 0.3.0-1 - Romain Acciari <romain.acciari@openio.io>
- account autocreate on account POST
* Mon Jun 29 2015 - 0.3.0-1 - Romain Acciari <romain.acciari@openio.io>
- Account support
* Thu Apr 23 2015 - 0.2-1 - Romain Acciari <romain.acciari@openio.io>
- New release
- OpenStack Swift dependency
- License changed to Apache License v2
* Fri Mar 13 2015 - 0.1-1 - Julien Kasarherou <julien.kasarherou@openio.io>
- Initial release
