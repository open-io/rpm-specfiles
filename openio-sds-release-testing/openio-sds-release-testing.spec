%define dist .f21
%define dist_version 21
%define dist_sn fedora
%define dist_ln Fedora

Name:           openio-sds-release-testing
Version:        0
Release:        1%{dist}
Summary:        OpenIO testing repository configuration

Group:          System Environment/Base
License:        WTFPL
URL:            http://www.openio.io/
Source0:        http://www.openio.io/pub/repo/RPM-GPG-KEY-OPENIO-0

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if "%{dist_sn}" == "centos"
Requires:       epel-release = %{dist_version}
%endif
Requires:       openio-sds-release

%description
This package contains the OpenIO testing repository GPG key as well as
configuration for yum and up2date.


%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} .

%build


%install
# Install yum repositories
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-testing.repo<< EOF
[openio-sds-testing-common]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0

[openio-sds-testing-common-debuginfo]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch - Debug
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch/debug
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0
gpgcheck=1

[openio-sds-testing-common-source]
name=OpenIO SDS testing packages for %{dist_ln} %{dist_version} - \$basearch - Source
baseurl=http://mirror.openio.io/pub/repo/testing/openio/sds/%{dist_sn}/%{dist_version}/common/\$basearch
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0
gpgcheck=1
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-testing.repo


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*


%changelog
* Thu Apr 09 2015 <romain.acciari@openio.io> - 0-1
- Initial release
