%define dist          .fc22
%define dist_suffix   .oio
%define dist_version  22
%define dist_sn       fedora
%define dist_ln       Fedora
%define fedora        22

%define host          http://mirror.openio.io
%define basedir       /pub/repo/stable/openio/sds
%define pki           file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0

Name:           openio-sds-release
Version:        0
Release:        3%{dist}
Summary:        OpenIO repository configuration for %{dist_ln}

Group:          System Environment/Base
License:        WTFPL
URL:            http://www.openio.io/
Source0:        http://www.openio.io/pub/repo/RPM-GPG-KEY-OPENIO-0

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?rhel}
Requires:       epel-release = %{dist_version}
%endif

%description
This package contains the OpenIO repository GPG key as well as
configuration for yum and up2date.


%package        devel
Summary:        OpenIO devel repository configuration for %{dist_ln}
Group:          openio
Requires:       openio-sds-release = %{version}
%description    devel
This package contains the OpenIO devel macro configuration for building packages.


%package        testing
Summary:        OpenIO testing repository configuration for %{dist_ln}
Group:          openio
Requires:       openio-sds-release = %{version}
%description    testing
This package contains the OpenIO testing repository configuration.


%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} .

%build


%install
# Install GPG key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-%{version}

### Install yum stable repositories
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds.repo<< EOF
[openio-sds-common]
name=OpenIO SDS packages for %{dist_ln} %{dist_version} - \$basearch
baseurl=%{host}%{basedir}/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=1
gpgcheck=1
gpgkey=%{pki}

[openio-sds-common-debuginfo]
name=OpenIO SDS packages for %{dist_ln} %{dist_version} - \$basearch - Debug
baseurl=%{host}%{basedir}/%{dist_sn}/%{dist_version}/common/\$basearch/debug
enabled=0
gpgkey=%{pki}
gpgcheck=1

[openio-sds-common-source]
name=OpenIO SDS packages for %{dist_ln} %{dist_version} - \$basearch - Source
baseurl=%{host}%{basedir}/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=0
gpgkey=%{pki}
gpgcheck=1
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds.repo

### Install yum testing repositories
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-testing.repo<< EOF
[openio-sds-testing-common]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=1
gpgcheck=1
gpgkey=%{pki}

[openio-sds-testing-common-debuginfo]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch - Debug
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch/debug
enabled=0
gpgkey=%{pki}
gpgcheck=1

[openio-sds-testing-common-source]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch - Source
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=0
gpgkey=%{pki}
gpgcheck=1
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-testing.repo

### Install rpm macros
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.openio << EOF
# dist macros.

%%openio              1
%%openio_sds_ver      0
%%dist                %{dist}%{dist_suffix}
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.openio


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/openio-sds.repo
/etc/pki/rpm-gpg/*

%files devel
%defattr(-,root,root,-)
%config(noreplace) /etc/rpm/macros.openio

%files testing
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/openio-sds-testing.repo


%changelog
* Tue Apr 21 2015 <romain.acciari@openio.io> - 0-3
- Refactoring
- Add testing repository
* Wed Mar 04 2015 <romain.acciari@openio.io> - 0-2
- Fix subdomain to mirror.openio.io
* Mon Jan 19 2015 <romain.acciari@openio.io> - 0-1
- Initial release
