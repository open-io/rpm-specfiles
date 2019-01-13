Name:          cosbench-openio
Version:       0.4.4
Release:       1%{?dist}
Source0:       https://github.com/open-io/cosbench/releases/download/%{version}-openio/cosbench-%{version}-openio.tar.gz
Source1:       cosbench-controller.service
Source2:       controller.default.service
Source3:       controller.log4j.properties
Source4:       cosbench-driver.service
Source5:       driver.default.service
Source6:       driver.log4j.properties

Summary:       A benchmark tool for cloud object storage service
License:       Apache 2.0
Url:           https://github.com/open-io/cosbench
BuildArch:     noarch

Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires: systemd
Requires: which
Requires: jre-headless = 1:1.8.0

%define        cosbench_home    %{_sharedstatedir}/cosbench
%define        cosbench_prefix  %{_prefix}/cosbench
%define        cosbench_etc     %{_sysconfdir}/cosbench
%define        cosbench_user    cosbench
%define        cosbench_group   %{cosbench_user}

%package controller
Summary:       Cosbench Controller
Requires:      %{name} = %{version}-%{release}

%package driver
Summary:       Cosbench Driver
Requires:      %{name} = %{version}-%{release}

%description
COSBench is a benchmarking tool to measure the performance of Cloud Object
Storage services. Object storage is an emerging technology that is different
from traditional file systems (e.g., NFS) or block device systems (e.g., iSCSI).
Amazon S3 and Openstack* swift are well-known object storage solutions.

COSBench now supports:
 * OpenStack Swift
 * Amazon S3, 
 * OpenIO
 * Amplidata v2.3, 2.5 and 3.1
 * Scality
 * Ceph
 * CDMI
 * Google Cloud Storage
 * Aliyun OSS
 * ... as well as custom adaptors

%description controller
Only the controller part of Cosbench is included.

%description driver
Only the driver part of Cosbench is included.



%prep
%setup -q -n cosbench-%{version}-openio
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} conf/
cp %{SOURCE4} %{SOURCE5} %{SOURCE6} conf/

# comment default value
sed 's/^/#/' conf/controller.default.service > conf/controller.sysconfig.service
sed 's/^/#/' conf/driver.default.service > conf/driver.sysconfig.service

# update path to cosbench-users.xml
sed -i "s@./conf/cosbench-users.xml@%{cosbench_etc}/cosbench-users.xml@" conf/controller-tomcat-server.xml
sed -i "s@./conf/cosbench-users.xml@%{cosbench_etc}/cosbench-users.xml@" conf/driver-tomcat-server.xml

# update log file path
sed -i "s@log/system.log@/var/log/cosbench/system-controller.log@" conf/controller.conf
echo -e "\nlog_file = /var/log/cosbench/system-driver.log" >> conf/driver.conf

# update arhive dir
sed -i "s@= archive@= %{cosbench_home}/archives@" conf/controller.conf

%build

%install
# Main files
install -d $RPM_BUILD_ROOT%{cosbench_prefix}
cp -r ext main osgi VERSION BUILD.no $RPM_BUILD_ROOT%{cosbench_prefix}/

install -d  $RPM_BUILD_ROOT%{_bindir}
install -m 0755 cli.sh $RPM_BUILD_ROOT%{_bindir}/cosbench-cli

# Docs
install -d $RPM_BUILD_ROOT%{_datadir}/cosbench
cp -r      3rd-party-licenses.pdf CHANGELOG LICENSE licenses NOTICE workloads $RPM_BUILD_ROOT%{_datadir}/cosbench/

install -d $RPM_BUILD_ROOT%{_datadir}/doc/cosbench
cp -r      README.md BUILD.md COSBenchAdaptorDevGuide.pdf COSBenchUserGuide.pdf javadoc $RPM_BUILD_ROOT%{_datadir}/doc/cosbench/

# Conf files
install -d $RPM_BUILD_ROOT%{cosbench_etc}
install    conf/cosbench-users.xml $RPM_BUILD_ROOT%{cosbench_etc}/

# Controller 
install -d $RPM_BUILD_ROOT%{cosbench_home}/controller
install    conf/.controller/config.ini $RPM_BUILD_ROOT%{cosbench_home}/controller/
install    conf/{controller.conf,controller-tomcat-server.xml,controller.log4j.properties} $RPM_BUILD_ROOT%{cosbench_etc}/
install -D conf/controller.default.service $RPM_BUILD_ROOT%{_sysconfdir}/default/cosbench-controller
install -D conf/controller.sysconfig.service $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/cosbench-controller
install -d $RPM_BUILD_ROOT%{_unitdir}/
install    conf/cosbench-controller.service $RPM_BUILD_ROOT%{_unitdir}/

# Driver
install -d $RPM_BUILD_ROOT%{cosbench_home}/driver
install    conf/.driver/config.ini $RPM_BUILD_ROOT%{cosbench_home}/driver/
install    conf/{driver.conf,driver-tomcat-server.xml,driver.log4j.properties} $RPM_BUILD_ROOT%{cosbench_etc}/
install -D conf/driver.default.service $RPM_BUILD_ROOT%{_sysconfdir}/default/cosbench-driver
install -D conf/driver.sysconfig.service $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/cosbench-driver
install -d $RPM_BUILD_ROOT%{_unitdir}/
install    conf/cosbench-driver.service $RPM_BUILD_ROOT%{_unitdir}/

# Logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/cosbench

# archives
install -d $RPM_BUILD_ROOT%{cosbench_home}/archives

# temporary fix until mission dir is not hardcoded anymore
(cd $RPM_BUILD_ROOT%{cosbench_prefix}/ && ln -s %{_localstatedir}/log/cosbench log)

%files
%defattr(-,root,root) 
%{cosbench_prefix}
%config %{cosbench_etc}/cosbench-users.xml
%{_bindir}/cosbench-cli

%defattr(-,%{cosbench_user},%{cosbench_group}) 
%{_localstatedir}/log/cosbench

# docs
%{_datadir}/cosbench
%{_datadir}/doc/cosbench

%files controller
%defattr(-,root,root) 
%config %{cosbench_etc}/controller.conf
%config %{cosbench_etc}/controller-tomcat-server.xml
%config %{cosbench_etc}/controller.log4j.properties
%{_sysconfdir}/default/cosbench-controller
%config %{_sysconfdir}/sysconfig/cosbench-controller
%{_unitdir}/cosbench-controller.service

%defattr(-,%{cosbench_user},%{cosbench_group}) 
%{cosbench_home}/controller
%config %dir %{cosbench_home}/archives

%files driver
%defattr(-,root,root) 
%config %{cosbench_etc}/driver.conf
%config %{cosbench_etc}/driver-tomcat-server.xml
%config %{cosbench_etc}/driver.log4j.properties
%{_sysconfdir}/default/cosbench-driver
%config %{_sysconfdir}/sysconfig/cosbench-driver
%{_unitdir}/cosbench-driver.service

%defattr(-,%{cosbench_user},%{cosbench_group}) 
%{cosbench_home}/driver

%pre
getent group %{cosbench_group} >/dev/null || groupadd -r %{cosbench_group}
getent passwd %{cosbench_user}  >/dev/null || useradd -r -g %{cosbench_group} -d %{cosbench_home} -s /sbin/nologin -c "Cosbench Running User" %{cosbench_user}
exit 0

%post controller
%systemd_post cosbench-controller.service

%preun controller
%systemd_preun cosbench-controller.service

%postun controller
%systemd_postun_with_restart cosbench-controller.service

%post driver
%systemd_post cosbench-driver.service

%preun driver
%systemd_preun cosbench-driver.service

%postun driver
%systemd_postun_with_restart cosbench-driver.service

%changelog
* Thu Jan 10 2019 - Jérôme Loyet <jerome.loyet@openio.io> - 0.4.4-1
- Initial release
