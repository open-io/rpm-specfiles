%define dist_sn       el
%define dist_ln       Entreprise Linux

%define oiorelease    15.12

%define host          http://mirror.openio.io
%define basedir       /pub/repo/openio/sds/%{oiorelease}
%define pki           file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0


Name:           openio-sds-release
Version:        %{oiorelease}
Release:        1.%{dist_sn}
Summary:        OpenIO repository configuration for %{dist_ln}

Group:          System Environment/Base
License:        Apachev2
URL:            http://www.openio.io/
Source0:        http://mirror.openio.io/pub/repo/openio/RPM-GPG-KEY-OPENIO-0

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?rhel}
Requires:       epel-release
%endif

%description
This package contains the OpenIO repository GPG key as well as
configuration for yum and up2date.


%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} .

%build


%install
# Install GPG key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OPENIO-0

### Install yum stable repositories
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-%{version}.repo<< EOF
[openio-sds-%{version}]
name=OpenIO SDS packages for %{dist_ln} \$releasever - \$basearch
baseurl=%{host}%{basedir}/%{dist_sn}/\$releasever/\$basearch
enabled=1
gpgcheck=1
gpgkey=%{pki}

[openio-sds-%{version}-source]
name=OpenIO SDS packages for %{dist_ln} \$releasever - \$basearch - Source
baseurl=%{host}%{basedir}/%{dist_sn}/\$releasever/SRPM
enabled=0
gpgkey=%{pki}
gpgcheck=1
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio*.repo


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/openio*.repo
/etc/pki/rpm-gpg/*


%changelog
* Fri Dec 04 2015 <romain.acciari@openio.io> - 15.12-1.%{dist_sn}
- Initial release
