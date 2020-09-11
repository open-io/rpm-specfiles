# rpmbuild --rebuild --with testsuite --without clustering samba.src.rpm
#
# The testsuite is disabled by default. Set --with testsuite or bcond_without
# to run the Samba torture testsuite.
%bcond_with testsuite
# ctdb is enabled by default, you can disable it with: --without clustering
%bcond_without clustering

%define main_release 1

%define samba_version 4.11.12
# This should be rc1 or nil
%define pre_release %nil

%if "x%{?pre_release}" != "x"
%define samba_release 0.%{main_release}.%{pre_release}%{?dist}
%else
%define samba_release %{main_release}%{?dist}
%endif

# This is a network daemon, do a hardened build
# Enables PIE and full RELRO protection
%global _hardened_build 1
# Samba cannot be linked with -Wl,-z,defs (from hardened build config)
# For exmple the samba-cluster-support library is marked to allow undefined
# symbols in the samba build.
#
# https://src.fedoraproject.org/rpms/redhat-rpm-config/blob/master/f/buildflags.md
%undefine _strict_symbol_defs_build

%global with_libsmbclient 1
%global with_libwbclient 1

%global with_internal_talloc 1
%global with_internal_tevent 1
%global with_internal_tdb 1
%global with_internal_ldb 1

%global with_profiling 1

%global with_vfs_cephfs 1
%if 0%{?rhel}
%global with_vfs_cephfs 0
%endif

%global with_vfs_glusterfs 1

%global with_intel_aes_accel 0
%ifarch x86_64
%global with_intel_aes_accel 1
%endif

%define ctdbrundir /run/ctdb
%define ctdbsocketpath %{ctdbrundir}/ctdbd.socket

%global libwbc_alternatives_version 0.15
%global libwbc_alternatives_suffix %nil
%if 0%{?__isa_bits} == 64
%global libwbc_alternatives_suffix -64
%endif

%global with_dc 1

%if 0%{?rhel}
%global with_dc 0
%endif

%if %{with testsuite}
%global with_dc 1
%endif

%global required_mit_krb5 1.15.1

%global with_clustering_support 0

%if %{with clustering}
%global with_clustering_support 1
%endif

%global _systemd_extra "Environment=KRB5CCNAME=FILE:/run/samba/krb5cc_samba"

Name:           samba
Version:        %{samba_version}
Release:        %{samba_release}

%if 0%{?rhel}
Epoch:          0
%else
Epoch:          2
%endif

%if 0%{?epoch} > 0
%define samba_depver %{epoch}:%{version}-%{release}
%else
%define samba_depver %{version}-%{release}
%endif

Summary:   Server and Client software to interoperate with Windows machines
License:   GPLv3+ and LGPLv3+
URL:       https://www.samba.org

# This is a xz recompressed file of https://ftp.samba.org/pub/samba/samba-%%{version}%%{pre_release}.tar.gz
Source0:        https://ftp.samba.org/pub/samba/samba-%{version}%{pre_release}.tar.gz#/samba-%{version}%{pre_release}.tar.xz
Source1:        https://ftp.samba.org/pub/samba/samba-%{version}%{pre_release}.tar.asc
Source2:        gpgkey-52FBC0B86D954B0843324CDC6F33915B6568B7EA.gpg

Source10:  samba.logrotate
Source11:  smb.conf.vendor
Source12:  smb.conf.example
Source13:  README.downgrade
Source14:  pam_winbind.conf
Source15:  samba.pamd

Source100: ctdb.conf
Source101: script.options

Patch1: do-not-install-test-util-binary.patch
Patch2: remove-talloc-ldb-requires-from-samba-policy.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(pre): /usr/sbin/groupadd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif
%if %{with_vfs_glusterfs}
Requires: %{name}-vfs-glusterfs = %{samba_depver}
%endif

Requires: pam

Provides: samba4 = %{samba_depver}
Obsoletes: samba4 < %{samba_depver}

# We don't build it outdated docs anymore
Provides: samba-doc = %{samba_depver}
Obsoletes: samba-doc < %{samba_depver}

# Is not supported yet
Provides: samba-domainjoin-gui = %{samba_depver}
Obsoletes: samba-domainjoin-gui < %{samba_depver}

# SWAT been deprecated and removed from samba
Provides: samba-swat = %{samba_depver}
Obsoletes: samba-swat < %{samba_depver}

Provides: samba4-swat = %{samba_depver}
Obsoletes: samba4-swat < %{samba_depver}

BuildRequires: gcc
BuildRequires: avahi-devel
BuildRequires: cups-devel
BuildRequires: dbus-devel
BuildRequires: docbook-style-xsl
BuildRequires: e2fsprogs-devel
BuildRequires: gawk
BuildRequires: gnupg2
%if %{defined rhel} && %{rhel} >= 8
BuildRequires: gnutls-devel >= 3.4.7
BuildRequires: gpgme-devel
%else
BuildRequires: gnutls-devel >= 3.2.0
%endif
BuildRequires: gpgme-devel
BuildRequires: jansson-devel
BuildRequires: krb5-devel >= %{required_mit_krb5}
BuildRequires: libacl-devel
BuildRequires: libaio-devel
BuildRequires: libarchive-devel
BuildRequires: libattr-devel
BuildRequires: libcap-devel
%if %{defined rhel} && %{rhel} >= 8
BuildRequires: libcmocka-devel
BuildRequires: libnsl2-devel
%endif
BuildRequires: libtirpc-devel
BuildRequires: libuuid-devel
BuildRequires: libxslt
# We build without AD DC and with internal ldb
#%%if %%{defined rhel} && %%{rhel} >= 8
#BuildRequires: lmdb
#%%endif
BuildRequires: ncurses-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: perl-interpreter
%if %{defined rhel} && %{rhel} >= 8
BuildRequires: perl-generators
%endif
BuildRequires: perl(Archive::Tar)
BuildRequires: perl(Test::More)
BuildRequires: popt-devel
BuildRequires: python3-devel
BuildRequires: quota-devel
BuildRequires: readline-devel
%if %{defined rhel} && %{rhel} >= 8
BuildRequires: rpcgen
BuildRequires: rpcsvc-proto-devel
%endif
BuildRequires: sed
BuildRequires: libtasn1-devel
# We need asn1Parser
BuildRequires: libtasn1-tools
BuildRequires: xfsprogs-devel
BuildRequires: xz
BuildRequires: zlib-devel >= 1.2.3
BuildRequires: pkgconfig(libsystemd)

%if %{with_vfs_glusterfs}
BuildRequires: glusterfs-api-devel >= 3.4.0.16
BuildRequires: glusterfs-devel >= 3.4.0.16
%endif

%if %{with_vfs_cephfs}
BuildRequires: libcephfs-devel
%endif

%if %{with_dc}
# Add python3-iso8601 to avoid that the
# version in Samba is being packaged
BuildRequires: python3-iso8601
BuildRequires: python3-subunit-test
# Required by samba-tool to run tests
BuildRequires: python3-crypto

BuildRequires: bind
BuildRequires: krb5-server >= %{required_mit_krb5}
#endif with_dc
%endif

# pidl requirements
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Parse::Yapp)

%if ! %with_internal_talloc
%global libtalloc_version 2.2.0

BuildRequires: libtalloc-devel >= %{libtalloc_version}
BuildRequires: python3-talloc-devel >= %{libtalloc_version}
%endif

%if ! %with_internal_tevent
%global libtevent_version 0.10.0

BuildRequires: libtevent-devel >= %{libtevent_version}
BuildRequires: python3-tevent >= %{libtevent_version}
%endif

%if ! %with_internal_ldb
%global libldb_version 2.0.11

BuildRequires: libldb-devel >= %{libldb_version}
BuildRequires: python3-ldb-devel >= %{libldb_version}
%endif

%if ! %with_internal_tdb
%global libtdb_version 1.4.2

BuildRequires: libtdb-devel >= %{libtdb_version}
BuildRequires: python3-tdb >= %{libtdb_version}
%endif

%if %{with testsuite}
BuildRequires: ldb-tools
BuildRequires: tdb-tools
BuildRequires: python3-gpg
BuildRequires: python3-markdown
%endif

%if %{with_dc}
BuildRequires: krb5-server >= %{required_mit_krb5}
BuildRequires: bind
%endif

# filter out perl requirements pulled in from examples in the docdir.
%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{_docdir}/.*$

### SAMBA
%description
Samba is the standard Windows interoperability suite of programs for Linux and
Unix.

### CLIENT
%package client
Summary: Samba client programs
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
%if %with_libsmbclient
Requires: libsmbclient = %{samba_depver}
%endif
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-client = %{samba_depver}
Obsoletes: samba4-client < %{samba_depver}

Provides: tdb-tools = %{samba_depver}
Obsoletes: tdb-tools < %{samba_depver}

Provides: ldb-tools = %{samba_depver}
Obsoletes: ldb-tools < %{samba_depver}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description client
The %{name}-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.

### CLIENT-LIBS
%package client-libs
Summary: Samba client libraries
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif
Requires: krb5-libs >= %{required_mit_krb5}

Provides: python3-talloc = %{samba_depver}
Obsoletes: python3-talloc < %{samba_depver}
Provides: pytalloc = %{samba_depver}
Obsoletes: pytalloc < %{samba_depver}

Provides: python3-tdb = %{samba_depver}
Obsoletes: python3-tdb < %{samba_depver}
Provides: python-tdb = %{samba_depver}
Obsoletes: python-tdb < %{samba_depver}

Provides: python3-tevent = %{samba_depver}
Obsoletes: python3-tevent < %{samba_depver}
Provides: python-tevent = %{samba_depver}
Obsoletes: python-tevent < %{samba_depver}

Provides: python3-ldb = %{samba_depver}
Obsoletes: python3-ldb < %{samba_depver}
Provides: pyldb = %{samba_depver}
Obsoletes: pyldb < %{samba_depver}

%description client-libs
The samba-client-libs package contains internal libraries needed by the
SMB/CIFS clients.

### COMMON
%package common
Summary: Files used by both Samba servers and clients
BuildArch: noarch

Requires(post): systemd
%if %{defined rhel} && %{rhel} >= 8
Recommends:     logrotate
%endif


Provides: samba4-common = %{samba_depver}
Obsoletes: samba4-common < %{samba_depver}

%if ! %{with_dc}
Obsoletes: samba-dc < %{samba_depver}
Obsoletes: samba-dc-libs < %{samba_depver}
Obsoletes: samba-dc-bind-dlz < %{samba_depver}
%endif

%description common
samba-common provides files necessary for both the server and client
packages of Samba.

### COMMON-LIBS
%package common-libs
Summary: Libraries used by both Samba servers and clients
Requires(pre): samba-common = %{samba_depver}
Requires: samba-common = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

%description common-libs
The samba-common-libs package contains internal libraries needed by the
SMB/CIFS clients.

### COMMON-TOOLS
%package common-tools
Summary: Tools for Samba servers and clients
Requires: samba-common-libs = %{samba_depver}
Requires: samba-client-libs = %{samba_depver}
Requires: samba-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

%description common-tools
The samba-common-tools package contains tools for Samba servers and
SMB/CIFS clients.

### DC
%if %{with_dc}
%package dc
Summary: Samba AD Domain Controller
Requires: %{name} = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-dc-provision = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}
# samba-tool needs tdbbackup
Requires: tdb-tools
# samba-tool needs mdb_copy
Requires: lmdb
Requires: ldb-tools
# Force using libldb version to be the same as build version
# Otherwise LDB modules will not be loaded and samba-tool will fail
# See bug 1507420
%requires_eq libldb

Requires: python3-crypto
Requires: python3-%{name} = %{samba_depver}
Requires: python3-%{name}-dc = %{samba_depver}
Requires: krb5-server >= %{required_mit_krb5}

Provides: samba4-dc = %{samba_depver}
Obsoletes: samba4-dc < %{samba_depver}

%description dc
The samba-dc package provides AD Domain Controller functionality

### DC-PROVISION
%package dc-provision
Summary: Samba AD files to provision a DC
BuildArch: noarch

%description dc-provision
The samba-dc-provision package provides files to setup a domoin controller

### DC-LIBS
%package dc-libs
Summary: Samba AD Domain Controller Libraries
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}

Provides: samba4-dc-libs = %{samba_depver}
Obsoletes: samba4-dc-libs < %{samba_depver}

%description dc-libs
The %{name}-dc-libs package contains the libraries needed by the DC to
link against the SMB, RPC and other protocols.

### DC-BIND
%package dc-bind-dlz
Summary: Bind DLZ module for Samba AD
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: %{name}-dc = %{samba_depver}
Requires: bind

%description dc-bind-dlz
The %{name}-dc-bind-dlz package contains the libraries for bind to manage all
name server related details of Samba AD.
#endif with_dc
%endif

### DEVEL
%package devel
Summary: Developer tools for Samba libraries
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}

Provides: samba4-devel = %{samba_depver}
Obsoletes: samba4-devel < %{samba_depver}

%description devel
The %{name}-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

### CEPH
%if %{with_vfs_cephfs}
%package vfs-cephfs
Summary: Samba VFS module for Ceph distributed storage system
Requires: %{name} = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}

%description vfs-cephfs
Samba VFS module for Ceph distributed storage system integration.
#endif with_vfs_cephfs
%endif

### GLUSTER
%if %{with_vfs_glusterfs}
%package vfs-glusterfs
Summary: Samba VFS module for GlusterFS
Requires: glusterfs-api >= 3.4.0.16
Requires: glusterfs >= 3.4.0.16
Requires: %{name} = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
%if %{with_vfs_glusterfs}
Requires: selinux-policy-targeted >= 3.13.1-23.el7_1.8
%if %{defined rhel} && %{rhel} >= 8
Requires: python3-policycoreutils
%else
Requires: policycoreutils-python
%endif
%endif
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

Obsoletes: samba-glusterfs < %{samba_depver}
Provides: samba-glusterfs = %{samba_depver}

%description vfs-glusterfs
Samba VFS module for GlusterFS integration.
%endif

### KRB5-PRINTING
%package krb5-printing
Summary: Samba CUPS backend for printing with Kerberos
Requires(pre): %{name}-client
Requires: %{name}-client = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description krb5-printing
If you need Kerberos for print jobs to a printer connection to cups via the SMB
backend, then you need to install that package. It will allow cups to access
the Kerberos credentials cache of the user issuing the print job.

### LIBS
%package libs
Summary: Samba libraries
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-libs = %{samba_depver}
Obsoletes: samba4-libs < %{samba_depver}

%description libs
The %{name}-libs package contains the libraries needed by programs that link
against the SMB, RPC and other protocols provided by the Samba suite.

### LIBSMBCLIENT
%if %with_libsmbclient
%package -n libsmbclient
Summary: The SMB client library
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

%description -n libsmbclient
The libsmbclient contains the SMB client library from the Samba suite.

%package -n libsmbclient-devel
Summary: Developer tools for the SMB client library
Requires: libsmbclient = %{samba_depver}

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed
to develop programs that link against the SMB client library in the Samba
suite.
#endif with_libsmbclient
%endif

### LIBWBCLIENT
%if %with_libwbclient
%package -n libwbclient
Summary: The winbind client library
Requires: %{name}-client-libs = %{samba_depver}

%description -n libwbclient
The libwbclient package contains the winbind client library from the Samba
suite.

%package -n libwbclient-devel
Summary: Developer tools for the winbind library
Requires: libwbclient = %{samba_depver}

Provides: samba-winbind-devel = %{samba_depver}
Obsoletes: samba-winbind-devel < %{samba_depver}

%description -n libwbclient-devel
The libwbclient-devel package provides developer tools for the wbclient
library.
#endif with_libwbclient
%endif

### PYTHON3
%package -n python3-%{name}
Summary: Samba Python3 libraries
Requires: %{name} = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Obsoletes: samba-python < %{version}-%{release}
Requires: python3-talloc
Requires: python3-tevent
Requires: python3-tdb
Requires: python3-ldb
%if %{defined rhel} && %{rhel} >= 8
Requires: python3-dns
%endif
%if %with_libsmbclient
Requires: libsmbclient = %{samba_depver}
%endif
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

%description -n python3-%{name}
The python3-%{name} package contains the Python 3 libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python 3 programs.

%package -n python3-samba-test
Summary: Samba Python libraries
Requires: python3-%{name} = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}

%description -n python3-samba-test
The python3-%{name}-test package contains the Python libraries used by the test suite of Samba.
If you want to run full set of Samba tests, you need to install this package.

%if %{with_dc}
%package -n python3-samba-dc
Summary: Samba Python libraries for Samba AD
Requires: python3-%{name} = %{samba_depver}

%description -n python3-samba-dc
The python3-%{name}-dc package contains the Python libraries needed by programs
to manage Samba AD.
%endif

### PIDL
%package pidl
Summary: Perl IDL compiler
Requires: perl-interpreter
Requires: perl(Parse::Yapp)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

Provides: samba4-pidl = %{samba_depver}
Obsoletes: samba4-pidl < %{samba_depver}

%description pidl
The %{name}-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols

### TEST
%package test
Summary: Testing tools for Samba servers and clients
Requires: %{name} = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}

Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-test-libs = %{samba_depver}
%if %with_dc
Requires: %{name}-dc-libs = %{samba_depver}
%endif
Requires: %{name}-libs = %{samba_depver}
%if %with_libsmbclient
Requires: libsmbclient = %{samba_depver}
%endif
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif
Requires: python3-%{name} = %{samba_depver}
Requires: perl(Archive::Tar)

Provides: samba4-test = %{samba_depver}
Obsoletes: samba4-test < %{samba_depver}

%description test
%{name}-test provides testing tools for both the server and client
packages of Samba.

### TEST-LIBS
%package test-libs
Summary: Libraries need by the testing tools for Samba servers and clients
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

Provides: %{name}-test-devel = %{samba_depver}
Obsoletes: %{name}-test-devel < %{samba_depver}

%description test-libs
%{name}-test-libs provides libraries required by the testing tools.

### WINBIND
%package winbind
Summary: Samba winbind
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-winbind-modules = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: samba4-winbind = %{samba_depver}
Obsoletes: samba4-winbind < %{samba_depver}

%description winbind
The samba-winbind package provides the winbind NSS library, and some client
tools.  Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.

### WINBIND-CLIENTS
%package winbind-clients
Summary: Samba winbind clients
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-winbind-clients = %{samba_depver}
Obsoletes: samba4-winbind-clients < %{samba_depver}

%description winbind-clients
The samba-winbind-clients package provides the wbinfo and ntlm_auth
tool.

### WINBIND-KRB5-LOCATOR
%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}
%else
Requires: %{name}-libs = %{samba_depver}
%endif
Requires: samba-client-libs = %{samba_depver}

Provides: samba4-winbind-krb5-locator = %{samba_depver}
Obsoletes: samba4-winbind-krb5-locator < %{samba_depver}

# Handle winbind_krb5_locator.so as alternatives to allow
# IPA AD trusts case where it should not be used by libkrb5
# The plugin will be diverted to /dev/null by the FreeIPA
# freeipa-server-trust-ad subpackage due to higher priority
# and restored to the proper one on uninstall
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use

### WINBIND-MODULES
%package winbind-modules
Summary: Samba winbind modules
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
%if %with_libwbclient
Requires: libwbclient = %{samba_depver}
%endif
Requires: pam

%description winbind-modules
The samba-winbind-modules package provides the NSS library and a PAM module
necessary to communicate to the Winbind Daemon

### CTDB
%if %with_clustering_support
%package -n ctdb
Summary: A Clustered Database based on Samba's Trivial Database (TDB)

Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}

Requires: coreutils
Requires: fileutils
# for ps and killall
Requires: psmisc
Requires: sed
Requires: tdb-tools
Requires: gawk
# for pkill and pidof:
Requires: procps-ng
# for netstat:
Requires: net-tools
Requires: ethtool
# for ip:
Requires: iproute
Requires: iptables
# for flock, getopt, kill:
Requires: util-linux

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

Provides: ctdb2.5 = %{samba_depver}
Obsoletes: ctdb2.5 < %{samba_depver}

%description -n ctdb
CTDB is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.

### CTDB-TEST
%package -n ctdb-tests
Summary: CTDB clustered database test suite

Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}

Requires: ctdb = %{samba_depver}
Requires: nc
Provides: ctdb2.5-tests = %{samba_depver}
Obsoletes: ctdb2.5-tests < %{samba_depver}

Provides: ctdb-devel = %{samba_depver}
Obsoletes: ctdb-devel < %{samba_depver}

%description -n ctdb-tests
Test suite for CTDB.
CTDB is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.
#endif with_clustering_support
%endif



%prep
xzcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
%autosetup -n samba-%{version}%{pre_release} -p1

%build
%global _talloc_lib ,talloc,pytalloc,pytalloc-util
%global _tevent_lib ,tevent,pytevent
%global _tdb_lib ,tdb,pytdb
%global _ldb_lib ,ldb,pyldb,pyldb-util

%if ! %{with_internal_talloc}
%global _talloc_lib ,!talloc,!pytalloc,!pytalloc-util
%endif

%if ! %{with_internal_tevent}
%global _tevent_lib ,!tevent,!pytevent
%endif

%if ! %{with_internal_tdb}
%global _tdb_lib ,!tdb,!pytdb
%endif

%if ! %{with_internal_ldb}
%global _ldb_lib ,!ldb,!pyldb,!pyldb-util
%endif

%global _samba_libraries !zlib,!popt%{_talloc_lib}%{_tevent_lib}%{_tdb_lib}%{_ldb_lib}

%global _samba_idmap_modules idmap_ad,idmap_rid,idmap_ldap,idmap_hash,idmap_tdb2
%global _samba_pdb_modules pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%global _samba_auth_modules auth_wbc,auth_unix,auth_server,auth_script,auth_samba4
%global _samba_vfs_modules vfs_dfs_samba4

%global _samba_modules %{_samba_idmap_modules},%{_samba_pdb_modules},%{_samba_auth_modules},%{_samba_vfs_modules}

%global _libsmbclient %nil
%global _libwbclient %nil

%if ! %with_libsmbclient
%global _libsmbclient smbclient,
%endif

%if ! %with_libwbclient
%global _libwbclient wbclient,
%endif

%global _samba_private_libraries %{_libsmbclient}%{_libwbclient}%{_talloc_lib}%{_tevent_lib}%{_tdb_lib}%{_ldb_lib}

# TODO: resolve underlinked python modules
export python_LDFLAGS="$(echo %{__global_ldflags} | sed -e 's/-Wl,-z,defs//g')"

# Use the gold linker
export LDFLAGS="%{__global_ldflags} -fuse-ld=gold"

%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=/var/lib/samba/lock \
        --with-statedir=/var/lib/samba \
        --with-cachedir=/var/lib/samba \
        --disable-rpath-install \
        --with-shared-modules=%{_samba_modules} \
        --bundled-libraries=%{_samba_libraries} \
        --with-pam \
        --with-pie \
        --with-relro \
        --without-fam \
        --private-libraries=%{_samba_private_libraries} \
        --with-system-mitkrb5 \
        --with-experimental-mit-ad-dc \
%if ! %with_dc
        --without-ad-dc \
%endif
%if ! %with_vfs_glusterfs
        --disable-glusterfs \
%endif
%if %with_clustering_support
        --with-cluster-support \
%endif
%if %with_profiling
        --with-profiling-data \
%endif
%if %{with testsuite}
        --enable-selftest \
%endif
%if %with_intel_aes_accel
        --accel-aes=intelaesni \
%endif
        --with-systemd \
        --systemd-install-services \
        --with-systemddir=/usr/lib/systemd/system \
        --systemd-smb-extra=%{_systemd_extra} \
        --systemd-nmb-extra=%{_systemd_extra} \
        --systemd-winbind-extra=%{_systemd_extra} \
        --systemd-samba-extra=%{_systemd_extra}

make %{?_smp_mflags}

pushd pidl
%__perl Makefile.PL PREFIX=%{_prefix}

make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot}

install -d -m 0755 %{buildroot}/usr/{sbin,bin}
install -d -m 0755 %{buildroot}%{_libdir}/security
install -d -m 0755 %{buildroot}/var/lib/samba
install -d -m 0755 %{buildroot}/var/lib/samba/drivers
install -d -m 0755 %{buildroot}/var/lib/samba/lock
install -d -m 0755 %{buildroot}/var/lib/samba/private
install -d -m 0755 %{buildroot}/var/lib/samba/scripts
install -d -m 0755 %{buildroot}/var/lib/samba/sysvol
install -d -m 0755 %{buildroot}/var/lib/samba/winbindd_privileged
install -d -m 0755 %{buildroot}/var/log/samba/old
install -d -m 0755 %{buildroot}/var/spool/samba
install -d -m 0755 %{buildroot}/run/samba
install -d -m 0755 %{buildroot}/run/winbindd
%if %with_clustering_support
install -d -m 0755 %{buildroot}/run/ctdb
%endif
install -d -m 0755 %{buildroot}/%{_libdir}/samba
install -d -m 0755 %{buildroot}/%{_libdir}/samba/ldb
install -d -m 0755 %{buildroot}/%{_libdir}/pkgconfig

# Move libwbclient.so* into private directory, it cannot be just libdir/samba
# because samba uses rpath with this directory.
install -d -m 0755 %{buildroot}/%{_libdir}/samba/wbclient
mv %{buildroot}/%{_libdir}/libwbclient.so* %{buildroot}/%{_libdir}/samba/wbclient
if [ ! -f %{buildroot}/%{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version} ]
then
    echo "Expected libwbclient version not found, please check if version has changed."
    exit -1
fi


touch %{buildroot}%{_libexecdir}/samba/cups_backend_smb

# Install other stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/samba

install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/samba/smb.conf
install -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/samba/smb.conf.example

install -m 0644 %{SOURCE13} packaging/README.downgrade

install -d -m 0755 %{buildroot}%{_sysconfdir}/security
install -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/pam.d/samba

echo 127.0.0.1 localhost > %{buildroot}%{_sysconfdir}/samba/lmhosts

# openLDAP database schema
install -d -m 0755 %{buildroot}%{_sysconfdir}/openldap/schema
install -m 0644 examples/LDAP/samba.schema %{buildroot}%{_sysconfdir}/openldap/schema/samba.schema

install -m 0744 packaging/printing/smbprint %{buildroot}%{_bindir}/smbprint

install -d -m 0755 %{buildroot}%{_tmpfilesdir}
# Create /run/samba.
echo "d /run/samba  755 root root" > %{buildroot}%{_tmpfilesdir}/samba.conf
%if %with_clustering_support
echo "d /run/ctdb 755 root root" > %{buildroot}%{_tmpfilesdir}/ctdb.conf
%endif

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba
%if %with_clustering_support
cat > %{buildroot}%{_sysconfdir}/sysconfig/ctdb <<EOF
# CTDB configuration is now in %%{_sysconfdir}/ctdb/ directory
EOF

install -d -m 0755 %{buildroot}%{_sysconfdir}/ctdb
install -m 0644 %{SOURCE100} %{buildroot}%{_sysconfdir}/ctdb/ctdb.conf
install -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/ctdb/script.options
%endif

%if %with_clustering_support
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 ctdb/config/ctdb.service %{buildroot}%{_unitdir}
%endif

# NetworkManager online/offline script
%if %{defined rhel} && %{rhel} >= 8
install -d -m 0755 %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd \
            %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/30-winbind
%else
install -d -m 0755 %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd \
            %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind
%endif

# winbind krb5 plugins
install -d -m 0755 %{buildroot}%{_libdir}/krb5/plugins/libkrb5
touch %{buildroot}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

%if ! %with_dc
for i in \
    %{_libdir}/samba/libdfs-server-ad-samba4.so \
    %{_libdir}/samba/libdnsserver-common-samba4.so \
    %{_libdir}/samba/libdsdb-garbage-collect-tombstones-samba4.so \
    %{_libdir}/samba/libscavenge-dns-records-samba4.so \
    %{_mandir}/man8/samba.8 \
    %{_mandir}/man8/samba_downgrade_db.8 \
    %{_mandir}/man8/samba-tool.8 \
    %{_mandir}/man8/samba-gpupdate.8 \
    %{_libdir}/samba/ldb/ildap.so \
    %{_libdir}/samba/ldb/ldbsamba_extensions.so \
    %{_unitdir}/samba.service \
    %{python3_sitearch}/samba/dcerpc/dnsserver.*.so \
    %{python3_sitearch}/samba/dnsserver.py \
    %{python3_sitearch}/samba/domain_update.py \
    %{python3_sitearch}/samba/forest_update.py \
    %{python3_sitearch}/samba/kcc/__init__.py \
    %{python3_sitearch}/samba/kcc/debug.py \
    %{python3_sitearch}/samba/kcc/graph.py \
    %{python3_sitearch}/samba/kcc/graph_utils.py \
    %{python3_sitearch}/samba/kcc/kcc_utils.py \
    %{python3_sitearch}/samba/kcc/ldif_import_export.py \
    %{python3_sitearch}/samba/kcc/__pycache__/__init__.*.pyc \
    %{python3_sitearch}/samba/kcc/__pycache__/debug.*.pyc \
    %{python3_sitearch}/samba/kcc/__pycache__/graph.*.pyc \
    %{python3_sitearch}/samba/kcc/__pycache__/graph_utils.*.pyc \
    %{python3_sitearch}/samba/kcc/__pycache__/kcc_utils.*.pyc \
    %{python3_sitearch}/samba/kcc/__pycache__/ldif_import_export.*.pyc \
    %{python3_sitearch}/samba/ms_forest_updates_markdown.py \
    %{python3_sitearch}/samba/ms_schema_markdown.py \
    %{python3_sitearch}/samba/provision/__init__.py \
    %{python3_sitearch}/samba/provision/backend.py \
    %{python3_sitearch}/samba/provision/common.py \
    %{python3_sitearch}/samba/provision/kerberos_implementation.py \
    %{python3_sitearch}/samba/provision/kerberos.py \
    %{python3_sitearch}/samba/provision/sambadns.py \
    %{python3_sitearch}/samba/provision/__pycache__/__init__.*.pyc \
    %{python3_sitearch}/samba/provision/__pycache__/backend.*.pyc \
    %{python3_sitearch}/samba/provision/__pycache__/common.*.pyc \
    %{python3_sitearch}/samba/provision/__pycache__/kerberos_implementation.*.pyc \
    %{python3_sitearch}/samba/provision/__pycache__/kerberos.*.pyc \
    %{python3_sitearch}/samba/provision/__pycache__/sambadns.*.pyc \
    %{python3_sitearch}/samba/__pycache__/domain_update.*.pyc \
    %{python3_sitearch}/samba/__pycache__/forest_update.*.pyc \
    %{python3_sitearch}/samba/__pycache__/ms_forest_updates_markdown.*.pyc \
    %{python3_sitearch}/samba/__pycache__/ms_schema_markdown.*.pyc \
    %{python3_sitearch}/samba/__pycache__/remove_dc.*.pyc \
    %{python3_sitearch}/samba/__pycache__/schema.*.pyc \
    %{python3_sitearch}/samba/__pycache__/uptodateness.*.pyc \
    %{python3_sitearch}/samba/remove_dc.py \
    %{python3_sitearch}/samba/samdb.py \
    %{python3_sitearch}/samba/schema.py \
    %{python3_sitearch}/samba/third_party/iso8601/__init__.py \
    %{python3_sitearch}/samba/third_party/iso8601/__pycache__/__init__.*.pyc \
    %{python3_sitearch}/samba/third_party/iso8601/__pycache__/iso8601.*.pyc \
    %{python3_sitearch}/samba/third_party/iso8601/__pycache__/test_iso8601.*.pyc \
    %{python3_sitearch}/samba/third_party/iso8601/iso8601.py \
    %{python3_sitearch}/samba/third_party/iso8601/test_iso8601.py \
    %{python3_sitearch}/samba/uptodateness.py \
    %{_sbindir}/samba-gpupdate \
    ; do
    rm -f %{buildroot}$i
done
%endif

# This makes the right links, as rpmlint requires that
# the ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n %{buildroot}%{_libdir}

%if ! %with_dc
for f in samba/libsamba-net-samba4.so \
         samba/libsamba-python-samba4.so \
         libsamba-policy.so* \
         pkgconfig/samba-policy.pc ; do
    rm -f %{buildroot}%{_libdir}/$f
done
#endif ! with_dc
%endif

pushd pidl
make DESTDIR=%{buildroot} install_vendor

rm -f %{buildroot}%{perl_archlib}/perllocal.pod
rm -f %{buildroot}%{perl_archlib}/vendor_perl/auto/Parse/Pidl/.packlist

# Already packaged by perl Parse:Yapp
rm -rf %{buildroot}%{perl_vendorlib}/Parse/Yapp
popd

%if %{with testsuite}
%check
TDB_NO_FSYNC=1 make %{?_smp_mflags} test FAIL_IMMEDIATELY=1
#endif with testsuite
%endif

%post
%systemd_post smb.service
%systemd_post nmb.service
exit 0

%preun
%systemd_preun smb.service
%systemd_preun nmb.service

%postun
%systemd_postun_with_restart smb.service
%systemd_postun_with_restart nmb.service

%pre common
getent group printadmin >/dev/null || groupadd -r printadmin || :

%post common
/sbin/ldconfig
/usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/samba.conf
if [ -d /var/cache/samba ]; then
    mv /var/cache/samba/netsamlogon_cache.tdb /var/lib/samba/ 2>/dev/null
    mv /var/cache/samba/winbindd_cache.tdb /var/lib/samba/ 2>/dev/null
    rm -rf /var/cache/samba/
    ln -sf /var/cache/samba /var/lib/samba/
fi

%post client
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
    cups_backend_smb \
    %{_bindir}/smbspool 10

%postun client
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove cups_backend_smb %{_bindir}/smbspool
fi

%post client-libs -p /sbin/ldconfig

%postun client-libs -p /sbin/ldconfig

%post common-libs -p /sbin/ldconfig

%postun common-libs -p /sbin/ldconfig

%if %with_dc
%post dc-libs -p /sbin/ldconfig

%postun dc-libs -p /sbin/ldconfig

%post dc
%systemd_post samba.service

%preun dc
%systemd_preun samba.service

%postun dc
%systemd_postun_with_restart samba.service
#endif with_dc
%endif

%post krb5-printing
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
        cups_backend_smb \
        %{_libexecdir}/samba/smbspool_krb5_wrapper 50

%postun krb5-printing
if [ $1 -eq 0 ] ; then
        %{_sbindir}/update-alternatives --remove cups_backend_smb %{_libexecdir}/samba/smbspool_krb5_wrapper
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%if %{with_vfs_glusterfs}
%posttrans vfs-glusterfs
if type getsebool &>/dev/null && getsebool samba_load_libgfapi &>/dev/null; then
        setsebool -P samba_load_libgfapi 1 &>/dev/null || true
fi

%postun vfs-glusterfs
if type getsebool &>/dev/null && getsebool samba_load_libgfapi &>/dev/null; then
        setsebool -P samba_load_libgfapi 0 &>/dev/null || true
fi
%endif

%if %with_libsmbclient
%post -n libsmbclient -p /sbin/ldconfig

%postun -n libsmbclient -p /sbin/ldconfig
%endif

%if %with_libwbclient
%posttrans -n libwbclient
# It has to be posttrans here to make sure all files of a previous version
# without alternatives support are removed
%{_sbindir}/update-alternatives \
        --install \
        %{_libdir}/libwbclient.so.%{libwbc_alternatives_version} \
        libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
        %{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version} \
        10
/sbin/ldconfig

%preun -n libwbclient
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives \
            --remove \
            libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
            %{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version}
fi
/sbin/ldconfig

%posttrans -n libwbclient-devel
%{_sbindir}/update-alternatives \
        --install %{_libdir}/libwbclient.so \
        libwbclient.so%{libwbc_alternatives_suffix} \
        %{_libdir}/samba/wbclient/libwbclient.so \
        10

%preun -n libwbclient-devel
# alternatives checks if the file which should be removed is a link or not, but
# not if it points to the /etc/alternatives directory or to some other place.
# When downgrading to a version where alternatives is not used and
# libwbclient.so is a link and not a file it will be removed. The following
# check removes the alternatives files manually if that is the case.
if [ $1 -eq 0 ]; then
    if [ "`readlink %{_libdir}/libwbclient.so`" == "libwbclient.so.%{libwbc_alternatives_version}" ]; then
        /bin/rm -f /etc/alternatives/libwbclient.so%{libwbc_alternatives_suffix} \
            /var/lib/alternatives/libwbclient.so%{libwbc_alternatives_suffix} 2> /dev/null
    else
        %{_sbindir}/update-alternatives \
            --remove \
            libwbclient.so%{libwbc_alternatives_suffix} \
            %{_libdir}/samba/wbclient/libwbclient.so
    fi
fi

#endif with_libwbclient
%endif

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%pre winbind
/usr/sbin/groupadd -g 88 wbpriv >/dev/null 2>&1 || :

%post winbind
%systemd_post winbind.service

%preun winbind
%systemd_preun winbind.service

%postun winbind
%systemd_postun_with_restart winbind.service

%postun winbind-krb5-locator
if [ "$1" -ge "1" ]; then
        if [ "`readlink %{_sysconfdir}/alternatives/winbind_krb5_locator.so`" == "%{_libdir}/samba/krb5/winbind_krb5_locator.so" ]; then
                %{_sbindir}/update-alternatives --set winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
        fi
fi

%post winbind-krb5-locator
%{_sbindir}/update-alternatives --install %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so \
                                winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so 10

%preun winbind-krb5-locator
if [ $1 -eq 0 ]; then
        %{_sbindir}/update-alternatives --remove winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
fi

%post winbind-modules -p /sbin/ldconfig

%postun winbind-modules -p /sbin/ldconfig

%if %with_clustering_support
%post -n ctdb
/usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/ctdb.conf
%systemd_post ctdb.service
# Enable some legacy scripts
legacy_scripts="00.ctdb 01.reclock 05.system 10.interface 50.samba"
if grep -q -i "CTDB_MANAGES_WINBIND=yes" /etc/sysconfig/ctdb; then
        legacy_scripts="${legacy_scripts} 49.winbind"
fi
for s in $legacy_scripts ; do
        /usr/bin/ctdb event script enable legacy $s
done

%if %{with_vfs_glusterfs}
%posttrans -n ctdb
if type getsebool &>/dev/null && getsebool use_fusefs_home_dirs &>/dev/null; then
        setsebool -P use_fusefs_home_dirs 1 &>/dev/null || true
fi

%endif

%preun -n ctdb
%systemd_preun ctdb.service

%postun -n ctdb
%systemd_postun_with_restart ctdb.service

%if %{with_vfs_glusterfs}
if type getsebool &>/dev/null && getsebool use_fusefs_home_dirs &>/dev/null; then
        setsebool -P use_fusefs_home_dirs 0 &>/dev/null || true
fi
%endif
%endif

%clean
rm -rf %{buildroot}

### SAMBA
%files
%license COPYING
%doc README.md WHATSNEW.txt
%doc examples/autofs examples/LDAP examples/misc
%doc examples/printer-accounting examples/printing
%doc packaging/README.downgrade
%{_bindir}/smbstatus
%{_sbindir}/eventlogadm
%{_sbindir}/nmbd
%{_sbindir}/smbd
%if %{with_dc}
# This is only used by vfs_dfs_samba4
%{_libdir}/samba/libdfs-server-ad-samba4.so
%endif
%dir %{_libdir}/samba/auth
%{_libdir}/samba/auth/script.so
%{_libdir}/samba/auth/unix.so
%dir %{_libdir}/samba/vfs
%{_libdir}/samba/vfs/acl_tdb.so
%{_libdir}/samba/vfs/acl_xattr.so
%{_libdir}/samba/vfs/aio_fork.so
%{_libdir}/samba/vfs/aio_pthread.so
%{_libdir}/samba/vfs/audit.so
%{_libdir}/samba/vfs/btrfs.so
%{_libdir}/samba/vfs/cap.so
%{_libdir}/samba/vfs/catia.so
%{_libdir}/samba/vfs/commit.so
%{_libdir}/samba/vfs/crossrename.so
%{_libdir}/samba/vfs/default_quota.so
%if %{with_dc}
%{_libdir}/samba/vfs/dfs_samba4.so
%endif
%{_libdir}/samba/vfs/dirsort.so
%{_libdir}/samba/vfs/expand_msdfs.so
%{_libdir}/samba/vfs/extd_audit.so
%{_libdir}/samba/vfs/fake_perms.so
%{_libdir}/samba/vfs/fileid.so
%{_libdir}/samba/vfs/fruit.so
%{_libdir}/samba/vfs/full_audit.so
%{_libdir}/samba/vfs/gpfs.so
%{_libdir}/samba/vfs/linux_xfs_sgid.so
%{_libdir}/samba/vfs/media_harmony.so
%{_libdir}/samba/vfs/netatalk.so
%{_libdir}/samba/vfs/offline.so
%{_libdir}/samba/vfs/preopen.so
%{_libdir}/samba/vfs/readahead.so
%{_libdir}/samba/vfs/readonly.so
%{_libdir}/samba/vfs/recycle.so
%{_libdir}/samba/vfs/shadow_copy.so
%{_libdir}/samba/vfs/shadow_copy2.so
%{_libdir}/samba/vfs/shell_snap.so
%{_libdir}/samba/vfs/snapper.so
%{_libdir}/samba/vfs/streams_depot.so
%{_libdir}/samba/vfs/streams_xattr.so
%{_libdir}/samba/vfs/syncops.so
%{_libdir}/samba/vfs/time_audit.so
%{_libdir}/samba/vfs/unityed_media.so
%{_libdir}/samba/vfs/virusfilter.so
%{_libdir}/samba/vfs/worm.so
%{_libdir}/samba/vfs/xattr_tdb.so

%{_unitdir}/nmb.service
%{_unitdir}/smb.service
%attr(1777,root,root) %dir /var/spool/samba
%dir %{_sysconfdir}/openldap/schema
%config %{_sysconfdir}/openldap/schema/samba.schema
%config(noreplace) %{_sysconfdir}/pam.d/samba
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_netatalk.8*
%{_mandir}/man8/vfs_offline.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_shell_snap.8*
%{_mandir}/man8/vfs_snapper.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_unityed_media.8*
%{_mandir}/man8/vfs_virusfilter.8*
%{_mandir}/man8/vfs_worm.8*
%{_mandir}/man8/vfs_xattr_tdb.8*

%if ! %{with_vfs_glusterfs}
%exclude %{_mandir}/man8/vfs_glusterfs.8*
%exclude %{_mandir}/man8/vfs_glusterfs_fuse.8*
%endif

%attr(775,root,printadmin) %dir /var/lib/samba/drivers

### CLIENT
%files client
%doc source3/client/README.smbspool
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%if %{defined rhel} && %{rhel} >= 8
%{_bindir}/dumpmscat
%endif
%{_bindir}/findsmb
%{_bindir}/mvxattr
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/regdiff
%{_bindir}/regpatch
%{_bindir}/regshell
%{_bindir}/regtree
%{_bindir}/rpcclient
%{_bindir}/samba-regedit
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/smbtree
%dir %{_libexecdir}/samba
%ghost %{_libexecdir}/samba/cups_backend_smb
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/oLschema2ldif.1*
%{_mandir}/man1/regdiff.1*
%{_mandir}/man1/regpatch.1*
%{_mandir}/man1/regshell.1*
%{_mandir}/man1/regtree.1*
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/log2pcap.1*
%{_mandir}/man1/mvxattr.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man7/traffic_learner.7.*
%{_mandir}/man7/traffic_replay.7.*
%{_mandir}/man8/cifsdd.8.*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/smbspool.8*

%if %{with_internal_tdb}
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbrestore
%{_bindir}/tdbtool
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbrestore.8*
%{_mandir}/man8/tdbtool.8*
%endif

%if %with_internal_ldb
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir}/samba/libldb-cmdline-samba4.so
%{_libdir}/samba/ldb/asq.so
%{_libdir}/samba/ldb/paged_searches.so
%{_libdir}/samba/ldb/rdn_name.so
%{_libdir}/samba/ldb/sample.so
%{_libdir}/samba/ldb/server_sort.so
%{_libdir}/samba/ldb/skel.so
%{_libdir}/samba/ldb/tdb.so
%{_mandir}/man1/ldbadd.1.gz
%{_mandir}/man1/ldbdel.1.gz
%{_mandir}/man1/ldbedit.1.gz
%{_mandir}/man1/ldbmodify.1.gz
%{_mandir}/man1/ldbrename.1.gz
%{_mandir}/man1/ldbsearch.1.gz
%endif

### CLIENT-LIBS
%files client-libs
%{_libdir}/libdcerpc-binding.so.*
%{_libdir}/libndr.so.*
%{_libdir}/libndr-krb5pac.so.*
%{_libdir}/libndr-nbt.so.*
%{_libdir}/libndr-standard.so.*
%{_libdir}/libnetapi.so.*
%{_libdir}/libsamba-credentials.so.*
%{_libdir}/libsamba-errors.so.*
%{_libdir}/libsamba-passdb.so.*
%{_libdir}/libsamba-util.so.*
%{_libdir}/libsamba-hostconfig.so.*
%{_libdir}/libsamdb.so.*
%{_libdir}/libsmbconf.so.*
%{_libdir}/libsmbldap.so.*
%{_libdir}/libtevent-util.so.*
%{_libdir}/libdcerpc.so.*

%dir %{_libdir}/samba
%{_libdir}/samba/libCHARSET3-samba4.so
%{_libdir}/samba/libMESSAGING-SEND-samba4.so
%{_libdir}/samba/libMESSAGING-samba4.so
%{_libdir}/samba/libaddns-samba4.so
%{_libdir}/samba/libads-samba4.so
%{_libdir}/samba/libasn1util-samba4.so
%{_libdir}/samba/libauth-samba4.so
%{_libdir}/samba/libauthkrb5-samba4.so
%{_libdir}/samba/libcli-cldap-samba4.so
%{_libdir}/samba/libcli-ldap-common-samba4.so
%{_libdir}/samba/libcli-ldap-samba4.so
%{_libdir}/samba/libcli-nbt-samba4.so
%{_libdir}/samba/libcli-smb-common-samba4.so
%{_libdir}/samba/libcli-spoolss-samba4.so
%{_libdir}/samba/libcliauth-samba4.so
%{_libdir}/samba/libclidns-samba4.so
%{_libdir}/samba/libcluster-samba4.so
%{_libdir}/samba/libcmdline-contexts-samba4.so
%{_libdir}/samba/libcmdline-credentials-samba4.so
%{_libdir}/samba/libcommon-auth-samba4.so
%{_libdir}/samba/libctdb-event-client-samba4.so
%{_libdir}/samba/libdbwrap-samba4.so
%{_libdir}/samba/libdcerpc-samba-samba4.so
%{_libdir}/samba/libevents-samba4.so
%{_libdir}/samba/libflag-mapping-samba4.so
%{_libdir}/samba/libgenrand-samba4.so
%{_libdir}/samba/libgensec-samba4.so
%{_libdir}/samba/libgpext-samba4.so
%{_libdir}/samba/libgpo-samba4.so
%{_libdir}/samba/libgse-samba4.so
%{_libdir}/samba/libhttp-samba4.so
%{_libdir}/samba/libinterfaces-samba4.so
%{_libdir}/samba/libiov-buf-samba4.so
%{_libdir}/samba/libkrb5samba-samba4.so
%{_libdir}/samba/libldbsamba-samba4.so
%{_libdir}/samba/liblibcli-lsa3-samba4.so
%{_libdir}/samba/liblibcli-netlogon3-samba4.so
%{_libdir}/samba/liblibsmb-samba4.so
%{_libdir}/samba/libmessages-dgm-samba4.so
%{_libdir}/samba/libmessages-util-samba4.so
%if %{defined rhel} && %{rhel} >= 8
%{_libdir}/samba/libmscat-samba4.so
%endif
%{_libdir}/samba/libmsghdr-samba4.so
%{_libdir}/samba/libmsrpc3-samba4.so
%{_libdir}/samba/libndr-samba-samba4.so
%{_libdir}/samba/libndr-samba4.so
%{_libdir}/samba/libnet-keytab-samba4.so
%{_libdir}/samba/libnetif-samba4.so
%{_libdir}/samba/libnpa-tstream-samba4.so
%{_libdir}/samba/libposix-eadb-samba4.so
%{_libdir}/samba/libprinter-driver-samba4.so
%{_libdir}/samba/libprinting-migrate-samba4.so
%{_libdir}/samba/libreplace-samba4.so
%{_libdir}/samba/libregistry-samba4.so
%{_libdir}/samba/libsamba-cluster-support-samba4.so
%{_libdir}/samba/libsamba-debug-samba4.so
%{_libdir}/samba/libsamba-modules-samba4.so
%{_libdir}/samba/libsamba-security-samba4.so
%{_libdir}/samba/libsamba-sockets-samba4.so
%{_libdir}/samba/libsamba3-util-samba4.so
%{_libdir}/samba/libsamdb-common-samba4.so
%{_libdir}/samba/libsecrets3-samba4.so
%{_libdir}/samba/libserver-id-db-samba4.so
%{_libdir}/samba/libserver-role-samba4.so
%{_libdir}/samba/libsmb-transport-samba4.so
%{_libdir}/samba/libsmbclient-raw-samba4.so
%{_libdir}/samba/libsmbd-base-samba4.so
%{_libdir}/samba/libsmbd-conn-samba4.so
%{_libdir}/samba/libsmbd-shim-samba4.so
%{_libdir}/samba/libsmbldaphelper-samba4.so
%{_libdir}/samba/libsys-rw-samba4.so
%{_libdir}/samba/libsocket-blocking-samba4.so
%{_libdir}/samba/libtalloc-report-samba4.so
%{_libdir}/samba/libtdb-wrap-samba4.so
%{_libdir}/samba/libtime-basic-samba4.so
%{_libdir}/samba/libtorture-samba4.so
%{_libdir}/samba/libtrusts-util-samba4.so
%{_libdir}/samba/libutil-cmdline-samba4.so
%{_libdir}/samba/libutil-reg-samba4.so
%{_libdir}/samba/libutil-setid-samba4.so
%{_libdir}/samba/libutil-tdb-samba4.so

%if ! %with_libwbclient
%{_libdir}/samba/libwbclient.so.*
%{_libdir}/samba/libwinbind-client-samba4.so
#endif ! with_libwbclient
%endif

%if ! %with_libsmbclient
%{_libdir}/samba/libsmbclient.so.*
%{_mandir}/man7/libsmbclient.7*
#endif ! with_libsmbclient
%endif

%if %{with_internal_talloc}
%{_libdir}/samba/libtalloc.so.*
%{_libdir}/samba/libpytalloc-util.*.so.*
%{python3_sitearch}/talloc.*.so
%exclude %{_mandir}/man3/talloc.3.gz
%endif

%if %{with_internal_tevent}
%{_libdir}/samba/libtevent.so.*
%{python3_sitearch}/__pycache__/tevent.*.pyc
%{python3_sitearch}/tevent.py*
%{python3_sitearch}/_tevent.*.so
%endif

%if %{with_internal_tdb}
%{_libdir}/samba/libtdb.so.*
%{python3_sitearch}/__pycache__/_tdb_text.*.pyc
%{python3_sitearch}/_tdb_text.py
%{python3_sitearch}/tdb.*.so
%endif

%if %{with_internal_ldb}
%{_libdir}/samba/libldb.so.*
%{_libdir}/samba/libldb-tdb-err-map-samba4.so
%{_libdir}/samba/libldb-tdb-int-samba4.so
%{_libdir}/samba/libpyldb-util.*.so.*
%{python3_sitearch}/__pycache__/_ldb_text.*.pyc
%{python3_sitearch}/_ldb_text.py*
%{python3_sitearch}/ldb.*.so
%exclude %{_mandir}/man3/ldb.3.gz
%endif

### COMMON
%files common
%{_tmpfilesdir}/samba.conf
%dir %{_sysconfdir}/logrotate.d/
%config(noreplace) %{_sysconfdir}/logrotate.d/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(0700,root,root) %dir /var/log/samba/old
%ghost %dir /run/samba
%ghost %dir /run/winbindd
%dir /var/lib/samba
%attr(700,root,root) %dir /var/lib/samba/private
%dir /var/lib/samba/lock
%attr(755,root,root) %dir %{_sysconfdir}/samba
# FIXME: do we want to enforce the changed settings for stat cache ? if so, then
# we need to remove the "noreplace"
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%{_sysconfdir}/samba/smb.conf.example
%config(noreplace) %{_sysconfdir}/samba/lmhosts
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*

### COMMON-libs
%files common-libs
# common libraries
%{_libdir}/samba/libpopt-samba3-cmdline-samba4.so
%{_libdir}/samba/libpopt-samba3-samba4.so
%if %{with_intel_aes_accel}
%{_libdir}/samba/libaesni-intel-samba4.so
%endif

%dir %{_libdir}/samba/ldb
%{_libdir}/samba/ldb/ldb.so
%{_libdir}/samba/libldb-key-value-samba4.so

%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so

%files common-tools
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/testparm
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man8/net.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbpasswd.8*

### DC
%if %{with_dc}
%files dc
%{_unitdir}/samba.service
%{_bindir}/samba-tool
%{_sbindir}/samba
%{_sbindir}/samba_dnsupdate
%{_sbindir}/samba_downgrade_db
%{_sbindir}/samba-gpupdate
%{_sbindir}/samba_kcc
%{_sbindir}/samba_spnupdate
%{_sbindir}/samba_upgradedns

%{_libdir}/krb5/plugins/kdb/samba.so

%{_libdir}/samba/auth/samba4.so
%{_libdir}/samba/libpac-samba4.so
%dir %{_libdir}/samba/gensec
%{_libdir}/samba/gensec/krb5.so
%{_libdir}/samba/ldb/acl.so
%{_libdir}/samba/ldb/aclread.so
%{_libdir}/samba/ldb/anr.so
%{_libdir}/samba/ldb/audit_log.so
%{_libdir}/samba/ldb/count_attrs.so
%{_libdir}/samba/ldb/descriptor.so
%{_libdir}/samba/ldb/dirsync.so
%{_libdir}/samba/ldb/dns_notify.so
%{_libdir}/samba/ldb/dsdb_notification.so
%{_libdir}/samba/ldb/encrypted_secrets.so
%{_libdir}/samba/ldb/extended_dn_in.so
%{_libdir}/samba/ldb/extended_dn_out.so
%{_libdir}/samba/ldb/extended_dn_store.so
%{_libdir}/samba/ldb/group_audit_log.so
%{_libdir}/samba/ldb/ildap.so
%{_libdir}/samba/ldb/instancetype.so
%{_libdir}/samba/ldb/lazy_commit.so
%{_libdir}/samba/ldb/ldbsamba_extensions.so
%{_libdir}/samba/ldb/linked_attributes.so
%{_libdir}/samba/ldb/local_password.so
%{_libdir}/samba/ldb/new_partition.so
%{_libdir}/samba/ldb/objectclass.so
%{_libdir}/samba/ldb/objectclass_attrs.so
%{_libdir}/samba/ldb/objectguid.so
%{_libdir}/samba/ldb/operational.so
%{_libdir}/samba/ldb/paged_results.so
%{_libdir}/samba/ldb/partition.so
%{_libdir}/samba/ldb/password_hash.so
%{_libdir}/samba/ldb/ranged_results.so
%{_libdir}/samba/ldb/repl_meta_data.so
%{_libdir}/samba/ldb/resolve_oids.so
%{_libdir}/samba/ldb/rootdse.so
%{_libdir}/samba/ldb/samba3sam.so
%{_libdir}/samba/ldb/samba3sid.so
%{_libdir}/samba/ldb/samba_dsdb.so
%{_libdir}/samba/ldb/samba_secrets.so
%{_libdir}/samba/ldb/samldb.so
%{_libdir}/samba/ldb/schema_data.so
%{_libdir}/samba/ldb/schema_load.so
%{_libdir}/samba/ldb/secrets_tdb_sync.so
%{_libdir}/samba/ldb/show_deleted.so
%{_libdir}/samba/ldb/simple_dn.so
%{_libdir}/samba/ldb/simple_ldap_map.so
%{_libdir}/samba/ldb/subtree_delete.so
%{_libdir}/samba/ldb/subtree_rename.so
%{_libdir}/samba/ldb/tombstone_reanimate.so
%{_libdir}/samba/ldb/unique_object_sids.so
%{_libdir}/samba/ldb/update_keytab.so
%{_libdir}/samba/ldb/vlv.so
%{_libdir}/samba/ldb/wins_ldb.so
%{_libdir}/samba/vfs/posix_eadb.so
%dir /var/lib/samba/sysvol
%{_mandir}/man8/samba.8*
%{_mandir}/man8/samba_downgrade_db.8*
%{_mandir}/man8/samba-gpupdate.8*
%{_mandir}/man8/samba-tool.8*

%files dc-provision
%{_datadir}/samba/setup

### DC-LIBS
%files dc-libs
%{_libdir}/samba/libdb-glue-samba4.so
%{_libdir}/samba/libprocess-model-samba4.so
%{_libdir}/samba/libservice-samba4.so
%dir %{_libdir}/samba/process_model
%{_libdir}/samba/process_model/prefork.so
%{_libdir}/samba/process_model/standard.so
%dir %{_libdir}/samba/service
%{_libdir}/samba/service/cldap.so
%{_libdir}/samba/service/dcerpc.so
%{_libdir}/samba/service/dns.so
%{_libdir}/samba/service/dns_update.so
%{_libdir}/samba/service/drepl.so
%{_libdir}/samba/service/kcc.so
%{_libdir}/samba/service/kdc.so
%{_libdir}/samba/service/ldap.so
%{_libdir}/samba/service/nbtd.so
%{_libdir}/samba/service/ntp_signd.so
%{_libdir}/samba/service/s3fs.so
%{_libdir}/samba/service/winbindd.so
%{_libdir}/samba/service/wrepl.so
%{_libdir}/libdcerpc-server.so.*
%{_libdir}/samba/libdnsserver-common-samba4.so
%{_libdir}/samba/libdsdb-module-samba4.so
%{_libdir}/samba/libdsdb-garbage-collect-tombstones-samba4.so
%{_libdir}/samba/libscavenge-dns-records-samba4.so

### DC-BIND
%files dc-bind-dlz
%attr(770,root,named) %dir /var/lib/samba/bind-dns
%dir %{_libdir}/samba/bind9
%{_libdir}/samba/bind9/dlz_bind9.so
%{_libdir}/samba/bind9/dlz_bind9_9.so
%{_libdir}/samba/bind9/dlz_bind9_10.so
%{_libdir}/samba/bind9/dlz_bind9_11.so
%{_libdir}/samba/bind9/dlz_bind9_12.so
#endif with_dc
%endif

### DEVEL
%files devel
%{_includedir}/samba-4.0/charset.h
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/hresult.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/ntstatus_gen.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/core/werror_gen.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/domain_credentials.h
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_misc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl_c.h
%{_includedir}/samba-4.0/gen_ndr/netlogon.h
%{_includedir}/samba-4.0/gen_ndr/samr.h
%{_includedir}/samba-4.0/gen_ndr/security.h
%{_includedir}/samba-4.0/gen_ndr/server_id.h
%{_includedir}/samba-4.0/gen_ndr/svcctl.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/blocking.h
%{_includedir}/samba-4.0/util/byteorder.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/discard.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/string_wrappers.h
%{_includedir}/samba-4.0/util/substitute.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util/tfork.h
%{_includedir}/samba-4.0/util_ldb.h
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so
%{_libdir}/libndr.so
%{_libdir}/libnetapi.so
%{_libdir}/libsamba-credentials.so
%{_libdir}/libsamba-errors.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-util.so
%{_libdir}/libsamdb.so
%{_libdir}/libsmbconf.so
%{_libdir}/libtevent-util.so
%{_libdir}/pkgconfig/dcerpc.pc
%{_libdir}/pkgconfig/dcerpc_samr.pc
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_krb5pac.pc
%{_libdir}/pkgconfig/ndr_nbt.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/pkgconfig/netapi.pc
%{_libdir}/pkgconfig/samba-credentials.pc
%{_libdir}/pkgconfig/samba-hostconfig.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/samdb.pc
%{_libdir}/libsamba-passdb.so
%{_libdir}/libsmbldap.so

%if %with_dc
%{_includedir}/samba-4.0/dcerpc_server.h
%{_libdir}/libdcerpc-server.so
%{_libdir}/pkgconfig/dcerpc_server.pc
%endif

%if ! %with_libsmbclient
%{_includedir}/samba-4.0/libsmbclient.h
#endif ! with_libsmbclient
%endif

%if ! %with_libwbclient
%{_includedir}/samba-4.0/wbclient.h
#endif ! with_libwbclient
%endif

### VFS-CEPHFS
%if %{with_vfs_cephfs}
%files vfs-cephfs
%{_libdir}/samba/vfs/ceph.so
%{_libdir}/samba/vfs/ceph_snapshots.so
%{_mandir}/man8/vfs_ceph.8*
%{_mandir}/man8/vfs_ceph_snapshots.8*
%endif

### VFS-GLUSTERFS
%if %{with_vfs_glusterfs}
%files vfs-glusterfs
%{_libdir}/samba/vfs/glusterfs.so
%{_libdir}/samba/vfs/glusterfs_fuse.so
%{_mandir}/man8/vfs_glusterfs.8*
%{_mandir}/man8/vfs_glusterfs_fuse.8*
%endif

### KRB5-PRINTING
%files krb5-printing
%attr(0700,root,root) %{_libexecdir}/samba/smbspool_krb5_wrapper
%{_mandir}/man8/smbspool_krb5_wrapper.8*

### LIBS
%files libs
%{_libdir}/libdcerpc-samr.so.*

%{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so
%{_libdir}/samba/libauth4-samba4.so
%{_libdir}/samba/libauth-unix-token-samba4.so
%{_libdir}/samba/libdcerpc-samba4.so
%{_libdir}/samba/libshares-samba4.so
%{_libdir}/samba/libsmbpasswdparser-samba4.so
%{_libdir}/samba/libxattr-tdb-samba4.so

### LIBSMBCLIENT
%if %with_libsmbclient
%files -n libsmbclient
%{_libdir}/libsmbclient.so.*

### LIBSMBCLIENT-DEVEL
%files -n libsmbclient-devel
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*
#endif with_libsmbclient
%endif

### LIBWBCLIENT
%if %with_libwbclient
%files -n libwbclient
%{_libdir}/samba/wbclient/libwbclient.so.*
%{_libdir}/samba/libwinbind-client-samba4.so

### LIBWBCLIENT-DEVEL
%files -n libwbclient-devel
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/samba/wbclient/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc
#endif with_libwbclient
%endif

### PIDL
%files pidl
%doc pidl/README
%attr(755,root,root) %{_bindir}/pidl
%dir %{perl_vendorlib}/Parse
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl.pm
%dir %{perl_vendorlib}/Parse/Pidl
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/CUtil.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Expr.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/ODL.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Typelist.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/IDL.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Compat.pm
%dir %{perl_vendorlib}/Parse/Pidl/Wireshark
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Wireshark/Conformance.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Wireshark/NDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Dump.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba3
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/ServerNDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/ClientNDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/Template.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Header.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/COM
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Header.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Proxy.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Stub.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Python.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Template.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/NDR
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Server.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Client.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Parser.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/TDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/NDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Util.pm
%attr(644,root,root) %{_mandir}/man1/pidl.1*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Dump.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::NDR.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Util.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Wireshark::Conformance.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Wireshark::NDR.3pm*

### PYTHON3
%files -n python3-%{name}
%dir %{python3_sitearch}/samba/
%{python3_sitearch}/samba/__init__.py
%dir %{python3_sitearch}/samba/__pycache__
%{python3_sitearch}/samba/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/__pycache__/colour.*.pyc
%{python3_sitearch}/samba/__pycache__/common.*.pyc
%{python3_sitearch}/samba/__pycache__/compat.*.pyc
%{python3_sitearch}/samba/__pycache__/dbchecker.*.pyc
%{python3_sitearch}/samba/__pycache__/descriptor.*.pyc
%{python3_sitearch}/samba/__pycache__/drs_utils.*.pyc
%{python3_sitearch}/samba/__pycache__/getopt.*.pyc
%{python3_sitearch}/samba/__pycache__/gpclass.*.pyc
%{python3_sitearch}/samba/__pycache__/gp_ext_loader.*.pyc
%{python3_sitearch}/samba/__pycache__/gp_sec_ext.*.pyc
%{python3_sitearch}/samba/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/samba/__pycache__/idmap.*.pyc
%{python3_sitearch}/samba/__pycache__/join.*.pyc
%{python3_sitearch}/samba/__pycache__/logger.*.pyc
%{python3_sitearch}/samba/__pycache__/mdb_util.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_display_specifiers.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_schema.*.pyc
%{python3_sitearch}/samba/__pycache__/ndr.*.pyc
%{python3_sitearch}/samba/__pycache__/ntacls.*.pyc
%{python3_sitearch}/samba/__pycache__/sd_utils.*.pyc
%{python3_sitearch}/samba/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/__pycache__/subnets.*.pyc
%{python3_sitearch}/samba/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/samba/__pycache__/upgrade.*.pyc
%{python3_sitearch}/samba/__pycache__/upgradehelpers.*.pyc
%{python3_sitearch}/samba/__pycache__/xattr.*.pyc
%{python3_sitearch}/samba/_glue.*.so
%{python3_sitearch}/samba/_ldb.*.so
%{python3_sitearch}/samba/auth.*.so
%{python3_sitearch}/samba/dbchecker.py
%{python3_sitearch}/samba/colour.py
%{python3_sitearch}/samba/common.py
%{python3_sitearch}/samba/compat.py
%{python3_sitearch}/samba/credentials.*.so
%{python3_sitearch}/samba/crypto.*.so
%dir %{python3_sitearch}/samba/dcerpc
%dir %{python3_sitearch}/samba/dcerpc/__pycache__
%{python3_sitearch}/samba/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/dcerpc/__init__.py
%{python3_sitearch}/samba/dcerpc/atsvc.*.so
%{python3_sitearch}/samba/dcerpc/auth.*.so
%{python3_sitearch}/samba/dcerpc/base.*.so
%{python3_sitearch}/samba/dcerpc/dcerpc.*.so
%{python3_sitearch}/samba/dcerpc/dfs.*.so
%{python3_sitearch}/samba/dcerpc/dns.*.so
%{python3_sitearch}/samba/dcerpc/dnsp.*.so
%{python3_sitearch}/samba/dcerpc/drsblobs.*.so
%{python3_sitearch}/samba/dcerpc/drsuapi.*.so
%{python3_sitearch}/samba/dcerpc/echo.*.so
%{python3_sitearch}/samba/dcerpc/epmapper.*.so
%{python3_sitearch}/samba/dcerpc/idmap.*.so
%{python3_sitearch}/samba/dcerpc/initshutdown.*.so
%{python3_sitearch}/samba/dcerpc/irpc.*.so
%{python3_sitearch}/samba/dcerpc/krb5pac.*.so
%{python3_sitearch}/samba/dcerpc/lsa.*.so
%{python3_sitearch}/samba/dcerpc/messaging.*.so
%{python3_sitearch}/samba/dcerpc/mgmt.*.so
%{python3_sitearch}/samba/dcerpc/misc.*.so
%{python3_sitearch}/samba/dcerpc/nbt.*.so
%{python3_sitearch}/samba/dcerpc/netlogon.*.so
%{python3_sitearch}/samba/dcerpc/ntlmssp.*.so
%{python3_sitearch}/samba/dcerpc/preg.*.so
%{python3_sitearch}/samba/dcerpc/samr.*.so
%{python3_sitearch}/samba/dcerpc/security.*.so
%{python3_sitearch}/samba/dcerpc/server_id.*.so
%{python3_sitearch}/samba/dcerpc/smb_acl.*.so
%{python3_sitearch}/samba/dcerpc/spoolss.*.so
%{python3_sitearch}/samba/dcerpc/srvsvc.*.so
%{python3_sitearch}/samba/dcerpc/svcctl.*.so
%{python3_sitearch}/samba/dcerpc/unixinfo.*.so
%{python3_sitearch}/samba/dcerpc/winbind.*.so
%{python3_sitearch}/samba/dcerpc/windows_event_ids.*.so
%{python3_sitearch}/samba/dcerpc/winreg.*.so
%{python3_sitearch}/samba/dcerpc/winspool.*.so
%{python3_sitearch}/samba/dcerpc/witness.*.so
%{python3_sitearch}/samba/dcerpc/wkssvc.*.so
%{python3_sitearch}/samba/dcerpc/xattr.*.so
%{python3_sitearch}/samba/descriptor.py
%{python3_sitearch}/samba/drs_utils.py
%{python3_sitearch}/samba/gensec.*.so
%{python3_sitearch}/samba/getopt.py
%{python3_sitearch}/samba/gpclass.py
%{python3_sitearch}/samba/gp_sec_ext.py
%{python3_sitearch}/samba/gpo.*.so
%{python3_sitearch}/samba/graph.py
%{python3_sitearch}/samba/hostconfig.py
%{python3_sitearch}/samba/idmap.py
%{python3_sitearch}/samba/join.py
%{python3_sitearch}/samba/messaging.*.so
%{python3_sitearch}/samba/ndr.py
%{python3_sitearch}/samba/net.*.so
%{python3_sitearch}/samba/ntstatus.*.so
%{python3_sitearch}/samba/posix_eadb.*.so
%dir %{python3_sitearch}/samba/emulate
%dir %{python3_sitearch}/samba/emulate/__pycache__
%{python3_sitearch}/samba/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/samba/emulate/__pycache__/traffic_packets.*.pyc
%{python3_sitearch}/samba/emulate/__init__.py
%{python3_sitearch}/samba/emulate/traffic.py
%{python3_sitearch}/samba/emulate/traffic_packets.py
%{python3_sitearch}/samba/gp_ext_loader.py
%dir %{python3_sitearch}/samba/gp_parse
%{python3_sitearch}/samba/gp_parse/__init__.py
%dir %{python3_sitearch}/samba/gp_parse/__pycache__
%{python3_sitearch}/samba/gp_parse/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_aas.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_csv.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_inf.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_ini.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_pol.*.pyc
%{python3_sitearch}/samba/gp_parse/gp_aas.py
%{python3_sitearch}/samba/gp_parse/gp_csv.py
%{python3_sitearch}/samba/gp_parse/gp_inf.py
%{python3_sitearch}/samba/gp_parse/gp_ini.py
%{python3_sitearch}/samba/gp_parse/gp_pol.py
%{python3_sitearch}/samba/logger.py
%{python3_sitearch}/samba/mdb_util.py
%{python3_sitearch}/samba/ms_display_specifiers.py
%{python3_sitearch}/samba/ms_schema.py
%{python3_sitearch}/samba/netbios.*.so
%dir %{python3_sitearch}/samba/netcmd
%{python3_sitearch}/samba/netcmd/__init__.py
%dir %{python3_sitearch}/samba/netcmd/__pycache__
%{python3_sitearch}/samba/netcmd/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/common.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/computer.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/contact.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dbcheck.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/delegation.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dns.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/domain.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/domain_backup.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/drs.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dsacl.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/forest.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/fsmo.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/group.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ldapcmp.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/main.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/nettime.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ntacl.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ou.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/processes.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/pso.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/rodc.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/spn.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/testparm.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/user.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/visualize.*.pyc
%{python3_sitearch}/samba/netcmd/common.py
%{python3_sitearch}/samba/netcmd/computer.py
%{python3_sitearch}/samba/netcmd/contact.py
%{python3_sitearch}/samba/netcmd/dbcheck.py
%{python3_sitearch}/samba/netcmd/delegation.py
%{python3_sitearch}/samba/netcmd/dns.py
%{python3_sitearch}/samba/netcmd/domain.py
%{python3_sitearch}/samba/netcmd/domain_backup.py
%{python3_sitearch}/samba/netcmd/drs.py
%{python3_sitearch}/samba/netcmd/dsacl.py
%{python3_sitearch}/samba/netcmd/forest.py
%{python3_sitearch}/samba/netcmd/fsmo.py
%{python3_sitearch}/samba/netcmd/gpo.py
%{python3_sitearch}/samba/netcmd/group.py
%{python3_sitearch}/samba/netcmd/ldapcmp.py
%{python3_sitearch}/samba/netcmd/main.py
%{python3_sitearch}/samba/netcmd/nettime.py
%{python3_sitearch}/samba/netcmd/ntacl.py
%{python3_sitearch}/samba/netcmd/ou.py
%{python3_sitearch}/samba/netcmd/processes.py
%{python3_sitearch}/samba/netcmd/pso.py
%{python3_sitearch}/samba/netcmd/rodc.py
%{python3_sitearch}/samba/netcmd/schema.py
%{python3_sitearch}/samba/netcmd/sites.py
%{python3_sitearch}/samba/netcmd/spn.py
%{python3_sitearch}/samba/netcmd/testparm.py
%{python3_sitearch}/samba/netcmd/user.py
%{python3_sitearch}/samba/netcmd/visualize.py
%{python3_sitearch}/samba/ntacls.py
%{python3_sitearch}/samba/param.*.so
%{python3_sitearch}/samba/policy.*.so
%{python3_sitearch}/samba/registry.*.so
%{python3_sitearch}/samba/security.*.so
%dir %{python3_sitearch}/samba/samba3
%{python3_sitearch}/samba/samba3/__init__.py
%dir %{python3_sitearch}/samba/samba3/__pycache__
%{python3_sitearch}/samba/samba3/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/samba3/libsmb_samba_internal.*.so
%{python3_sitearch}/samba/samba3/param.*.so
%{python3_sitearch}/samba/samba3/passdb.*.so
%{python3_sitearch}/samba/samba3/smbd.*.so
%{python3_sitearch}/samba/sd_utils.py
%{python3_sitearch}/samba/sites.py
%{python3_sitearch}/samba/subnets.py
%dir %{python3_sitearch}/samba/subunit
%{python3_sitearch}/samba/subunit/__init__.py
%dir %{python3_sitearch}/samba/subunit/__pycache__
%{python3_sitearch}/samba/subunit/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/subunit/__pycache__/run.*.pyc
%{python3_sitearch}/samba/subunit/run.py
%{python3_sitearch}/samba/tdb_util.py
%dir %{python3_sitearch}/samba/third_party
%{python3_sitearch}/samba/third_party/__init__.py
%dir %{python3_sitearch}/samba/third_party/__pycache__
%{python3_sitearch}/samba/third_party/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/upgrade.py
%{python3_sitearch}/samba/upgradehelpers.py
%{python3_sitearch}/samba/werror.*.so
%{python3_sitearch}/samba/xattr.py
%{python3_sitearch}/samba/xattr_native.*.so
%{python3_sitearch}/samba/xattr_tdb.*.so
# FIXME:
# /usr/lib64/libsamba-policy.cpython-36m-x86-64-linux-gnu.so
# /usr/lib64/libsamba-policy.cpython-36m-x86-64-linux-gnu.so.0
# /usr/lib64/libsamba-policy.cpython-36m-x86-64-linux-gnu.so.0.0.1
%{_libdir}/libsamba-policy.*.so*
# FIXME:
# /usr/lib64/pkgconfig/samba-policy.cpython-36m-x86_64-linux-gnu.pc
%{_libdir}/pkgconfig/samba-policy.*.pc
# FIXME:
# /usr/lib64/samba/libsamba-net.cpython-36m-x86-64-linux-gnu-samba4.so
# /usr/lib64/samba/libsamba-python.cpython-36m-x86-64-linux-gnu-samba4.so
%{_libdir}/samba/libsamba-net.*-samba4.so
%{_libdir}/samba/libsamba-python.*-samba4.so

%if %{with_dc}
%files -n python3-%{name}-dc
%{python3_sitearch}/samba/samdb.py
%{python3_sitearch}/samba/schema.py

%{python3_sitearch}/samba/__pycache__/domain_update.*.pyc
%{python3_sitearch}/samba/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/samba/__pycache__/forest_update.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_forest_updates_markdown.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_schema_markdown.*.pyc
%{python3_sitearch}/samba/__pycache__/remove_dc.*.pyc
%{python3_sitearch}/samba/__pycache__/samdb.*.pyc
%{python3_sitearch}/samba/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/__pycache__/uptodateness.*.pyc

%{python3_sitearch}/samba/dcerpc/dnsserver.*.so
%{python3_sitearch}/samba/dckeytab.*.so
%{python3_sitearch}/samba/dsdb.*.so
%{python3_sitearch}/samba/dsdb_dns.*.so
%{python3_sitearch}/samba/domain_update.py
%{python3_sitearch}/samba/forest_update.py
%{python3_sitearch}/samba/ms_forest_updates_markdown.py
%{python3_sitearch}/samba/ms_schema_markdown.py

%dir %{python3_sitearch}/samba/kcc
%{python3_sitearch}/samba/kcc/__init__.py
%{python3_sitearch}/samba/kcc/debug.py
%{python3_sitearch}/samba/kcc/graph.py
%{python3_sitearch}/samba/kcc/graph_utils.py
%{python3_sitearch}/samba/kcc/kcc_utils.py
%{python3_sitearch}/samba/kcc/ldif_import_export.py
%{python3_sitearch}/samba/dnsserver.py

%dir %{python3_sitearch}/samba/kcc/__pycache__
%{python3_sitearch}/samba/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/debug.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/ldif_import_export.*.pyc

%dir %{python3_sitearch}/samba/provision
%{python3_sitearch}/samba/provision/backend.py
%{python3_sitearch}/samba/provision/common.py
%{python3_sitearch}/samba/provision/kerberos.py
%{python3_sitearch}/samba/provision/kerberos_implementation.py
%{python3_sitearch}/samba/provision/sambadns.py

%dir %{python3_sitearch}/samba/provision/__pycache__
%{python3_sitearch}/samba/provision/__init__.py
%{python3_sitearch}/samba/provision/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/backend.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/common.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/kerberos.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/kerberos_implementation.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/sambadns.*.pyc

%{python3_sitearch}/samba/remove_dc.py
%{python3_sitearch}/samba/uptodateness.py
%endif

%files -n python3-%{name}-test
%dir %{python3_sitearch}/samba/tests
%{python3_sitearch}/samba/tests/__init__.py
%dir %{python3_sitearch}/samba/tests/__pycache__
%{python3_sitearch}/samba/tests/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_dsdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_pass_change.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_pass_change.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_ncalrpc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_netlogon.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_netlogon_bad_creds.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_samlogon.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_winbind.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/common.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/complex_expressions.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/core.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dckeytab.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_forwarder.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_invalid.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_packet.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_tkey.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_wildcard.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_lock.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_schema_attributes.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/docs.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/domain_backup.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/domain_backup_offline.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/encrypted_secrets.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gensec.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/get_opt.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/getdcname.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/glue.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/group_audit.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/join.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/krb5_credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_raw.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_referrals.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/loadparm.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/libsmb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/lsa_string.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/messaging.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netbios.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netcmd.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/net_join_no_spnego.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/net_join.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netlogonsvc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntacls.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntacls_backup.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlmdisabled.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth_krb5.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind_chauthtok.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind_warn_pwd_expire.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/param.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_fl2003.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_fl2008.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_gpgme.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_ldap.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_quality.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_test.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/policy.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/posixacl.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/prefork_restart.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/process_limits.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/provision.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pso.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/py_credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/registry.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3idmapdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3param.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3passdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3registry.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3windb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samba3sam.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samba_upgradedns_lmdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samdb_api.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/security.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/segfault.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smbd_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smbd_fuzztest.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/source.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/strings.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/subunitrun.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgrade.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgradeprovision.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgradeprovisionneeddc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/usage.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/xattr.*.pyc
%{python3_sitearch}/samba/tests/audit_log_base.py
%{python3_sitearch}/samba/tests/audit_log_dsdb.py
%{python3_sitearch}/samba/tests/audit_log_pass_change.py
%{python3_sitearch}/samba/tests/auth.py
%{python3_sitearch}/samba/tests/auth_log.py
%{python3_sitearch}/samba/tests/auth_log_base.py
%{python3_sitearch}/samba/tests/auth_log_ncalrpc.py
%{python3_sitearch}/samba/tests/auth_log_netlogon_bad_creds.py
%{python3_sitearch}/samba/tests/auth_log_netlogon.py
%{python3_sitearch}/samba/tests/auth_log_pass_change.py
%{python3_sitearch}/samba/tests/auth_log_samlogon.py
%{python3_sitearch}/samba/tests/auth_log_winbind.py
%dir %{python3_sitearch}/samba/tests/blackbox
%{python3_sitearch}/samba/tests/blackbox/__init__.py
%dir %{python3_sitearch}/samba/tests/blackbox/__pycache__
%{python3_sitearch}/samba/tests/blackbox/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/bug13653.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/check_output.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/downgradedatabase.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/ndrdump.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/netads_json.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/samba_dnsupdate.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcontrol.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcontrol_process.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_learner.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_replay.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_summary.*.pyc
%{python3_sitearch}/samba/tests/blackbox/bug13653.py
%{python3_sitearch}/samba/tests/blackbox/check_output.py
%{python3_sitearch}/samba/tests/blackbox/downgradedatabase.py
%{python3_sitearch}/samba/tests/blackbox/ndrdump.py
%{python3_sitearch}/samba/tests/blackbox/netads_json.py
%{python3_sitearch}/samba/tests/blackbox/samba_dnsupdate.py
%{python3_sitearch}/samba/tests/blackbox/smbcontrol.py
%{python3_sitearch}/samba/tests/blackbox/smbcontrol_process.py
%{python3_sitearch}/samba/tests/blackbox/traffic_learner.py
%{python3_sitearch}/samba/tests/blackbox/traffic_replay.py
%{python3_sitearch}/samba/tests/blackbox/traffic_summary.py
%{python3_sitearch}/samba/tests/common.py
%{python3_sitearch}/samba/tests/complex_expressions.py
%{python3_sitearch}/samba/tests/core.py
%{python3_sitearch}/samba/tests/credentials.py
%dir %{python3_sitearch}/samba/tests/dcerpc
%{python3_sitearch}/samba/tests/dcerpc/__init__.py
%dir %{python3_sitearch}/samba/tests/dcerpc/__pycache__
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/array.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/bare.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/integer.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/misc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/raw_protocol.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/raw_testcase.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/registry.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/rpc_talloc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/rpcecho.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/sam.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/srvsvc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/string_tests.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/testrpc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/unix.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/array.py
%{python3_sitearch}/samba/tests/dcerpc/bare.py
%{python3_sitearch}/samba/tests/dcerpc/dnsserver.py
%{python3_sitearch}/samba/tests/dcerpc/integer.py
%{python3_sitearch}/samba/tests/dcerpc/misc.py
%{python3_sitearch}/samba/tests/dcerpc/raw_protocol.py
%{python3_sitearch}/samba/tests/dcerpc/raw_testcase.py
%{python3_sitearch}/samba/tests/dcerpc/registry.py
%{python3_sitearch}/samba/tests/dcerpc/rpc_talloc.py
%{python3_sitearch}/samba/tests/dcerpc/rpcecho.py
%{python3_sitearch}/samba/tests/dcerpc/sam.py
%{python3_sitearch}/samba/tests/dcerpc/srvsvc.py
%{python3_sitearch}/samba/tests/dcerpc/string_tests.py
%{python3_sitearch}/samba/tests/dcerpc/testrpc.py
%{python3_sitearch}/samba/tests/dcerpc/unix.py
%{python3_sitearch}/samba/tests/dckeytab.py
%{python3_sitearch}/samba/tests/dns.py
%{python3_sitearch}/samba/tests/dns_base.py
%{python3_sitearch}/samba/tests/dns_forwarder.py
%dir %{python3_sitearch}/samba/tests/dns_forwarder_helpers
%{python3_sitearch}/samba/tests/dns_forwarder_helpers/__pycache__/server.*.pyc
%{python3_sitearch}/samba/tests/dns_forwarder_helpers/server.py
%{python3_sitearch}/samba/tests/dns_invalid.py
%{python3_sitearch}/samba/tests/dns_packet.py
%{python3_sitearch}/samba/tests/dns_tkey.py
%{python3_sitearch}/samba/tests/dns_wildcard.py
%{python3_sitearch}/samba/tests/dsdb.py
%{python3_sitearch}/samba/tests/dsdb_lock.py
%{python3_sitearch}/samba/tests/dsdb_schema_attributes.py
%{python3_sitearch}/samba/tests/docs.py
%{python3_sitearch}/samba/tests/domain_backup.py
%{python3_sitearch}/samba/tests/domain_backup_offline.py
%dir %{python3_sitearch}/samba/tests/emulate
%{python3_sitearch}/samba/tests/emulate/__init__.py
%dir %{python3_sitearch}/samba/tests/emulate/__pycache__
%{python3_sitearch}/samba/tests/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/samba/tests/emulate/__pycache__/traffic_packet.*.pyc
%{python3_sitearch}/samba/tests/emulate/traffic.py
%{python3_sitearch}/samba/tests/emulate/traffic_packet.py
%{python3_sitearch}/samba/tests/encrypted_secrets.py
%{python3_sitearch}/samba/tests/gensec.py
%{python3_sitearch}/samba/tests/getdcname.py
%{python3_sitearch}/samba/tests/get_opt.py
%{python3_sitearch}/samba/tests/glue.py
%{python3_sitearch}/samba/tests/gpo.py
%{python3_sitearch}/samba/tests/graph.py
%{python3_sitearch}/samba/tests/group_audit.py
%{python3_sitearch}/samba/tests/hostconfig.py
%{python3_sitearch}/samba/tests/join.py
%dir %{python3_sitearch}/samba/tests/kcc
%{python3_sitearch}/samba/tests/kcc/__init__.py
%dir %{python3_sitearch}/samba/tests/kcc/__pycache__
%{python3_sitearch}/samba/tests/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/ldif_import_export.*.pyc
%{python3_sitearch}/samba/tests/kcc/graph.py
%{python3_sitearch}/samba/tests/kcc/graph_utils.py
%{python3_sitearch}/samba/tests/kcc/kcc_utils.py
%{python3_sitearch}/samba/tests/kcc/ldif_import_export.py
%{python3_sitearch}/samba/tests/krb5_credentials.py
%{python3_sitearch}/samba/tests/ldap_raw.py
%{python3_sitearch}/samba/tests/ldap_referrals.py
%{python3_sitearch}/samba/tests/libsmb.py
%{python3_sitearch}/samba/tests/loadparm.py
%{python3_sitearch}/samba/tests/lsa_string.py
%{python3_sitearch}/samba/tests/messaging.py
%{python3_sitearch}/samba/tests/netbios.py
%{python3_sitearch}/samba/tests/netcmd.py
%{python3_sitearch}/samba/tests/net_join_no_spnego.py
%{python3_sitearch}/samba/tests/net_join.py
%{python3_sitearch}/samba/tests/netlogonsvc.py
%{python3_sitearch}/samba/tests/ntacls.py
%{python3_sitearch}/samba/tests/ntacls_backup.py
%{python3_sitearch}/samba/tests/ntlmdisabled.py
%{python3_sitearch}/samba/tests/ntlm_auth.py
%{python3_sitearch}/samba/tests/ntlm_auth_base.py
%{python3_sitearch}/samba/tests/ntlm_auth_krb5.py
%{python3_sitearch}/samba/tests/pam_winbind.py
%{python3_sitearch}/samba/tests/pam_winbind_chauthtok.py
%{python3_sitearch}/samba/tests/pam_winbind_warn_pwd_expire.py
%{python3_sitearch}/samba/tests/param.py
%{python3_sitearch}/samba/tests/password_hash.py
%{python3_sitearch}/samba/tests/password_hash_fl2003.py
%{python3_sitearch}/samba/tests/password_hash_fl2008.py
%{python3_sitearch}/samba/tests/password_hash_gpgme.py
%{python3_sitearch}/samba/tests/password_hash_ldap.py
%{python3_sitearch}/samba/tests/password_quality.py
%{python3_sitearch}/samba/tests/password_test.py
%{python3_sitearch}/samba/tests/policy.py
%{python3_sitearch}/samba/tests/posixacl.py
%{python3_sitearch}/samba/tests/prefork_restart.py
%{python3_sitearch}/samba/tests/process_limits.py
%{python3_sitearch}/samba/tests/provision.py
%{python3_sitearch}/samba/tests/pso.py
%{python3_sitearch}/samba/tests/py_credentials.py
%{python3_sitearch}/samba/tests/registry.py
%{python3_sitearch}/samba/tests/s3idmapdb.py
%{python3_sitearch}/samba/tests/s3param.py
%{python3_sitearch}/samba/tests/s3passdb.py
%{python3_sitearch}/samba/tests/s3registry.py
%{python3_sitearch}/samba/tests/s3windb.py
%{python3_sitearch}/samba/tests/samba3sam.py
%dir %{python3_sitearch}/samba/tests/samba_tool
%{python3_sitearch}/samba/tests/samba_tool/__init__.py
%dir %{python3_sitearch}/samba/tests/samba_tool/__pycache__
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/base.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/computer.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/contact.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/demote.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/dnscmd.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/drs_clone_dc_data_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/dsacl.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/forest.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/fsmo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/group.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/help.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/join.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/join_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/ntacl.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/ou.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/passwordsettings.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/processes.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/promote_dc_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/provision_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/provision_password_check.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/rodc.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/timecmd.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_check_password_script.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_base.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_gpg.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_userPassword.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_wdigest.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/visualize.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/visualize_drs.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/base.py
%{python3_sitearch}/samba/tests/samba_tool/computer.py
%{python3_sitearch}/samba/tests/samba_tool/contact.py
%{python3_sitearch}/samba/tests/samba_tool/demote.py
%{python3_sitearch}/samba/tests/samba_tool/dnscmd.py
%{python3_sitearch}/samba/tests/samba_tool/drs_clone_dc_data_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/dsacl.py
%{python3_sitearch}/samba/tests/samba_tool/forest.py
%{python3_sitearch}/samba/tests/samba_tool/fsmo.py
%{python3_sitearch}/samba/tests/samba_tool/gpo.py
%{python3_sitearch}/samba/tests/samba_tool/group.py
%{python3_sitearch}/samba/tests/samba_tool/help.py
%{python3_sitearch}/samba/tests/samba_tool/join.py
%{python3_sitearch}/samba/tests/samba_tool/join_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/ntacl.py
%{python3_sitearch}/samba/tests/samba_tool/ou.py
%{python3_sitearch}/samba/tests/samba_tool/passwordsettings.py
%{python3_sitearch}/samba/tests/samba_tool/processes.py
%{python3_sitearch}/samba/tests/samba_tool/promote_dc_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/provision_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/provision_password_check.py
%{python3_sitearch}/samba/tests/samba_tool/rodc.py
%{python3_sitearch}/samba/tests/samba_tool/schema.py
%{python3_sitearch}/samba/tests/samba_tool/sites.py
%{python3_sitearch}/samba/tests/samba_tool/timecmd.py
%{python3_sitearch}/samba/tests/samba_tool/user.py
%{python3_sitearch}/samba/tests/samba_tool/user_check_password_script.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_base.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_gpg.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_userPassword.py
%{python3_sitearch}/samba/tests/samba_tool/user_wdigest.py
%{python3_sitearch}/samba/tests/samba_tool/visualize.py
%{python3_sitearch}/samba/tests/samba_tool/visualize_drs.py
%{python3_sitearch}/samba/tests/samba_upgradedns_lmdb.py
%{python3_sitearch}/samba/tests/samdb.py
%{python3_sitearch}/samba/tests/samdb_api.py
%{python3_sitearch}/samba/tests/security.py
%{python3_sitearch}/samba/tests/segfault.py
%{python3_sitearch}/samba/tests/smb.py
%{python3_sitearch}/samba/tests/smbd_base.py
%{python3_sitearch}/samba/tests/smbd_fuzztest.py
%{python3_sitearch}/samba/tests/source.py
%{python3_sitearch}/samba/tests/strings.py
%{python3_sitearch}/samba/tests/subunitrun.py
%{python3_sitearch}/samba/tests/tdb_util.py
%{python3_sitearch}/samba/tests/upgrade.py
%{python3_sitearch}/samba/tests/upgradeprovision.py
%{python3_sitearch}/samba/tests/upgradeprovisionneeddc.py
%{python3_sitearch}/samba/tests/usage.py
%{python3_sitearch}/samba/tests/xattr.py

### TEST
%files test
%{_bindir}/gentest
%{_bindir}/locktest
%{_bindir}/masktest
%{_bindir}/ndrdump
%{_bindir}/smbtorture
%{_mandir}/man1/gentest.1*
%{_mandir}/man1/locktest.1*
%{_mandir}/man1/masktest.1*
%{_mandir}/man1/ndrdump.1*
%{_mandir}/man1/smbtorture.1*
%{_mandir}/man1/vfstest.1*

%if %{with testsuite}
# files to ignore in testsuite mode
%{_libdir}/samba/libnss-wrapper.so
%{_libdir}/samba/libsocket-wrapper.so
%{_libdir}/samba/libuid-wrapper.so
%endif

### TEST-LIBS
%files test-libs
%if %with_dc
%{_libdir}/samba/libdlz-bind9-for-torture-samba4.so
%else
%{_libdir}/samba/libdsdb-module-samba4.so
%endif
%if %{defined rhel} && %{rhel} < 8
%{_libdir}/samba/libcmocka-samba4.so
%endif

### WINBIND
%files winbind
%{_libdir}/samba/idmap
%{_libdir}/samba/nss_info
%{_libdir}/samba/libnss-info-samba4.so
%{_libdir}/samba/libidmap-samba4.so
%{_sbindir}/winbindd
%attr(750,root,wbpriv) %dir /var/lib/samba/winbindd_privileged
%{_unitdir}/winbind.service
%if %{defined rhel} && %{rhel} >= 8
%{_prefix}/lib/NetworkManager/dispatcher.d/30-winbind
%else
%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind
%endif
%{_mandir}/man8/winbindd.8*
%{_mandir}/man8/idmap_*.8*

### WINBIND-CLIENTS
%files winbind-clients
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_libdir}/samba/krb5/winbind_krb5_localauth.so
%{_mandir}/man1/ntlm_auth.1.gz
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man8/winbind_krb5_localauth.8*

### WINBIND-KRB5-LOCATOR
%files winbind-krb5-locator
%ghost %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
%{_libdir}/samba/krb5/winbind_krb5_locator.so
%{_mandir}/man8/winbind_krb5_locator.8*

### WINBIND-MODULES
%files winbind-modules
%{_libdir}/libnss_winbind.so*
%{_libdir}/libnss_wins.so*
%{_libdir}/security/pam_winbind.so
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man8/pam_winbind.8*

%if %with_clustering_support
%files -n ctdb
%doc ctdb/README
%doc ctdb/doc/examples
# Obsolete
%config(noreplace, missingok) %{_sysconfdir}/sysconfig/ctdb

%dir /run/ctdb

%dir %{_sysconfdir}/ctdb
%config(noreplace) %{_sysconfdir}/ctdb/ctdb.conf
%config(noreplace) %{_sysconfdir}/ctdb/script.options
%config(noreplace) %{_sysconfdir}/ctdb/notify.sh
%config(noreplace) %{_sysconfdir}/ctdb/debug-hung-script.sh
%config(noreplace) %{_sysconfdir}/ctdb/ctdb-crash-cleanup.sh
%config(noreplace) %{_sysconfdir}/ctdb/debug_locks.sh
%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/nfs-linux-kernel-callout
%{_sysconfdir}/ctdb/statd-callout
%config %{_sysconfdir}/sudoers.d/ctdb

# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/events
%dir %{_sysconfdir}/ctdb/events/legacy
%dir %{_sysconfdir}/ctdb/events/notification
%{_sysconfdir}/ctdb/events/notification/README

# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/nfs-checks.d
%{_sysconfdir}/ctdb/nfs-checks.d/README
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/00.portmapper.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/10.status.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/20.nfs.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/30.nlockmgr.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/40.mountd.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/50.rquotad.check

%{_sbindir}/ctdbd
%{_sbindir}/ctdbd_wrapper
%{_bindir}/ctdb
%{_bindir}/ctdb_local_daemons
%{_bindir}/ping_pong
%{_bindir}/ltdbtool
%{_bindir}/ctdb_diagnostics
%{_bindir}/onnode

%dir %{_libexecdir}/ctdb
%{_libexecdir}/ctdb/ctdb-config
%{_libexecdir}/ctdb/ctdb-event
%{_libexecdir}/ctdb/ctdb-eventd
%{_libexecdir}/ctdb/ctdb_killtcp
%{_libexecdir}/ctdb/ctdb_lock_helper
%{_libexecdir}/ctdb/ctdb_lvs
%{_libexecdir}/ctdb/ctdb_mutex_fcntl_helper
%{_libexecdir}/ctdb/ctdb_natgw
%{_libexecdir}/ctdb/ctdb-path
%{_libexecdir}/ctdb/ctdb_recovery_helper
%{_libexecdir}/ctdb/ctdb_takeover_helper
%{_libexecdir}/ctdb/smnotify

%dir %{_localstatedir}/lib/ctdb/
%dir %{_localstatedir}/lib/ctdb/persistent
%dir %{_localstatedir}/lib/ctdb/state
%dir %{_localstatedir}/lib/ctdb/volatile

%{_mandir}/man1/ctdb.1.gz
%{_mandir}/man1/ctdb_diagnostics.1.gz
%{_mandir}/man1/ctdbd.1.gz
%{_mandir}/man1/onnode.1.gz
%{_mandir}/man1/ltdbtool.1.gz
%{_mandir}/man1/ping_pong.1.gz
%{_mandir}/man1/ctdbd_wrapper.1.gz
%{_mandir}/man5/ctdb.conf.5.gz
%{_mandir}/man5/ctdb-script.options.5.gz
%{_mandir}/man5/ctdb.sysconfig.5.gz
%{_mandir}/man7/ctdb.7.gz
%{_mandir}/man7/ctdb-tunables.7.gz
%{_mandir}/man7/ctdb-statistics.7.gz

%{_tmpfilesdir}/ctdb.conf

%{_unitdir}/ctdb.service

%dir %{_datadir}/ctdb
%dir %{_datadir}/ctdb/events
%dir %{_datadir}/ctdb/events/legacy/
%{_datadir}/ctdb/events/legacy/00.ctdb.script
%{_datadir}/ctdb/events/legacy/01.reclock.script
%{_datadir}/ctdb/events/legacy/05.system.script
%{_datadir}/ctdb/events/legacy/06.nfs.script
%{_datadir}/ctdb/events/legacy/10.interface.script
%{_datadir}/ctdb/events/legacy/11.natgw.script
%{_datadir}/ctdb/events/legacy/11.routing.script
%{_datadir}/ctdb/events/legacy/13.per_ip_routing.script
%{_datadir}/ctdb/events/legacy/20.multipathd.script
%{_datadir}/ctdb/events/legacy/31.clamd.script
%{_datadir}/ctdb/events/legacy/40.vsftpd.script
%{_datadir}/ctdb/events/legacy/41.httpd.script
%{_datadir}/ctdb/events/legacy/49.winbind.script
%{_datadir}/ctdb/events/legacy/50.samba.script
%{_datadir}/ctdb/events/legacy/60.nfs.script
%{_datadir}/ctdb/events/legacy/70.iscsi.script
%{_datadir}/ctdb/events/legacy/91.lvs.script

%files -n ctdb-tests
%doc ctdb/tests/README
%{_bindir}/ctdb_run_tests
%{_bindir}/ctdb_run_cluster_tests

%dir %{_libexecdir}/ctdb
%dir %{_libexecdir}/ctdb/tests
%{_libexecdir}/ctdb/tests/cmdline_test
%{_libexecdir}/ctdb/tests/comm_client_test
%{_libexecdir}/ctdb/tests/comm_server_test
%{_libexecdir}/ctdb/tests/comm_test
%{_libexecdir}/ctdb/tests/conf_test
%{_libexecdir}/ctdb/tests/ctdb_io_test
%{_libexecdir}/ctdb/tests/ctdb_packet_parse
%{_libexecdir}/ctdb/tests/ctdb_takeover_tests
%{_libexecdir}/ctdb/tests/db_hash_test
%{_libexecdir}/ctdb/tests/dummy_client
%{_libexecdir}/ctdb/tests/errcode
%{_libexecdir}/ctdb/tests/event_protocol_test
%{_libexecdir}/ctdb/tests/event_script_test
%{_libexecdir}/ctdb/tests/fake_ctdbd
%{_libexecdir}/ctdb/tests/fetch_loop
%{_libexecdir}/ctdb/tests/fetch_loop_key
%{_libexecdir}/ctdb/tests/fetch_readonly
%{_libexecdir}/ctdb/tests/fetch_readonly_loop
%{_libexecdir}/ctdb/tests/fetch_ring
%{_libexecdir}/ctdb/tests/g_lock_loop
%{_libexecdir}/ctdb/tests/hash_count_test
%{_libexecdir}/ctdb/tests/line_test
%{_libexecdir}/ctdb/tests/lock_tdb
%{_libexecdir}/ctdb/tests/message_ring
%{_libexecdir}/ctdb/tests/pidfile_test
%{_libexecdir}/ctdb/tests/pkt_read_test
%{_libexecdir}/ctdb/tests/pkt_write_test
%{_libexecdir}/ctdb/tests/porting_tests
%{_libexecdir}/ctdb/tests/protocol_basic_test
%{_libexecdir}/ctdb/tests/protocol_ctdb_compat_test
%{_libexecdir}/ctdb/tests/protocol_ctdb_test
%{_libexecdir}/ctdb/tests/protocol_types_compat_test
%{_libexecdir}/ctdb/tests/protocol_types_test
%{_libexecdir}/ctdb/tests/protocol_util_test
%{_libexecdir}/ctdb/tests/rb_test
%{_libexecdir}/ctdb/tests/reqid_test
%{_libexecdir}/ctdb/tests/run_event_test
%{_libexecdir}/ctdb/tests/run_proc_test
%{_libexecdir}/ctdb/tests/sigcode
%{_libexecdir}/ctdb/tests/sock_daemon_test
%{_libexecdir}/ctdb/tests/sock_io_test
%{_libexecdir}/ctdb/tests/srvid_test
%{_libexecdir}/ctdb/tests/system_socket_test
%{_libexecdir}/ctdb/tests/transaction_loop
%{_libexecdir}/ctdb/tests/tunnel_cmd
%{_libexecdir}/ctdb/tests/tunnel_test
%{_libexecdir}/ctdb/tests/update_record
%{_libexecdir}/ctdb/tests/update_record_persistent

%dir %{_datadir}/ctdb/tests

%dir %{_datadir}/ctdb/tests/complex
%{_datadir}/ctdb/tests/complex/README
%{_datadir}/ctdb/tests/complex/11_ctdb_delip_removes_ip.sh
%{_datadir}/ctdb/tests/complex/18_ctdb_reloadips.sh
%{_datadir}/ctdb/tests/complex/30_nfs_tickle_killtcp.sh
%{_datadir}/ctdb/tests/complex/31_nfs_tickle.sh
%{_datadir}/ctdb/tests/complex/32_cifs_tickle.sh
%{_datadir}/ctdb/tests/complex/33_gratuitous_arp.sh
%{_datadir}/ctdb/tests/complex/34_nfs_tickle_restart.sh
%{_datadir}/ctdb/tests/complex/36_smb_reset_server.sh
%{_datadir}/ctdb/tests/complex/37_nfs_reset_server.sh
%{_datadir}/ctdb/tests/complex/41_failover_ping_discrete.sh
%{_datadir}/ctdb/tests/complex/42_failover_ssh_hostname.sh
%{_datadir}/ctdb/tests/complex/43_failover_nfs_basic.sh
%{_datadir}/ctdb/tests/complex/44_failover_nfs_oneway.sh
%{_datadir}/ctdb/tests/complex/45_failover_nfs_kill.sh
%{_datadir}/ctdb/tests/complex/60_rogueip_releaseip.sh
%{_datadir}/ctdb/tests/complex/61_rogueip_takeip.sh

%dir %{_datadir}/ctdb/tests/complex/scripts
%{_datadir}/ctdb/tests/complex/scripts/local.bash

%dir %{_datadir}/ctdb/tests/cunit
%{_datadir}/ctdb/tests/cunit/cmdline_test_001.sh
%{_datadir}/ctdb/tests/cunit/comm_test_001.sh
%{_datadir}/ctdb/tests/cunit/comm_test_002.sh
%{_datadir}/ctdb/tests/cunit/conf_test_001.sh
%{_datadir}/ctdb/tests/cunit/config_test_001.sh
%{_datadir}/ctdb/tests/cunit/config_test_002.sh
%{_datadir}/ctdb/tests/cunit/config_test_003.sh
%{_datadir}/ctdb/tests/cunit/config_test_004.sh
%{_datadir}/ctdb/tests/cunit/config_test_005.sh
%{_datadir}/ctdb/tests/cunit/config_test_006.sh
%{_datadir}/ctdb/tests/cunit/config_test_007.sh
%{_datadir}/ctdb/tests/cunit/ctdb_io_test_001.sh
%{_datadir}/ctdb/tests/cunit/db_hash_test_001.sh
%{_datadir}/ctdb/tests/cunit/event_protocol_test_001.sh
%{_datadir}/ctdb/tests/cunit/event_script_test_001.sh
%{_datadir}/ctdb/tests/cunit/hash_count_test_001.sh
%{_datadir}/ctdb/tests/cunit/line_test_001.sh
%{_datadir}/ctdb/tests/cunit/path_tests_001.sh
%{_datadir}/ctdb/tests/cunit/pidfile_test_001.sh
%{_datadir}/ctdb/tests/cunit/pkt_read_001.sh
%{_datadir}/ctdb/tests/cunit/pkt_write_001.sh
%{_datadir}/ctdb/tests/cunit/porting_tests_001.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_001.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_002.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_012.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_101.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_111.sh
%{_datadir}/ctdb/tests/cunit/protocol_test_201.sh
%{_datadir}/ctdb/tests/cunit/rb_test_001.sh
%{_datadir}/ctdb/tests/cunit/reqid_test_001.sh
%{_datadir}/ctdb/tests/cunit/run_event_001.sh
%{_datadir}/ctdb/tests/cunit/run_proc_001.sh
%{_datadir}/ctdb/tests/cunit/sock_daemon_test_001.sh
%{_datadir}/ctdb/tests/cunit/sock_io_test_001.sh
%{_datadir}/ctdb/tests/cunit/srvid_test_001.sh
%{_datadir}/ctdb/tests/cunit/system_socket_test_001.sh
%dir %{_datadir}/ctdb/tests/etc-ctdb
%dir %{_datadir}/ctdb/tests/etc-ctdb/events
%dir %{_datadir}/ctdb/tests/etc-ctdb/events/legacy
%{_datadir}/ctdb/tests/etc-ctdb/events/legacy/00.test.script
%dir %{_datadir}/ctdb/tests/eventd
%{_datadir}/ctdb/tests/eventd/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb
%{_datadir}/ctdb/tests/eventd/etc-ctdb/ctdb.conf
%{_datadir}/ctdb/tests/eventd/etc-ctdb/debug-script.sh
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data/README
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data/03.notalink.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/empty
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/empty/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/01.test.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/02.test.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/03.test.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/01.disabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/02.enabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/README.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/a.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data/01.dummy.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data/02.disabled.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/empty
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/empty/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/01.disabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/02.enabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/a.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/README.script
%{_datadir}/ctdb/tests/eventd/eventd_001.sh
%{_datadir}/ctdb/tests/eventd/eventd_002.sh
%{_datadir}/ctdb/tests/eventd/eventd_003.sh
%{_datadir}/ctdb/tests/eventd/eventd_004.sh
%{_datadir}/ctdb/tests/eventd/eventd_005.sh
%{_datadir}/ctdb/tests/eventd/eventd_006.sh
%{_datadir}/ctdb/tests/eventd/eventd_007.sh
%{_datadir}/ctdb/tests/eventd/eventd_008.sh
%{_datadir}/ctdb/tests/eventd/eventd_009.sh
%{_datadir}/ctdb/tests/eventd/eventd_011.sh
%{_datadir}/ctdb/tests/eventd/eventd_012.sh
%{_datadir}/ctdb/tests/eventd/eventd_013.sh
%{_datadir}/ctdb/tests/eventd/eventd_014.sh
%{_datadir}/ctdb/tests/eventd/eventd_021.sh
%{_datadir}/ctdb/tests/eventd/eventd_022.sh
%{_datadir}/ctdb/tests/eventd/eventd_023.sh
%{_datadir}/ctdb/tests/eventd/eventd_024.sh
%{_datadir}/ctdb/tests/eventd/eventd_031.sh
%{_datadir}/ctdb/tests/eventd/eventd_032.sh
%{_datadir}/ctdb/tests/eventd/eventd_033.sh
%{_datadir}/ctdb/tests/eventd/eventd_041.sh
%{_datadir}/ctdb/tests/eventd/eventd_042.sh
%{_datadir}/ctdb/tests/eventd/eventd_043.sh
%{_datadir}/ctdb/tests/eventd/eventd_044.sh
%{_datadir}/ctdb/tests/eventd/eventd_051.sh
%{_datadir}/ctdb/tests/eventd/eventd_052.sh
%dir %{_datadir}/ctdb/tests/eventd/scripts
%{_datadir}/ctdb/tests/eventd/scripts/local.sh

%dir %{_datadir}/ctdb/tests/eventscripts
%{_datadir}/ctdb/tests/eventscripts/README
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.001.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.002.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.003.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.004.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.005.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.006.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.007.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.008.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.009.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.001.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.002.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.003.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.004.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.006.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.007.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.011.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.012.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.014.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.015.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.017.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.018.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.010.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.011.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.012.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.013.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.021.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.022.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.023.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.006.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.009.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.010.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.011.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.012.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.013.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.014.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.015.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.016.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.017.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.018.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.multi.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.003.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.001.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.002.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.003.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.004.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.011.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.012.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.013.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.014.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.015.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.021.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.022.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.023.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.024.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.025.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.031.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.041.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.042.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.051.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.052.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.053.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.054.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.001.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.002.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.003.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.004.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.005.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.006.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.007.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.008.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.009.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.010.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.011.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.012.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.013.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.014.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.015.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.016.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.017.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.018.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.019.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.021.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.022.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.023.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.024.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/31.clamd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/31.clamd.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.monitor.102.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.103.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.104.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.105.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.106.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.110.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.111.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.112.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.113.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.011.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.startup.011.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.102.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.103.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.104.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.105.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.106.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.107.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.108.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.109.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.111.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.112.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.113.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.114.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.121.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.122.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.131.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.132.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.141.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.142.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.143.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.144.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.151.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.152.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.153.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.161.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.162.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.multi.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.multi.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.011.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.012.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.013.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.014.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.001.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.002.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.003.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.004.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.005.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.006.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.007.sh

%dir %{_datadir}/ctdb/tests/eventscripts/etc-ctdb
%{_datadir}/ctdb/tests/eventscripts/etc-ctdb/public_addresses
%{_datadir}/ctdb/tests/eventscripts/etc-ctdb/rc.local

%dir %{_datadir}/ctdb/tests/eventscripts/etc
%dir %{_datadir}/ctdb/tests/eventscripts/etc/init.d
%{_datadir}/ctdb/tests/eventscripts/etc/init.d/nfs
%{_datadir}/ctdb/tests/eventscripts/etc/init.d/nfslock

%dir %{_datadir}/ctdb/tests/eventscripts/etc/samba
%{_datadir}/ctdb/tests/eventscripts/etc/samba/smb.conf

%dir %{_datadir}/ctdb/tests/eventscripts/etc/sysconfig
%{_datadir}/ctdb/tests/eventscripts/etc/sysconfig/nfs

%dir %{_datadir}/ctdb/tests/eventscripts/scripts
%{_datadir}/ctdb/tests/eventscripts/scripts/local.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/00.ctdb.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/01.reclock.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/05.system.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/06.nfs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/10.interface.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/11.natgw.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/13.per_ip_routing.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/20.multipathd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/31.clamd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/40.vsftpd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/41.httpd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/49.winbind.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/50.samba.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/60.nfs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/91.lvs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/statd-callout.sh

%dir %{_datadir}/ctdb/tests/eventscripts/stubs
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb-config
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_killtcp
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_lvs
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_natgw
%{_datadir}/ctdb/tests/eventscripts/stubs/date
%{_datadir}/ctdb/tests/eventscripts/stubs/df
%{_datadir}/ctdb/tests/eventscripts/stubs/ethtool
%{_datadir}/ctdb/tests/eventscripts/stubs/exportfs
%{_datadir}/ctdb/tests/eventscripts/stubs/id
%{_datadir}/ctdb/tests/eventscripts/stubs/ip
%{_datadir}/ctdb/tests/eventscripts/stubs/ip6tables
%{_datadir}/ctdb/tests/eventscripts/stubs/iptables
%{_datadir}/ctdb/tests/eventscripts/stubs/ipvsadm
%{_datadir}/ctdb/tests/eventscripts/stubs/kill
%{_datadir}/ctdb/tests/eventscripts/stubs/killall
%{_datadir}/ctdb/tests/eventscripts/stubs/multipath
%{_datadir}/ctdb/tests/eventscripts/stubs/net
%{_datadir}/ctdb/tests/eventscripts/stubs/pidof
%{_datadir}/ctdb/tests/eventscripts/stubs/pkill
%{_datadir}/ctdb/tests/eventscripts/stubs/ps
%{_datadir}/ctdb/tests/eventscripts/stubs/rm
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.lockd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.mountd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.rquotad
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.statd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpcinfo
%{_datadir}/ctdb/tests/eventscripts/stubs/service
%{_datadir}/ctdb/tests/eventscripts/stubs/sleep
%{_datadir}/ctdb/tests/eventscripts/stubs/smnotify
%{_datadir}/ctdb/tests/eventscripts/stubs/ss
%{_datadir}/ctdb/tests/eventscripts/stubs/tdbdump
%{_datadir}/ctdb/tests/eventscripts/stubs/tdbtool
%{_datadir}/ctdb/tests/eventscripts/stubs/testparm
%{_datadir}/ctdb/tests/eventscripts/stubs/timeout
%{_datadir}/ctdb/tests/eventscripts/stubs/wbinfo

%dir %{_datadir}/ctdb/tests/onnode
%{_datadir}/ctdb/tests/onnode/0001.sh
%{_datadir}/ctdb/tests/onnode/0002.sh
%{_datadir}/ctdb/tests/onnode/0003.sh
%{_datadir}/ctdb/tests/onnode/0004.sh
%{_datadir}/ctdb/tests/onnode/0005.sh
%{_datadir}/ctdb/tests/onnode/0006.sh
%{_datadir}/ctdb/tests/onnode/0010.sh
%{_datadir}/ctdb/tests/onnode/0011.sh
%{_datadir}/ctdb/tests/onnode/0070.sh
%{_datadir}/ctdb/tests/onnode/0071.sh
%{_datadir}/ctdb/tests/onnode/0072.sh
%{_datadir}/ctdb/tests/onnode/0075.sh

%dir %{_datadir}/ctdb/tests/onnode/etc-ctdb
%{_datadir}/ctdb/tests/onnode/etc-ctdb/nodes

%dir %{_datadir}/ctdb/tests/onnode/scripts
%{_datadir}/ctdb/tests/onnode/scripts/local.sh

%dir %{_datadir}/ctdb/tests/onnode/stubs
%{_datadir}/ctdb/tests/onnode/stubs/ctdb
%{_datadir}/ctdb/tests/onnode/stubs/ssh

%dir %{_datadir}/ctdb/tests/scripts
%{_datadir}/ctdb/tests/scripts/common.sh
%{_datadir}/ctdb/tests/scripts/integration.bash
%{_datadir}/ctdb/tests/scripts/script_install_paths.sh
%{_datadir}/ctdb/tests/scripts/test_wrap
%{_datadir}/ctdb/tests/scripts/unit.sh

%dir %{_datadir}/ctdb/tests/shellcheck
%{_datadir}/ctdb/tests/shellcheck/base_scripts.sh
%{_datadir}/ctdb/tests/shellcheck/ctdb_helpers.sh
%{_datadir}/ctdb/tests/shellcheck/ctdbd_wrapper.sh
%{_datadir}/ctdb/tests/shellcheck/event_scripts.sh
%{_datadir}/ctdb/tests/shellcheck/functions.sh
%{_datadir}/ctdb/tests/shellcheck/init_script.sh
%{_datadir}/ctdb/tests/shellcheck/tools.sh

%dir %{_datadir}/ctdb/tests/shellcheck/scripts
%{_datadir}/ctdb/tests/shellcheck/scripts/local.sh

%dir %{_datadir}/ctdb/tests/simple
%{_datadir}/ctdb/tests/simple/README
%{_datadir}/ctdb/tests/simple/00_ctdb_onnode.sh
%{_datadir}/ctdb/tests/simple/01_ctdb_reclock_command.sh
%{_datadir}/ctdb/tests/simple/02_ctdb_tunables.sh
%{_datadir}/ctdb/tests/simple/05_ctdb_listnodes.sh
%{_datadir}/ctdb/tests/simple/06_ctdb_getpid.sh
%{_datadir}/ctdb/tests/simple/07_ctdb_process_exists.sh
%{_datadir}/ctdb/tests/simple/08_ctdb_isnotrecmaster.sh
%{_datadir}/ctdb/tests/simple/09_ctdb_ping.sh
%{_datadir}/ctdb/tests/simple/11_ctdb_ip.sh
%{_datadir}/ctdb/tests/simple/12_ctdb_getdebug.sh
%{_datadir}/ctdb/tests/simple/13_ctdb_setdebug.sh
%{_datadir}/ctdb/tests/simple/14_ctdb_statistics.sh
%{_datadir}/ctdb/tests/simple/15_ctdb_statisticsreset.sh
%{_datadir}/ctdb/tests/simple/16_ctdb_config_add_ip.sh
%{_datadir}/ctdb/tests/simple/17_ctdb_config_delete_ip.sh
%{_datadir}/ctdb/tests/simple/18_ctdb_reloadips.sh
%{_datadir}/ctdb/tests/simple/19_ip_takeover_noop.sh
%{_datadir}/ctdb/tests/simple/20_delip_iface_gc.sh
%{_datadir}/ctdb/tests/simple/21_ctdb_attach.sh
%{_datadir}/ctdb/tests/simple/23_ctdb_moveip.sh
%{_datadir}/ctdb/tests/simple/24_ctdb_getdbmap.sh
%{_datadir}/ctdb/tests/simple/25_dumpmemory.sh
%{_datadir}/ctdb/tests/simple/26_ctdb_config_check_error_on_unreachable_ctdb.sh
%{_datadir}/ctdb/tests/simple/27_ctdb_detach.sh
%{_datadir}/ctdb/tests/simple/28_zero_eventscripts.sh
%{_datadir}/ctdb/tests/simple/32_ctdb_disable_enable.sh
%{_datadir}/ctdb/tests/simple/35_ctdb_getreclock.sh
%{_datadir}/ctdb/tests/simple/42_ctdb_stop_continue.sh
%{_datadir}/ctdb/tests/simple/43_stop_recmaster_yield.sh
%{_datadir}/ctdb/tests/simple/51_message_ring.sh
%{_datadir}/ctdb/tests/simple/52_fetch_ring.sh
%{_datadir}/ctdb/tests/simple/53_transaction_loop.sh
%{_datadir}/ctdb/tests/simple/54_transaction_loop_recovery.sh
%{_datadir}/ctdb/tests/simple/55_ctdb_ptrans.sh
%{_datadir}/ctdb/tests/simple/56_replicated_transaction_recovery.sh
%{_datadir}/ctdb/tests/simple/58_ctdb_restoredb.sh
%{_datadir}/ctdb/tests/simple/60_recoverd_missing_ip.sh
%{_datadir}/ctdb/tests/simple/69_recovery_resurrect_deleted.sh
%{_datadir}/ctdb/tests/simple/70_recoverpdbbyseqnum.sh
%{_datadir}/ctdb/tests/simple/71_ctdb_wipedb.sh
%{_datadir}/ctdb/tests/simple/72_update_record_persistent.sh
%{_datadir}/ctdb/tests/simple/73_tunable_NoIPTakeover.sh
%{_datadir}/ctdb/tests/simple/75_readonly_records_basic.sh
%{_datadir}/ctdb/tests/simple/76_ctdb_pdb_recovery.sh
%{_datadir}/ctdb/tests/simple/77_ctdb_db_recovery.sh
%{_datadir}/ctdb/tests/simple/78_ctdb_large_db_recovery.sh
%{_datadir}/ctdb/tests/simple/79_volatile_db_traverse.sh
%{_datadir}/ctdb/tests/simple/80_ctdb_traverse.sh
%{_datadir}/ctdb/tests/simple/81_tunnel_ring.sh
%{_datadir}/ctdb/tests/simple/90_debug_hung_script.sh
%{_datadir}/ctdb/tests/simple/91_version_check.sh


%dir %{_datadir}/ctdb/tests/simple/scripts
%{_datadir}/ctdb/tests/simple/scripts/local.bash
%{_datadir}/ctdb/tests/simple/scripts/local_daemons.bash

%dir %{_datadir}/ctdb/tests/takeover
%{_datadir}/ctdb/tests/takeover/README
%{_datadir}/ctdb/tests/takeover/det.001.sh
%{_datadir}/ctdb/tests/takeover/det.002.sh
%{_datadir}/ctdb/tests/takeover/det.003.sh
%{_datadir}/ctdb/tests/takeover/lcp2.001.sh
%{_datadir}/ctdb/tests/takeover/lcp2.002.sh
%{_datadir}/ctdb/tests/takeover/lcp2.003.sh
%{_datadir}/ctdb/tests/takeover/lcp2.004.sh
%{_datadir}/ctdb/tests/takeover/lcp2.005.sh
%{_datadir}/ctdb/tests/takeover/lcp2.006.sh
%{_datadir}/ctdb/tests/takeover/lcp2.007.sh
%{_datadir}/ctdb/tests/takeover/lcp2.008.sh
%{_datadir}/ctdb/tests/takeover/lcp2.009.sh
%{_datadir}/ctdb/tests/takeover/lcp2.010.sh
%{_datadir}/ctdb/tests/takeover/lcp2.011.sh
%{_datadir}/ctdb/tests/takeover/lcp2.012.sh
%{_datadir}/ctdb/tests/takeover/lcp2.013.sh
%{_datadir}/ctdb/tests/takeover/lcp2.014.sh
%{_datadir}/ctdb/tests/takeover/lcp2.015.sh
%{_datadir}/ctdb/tests/takeover/lcp2.016.sh
%{_datadir}/ctdb/tests/takeover/lcp2.024.sh
%{_datadir}/ctdb/tests/takeover/lcp2.025.sh
%{_datadir}/ctdb/tests/takeover/lcp2.027.sh
%{_datadir}/ctdb/tests/takeover/lcp2.028.sh
%{_datadir}/ctdb/tests/takeover/lcp2.029.sh
%{_datadir}/ctdb/tests/takeover/lcp2.030.sh
%{_datadir}/ctdb/tests/takeover/lcp2.031.sh
%{_datadir}/ctdb/tests/takeover/lcp2.032.sh
%{_datadir}/ctdb/tests/takeover/lcp2.033.sh
%{_datadir}/ctdb/tests/takeover/lcp2.034.sh
%{_datadir}/ctdb/tests/takeover/lcp2.035.sh
%{_datadir}/ctdb/tests/takeover/nondet.001.sh
%{_datadir}/ctdb/tests/takeover/nondet.002.sh
%{_datadir}/ctdb/tests/takeover/nondet.003.sh

%dir %{_datadir}/ctdb/tests/takeover/scripts
%{_datadir}/ctdb/tests/takeover/scripts/local.sh

%dir %{_datadir}/ctdb/tests/takeover_helper
%{_datadir}/ctdb/tests/takeover_helper/000.sh
%{_datadir}/ctdb/tests/takeover_helper/010.sh
%{_datadir}/ctdb/tests/takeover_helper/011.sh
%{_datadir}/ctdb/tests/takeover_helper/012.sh
%{_datadir}/ctdb/tests/takeover_helper/013.sh
%{_datadir}/ctdb/tests/takeover_helper/014.sh
%{_datadir}/ctdb/tests/takeover_helper/016.sh
%{_datadir}/ctdb/tests/takeover_helper/017.sh
%{_datadir}/ctdb/tests/takeover_helper/018.sh
%{_datadir}/ctdb/tests/takeover_helper/019.sh
%{_datadir}/ctdb/tests/takeover_helper/021.sh
%{_datadir}/ctdb/tests/takeover_helper/022.sh
%{_datadir}/ctdb/tests/takeover_helper/023.sh
%{_datadir}/ctdb/tests/takeover_helper/024.sh
%{_datadir}/ctdb/tests/takeover_helper/025.sh
%{_datadir}/ctdb/tests/takeover_helper/026.sh
%{_datadir}/ctdb/tests/takeover_helper/027.sh
%{_datadir}/ctdb/tests/takeover_helper/028.sh
%{_datadir}/ctdb/tests/takeover_helper/030.sh
%{_datadir}/ctdb/tests/takeover_helper/031.sh
%{_datadir}/ctdb/tests/takeover_helper/110.sh
%{_datadir}/ctdb/tests/takeover_helper/111.sh
%{_datadir}/ctdb/tests/takeover_helper/120.sh
%{_datadir}/ctdb/tests/takeover_helper/121.sh
%{_datadir}/ctdb/tests/takeover_helper/122.sh
%{_datadir}/ctdb/tests/takeover_helper/130.sh
%{_datadir}/ctdb/tests/takeover_helper/131.sh
%{_datadir}/ctdb/tests/takeover_helper/132.sh
%{_datadir}/ctdb/tests/takeover_helper/140.sh
%{_datadir}/ctdb/tests/takeover_helper/150.sh
%{_datadir}/ctdb/tests/takeover_helper/160.sh
%{_datadir}/ctdb/tests/takeover_helper/210.sh
%{_datadir}/ctdb/tests/takeover_helper/211.sh
%{_datadir}/ctdb/tests/takeover_helper/220.sh
%{_datadir}/ctdb/tests/takeover_helper/230.sh
%{_datadir}/ctdb/tests/takeover_helper/240.sh
%{_datadir}/ctdb/tests/takeover_helper/250.sh
%{_datadir}/ctdb/tests/takeover_helper/260.sh

%dir %{_datadir}/ctdb/tests/takeover_helper/scripts
%{_datadir}/ctdb/tests/takeover_helper/scripts/local.sh

%dir %{_datadir}/ctdb/tests/tool
%{_datadir}/ctdb/tests/tool/README
%{_datadir}/ctdb/tests/tool/ctdb.attach.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.attach.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.attach.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.catdb.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.catdb.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.cattdb.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.cattdb.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.deletekey.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbmap.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbseqnum.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbseqnum.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbstatus.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbstatus.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getpid.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getreclock.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getreclock.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getvar.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getvar.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ifaces.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.listnodes.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.listnodes.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.listvars.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.008.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.008.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.pdelete.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ping.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.pnn.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.pstore.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ptrans.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.readkey.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.recmaster.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.recmaster.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.recover.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.011.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.012.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.013.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.014.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.015.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.016.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.017.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.018.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.019.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.020.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.021.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.023.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.024.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setifacelink.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setifacelink.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setvar.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setvar.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.status.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.status.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.uptime.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.writekey.001.sh

%dir %{_datadir}/ctdb/tests/tool/scripts
%{_datadir}/ctdb/tests/tool/scripts/local.sh

#endif with_clustering_support
%endif

%changelog
* Tue Aug 25 2020 - Anoop C S <anoopcs@samba.org> - 4.11.12-1
- v4.11.12 GA

* Fri Jul 17 2020 - Anoop C S <anoopcs@samba.org> - 4.11.11-2
- Do not ship talloc and ldb man pages with samba-client-libs

* Tue Jul 14 2020 - Anoop C S <anoopcs@samba.org> - 4.11.11-1
- Initial version
