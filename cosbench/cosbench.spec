Name:          cosbench-openio
Version:       0.4.4
Release:       1%{?dist}
Source0:       https://github.com/open-io/cosbench/releases/download/%{version}-openio/cosbench-%{version}-openio.tar.gz
Source1:       cosbench-controller.service
Source2:       controller.default.service
Source3:       controller.log4j.properties

Summary:       A benchmark tool for cloud object storage service
License:       Apache 2.0
Url:           https://github.com/open-io/cosbench
BuildArch:     noarch

Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires: systemd
Requires: which

%define        cosbench_home    %{_sharedstatedir}/cosbench
%define        cosbench_prefix  %{_prefix}/cosbench
%define        cosbench_etc     %{_sysconfdir}/cosbench
%define        cosbench_user    cosbench
%define        cosbench_group   %{cosbench_user}

%package controller
Summary:       Cosbench Controller
Requires:      jre6
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
Only include the controller part of Cosbench.


%prep
%setup -q -n cosbench-%{version}-openio
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} conf/

# comment default value
sed 's/^/#/' conf/controller.default.service > conf/controller.sysconfig.service

# update path to cosbench-users.xml
sed -i "s@./conf/cosbench-users.xml@%{cosbench_etc}/cosbench-users.xml@" conf/controller-tomcat-server.xml

# update log file path
sed -i "s@log/system.log@/var/log/cosbench/system.log@" conf/controller.conf

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

# Logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/cosbench

# archives
install -d $RPM_BUILD_ROOT%{cosbench_home}/archives

%files
%defattr(-,root,root) 
%{cosbench_prefix}
%config %{cosbench_etc}/cosbench-users.xml
%{_bindir}/cosbench-cli

%defattr(-,%{cosbench_user},%{cosbench_group}) 
%{_localstatedir}/log/cosbench

# docs
%dir %{_datadir}/cosbench

%license %{_datadir}/cosbench/3rd-party-licenses.pdf
%license %{_datadir}/cosbench/LICENSE
%license %{_datadir}/cosbench/licenses

%doc %{_datadir}/cosbench/CHANGELOG
%doc %{_datadir}/cosbench/NOTICE
%doc %{_datadir}/cosbench/workloads

%dir %{_datadir}/doc/cosbench
%doc %{_datadir}/doc/cosbench/README.md
%doc %{_datadir}/doc/cosbench/BUILD.md
%doc %{_datadir}/doc/cosbench/COSBenchAdaptorDevGuide.pdf
%doc %{_datadir}/doc/cosbench/COSBenchUserGuide.pdf
%doc %{_datadir}/doc/cosbench/javadoc

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

%changelog
* Thu Jan 10 2019 - Jérôme Loyet <jerome.loyet@openio.io> - 0.4.4-1
- Initial release
