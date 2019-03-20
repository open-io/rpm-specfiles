%define dist_sn       el
%define dist_ln       Entreprise Linux

%define oiorelease    19.04

%define host          http://mirror.openio.io
%define basedir       /pub/repo/openio/sds/%{oiorelease}
%define pki_dir       %{_sysconfdir}/pki/rpm-gpg
%define pki_file      RPM-GPG-KEY-OPENIO-0

Name:           openio-sds-release
Version:        %{oiorelease}
Release:        1.%{dist_sn}
Summary:        OpenIO repository configuration for %{dist_ln}

Group:          System Environment/Base
License:        Apachev2
URL:            http://www.openio.io/
Source0:        %{host}/pub/repo/openio/%{pki_file}

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
install -Dpm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pki_dir}/%{pki_file}

### Install yum stable repositories
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio-sds-%{version}.repo<< EOF
[openio-sds-%{version}]
name=OpenIO SDS packages for %{dist_ln} \$releasever - \$basearch
baseurl=%{host}%{basedir}/%{dist_sn}/\$releasever/\$basearch
enabled=1
gpgcheck=1
gpgkey=file://%{pki_dir}/%{pki_file}

[openio-sds-%{version}-source]
name=OpenIO SDS packages for %{dist_ln} \$releasever - \$basearch - Source
baseurl=%{host}%{basedir}/%{dist_sn}/\$releasever/SRPM
enabled=0
gpgkey=file://%{pki_dir}/%{pki_file}
gpgcheck=1
EOF
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/openio*.repo


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/openio*.repo
/etc/pki/rpm-gpg/*


%changelog
* Wed Mar 20 2019 <vincent.legoll@openio.io> - 19.04-1
- New release
* Tue Sep 25 2018 <vincent.legoll@openio.io> - 18.10-1
- New release
* Thu Jul 05 2018 <vincent.legoll@openio.io> - 18.04-1
- New release
* Tue Jun 27 2017 <romain.acciari@openio.io> - 17.04-1
- New release
* Thu Oct 20 2016 <romain.acciari@openio.io> - 16.10-1
- New release
* Fri Apr 15 2016 <romain.acciari@openio.io> - 16.04-1
- New release
* Fri Dec 04 2015 <romain.acciari@openio.io> - 15.12-1
- Initial release
