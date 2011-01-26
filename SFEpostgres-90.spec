#
# spec file for package PostgreSQL 9.0
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%define _prefix /usr/postgres
%define _var_prefix /var/postgres
%define tarball_name     postgresql
%define tarball_version  9.0.2
%define major_version	 9.0

Name:                    SFEpostgres-90
IPS_package_name:        database/postgres-90
Summary:	         PostgreSQL client tools
Version:                 9.0.2
License:		 PostgreSQL
Url:                     http://www.postgresql.org/
Source:			 http://wwwmaster.postgresql.org/redir/311/h/source/v%{tarball_version}/%{tarball_name}-%{tarball_version}.tar.bz2
Source1:		 postgres-90-postgres_90
Source2:		 postgres-90-postgresql_90.xml
Source3:		 postgres-90-auth_attr
Source4:		 postgres-90-prof_attr
Source5:		 postgres-90-exec_attr
Source6:		 postgres-90-user_attr
#Patch1:			 %{name}-01-kohju.diff
Distribution:            OpenSolaris
Vendor:		         OpenSolaris Community
SUNW_Basedir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: library/libxslt
BuildRequires: library/libxml2
BuildRequires: library/security/openssl
BuildRequires: library/zlib
BuildRequires: library/readline
BuildRequires: system/library
BuildRequires: system/library/security/gss
BuildRequires: system/library/math
BuildRequires: system/library/security/gss
BuildRequires: runtime/tcl-8

Requires: database/postgres-90/library
Requires: library/libxslt
Requires: library/libxml2
Requires: library/zlib
Requires: system/library
Requires: library/security/openssl
Requires: system/library/math
Requires: system/library/security/gss
Requires: library/readline

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	PostgreSQL Global Development Group
Meta(info.maintainer):	 	pkglabo.justplayer.com <pkgadmin@justplayer.com>
# Meta(info.repository_url):	[open source code repository]
Meta(info.classification):	System Database

%description
PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness. It runs on all major operating systems, including Linux, UNIX (AIX, BSD, HP-UX, SGI IRIX, Mac OS X, Solaris, Tru64), and Windows. It is fully ACID compliant, has full support for foreign keys, joins, views, triggers, and stored procedures (in multiple languages). It includes most SQL:2008 data types, including INTEGER, NUMERIC, BOOLEAN, CHAR, VARCHAR, DATE, INTERVAL, and TIMESTAMP. It also supports storage of binary large objects, including pictures, sounds, or video. It has native programming interfaces for C/C++, Java, .Net, Perl, Python, Ruby, Tcl, ODBC, among others, and exceptional documentation. 

%package -n postgres-90-library

IPS_package_name: database/postgres-90/library
Summary: PostgreSQL client libraries
Requires: system/library/math
Requires: system/library

%package -n postgres-90-languages
IPS_package_name: database/postgres-90/language-bindings
Summary: PostgreSQL additional Perl, Python & TCL server procedural languages

Requires: runtime/perl-584
Requires: runtime/python-24
Requires: system/library/math
Requires: system/library
Requires: runtime/tcl-8
Requires: database/postgres-90
Requires: database/postgres-90/library

%package -n postgres-90-developer
IPS_package_name: database/postgres-90/developer
Summary: PostgreSQL development tools and header files

Requires: library/libxslt
Requires: library/libxml2
Requires: system/library/security/gss
Requires: library/security/openssl
Requires: system/library
Requires: library/zlib
Requires: system/library/math
Requires: database/postgres-90
Requires: database/postgres-90/library

%package -n postgres-90-documentation
IPS_package_name: database/postgres-90/documentation
Summary: PostgreSQL documentation and man pages

%package -n postgres-90-server
IPS_package_name: service/database/postgres-90
Summary: PostgreSQL database server

Requires: library/libxslt
Requires: library/libxml2
Requires: system/library/security/gss
Requires: library/security/openssl
Requires: system/library
Requires: library/zlib
Requires: system/library/math
Requires: database/postgres-90
Requires: database/postgres-90/library

%package -n postgres-90-contrib
IPS_package_name: database/postgres-90/contrib
Summary: PostgreSQL community contributed tools not part of core product

Requires: database/postgres-90/library
Requires: library/libxslt
Requires: library/libxml2
Requires: system/library/security/gss
Requires: library/security/openssl
Requires: system/library
Requires: library/zlib
Requires: system/library/math
Requires: database/postgres-90
Requires: database/postgres-90/library

%prep
%setup -c -n %{tarball_name}-%{tarball_version}
#%patch1 -p0

%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export CC=cc

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CCAS=/usr/bin/cc
export CCASFLAGS=
export CC=cc
export CFLAGS="-i -xO4 -xspace -xstrconst -fast -xregs=no%frameptr -xc99=none -xCC"

LD_OPTIONS="-R/usr/sfw/lib -L/usr/sfw/lib" ; export LD_OPTIONS

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin \
            --libexecdir=%{_prefix}/%{major_version}/bin \
            --sbindir=%{_prefix}/%{major_version}/bin \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            --with-tcl \
            --with-perl \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            --with-includes=/usr/include:/usr/sfw/include:/usr/sfw/include \
            --with-tclconfig=/usr/lib \
            --with-libs=/usr/lib:/usr/sfw/lib

gmake -j$CPUS world

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
export CFLAGS="-Xa -i -xO4 -xspace -xstrconst -m64 -fast -Kpic -xregs=no%frameptr"
export LD_OPTIONS="-R/usr/sfw/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64}"

./configure --prefix=%{_prefix}/%{major_version} \
            --exec-prefix=%{_prefix}/%{major_version} \
            --bindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --libexecdir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --sbindir=%{_prefix}/%{major_version}/bin/%{_arch64} \
            --datadir=%{_prefix}/%{major_version}/share \
            --sysconfdir=%{_prefix}/%{major_version}/etc \
            --mandir=%{_prefix}/%{major_version}/man \
            --libdir=%{_prefix}/%{major_version}/lib/%{_arch64} \
            --includedir=%{_prefix}/%{major_version}/include \
            --sharedstatedir=%{_var_prefix}/%{major_version} \
            --localstatedir=%{_var_prefix}/%{major_version} \
            --localedir=%{_prefix}/%{major_version}/share/locale/ \
            --enable-nls \
            --docdir=%{_prefix}/%{major_version}/doc \
            --with-system-tzdata=/usr/share/lib/zoneinfo \
            --with-tcl \
            --with-python \
            --with-pam \
            --with-openssl \
            --with-libedit-preferred \
            --with-libxml \
            --with-libxslt \
            --with-gssapi \
            --enable-thread-safety \
            --enable-dtrace \
            --with-includes=/usr/include:/usr/sfw/include:/usr/sfw/include \
            --with-tclconfig=/usr/lib \
            --with-libs=/usr/lib/%{_arch64}:/usr/sfw/lib/%{_arch64}

gmake -j$CPUS world

%endif
%install
cd %{tarball_name}-%{tarball_version}
gmake install-world DESTDIR=$RPM_BUILD_ROOT
if test -d sun-manpages; then
	cd sun-manpages
	make install DESTDIR=$RPM_BUILD_ROOT
	cd ..
fi

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
gmake install-world DESTDIR=$RPM_BUILD_ROOT

#export OLD_PATH=`pwd`
#cd $RPM_BUILD_ROOT%{_prefix}/%{major_version}/bin
#ln -s %{_arch64} 64
#cd ../lib
#ln -s %{_arch64} 64
#cd ${OLD_PATH}
#cd ..
%endif

mkdir -p $RPM_BUILD_ROOT/etc/security
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/backups
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data
mkdir -p $RPM_BUILD_ROOT%{_var_prefix}/%{major_version}/data_64

mkdir -p $RPM_BUILD_ROOT/lib/svc/method/
cp %{SOURCE1} $RPM_BUILD_ROOT/lib/svc/method/postgres_90
chmod +x $RPM_BUILD_ROOT/lib/svc/method/postgres_90
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/application/database/
cp %{SOURCE2} $RPM_BUILD_ROOT/var/svc/manifest/application/database/postgresql_90.xml

# attribute
mkdir -p $RPM_BUILD_ROOT/etc/security/auth_attr.d/
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-90
mkdir -p $RPM_BUILD_ROOT/etc/security/exec_attr.d/
cp %{SOURCE4} $RPM_BUILD_ROOT/etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-90
mkdir -p $RPM_BUILD_ROOT/etc/security/prof_attr.d/
cp %{SOURCE5} $RPM_BUILD_ROOT/etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-90
mkdir -p $RPM_BUILD_ROOT/etc/user_attr.d/
cp %{SOURCE5} $RPM_BUILD_ROOT/etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-90


mkdir -p $RPM_BUILD_ROOT/usr/share

# delete amd64
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libecpg.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpq.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpgtypes.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/amd64
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libpgport.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{major_version}/lib/amd64/libecpg_compat.a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# make symbolic link

cd $RPM_BUILD_ROOT/%{_prefix}/%{major_version}/bin/
ln -s amd64 64

%clean
rm -rf $RPM_BUILD_ROOT

%actions -n postgres-90-server
group groupname="postgres"
user ftpuser=false gcos-field="PostgreSQL Reserved UID" username="postgres" password=NP group="postgres"

%files
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%attr (0755, root, bin) %{_prefix}/%{major_version}/bin/64
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/vacuumdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/psql
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/clusterdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createlang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/createuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/droplang
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/dropuser
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dump
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_dumpall
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_restore
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/reindexdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/vacuumdb
%attr (0644, root, other) %{_prefix}/%{major_version}/share/psqlrc.sample
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pgscripts-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pgscripts-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/initdb-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/psql-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pg_dump-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pg_dump-%{major_version}.mo
#%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/psql-%{major_version}.mo



%files -n postgres-90-library
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%attr (0755, root, bin) %{_prefix}/%{major_version}/bin/64
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES

%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man5
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so.6.2
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so.3.2
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so.3.1
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so.6.2
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so.3.2
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so.3.1
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgport.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpq.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.a
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.a
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/psql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/libpq5-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_TW/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/ecpglib6-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/zh_CN/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/ecpg-%{major_version}.mo
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so.6
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so.5.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpgtypes.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpq.so.5
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg.so.6
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libecpg_compat.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpgtypes.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so.5
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/libpq.so.5.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg_compat.so.3
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/libecpg.so
 
%files -n postgres-90-languages
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_loadmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pltcl_delmod
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpython.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pltcl.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plperl.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pltcl.so
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_delmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_listmod
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pltcl_loadmod
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/unknown.pltcl





%files -n postgres-90-developer
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/informix
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/informix/esql
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/internal
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/internal/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/access
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/bootstrap
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/catalog
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/commands
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/executor
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/foreign
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/libpq
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/mb
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/nodes
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/optimizer
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/parser
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/arpa
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/netinet
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/sys
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/portability
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/postmaster
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/regex
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/rewrite
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/snowball
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/storage
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tcop
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tsearch
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/dicts
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/include/server/utils
%dir %attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/replication
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test/regress
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/nb
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/nb/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES
#%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/version.h
#%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/flatfiles.h
#%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config/mkinstalldirs
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/config/mkinstalldirs
#%attr (0644, root, bin) %{_prefix}/%{major_version}/include/informix/esql/sqlda.h
#%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_listener.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/tablespace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/trigger.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/typecmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/user.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/vacuum.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/variable.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/view.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/dynloader.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/execdebug.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/execdefs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/execdesc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/executor.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/functions.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/hashjoin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/instrument.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeAgg.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeAppend.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeBitmapAnd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeBitmapHeapscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeBitmapIndexscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeBitmapOr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeCtescan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeFunctionscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeGroup.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeHash.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeHashjoin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeIndexscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeLimit.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeMaterial.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeMergejoin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeNestloop.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeRecursiveunion.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeResult.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeSeqscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeSetOp.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeSort.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeSubplan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeSubqueryscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeTidscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeUnique.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeValuesscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeWindowAgg.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeWorktablescan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/spi.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/spi_priv.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/tstoreReceiver.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/tuptable.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeLockRows.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/executor/nodeModifyTable.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/fmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/foreign/foreign.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/funcapi.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/getaddrinfo.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/getopt_long.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/lib/dllist.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/lib/stringinfo.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/auth.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/be-fsstubs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/crypt.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/hba.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/ip.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/libpq-be.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/libpq-fs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/libpq.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/md5.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/pqcomm.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/pqformat.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/libpq/pqsignal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/mb/pg_wchar.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/miscadmin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/bitmapset.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/execnodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/makefuncs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/memnodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/nodeFuncs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/nodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/params.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/parsenodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/pg_list.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/plannodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/primnodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/print.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/readfuncs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/relation.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/tidbitmap.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/nodes/value.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/clauses.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/cost.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_copy.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_gene.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_misc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_mutation.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_pool.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_random.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_recombination.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/geqo_selection.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/joininfo.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/pathnode.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/paths.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/placeholder.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/plancat.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/planmain.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/planner.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/predtest.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/prep.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/restrictinfo.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/subselect.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/tlist.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/optimizer/var.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/analyze.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/gram.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/gramparse.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/keywords.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/kwlist.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_agg.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_clause.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_coerce.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_cte.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_expr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_func.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_node.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_oper.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_relation.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_target.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_type.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_utilcmd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parser.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parsetree.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/scansup.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pg_config_manual.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pg_config_os.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pg_trace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pgstat.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pgtime.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/aix.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/bsdi.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/cygwin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/darwin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/dgux.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/freebsd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/hpux.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/irix.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/linux.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/netbsd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/nextstep.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/openbsd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/osf.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/sco.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/solaris.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/sunos4.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/svr4.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/ultrix4.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/univel.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/unixware.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/arpa/inet.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/dlfcn.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/grp.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/netdb.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/netinet/in.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/pwd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/sys/socket.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32/sys/wait.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/dirent.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys/file.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys/param.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/sys/time.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/unistd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/port/win32_msvc/utime.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/portability/instr_time.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postgres.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postgres_ext.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postgres_fe.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/autovacuum.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/bgwriter.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/fork_process.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/pgarch.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/postmaster.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/syslogger.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/postmaster/walwriter.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/regex/regcustom.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/regex/regerrs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/regex/regex.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/regex/regguts.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/prs2lock.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/rewriteDefine.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/rewriteHandler.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/rewriteManip.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/rewriteRemove.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rewrite/rewriteSupport.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/rusagestub.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/header.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/api.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/header.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_danish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_dutch.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_english.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_finnish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_french.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_german.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_hungarian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_italian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_norwegian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_porter.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_portuguese.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_spanish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_1_swedish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_ISO_8859_2_romanian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_KOI8_R_russian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_danish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_dutch.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_english.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_finnish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_french.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_german.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_hungarian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_italian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_norwegian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_porter.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_portuguese.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_romanian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_russian.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_spanish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_swedish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/snowball/libstemmer/stem_UTF_8_turkish.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/backendid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/block.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/buf.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/buf_internals.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/buffile.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/bufmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/bufpage.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/fd.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/freespace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/fsm_internals.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/indexfsm.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/ipc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/item.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/itemid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/itemptr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/large_object.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/lmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/lock.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/lwlock.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/off.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/pg_sema.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/pg_shmem.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/pmsignal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/pos.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/proc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/procarray.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/relfilenode.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/s_lock.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/shmem.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/sinval.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/sinvaladt.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/smgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/spin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/dest.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/fastpath.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/pquery.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/tcopdebug.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/tcopprot.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tcop/utility.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/dicts/regis.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/dicts/spell.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/ts_cache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/ts_locale.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/ts_public.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/ts_type.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/tsearch/ts_utils.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/acl.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/array.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/ascii.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/builtins.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/cash.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/catcache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/combocid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/date.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/datetime.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/datum.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/dynahash.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/dynamic_loader.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/elog.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/errcodes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/fmgroids.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/fmgrtab.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/formatting.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/geo_decls.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/guc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/guc_tables.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/help_config.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/hsearch.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/inet.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/int8.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/inval.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/logtape.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/lsyscache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/memutils.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/nabstime.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/numeric.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/palloc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/pg_crc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/pg_locale.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/pg_lzcompress.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/pg_rusage.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/plancache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/portal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/probes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/ps_status.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/rel.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/relcache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/resowner.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/selfuncs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/snapmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/snapshot.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/syscache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/timestamp.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/tqual.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/tuplesort.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/tuplestore.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/typcache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/tzparser.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/uuid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/varbit.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/xml.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/windowapi.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/sql3types.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/sqlca.h
%attr (0755, root, bin) %{_prefix}/%{major_version}/lib/pgxs/config/install-sh
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.port
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.shlib
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/makefiles/pgxs.mk
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_config
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/ecpg
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_config
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pg_config.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/pg_config.h
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/config/install-sh
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.global
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.port
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/Makefile.shlib
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/makefiles/pgxs.mk
%attr (0444, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/nls-global.mk
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/pgxs/src/test/regress/pg_regress
%attr (0644, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/Makefile.global
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/pgxs/src/test/regress/pg_regress
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/nb/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pg_config-%{major_version}.mo
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/ecpg_config.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/ecpg_informix.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/ecpgerrno.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/ecpglib.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/ecpgtype.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/informix/esql/datetime.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/informix/esql/decimal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/informix/esql/sqltypes.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/c.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/libpq-int.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/libpq/pqcomm.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/port.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/postgres_fe.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/internal/pqexpbuffer.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/libpq-events.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/libpq-fe.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/libpq/libpq-fs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pg_config_manual.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pg_config_os.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pgtypes_date.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pgtypes_error.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pgtypes_interval.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pgtypes_numeric.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/pgtypes_timestamp.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/postgres_ext.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/attnum.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/clog.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/genam.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/gin.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/gist.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/gist_private.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/gistscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/hash.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/heapam.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/hio.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/htup.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/itup.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/multixact.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/nbtree.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/printtup.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/reloptions.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/relscan.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/rewriteheap.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/rmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/sdir.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/skey.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/slru.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/subtrans.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/sysattr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/transam.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/tupconvert.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/tupdesc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/tupmacs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/tuptoaster.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/twophase.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/twophase_rmgr.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/valid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/xlog_internal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/xlogdefs.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/xlogutils.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/xact.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/visibilitymap.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/access/xlog.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/bootstrap/bootstrap.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/c.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/catalog.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/catversion.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/dependency.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/genbki.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/heap.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/index.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/indexing.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/namespace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_aggregate.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_am.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_amop.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_amproc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_attrdef.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_attribute.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_auth_members.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_authid.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_cast.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_class.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_constraint.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_control.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_conversion.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_conversion_fn.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_database.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_depend.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_description.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_enum.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_foreign_data_wrapper.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_foreign_server.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_index.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_inherits.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_inherits_fn.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_language.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_largeobject.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_namespace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_opclass.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_operator.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_opfamily.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_pltemplate.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_proc.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_proc_fn.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_rewrite.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_shdepend.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_shdescription.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_statistic.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_tablespace.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_trigger.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_ts_config.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_ts_config_map.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_ts_dict.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_ts_parser.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_ts_template.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_type.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_type_fn.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_user_mapping.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/storage.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/toasting.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_db_role_setting.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_default_acl.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/pg_largeobject_metadata.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/catalog/schemapg.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/alter.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/async.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/cluster.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/comment.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/conversioncmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/copy.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/dbcommands.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/defrem.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/discard.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/explain.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/lockcmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/portalcmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/prepare.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/proclang.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/schemacmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/sequence.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/commands/tablecmds.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/parse_param.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/parser/scanner.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/replication/walprotocol.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/replication/walreceiver.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/replication/walsender.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/procsignal.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/storage/standby.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/attoptcache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/bytea.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/rbtree.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/relmapper.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/server/utils/spccache.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/sqlda-compat.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/sqlda-native.h
%attr (0644, root, bin) %{_prefix}/%{major_version}/include/sqlda.h

%files -n postgres-90-documentation
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/html
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man1
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man3
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/man/man5
%{_prefix}/%{major_version}/doc/html/sql-createforeigndatawrapper.html
%{_prefix}/%{major_version}/doc/html/plpython-util.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-parts.html
%{_prefix}/%{major_version}/doc/html/charset.html
%{_prefix}/%{major_version}/doc/html/tutorial-inheritance.html
%{_prefix}/%{major_version}/doc/html/release-8-1-1.html
%{_prefix}/%{major_version}/doc/html/view-pg-settings.html
%{_prefix}/%{major_version}/doc/html/libpq-pgpass.html
%{_prefix}/%{major_version}/doc/html/infoschema-applicable-roles.html
%{_prefix}/%{major_version}/doc/html/wal-intro.html
%{_prefix}/%{major_version}/doc/html/warm-standby.html
%{_prefix}/%{major_version}/doc/html/rules.html
%{_prefix}/%{major_version}/doc/html/release-7-1-1.html
%{_prefix}/%{major_version}/doc/html/rules-status.html
%{_prefix}/%{major_version}/doc/html/app-ecpg.html
%{_prefix}/%{major_version}/doc/html/gist.html
%{_prefix}/%{major_version}/doc/html/release-8-0-15.html
%{_prefix}/%{major_version}/doc/html/sql-alteropclass.html
%{_prefix}/%{major_version}/doc/html/notation.html
%{_prefix}/%{major_version}/doc/html/release-8-2.html
%{_prefix}/%{major_version}/doc/html/sql-drop-owned.html
%{_prefix}/%{major_version}/doc/html/sql-createconstraint.html
%{_prefix}/%{major_version}/doc/html/release-7-4-21.html
%{_prefix}/%{major_version}/doc/html/view-pg-prepared-xacts.html
%{_prefix}/%{major_version}/doc/html/app-createuser.html
%{_prefix}/%{major_version}/doc/html/functions-window.html
%{_prefix}/%{major_version}/doc/html/queries-with.html
%{_prefix}/%{major_version}/doc/html/ecpg-library.html
%{_prefix}/%{major_version}/doc/html/release-8-0-24.html
%{_prefix}/%{major_version}/doc/html/index-locking.html
%{_prefix}/%{major_version}/doc/html/release-7-4-10.html
%{_prefix}/%{major_version}/doc/html/spi-visibility.html
%{_prefix}/%{major_version}/doc/html/sql-set-transaction.html
%{_prefix}/%{major_version}/doc/html/sql-createrule.html
%{_prefix}/%{major_version}/doc/html/ssh-tunnels.html
%{_prefix}/%{major_version}/doc/html/infoschema-foreign-servers.html
%{_prefix}/%{major_version}/doc/html/manage-ag-dropdb.html
%{_prefix}/%{major_version}/doc/html/different-replication-solutions.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-conversion.html
%{_prefix}/%{major_version}/doc/html/gist-extensibility.html
%{_prefix}/%{major_version}/doc/html/typeconv.html
%{_prefix}/%{major_version}/doc/html/infoschema-column-privileges.html
%{_prefix}/%{major_version}/doc/html/release-8-1-14.html
%{_prefix}/%{major_version}/doc/html/dblink.html
%{_prefix}/%{major_version}/doc/html/sql-set.html
%{_prefix}/%{major_version}/doc/html/release-7-3-13.html
%{_prefix}/%{major_version}/doc/html/runtime-config-custom.html
%{_prefix}/%{major_version}/doc/html/release-8-2-17.html
%{_prefix}/%{major_version}/doc/html/index-scanning.html
%{_prefix}/%{major_version}/doc/html/spi-spi-execute-with-args.html
%{_prefix}/%{major_version}/doc/html/extend-how.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-description.html
%{_prefix}/%{major_version}/doc/html/postgres-user.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getrelname.html
%{_prefix}/%{major_version}/doc/html/sql-explain.html
%{_prefix}/%{major_version}/doc/html/multibyte.html
%{_prefix}/%{major_version}/doc/html/release-8-0-7.html
%{_prefix}/%{major_version}/doc/html/release-8-3-9.html
%{_prefix}/%{major_version}/doc/html/libpq.html
%{_prefix}/%{major_version}/doc/html/ecpg-develop.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-default-acl.html
%{_prefix}/%{major_version}/doc/html/runtime-config-preset.html
%{_prefix}/%{major_version}/doc/html/sql-alterusermapping.html
%{_prefix}/%{major_version}/doc/html/release-7-3-9.html
%{_prefix}/%{major_version}/doc/html/view-pg-roles.html
%{_prefix}/%{major_version}/doc/html/release-8-0-20.html
%{_prefix}/%{major_version}/doc/html/recovery-config.html
%{_prefix}/%{major_version}/doc/html/xml2.html
%{_prefix}/%{major_version}/doc/html/sql-alterserver.html
%{_prefix}/%{major_version}/doc/html/release-1-01.html
%{_prefix}/%{major_version}/doc/html/sql-dropdatabase.html
%{_prefix}/%{major_version}/doc/html/infoschema-role-table-grants.html
%{_prefix}/%{major_version}/doc/html/release-7-4-14.html
%{_prefix}/%{major_version}/doc/html/rules-update.html
%{_prefix}/%{major_version}/doc/html/app-pg-ctl.html
%{_prefix}/%{major_version}/doc/html/datetime-units-history.html
%{_prefix}/%{major_version}/doc/html/spi-spi-copytuple.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-pltemplate.html
%{_prefix}/%{major_version}/doc/html/sql-createrole.html
%{_prefix}/%{major_version}/doc/html/release-8-1-10.html
%{_prefix}/%{major_version}/doc/html/pgstatstatements.html
%{_prefix}/%{major_version}/doc/html/datatype-character.html
%{_prefix}/%{major_version}/doc/html/sql-droptstemplate.html
%{_prefix}/%{major_version}/doc/html/release-8-1-5.html
%{_prefix}/%{major_version}/doc/html/bki-commands.html
%{_prefix}/%{major_version}/doc/html/pgupgrade.html
%{_prefix}/%{major_version}/doc/html/plpython-sharing.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-send-query.html
%{_prefix}/%{major_version}/doc/html/transaction-iso.html
%{_prefix}/%{major_version}/doc/html/sql-createsequence.html
%{_prefix}/%{major_version}/doc/html/spi-spi-prepare.html
%{_prefix}/%{major_version}/doc/html/release-8-1-21.html
%{_prefix}/%{major_version}/doc/html/sql-createtableas.html
%{_prefix}/%{major_version}/doc/html/adminpack.html
%{_prefix}/%{major_version}/doc/html/datatype-binary.html
%{_prefix}/%{major_version}/doc/html/spi-spi-gettype.html
%{_prefix}/%{major_version}/doc/html/release-8-0-11.html
%{_prefix}/%{major_version}/doc/html/gin-examples.html
%{_prefix}/%{major_version}/doc/html/features-sql-standard.html
%{_prefix}/%{major_version}/doc/html/release-7-4-25.html
%{_prefix}/%{major_version}/doc/html/libpq-exec.html
%{_prefix}/%{major_version}/doc/html/admin.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-index.html
%{_prefix}/%{major_version}/doc/html/plpgsql-cursors.html
%{_prefix}/%{major_version}/doc/html/release-7-0-3.html
%{_prefix}/%{major_version}/doc/html/tutorial-install.html
%{_prefix}/%{major_version}/doc/html/infoschema-administrable-role-authorizations.html
%{_prefix}/%{major_version}/doc/html/indexam.html
%{_prefix}/%{major_version}/doc/html/release-8-3-12.html
%{_prefix}/%{major_version}/doc/html/release-8-0-3.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-class.html
%{_prefix}/%{major_version}/doc/html/queries-union.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-language.html
%{_prefix}/%{major_version}/doc/html/tutorial-advanced-intro.html
%{_prefix}/%{major_version}/doc/html/runtime-config-statistics.html
%{_prefix}/%{major_version}/doc/html/sql-syntax.html
%{_prefix}/%{major_version}/doc/html/sql-alteroperator.html
%{_prefix}/%{major_version}/doc/html/ddl-priv.html
%{_prefix}/%{major_version}/doc/html/gist-recovery.html
%{_prefix}/%{major_version}/doc/html/infoschema-role-routine-grants.html
%{_prefix}/%{major_version}/doc/html/infoschema-domains.html
%{_prefix}/%{major_version}/doc/html/executor.html
%{_prefix}/%{major_version}/doc/html/release-9-0.html
%{_prefix}/%{major_version}/doc/html/lo.html
%{_prefix}/%{major_version}/doc/html/vacuumlo.html
%{_prefix}/%{major_version}/doc/html/spi-spi-prepare-cursor.html
%{_prefix}/%{major_version}/doc/html/release-7-3-17.html
%{_prefix}/%{major_version}/doc/html/spi-spi-freeplan.html
%{_prefix}/%{major_version}/doc/html/bug-reporting.html
%{_prefix}/%{major_version}/doc/html/infoschema-sequences.html
%{_prefix}/%{major_version}/doc/html/libpq-events.html
%{_prefix}/%{major_version}/doc/html/release-8-2-13.html
%{_prefix}/%{major_version}/doc/html/textsearch-limitations.html
%{_prefix}/%{major_version}/doc/html/release-6-5-1.html
%{_prefix}/%{major_version}/doc/html/indexes-multicolumn.html
%{_prefix}/%{major_version}/doc/html/runtime-config-resource.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-close.html
%{_prefix}/%{major_version}/doc/html/datatype-textsearch.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-user-mapping.html
%{_prefix}/%{major_version}/doc/html/datetime-config-files.html
%{_prefix}/%{major_version}/doc/html/sql-alterview.html
%{_prefix}/%{major_version}/doc/html/plperl.html
%{_prefix}/%{major_version}/doc/html/dict-xsyn.html
%{_prefix}/%{major_version}/doc/html/xfunc-c.html
%{_prefix}/%{major_version}/doc/html/sql-cluster.html
%{_prefix}/%{major_version}/doc/html/infoschema-element-types.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-is-busy.html
%{_prefix}/%{major_version}/doc/html/textsearch-migration.html
%{_prefix}/%{major_version}/doc/html/sql-createserver.html
%{_prefix}/%{major_version}/doc/html/runtime-config-connection.html
%{_prefix}/%{major_version}/doc/html/app-pgconfig.html
%{_prefix}/%{major_version}/doc/html/spi-memory.html
%{_prefix}/%{major_version}/doc/html/tsearch2.html
%{_prefix}/%{major_version}/doc/html/infoschema-usage-privileges.html
%{_prefix}/%{major_version}/doc/html/xfunc-internal.html
%{_prefix}/%{major_version}/doc/html/release-7-4-6.html
%{_prefix}/%{major_version}/doc/html/plpython.html
%{_prefix}/%{major_version}/doc/html/sql-notify.html
%{_prefix}/%{major_version}/doc/html/libpq-status.html
%{_prefix}/%{major_version}/doc/html/release-8-4-6.html
%{_prefix}/%{major_version}/doc/html/release-6-4.html
%{_prefix}/%{major_version}/doc/html/seg.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-ts-dict.html
%{_prefix}/%{major_version}/doc/html/spi-spi-fname.html
%{_prefix}/%{major_version}/doc/html/sql-reassign-owned.html
%{_prefix}/%{major_version}/doc/html/infoschema-triggered-update-columns.html
%{_prefix}/%{major_version}/doc/html/queries-table-expressions.html
%{_prefix}/%{major_version}/doc/html/release-7-3-1.html
%{_prefix}/%{major_version}/doc/html/libpq-envars.html
%{_prefix}/%{major_version}/doc/html/libpq-pgservice.html
%{_prefix}/%{major_version}/doc/html/sql-createtsparser.html
%{_prefix}/%{major_version}/doc/html/arrays.html
%{_prefix}/%{major_version}/doc/html/sql-createtablespace.html
%{_prefix}/%{major_version}/doc/html/manage-ag-templatedbs.html
%{_prefix}/%{major_version}/doc/html/release-8-3-1.html
%{_prefix}/%{major_version}/doc/html/datatype-numeric.html
%{_prefix}/%{major_version}/doc/html/tablefunc.html
%{_prefix}/%{major_version}/doc/html/tutorial-advanced.html
%{_prefix}/%{major_version}/doc/html/external-extensions.html
%{_prefix}/%{major_version}/doc/html/LEGALNOTICE.html
%{_prefix}/%{major_version}/doc/html/preface.html
%{_prefix}/%{major_version}/doc/html/pltcl-dbaccess.html
%{_prefix}/%{major_version}/doc/html/app-createlang.html
%{_prefix}/%{major_version}/doc/html/infoschema-triggers.html
%{_prefix}/%{major_version}/doc/html/tutorial-update.html
%{_prefix}/%{major_version}/doc/html/sql-altertablespace.html
%{_prefix}/%{major_version}/doc/html/datetime-appendix.html
%{_prefix}/%{major_version}/doc/html/release-8-1-9.html
%{_prefix}/%{major_version}/doc/html/geqo-pg-intro.html
%{_prefix}/%{major_version}/doc/html/install-upgrading.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-ts-template.html
%{_prefix}/%{major_version}/doc/html/release-7-4-29.html
%{_prefix}/%{major_version}/doc/html/isn.html
%{_prefix}/%{major_version}/doc/html/release-8-2-7.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-connect-u.html
%{_prefix}/%{major_version}/doc/html/pgcrypto.html
%{_prefix}/%{major_version}/doc/html/release-7-2-7.html
%{_prefix}/%{major_version}/doc/html/rules-views.html
%{_prefix}/%{major_version}/doc/html/release-9-0-2.html
%{_prefix}/%{major_version}/doc/html/dml-insert.html
%{_prefix}/%{major_version}/doc/html/locking-indexes.html
%{_prefix}/%{major_version}/doc/html/app-pgcontroldata.html
%{_prefix}/%{major_version}/doc/html/xfunc-pl.html
%{_prefix}/%{major_version}/doc/html/docguide-toolsets.html
%{_prefix}/%{major_version}/doc/html/release-7-4-18.html
%{_prefix}/%{major_version}/doc/html/plpython-database.html
%{_prefix}/%{major_version}/doc/html/tutorial-delete.html
%{_prefix}/%{major_version}/doc/html/queries.html
%{_prefix}/%{major_version}/doc/html/pgfreespacemap.html
%{_prefix}/%{major_version}/doc/html/using-explain.html
%{_prefix}/%{major_version}/doc/html/release-7-2.html
%{_prefix}/%{major_version}/doc/html/sql-createtrigger.html
%{_prefix}/%{major_version}/doc/html/unsupported-features-sql-standard.html
%{_prefix}/%{major_version}/doc/html/chkpass.html
%{_prefix}/%{major_version}/doc/html/extend-cpp.html
%{_prefix}/%{major_version}/doc/html/parser-stage.html
%{_prefix}/%{major_version}/doc/html/ddl-schemas.html
%{_prefix}/%{major_version}/doc/html/gin-intro.html
%{_prefix}/%{major_version}/doc/html/dml.html
%{_prefix}/%{major_version}/doc/html/regress.html
%{_prefix}/%{major_version}/doc/html/ddl-default.html
%{_prefix}/%{major_version}/doc/html/indexes-partial.html
%{_prefix}/%{major_version}/doc/html/sql-move.html
%{_prefix}/%{major_version}/doc/html/sql-savepoint.html
%{_prefix}/%{major_version}/doc/html/spi-spi-palloc.html
%{_prefix}/%{major_version}/doc/html/release-7-3-5.html
%{_prefix}/%{major_version}/doc/html/libpq-misc.html
%{_prefix}/%{major_version}/doc/html/nls-programmer.html
%{_prefix}/%{major_version}/doc/html/mvcc.html
%{_prefix}/%{major_version}/doc/html/release-8-3-5.html
%{_prefix}/%{major_version}/doc/html/infoschema-information-schema-catalog-name.html
%{_prefix}/%{major_version}/doc/html/spi-spi-execp.html
%{_prefix}/%{major_version}/doc/html/pgarchivecleanup.html
%{_prefix}/%{major_version}/doc/html/infoschema-table-privileges.html
%{_prefix}/%{major_version}/doc/html/trigger-definition.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-build-sql-insert.html
%{_prefix}/%{major_version}/doc/html/textsearch-psql.html
%{_prefix}/%{major_version}/doc/html/datatype-oid.html
%{_prefix}/%{major_version}/doc/html/sslinfo.html
%{_prefix}/%{major_version}/doc/html/storage-fsm.html
%{_prefix}/%{major_version}/doc/html/docguide-build.html
%{_prefix}/%{major_version}/doc/html/manage-ag-config.html
%{_prefix}/%{major_version}/doc/html/release-7-4-2.html
%{_prefix}/%{major_version}/doc/html/release-8-4-2.html
%{_prefix}/%{major_version}/doc/html/release-6-0.html
%{_prefix}/%{major_version}/doc/html/infoschema-foreign-data-wrappers.html
%{_prefix}/%{major_version}/doc/html/sql-createfunction.html
%{_prefix}/%{major_version}/doc/html/database-roles.html
%{_prefix}/%{major_version}/doc/html/textsearch-configuration.html
%{_prefix}/%{major_version}/doc/html/release-1-09.html
%{_prefix}/%{major_version}/doc/html/triggers.html
%{_prefix}/%{major_version}/doc/html/plperl-trusted.html
%{_prefix}/%{major_version}/doc/html/bki-format.html
%{_prefix}/%{major_version}/doc/html/sql-altertsconfig.html
%{_prefix}/%{major_version}/doc/html/release-8-1-18.html
%{_prefix}/%{major_version}/doc/html/infoschema-columns.html
%{_prefix}/%{major_version}/doc/html/git.html
%{_prefix}/%{major_version}/doc/html/extend-type-system.html
%{_prefix}/%{major_version}/doc/html/sql-createopfamily.html
%{_prefix}/%{major_version}/doc/html/sql-alterlanguage.html
%{_prefix}/%{major_version}/doc/html/indexes.html
%{_prefix}/%{major_version}/doc/html/datatype.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-operator.html
%{_prefix}/%{major_version}/doc/html/release-8-2-3.html
%{_prefix}/%{major_version}/doc/html/release-8-0-19.html
%{_prefix}/%{major_version}/doc/html/release-7-2-3.html
%{_prefix}/%{major_version}/doc/html/index.html
%{_prefix}/%{major_version}/doc/html/manage-ag-createdb.html
%{_prefix}/%{major_version}/doc/html/explicit-locking.html
%{_prefix}/%{major_version}/doc/html/ecpg-commands.html
%{_prefix}/%{major_version}/doc/html/functions-datetime.html
%{_prefix}/%{major_version}/doc/html/release-7-4-30.html
%{_prefix}/%{major_version}/doc/html/sql-load.html
%{_prefix}/%{major_version}/doc/html/sql-createdatabase.html
%{_prefix}/%{major_version}/doc/html/biblio.html
%{_prefix}/%{major_version}/doc/html/libpq-example.html
%{_prefix}/%{major_version}/doc/html/uuid-ossp.html
%{_prefix}/%{major_version}/doc/html/sql-alterrole.html
%{_prefix}/%{major_version}/doc/html/textsearch-debugging.html
%{_prefix}/%{major_version}/doc/html/release-6-5.html
%{_prefix}/%{major_version}/doc/html/textsearch-dictionaries.html
%{_prefix}/%{major_version}/doc/html/wal-internals.html
%{_prefix}/%{major_version}/doc/html/release-7-4-7.html
%{_prefix}/%{major_version}/doc/html/infoschema-parameters.html
%{_prefix}/%{major_version}/doc/html/functions-sequence.html
%{_prefix}/%{major_version}/doc/html/pgrowlocks.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-amproc.html
%{_prefix}/%{major_version}/doc/html/app-postgres.html
%{_prefix}/%{major_version}/doc/html/tutorial-join.html
%{_prefix}/%{major_version}/doc/html/ecpg-set-connection.html
%{_prefix}/%{major_version}/doc/html/trigger-interface.html
%{_prefix}/%{major_version}/doc/html/sql-dropsequence.html
%{_prefix}/%{major_version}/doc/html/runtime-config-short.html
%{_prefix}/%{major_version}/doc/html/ecpg-errors.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-sizing.html
%{_prefix}/%{major_version}/doc/html/infoschema-data-type-privileges.html
%{_prefix}/%{major_version}/doc/html/functions-subquery.html
%{_prefix}/%{major_version}/doc/html/runtime-config-autovacuum.html
%{_prefix}/%{major_version}/doc/html/libpq-copy.html
%{_prefix}/%{major_version}/doc/html/pltcl-global.html
%{_prefix}/%{major_version}/doc/html/release-8-1-8.html
%{_prefix}/%{major_version}/doc/html/external-projects.html
%{_prefix}/%{major_version}/doc/html/install-windows-libpq.html
%{_prefix}/%{major_version}/doc/html/sql-dropforeigndatawrapper.html
%{_prefix}/%{major_version}/doc/html/tutorial-accessdb.html
%{_prefix}/%{major_version}/doc/html/release-7-2-6.html
%{_prefix}/%{major_version}/doc/html/gist-intro.html
%{_prefix}/%{major_version}/doc/html/release-7-4-28.html
%{_prefix}/%{major_version}/doc/html/bookindex.html
%{_prefix}/%{major_version}/doc/html/release-8-2-6.html
%{_prefix}/%{major_version}/doc/html/disk-full.html
%{_prefix}/%{major_version}/doc/html/sql-declare.html
%{_prefix}/%{major_version}/doc/html/infoschema-key-column-usage.html
%{_prefix}/%{major_version}/doc/html/indexes-opclass.html
%{_prefix}/%{major_version}/doc/html/overview.html
%{_prefix}/%{major_version}/doc/html/release-7-4-19.html
%{_prefix}/%{major_version}/doc/html/error-message-reporting.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-languages.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-ts-config.html
%{_prefix}/%{major_version}/doc/html/geqo.html
%{_prefix}/%{major_version}/doc/html/ecpg-process.html
%{_prefix}/%{major_version}/doc/html/sql-createcast.html
%{_prefix}/%{major_version}/doc/html/sql-fetch.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-close.html
%{_prefix}/%{major_version}/doc/html/release-7-3.html
%{_prefix}/%{major_version}/doc/html/sql-createview.html
%{_prefix}/%{major_version}/doc/html/role-attributes.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-authid.html
%{_prefix}/%{major_version}/doc/html/docguide-authoring.html
%{_prefix}/%{major_version}/doc/html/release-8-3-4.html
%{_prefix}/%{major_version}/doc/html/release-6-1-1.html
%{_prefix}/%{major_version}/doc/html/tutorial.html
%{_prefix}/%{major_version}/doc/html/xoper.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-cast.html
%{_prefix}/%{major_version}/doc/html/indexes-bitmap-scans.html
%{_prefix}/%{major_version}/doc/html/release-7-3-4.html
%{_prefix}/%{major_version}/doc/html/view-pg-user.html
%{_prefix}/%{major_version}/doc/html/monitoring-locks.html
%{_prefix}/%{major_version}/doc/html/test-parser.html
%{_prefix}/%{major_version}/doc/html/textsearch-features.html
%{_prefix}/%{major_version}/doc/html/view-pg-stats.html
%{_prefix}/%{major_version}/doc/html/sql-commit.html
%{_prefix}/%{major_version}/doc/html/tutorial-views.html
%{_prefix}/%{major_version}/doc/html/plperl-funcs.html
%{_prefix}/%{major_version}/doc/html/release-8-4-3.html
%{_prefix}/%{major_version}/doc/html/release-6-1.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-am.html
%{_prefix}/%{major_version}/doc/html/contrib-spi.html
%{_prefix}/%{major_version}/doc/html/sql-createindex.html
%{_prefix}/%{major_version}/doc/html/tutorial-sql-intro.html
%{_prefix}/%{major_version}/doc/html/spi-spi-push.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-connect.html
%{_prefix}/%{major_version}/doc/html/release-7-4-3.html
%{_prefix}/%{major_version}/doc/html/gin-limit.html
%{_prefix}/%{major_version}/doc/html/functions-binarystring.html
%{_prefix}/%{major_version}/doc/html/view-pg-timezone-names.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-move.html
%{_prefix}/%{major_version}/doc/html/features.html
%{_prefix}/%{major_version}/doc/html/role-membership.html
%{_prefix}/%{major_version}/doc/html/release-8-1-19.html
%{_prefix}/%{major_version}/doc/html/textsearch-parsers.html
%{_prefix}/%{major_version}/doc/html/ddl-system-columns.html
%{_prefix}/%{major_version}/doc/html/docguide.html
%{_prefix}/%{major_version}/doc/html/sql-copy.html
%{_prefix}/%{major_version}/doc/html/tutorial-arch.html
%{_prefix}/%{major_version}/doc/html/release-7-2-2.html
%{_prefix}/%{major_version}/doc/html/plperl-data.html
%{_prefix}/%{major_version}/doc/html/libpq-control.html
%{_prefix}/%{major_version}/doc/html/bki-example.html
%{_prefix}/%{major_version}/doc/html/release-8-0-18.html
%{_prefix}/%{major_version}/doc/html/sql-values.html
%{_prefix}/%{major_version}/doc/html/release-8-2-2.html
%{_prefix}/%{major_version}/doc/html/internals.html
%{_prefix}/%{major_version}/doc/html/backup-dump.html
%{_prefix}/%{major_version}/doc/html/kernel-resources.html
%{_prefix}/%{major_version}/doc/html/spi-spi-execute.html
%{_prefix}/%{major_version}/doc/html/spi-spi-execute-plan.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-namespace.html
%{_prefix}/%{major_version}/doc/html/pltcl-functions.html
%{_prefix}/%{major_version}/doc/html/datatype-enum.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-enum.html
%{_prefix}/%{major_version}/doc/html/ecpg-dynamic.html
%{_prefix}/%{major_version}/doc/html/sql-dropserver.html
%{_prefix}/%{major_version}/doc/html/release-7-4-20.html
%{_prefix}/%{major_version}/doc/html/sql-dropuser.html
%{_prefix}/%{major_version}/doc/html/spi-spi-modifytuple.html
%{_prefix}/%{major_version}/doc/html/infoschema-column-domain-usage.html
%{_prefix}/%{major_version}/doc/html/release-8-3.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-sizing-profiles.html
%{_prefix}/%{major_version}/doc/html/release-8-0-14.html
%{_prefix}/%{major_version}/doc/html/typeconv-overview.html
%{_prefix}/%{major_version}/doc/html/plpgsql.html
%{_prefix}/%{major_version}/doc/html/resources.html
%{_prefix}/%{major_version}/doc/html/plpython-python23.html
%{_prefix}/%{major_version}/doc/html/view-pg-group.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-trigger.html
%{_prefix}/%{major_version}/doc/html/release-7-4-11.html
%{_prefix}/%{major_version}/doc/html/source-format.html
%{_prefix}/%{major_version}/doc/html/plperl-triggers.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-open.html
%{_prefix}/%{major_version}/doc/html/plperl-under-the-hood.html
%{_prefix}/%{major_version}/doc/html/release-6-4-2.html
%{_prefix}/%{major_version}/doc/html/release-8-0-25.html
%{_prefix}/%{major_version}/doc/html/functions-formatting.html
%{_prefix}/%{major_version}/doc/html/indexes-unique.html
%{_prefix}/%{major_version}/doc/html/perm-functions.html
%{_prefix}/%{major_version}/doc/html/infoschema-check-constraints.html
%{_prefix}/%{major_version}/doc/html/view-pg-tables.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-statistic.html
%{_prefix}/%{major_version}/doc/html/release-8-1-15.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-ts-config-map.html
%{_prefix}/%{major_version}/doc/html/nls.html
%{_prefix}/%{major_version}/doc/html/external-pl.html
%{_prefix}/%{major_version}/doc/html/pgbench.html
%{_prefix}/%{major_version}/doc/html/sql-commit-prepared.html
%{_prefix}/%{major_version}/doc/html/runtime-config-query.html
%{_prefix}/%{major_version}/doc/html/sql-dropfunction.html
%{_prefix}/%{major_version}/doc/html/release-8-2-16.html
%{_prefix}/%{major_version}/doc/html/gin-implementation.html
%{_prefix}/%{major_version}/doc/html/datetime-input-rules.html
%{_prefix}/%{major_version}/doc/html/release-7-3-12.html
%{_prefix}/%{major_version}/doc/html/trigger-example.html
%{_prefix}/%{major_version}/doc/html/sql-truncate.html
%{_prefix}/%{major_version}/doc/html/sql-droptype.html
%{_prefix}/%{major_version}/doc/html/view-pg-user-mappings.html
%{_prefix}/%{major_version}/doc/html/hstore.html
%{_prefix}/%{major_version}/doc/html/reference.html
%{_prefix}/%{major_version}/doc/html/sql-alterindex.html
%{_prefix}/%{major_version}/doc/html/auth-pg-hba-conf.html
%{_prefix}/%{major_version}/doc/html/infoschema-domain-constraints.html
%{_prefix}/%{major_version}/doc/html/row-estimation-examples.html
%{_prefix}/%{major_version}/doc/html/queries-order.html
%{_prefix}/%{major_version}/doc/html/storage-toast.html
%{_prefix}/%{major_version}/doc/html/plpgsql-overview.html
%{_prefix}/%{major_version}/doc/html/release-8-0-6.html
%{_prefix}/%{major_version}/doc/html/plpgsql-errors-and-messages.html
%{_prefix}/%{major_version}/doc/html/wal.html
%{_prefix}/%{major_version}/doc/html/datatype-bit.html
%{_prefix}/%{major_version}/doc/html/sql-dropopfamily.html
%{_prefix}/%{major_version}/doc/html/app-psql.html
%{_prefix}/%{major_version}/doc/html/installation-platform-notes.html
%{_prefix}/%{major_version}/doc/html/pltcl-trigger.html
%{_prefix}/%{major_version}/doc/html/release-7-3-8.html
%{_prefix}/%{major_version}/doc/html/release-8-3-8.html
%{_prefix}/%{major_version}/doc/html/acronyms.html
%{_prefix}/%{major_version}/doc/html/locale.html
%{_prefix}/%{major_version}/doc/html/runtime-config-developer.html
%{_prefix}/%{major_version}/doc/html/spi-spi-gettypeid.html
%{_prefix}/%{major_version}/doc/html/ecpg-concept.html
%{_prefix}/%{major_version}/doc/html/functions-textsearch.html
%{_prefix}/%{major_version}/doc/html/release-7-4-15.html
%{_prefix}/%{major_version}/doc/html/regress-run.html
%{_prefix}/%{major_version}/doc/html/sql-dropopclass.html
%{_prefix}/%{major_version}/doc/html/view-pg-indexes.html
%{_prefix}/%{major_version}/doc/html/infoschema-user-mapping-options.html
%{_prefix}/%{major_version}/doc/html/textsearch.html
%{_prefix}/%{major_version}/doc/html/auth-username-maps.html
%{_prefix}/%{major_version}/doc/html/sql-analyze.html
%{_prefix}/%{major_version}/doc/html/ddl-partitioning.html
%{_prefix}/%{major_version}/doc/html/protocol-error-fields.html
%{_prefix}/%{major_version}/doc/html/continuous-archiving.html
%{_prefix}/%{major_version}/doc/html/libpq-ldap.html
%{_prefix}/%{major_version}/doc/html/release-8-0-21.html
%{_prefix}/%{major_version}/doc/html/libpq-threading.html
%{_prefix}/%{major_version}/doc/html/monitoring-stats.html
%{_prefix}/%{major_version}/doc/html/server-shutdown.html
%{_prefix}/%{major_version}/doc/html/external-interfaces.html
%{_prefix}/%{major_version}/doc/html/release-8-1-11.html
%{_prefix}/%{major_version}/doc/html/infoschema-check-constraint-routine-usage.html
%{_prefix}/%{major_version}/doc/html/spi-spi-connect.html
%{_prefix}/%{major_version}/doc/html/install-short.html
%{_prefix}/%{major_version}/doc/html/routine-reindex.html
%{_prefix}/%{major_version}/doc/html/ssl-tcp.html
%{_prefix}/%{major_version}/doc/html/release-8-1-20.html
%{_prefix}/%{major_version}/doc/html/largeobjects.html
%{_prefix}/%{major_version}/doc/html/spi-realloc.html
%{_prefix}/%{major_version}/doc/html/release-0-01.html
%{_prefix}/%{major_version}/doc/html/view-pg-locks.html
%{_prefix}/%{major_version}/doc/html/xfunc.html
%{_prefix}/%{major_version}/doc/html/release-6-3-1.html
%{_prefix}/%{major_version}/doc/html/release-8-1-4.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getargcount.html
%{_prefix}/%{major_version}/doc/html/sql-droptsparser.html
%{_prefix}/%{major_version}/doc/html/logfile-maintenance.html
%{_prefix}/%{major_version}/doc/html/release-7-4-24.html
%{_prefix}/%{major_version}/doc/html/release-8-0-10.html
%{_prefix}/%{major_version}/doc/html/functions-bitstring.html
%{_prefix}/%{major_version}/doc/html/sql-dropconversion.html
%{_prefix}/%{major_version}/doc/html/sql-createtsdictionary.html
%{_prefix}/%{major_version}/doc/html/libpq-notice-processing.html
%{_prefix}/%{major_version}/doc/html/plpgsql-control-structures.html
%{_prefix}/%{major_version}/doc/html/release-8-0-2.html
%{_prefix}/%{major_version}/doc/html/query-path.html
%{_prefix}/%{major_version}/doc/html/storage-page-layout.html
%{_prefix}/%{major_version}/doc/html/release-8-3-13.html
%{_prefix}/%{major_version}/doc/html/release-7-0-2.html
%{_prefix}/%{major_version}/doc/html/source.html
%{_prefix}/%{major_version}/doc/html/protocol-message-formats.html
%{_prefix}/%{major_version}/doc/html/sql-select.html
%{_prefix}/%{major_version}/doc/html/libpq-fastpath.html
%{_prefix}/%{major_version}/doc/html/rules-privileges.html
%{_prefix}/%{major_version}/doc/html/infoschema-table-constraints.html
%{_prefix}/%{major_version}/doc/html/history.html
%{_prefix}/%{major_version}/doc/html/geqo-biblio.html
%{_prefix}/%{major_version}/doc/html/sql-dropindex.html
%{_prefix}/%{major_version}/doc/html/release-8-2-12.html
%{_prefix}/%{major_version}/doc/html/stylesheet.css
%{_prefix}/%{major_version}/doc/html/runtime-config-wal.html
%{_prefix}/%{major_version}/doc/html/plpgsql-statements.html
%{_prefix}/%{major_version}/doc/html/release-7-3-16.html
%{_prefix}/%{major_version}/doc/html/log-shipping-alternative.html
%{_prefix}/%{major_version}/doc/html/sql-insert.html
%{_prefix}/%{major_version}/doc/html/oid2name.html
%{_prefix}/%{major_version}/doc/html/sql-syntax-lexical.html
%{_prefix}/%{major_version}/doc/html/sql-end.html
%{_prefix}/%{major_version}/doc/html/datatype-uuid.html
%{_prefix}/%{major_version}/doc/html/infoschema-constraint-table-usage.html
%{_prefix}/%{major_version}/doc/html/sql-prepare-transaction.html
%{_prefix}/%{major_version}/doc/html/plpgsql-porting.html
%{_prefix}/%{major_version}/doc/html/release-7-4-5.html
%{_prefix}/%{major_version}/doc/html/sql-createuser.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-shdescription.html
%{_prefix}/%{major_version}/doc/html/index-functions.html
%{_prefix}/%{major_version}/doc/html/release-8-4-5.html
%{_prefix}/%{major_version}/doc/html/applevel-consistency.html
%{_prefix}/%{major_version}/doc/html/intro-whatis.html
%{_prefix}/%{major_version}/doc/html/information-schema.html
%{_prefix}/%{major_version}/doc/html/sql-alterlargeobject.html
%{_prefix}/%{major_version}/doc/html/functions-info.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-foreign-data-wrapper.html
%{_prefix}/%{major_version}/doc/html/geqo-intro2.html
%{_prefix}/%{major_version}/doc/html/standby-settings.html
%{_prefix}/%{major_version}/doc/html/release-7-3-18.html
%{_prefix}/%{major_version}/doc/html/storage-vm.html
%{_prefix}/%{major_version}/doc/html/catalogs-overview.html
%{_prefix}/%{major_version}/doc/html/infoschema-datatypes.html
%{_prefix}/%{major_version}/doc/html/lo-interfaces.html
%{_prefix}/%{major_version}/doc/html/lo-implementation.html
%{_prefix}/%{major_version}/doc/html/spi-spi-returntuple.html
%{_prefix}/%{major_version}/doc/html/btree-gin.html
%{_prefix}/%{major_version}/doc/html/release-7-3-2.html
%{_prefix}/%{major_version}/doc/html/queries-overview.html
%{_prefix}/%{major_version}/doc/html/release.html
%{_prefix}/%{major_version}/doc/html/regress-coverage.html
%{_prefix}/%{major_version}/doc/html/auto-explain.html
%{_prefix}/%{major_version}/doc/html/release-8-3-2.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-shdepend.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-disconnect.html
%{_prefix}/%{major_version}/doc/html/release-1-0.html
%{_prefix}/%{major_version}/doc/html/hot-standby.html
%{_prefix}/%{major_version}/doc/html/gin.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-ts-parser.html
%{_prefix}/%{major_version}/doc/html/planner-stats.html
%{_prefix}/%{major_version}/doc/html/plhandler.html
%{_prefix}/%{major_version}/doc/html/spi-interface-support.html
%{_prefix}/%{major_version}/doc/html/libpq-cancel.html
%{_prefix}/%{major_version}/doc/html/plpython-envar.html
%{_prefix}/%{major_version}/doc/html/sql-createtype.html
%{_prefix}/%{major_version}/doc/html/spi-spi-fnumber.html
%{_prefix}/%{major_version}/doc/html/docguide-docbook.html
%{_prefix}/%{major_version}/doc/html/spi-spi-saveplan.html
%{_prefix}/%{major_version}/doc/html/sql-unlisten.html
%{_prefix}/%{major_version}/doc/html/release-8-2-4.html
%{_prefix}/%{major_version}/doc/html/storage-file-layout.html
%{_prefix}/%{major_version}/doc/html/functions-srf.html
%{_prefix}/%{major_version}/doc/html/release-7-2-4.html
%{_prefix}/%{major_version}/doc/html/release-9-0-1.html
%{_prefix}/%{major_version}/doc/html/disk-usage.html
%{_prefix}/%{major_version}/doc/html/typeconv-query.html
%{_prefix}/%{major_version}/doc/html/datetime-keywords.html
%{_prefix}/%{major_version}/doc/html/datatype-xml.html
%{_prefix}/%{major_version}/doc/html/protocol-overview.html
%{_prefix}/%{major_version}/doc/html/plpython-do.html
%{_prefix}/%{major_version}/doc/html/plpgsql-declarations.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-get-notify.html
%{_prefix}/%{major_version}/doc/html/release-7-1.html
%{_prefix}/%{major_version}/doc/html/libpq-notify.html
%{_prefix}/%{major_version}/doc/html/pgtrgm.html
%{_prefix}/%{major_version}/doc/html/install-post.html
%{_prefix}/%{major_version}/doc/html/lo-examplesect.html
%{_prefix}/%{major_version}/doc/html/sql-alterschema.html
%{_prefix}/%{major_version}/doc/html/infoschema-routine-privileges.html
%{_prefix}/%{major_version}/doc/html/view-pg-prepared-statements.html
%{_prefix}/%{major_version}/doc/html/xfunc-volatility.html
%{_prefix}/%{major_version}/doc/html/libpq-ssl.html
%{_prefix}/%{major_version}/doc/html/release-7-3-6.html
%{_prefix}/%{major_version}/doc/html/intagg.html
%{_prefix}/%{major_version}/doc/html/xplang-install.html
%{_prefix}/%{major_version}/doc/html/functions-trigger.html
%{_prefix}/%{major_version}/doc/html/app-pg-dumpall.html
%{_prefix}/%{major_version}/doc/html/release-8-3-6.html
%{_prefix}/%{major_version}/doc/html/app-createdb.html
%{_prefix}/%{major_version}/doc/html/sql-dropdomain.html
%{_prefix}/%{major_version}/doc/html/release-8-0-8.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink.html
%{_prefix}/%{major_version}/doc/html/plpython-trigger.html
%{_prefix}/%{major_version}/doc/html/infoschema-column-udt-usage.html
%{_prefix}/%{major_version}/doc/html/release-7-4-1.html
%{_prefix}/%{major_version}/doc/html/planner-stats-details.html
%{_prefix}/%{major_version}/doc/html/functions-admin.html
%{_prefix}/%{major_version}/doc/html/sql-alterdatabase.html
%{_prefix}/%{major_version}/doc/html/release-8-4-1.html
%{_prefix}/%{major_version}/doc/html/release-6-3.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-type.html
%{_prefix}/%{major_version}/doc/html/release-8-2-18.html
%{_prefix}/%{major_version}/doc/html/sql-altertrigger.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-open.html
%{_prefix}/%{major_version}/doc/html/sql-start-transaction.html
%{_prefix}/%{major_version}/doc/html/ddl.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-open-with-paramlist.html
%{_prefix}/%{major_version}/doc/html/regress-variant.html
%{_prefix}/%{major_version}/doc/html/wal-reliability.html
%{_prefix}/%{major_version}/doc/html/functions-geometry.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-tablespace.html
%{_prefix}/%{major_version}/doc/html/unaccent.html
%{_prefix}/%{major_version}/doc/html/sql-do.html
%{_prefix}/%{major_version}/doc/html/gist-implementation.html
%{_prefix}/%{major_version}/doc/html/spi-spi-execute-plan-with-paramlist.html
%{_prefix}/%{major_version}/doc/html/manage-ag-overview.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-exec.html
%{_prefix}/%{major_version}/doc/html/pltcl-unknown.html
%{_prefix}/%{major_version}/doc/html/app-droplang.html
%{_prefix}/%{major_version}/doc/html/sql-lock.html
%{_prefix}/%{major_version}/doc/html/ecpg-disconnect.html
%{_prefix}/%{major_version}/doc/html/sql-selectinto.html
%{_prefix}/%{major_version}/doc/html/extend.html
%{_prefix}/%{major_version}/doc/html/sql-delete.html
%{_prefix}/%{major_version}/doc/html/warm-standby-failover.html
%{_prefix}/%{major_version}/doc/html/docguide-style.html
%{_prefix}/%{major_version}/doc/html/indexes-ordering.html
%{_prefix}/%{major_version}/doc/html/runtime.html
%{_prefix}/%{major_version}/doc/html/functions-aggregate.html
%{_prefix}/%{major_version}/doc/html/appendixes.html
%{_prefix}/%{major_version}/doc/html/sql-dropoperator.html
%{_prefix}/%{major_version}/doc/html/sql-syntax-calling-funcs.html
%{_prefix}/%{major_version}/doc/html/indexes-examine.html
%{_prefix}/%{major_version}/doc/html/ddl-depend.html
%{_prefix}/%{major_version}/doc/html/view-pg-views.html
%{_prefix}/%{major_version}/doc/html/sql-expressions.html
%{_prefix}/%{major_version}/doc/html/sql-update.html
%{_prefix}/%{major_version}/doc/html/tutorial-transactions.html
%{_prefix}/%{major_version}/doc/html/install-requirements.html
%{_prefix}/%{major_version}/doc/html/plpgsql-structure.html
%{_prefix}/%{major_version}/doc/html/textsearch-intro.html
%{_prefix}/%{major_version}/doc/html/release-8-1.html
%{_prefix}/%{major_version}/doc/html/infoschema-view-column-usage.html
%{_prefix}/%{major_version}/doc/html/pgbuffercache.html
%{_prefix}/%{major_version}/doc/html/ecpg-variables.html
%{_prefix}/%{major_version}/doc/html/release-8-0-16.html
%{_prefix}/%{major_version}/doc/html/tutorial-window.html
%{_prefix}/%{major_version}/doc/html/release-7-4-22.html
%{_prefix}/%{major_version}/doc/html/textsearch-indexes.html
%{_prefix}/%{major_version}/doc/html/release-8-1-2.html
%{_prefix}/%{major_version}/doc/html/release-7-1-2.html
%{_prefix}/%{major_version}/doc/html/spi-spi-is-cursor-plan.html
%{_prefix}/%{major_version}/doc/html/catalogs.html
%{_prefix}/%{major_version}/doc/html/btree-gist.html
%{_prefix}/%{major_version}/doc/html/sql-execute.html
%{_prefix}/%{major_version}/doc/html/release-8-1-17.html
%{_prefix}/%{major_version}/doc/html/queries-limit.html
%{_prefix}/%{major_version}/doc/html/sql-rollback.html
%{_prefix}/%{major_version}/doc/html/functions-string.html
%{_prefix}/%{major_version}/doc/html/querytree.html
%{_prefix}/%{major_version}/doc/html/tutorial-sql.html
%{_prefix}/%{major_version}/doc/html/protocol-changes.html
%{_prefix}/%{major_version}/doc/html/contrib.html
%{_prefix}/%{major_version}/doc/html/release-7-4-13.html
%{_prefix}/%{major_version}/doc/html/monitoring-ps.html
%{_prefix}/%{major_version}/doc/html/rowtypes.html
%{_prefix}/%{major_version}/doc/html/infoschema-tables.html
%{_prefix}/%{major_version}/doc/html/indexes-types.html
%{_prefix}/%{major_version}/doc/html/indexes-intro.html
%{_prefix}/%{major_version}/doc/html/infoschema-view-routine-usage.html
%{_prefix}/%{major_version}/doc/html/connect-estab.html
%{_prefix}/%{major_version}/doc/html/citext.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-fetch.html
%{_prefix}/%{major_version}/doc/html/textsearch-tables.html
%{_prefix}/%{major_version}/doc/html/rules-triggers.html
%{_prefix}/%{major_version}/doc/html/pgstandby.html
%{_prefix}/%{major_version}/doc/html/release-7-3-10.html
%{_prefix}/%{major_version}/doc/html/config-setting.html
%{_prefix}/%{major_version}/doc/html/release-8-2-14.html
%{_prefix}/%{major_version}/doc/html/sql-close.html
%{_prefix}/%{major_version}/doc/html/sql-dropcast.html
%{_prefix}/%{major_version}/doc/html/release-7-3-21.html
%{_prefix}/%{major_version}/doc/html/datatype-geometric.html
%{_prefix}/%{major_version}/doc/html/infoschema-schema.html
%{_prefix}/%{major_version}/doc/html/runtime-config-client.html
%{_prefix}/%{major_version}/doc/html/sql-dropview.html
%{_prefix}/%{major_version}/doc/html/xplang.html
%{_prefix}/%{major_version}/doc/html/infoschema-referential-constraints.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getbinval.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-foreign-server.html
%{_prefix}/%{major_version}/doc/html/release-8-0-4.html
%{_prefix}/%{major_version}/doc/html/release-6-2-1.html
%{_prefix}/%{major_version}/doc/html/infoschema-user-mappings.html
%{_prefix}/%{major_version}/doc/html/infoschema-role-usage-grants.html
%{_prefix}/%{major_version}/doc/html/plpgsql-development-tips.html
%{_prefix}/%{major_version}/doc/html/sql-createaggregate.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-database.html
%{_prefix}/%{major_version}/doc/html/functions-array.html
%{_prefix}/%{major_version}/doc/html/privileges.html
%{_prefix}/%{major_version}/doc/html/release-8-1-13.html
%{_prefix}/%{major_version}/doc/html/spi-spi-scroll-cursor-move.html
%{_prefix}/%{major_version}/doc/html/sql-set-role.html
%{_prefix}/%{major_version}/doc/html/spi-examples.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-constraint.html
%{_prefix}/%{major_version}/doc/html/release-8-0-23.html
%{_prefix}/%{major_version}/doc/html/gin-extensibility.html
%{_prefix}/%{major_version}/doc/html/release-7-4-17.html
%{_prefix}/%{major_version}/doc/html/queries-select-lists.html
%{_prefix}/%{major_version}/doc/html/release-1-02.html
%{_prefix}/%{major_version}/doc/html/ddl-others.html
%{_prefix}/%{major_version}/doc/html/lo-intro.html
%{_prefix}/%{major_version}/doc/html/release-8-0-12.html
%{_prefix}/%{major_version}/doc/html/release-7-2-8.html
%{_prefix}/%{major_version}/doc/html/spi-spi-freetuple.html
%{_prefix}/%{major_version}/doc/html/datatype-datetime.html
%{_prefix}/%{major_version}/doc/html/release-8-2-8.html
%{_prefix}/%{major_version}/doc/html/infoschema-attributes.html
%{_prefix}/%{major_version}/doc/html/release-7-4-26.html
%{_prefix}/%{major_version}/doc/html/release-0-03.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-error-message.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-packages.html
%{_prefix}/%{major_version}/doc/html/app-reindexdb.html
%{_prefix}/%{major_version}/doc/html/preventing-server-spoofing.html
%{_prefix}/%{major_version}/doc/html/release-8-1-6.html
%{_prefix}/%{major_version}/doc/html/release-8-1-22.html
%{_prefix}/%{major_version}/doc/html/sql-checkpoint.html
%{_prefix}/%{major_version}/doc/html/sql-createconversion.html
%{_prefix}/%{major_version}/doc/html/tutorial-populate.html
%{_prefix}/%{major_version}/doc/html/regress-evaluation.html
%{_prefix}/%{major_version}/doc/html/gin-tips.html
%{_prefix}/%{major_version}/doc/html/sql-droplanguage.html
%{_prefix}/%{major_version}/doc/html/sql-alterconversion.html
%{_prefix}/%{major_version}/doc/html/app-dropuser.html
%{_prefix}/%{major_version}/doc/html/tutorial-table.html
%{_prefix}/%{major_version}/doc/html/protocol-replication.html
%{_prefix}/%{major_version}/doc/html/ecpg-preproc.html
%{_prefix}/%{major_version}/doc/html/indexes-expressional.html
%{_prefix}/%{major_version}/doc/html/ltree.html
%{_prefix}/%{major_version}/doc/html/sql.html
%{_prefix}/%{major_version}/doc/html/plpython-data.html
%{_prefix}/%{major_version}/doc/html/libpq-build.html
%{_prefix}/%{major_version}/doc/html/functions-enum.html
%{_prefix}/%{major_version}/doc/html/sql-createopclass.html
%{_prefix}/%{major_version}/doc/html/release-8-3-11.html
%{_prefix}/%{major_version}/doc/html/client-authentication.html
%{_prefix}/%{major_version}/doc/html/app-dropdb.html
%{_prefix}/%{major_version}/doc/html/explicit-joins.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-open-with-args.html
%{_prefix}/%{major_version}/doc/html/migration.html
%{_prefix}/%{major_version}/doc/html/spi-spi-scroll-cursor-fetch.html
%{_prefix}/%{major_version}/doc/html/functions-conditional.html
%{_prefix}/%{major_version}/doc/html/release-7-4-9.html
%{_prefix}/%{major_version}/doc/html/spi-spi-prepare-params.html
%{_prefix}/%{major_version}/doc/html/release-7-3-14.html
%{_prefix}/%{major_version}/doc/html/storage.html
%{_prefix}/%{major_version}/doc/html/sql-revoke.html
%{_prefix}/%{major_version}/doc/html/sql-droptsconfig.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-get-result.html
%{_prefix}/%{major_version}/doc/html/tutorial-fk.html
%{_prefix}/%{major_version}/doc/html/sql-discard.html
%{_prefix}/%{major_version}/doc/html/queries-values.html
%{_prefix}/%{major_version}/doc/html/sql-createschema.html
%{_prefix}/%{major_version}/doc/html/release-8-2-10.html
%{_prefix}/%{major_version}/doc/html/release-6-5-2.html
%{_prefix}/%{major_version}/doc/html/sql-set-session-authorization.html
%{_prefix}/%{major_version}/doc/html/supported-platforms.html
%{_prefix}/%{major_version}/doc/html/protocol-flow.html
%{_prefix}/%{major_version}/doc/html/sql-deallocate.html
%{_prefix}/%{major_version}/doc/html/release-7-4-23.html
%{_prefix}/%{major_version}/doc/html/ecpg-descriptors.html
%{_prefix}/%{major_version}/doc/html/release-8-0-17.html
%{_prefix}/%{major_version}/doc/html/plpython-funcs.html
%{_prefix}/%{major_version}/doc/html/datatype-money.html
%{_prefix}/%{major_version}/doc/html/sql-altersequence.html
%{_prefix}/%{major_version}/doc/html/release-8-0.html
%{_prefix}/%{major_version}/doc/html/sql-rollback-prepared.html
%{_prefix}/%{major_version}/doc/html/sql-listen.html
%{_prefix}/%{major_version}/doc/html/sql-altertsdictionary.html
%{_prefix}/%{major_version}/doc/html/high-availability.html
%{_prefix}/%{major_version}/doc/html/release-7-1-3.html
%{_prefix}/%{major_version}/doc/html/sql-dropaggregate.html
%{_prefix}/%{major_version}/doc/html/ddl-basics.html
%{_prefix}/%{major_version}/doc/html/sql-vacuum.html
%{_prefix}/%{major_version}/doc/html/pageinspect.html
%{_prefix}/%{major_version}/doc/html/app-pgrestore.html
%{_prefix}/%{major_version}/doc/html/sql-rollback-to.html
%{_prefix}/%{major_version}/doc/html/app-clusterdb.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-largeobject-metadata.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-aggregate.html
%{_prefix}/%{major_version}/doc/html/release-8-1-3.html
%{_prefix}/%{major_version}/doc/html/diskusage.html
%{_prefix}/%{major_version}/doc/html/planner-optimizer.html
%{_prefix}/%{major_version}/doc/html/typeconv-func.html
%{_prefix}/%{major_version}/doc/html/release-8-1-16.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-inherits.html
%{_prefix}/%{major_version}/doc/html/archive-recovery-settings.html
%{_prefix}/%{major_version}/doc/html/trigger-datachanges.html
%{_prefix}/%{major_version}/doc/html/functions-logical.html
%{_prefix}/%{major_version}/doc/html/server-start.html
%{_prefix}/%{major_version}/doc/html/release-7-4-12.html
%{_prefix}/%{major_version}/doc/html/infoschema-view-table-usage.html
%{_prefix}/%{major_version}/doc/html/pltcl-procnames.html
%{_prefix}/%{major_version}/doc/html/tutorial-concepts.html
%{_prefix}/%{major_version}/doc/html/view-pg-shadow.html
%{_prefix}/%{major_version}/doc/html/app-vacuumdb.html
%{_prefix}/%{major_version}/doc/html/geqo-intro.html
%{_prefix}/%{major_version}/doc/html/release-6-4-1.html
%{_prefix}/%{major_version}/doc/html/release-8-0-26.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-get-connections.html
%{_prefix}/%{major_version}/doc/html/functions-math.html
%{_prefix}/%{major_version}/doc/html/sql-grant.html
%{_prefix}/%{major_version}/doc/html/xaggr.html
%{_prefix}/%{major_version}/doc/html/plperl-builtins.html
%{_prefix}/%{major_version}/doc/html/sql-createtable.html
%{_prefix}/%{major_version}/doc/html/functions-net.html
%{_prefix}/%{major_version}/doc/html/pltcl-data.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-amop.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getnspname.html
%{_prefix}/%{major_version}/doc/html/dml-update.html
%{_prefix}/%{major_version}/doc/html/spi-spi-freetupletable.html
%{_prefix}/%{major_version}/doc/html/app-pgresetxlog.html
%{_prefix}/%{major_version}/doc/html/xtypes.html
%{_prefix}/%{major_version}/doc/html/sql-set-constraints.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-depend.html
%{_prefix}/%{major_version}/doc/html/release-8-2-15.html
%{_prefix}/%{major_version}/doc/html/plpgsql-expressions.html
%{_prefix}/%{major_version}/doc/html/wal-configuration.html
%{_prefix}/%{major_version}/doc/html/release-7-3-11.html
%{_prefix}/%{major_version}/doc/html/view-pg-cursors.html
%{_prefix}/%{major_version}/doc/html/protocol-message-types.html
%{_prefix}/%{major_version}/doc/html/sql-alteraggregate.html
%{_prefix}/%{major_version}/doc/html/plpgsql-implementation.html
%{_prefix}/%{major_version}/doc/html/infoschema-enabled-roles.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-opfamily.html
%{_prefix}/%{major_version}/doc/html/tutorial-select.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-auth-members.html
%{_prefix}/%{major_version}/doc/html/release-7-3-20.html
%{_prefix}/%{major_version}/doc/html/infoschema-role-column-grants.html
%{_prefix}/%{major_version}/doc/html/dml-delete.html
%{_prefix}/%{major_version}/doc/html/sql-createoperator.html
%{_prefix}/%{major_version}/doc/html/populate.html
%{_prefix}/%{major_version}/doc/html/release-8-0-5.html
%{_prefix}/%{major_version}/doc/html/infoschema-foreign-server-options.html
%{_prefix}/%{major_version}/doc/html/view-pg-timezone-abbrevs.html
%{_prefix}/%{major_version}/doc/html/datatype-boolean.html
%{_prefix}/%{major_version}/doc/html/ddl-constraints.html
%{_prefix}/%{major_version}/doc/html/earthdistance.html
%{_prefix}/%{major_version}/doc/html/release-8-1-12.html
%{_prefix}/%{major_version}/doc/html/sql-createdomain.html
%{_prefix}/%{major_version}/doc/html/index-unique-checks.html
%{_prefix}/%{major_version}/doc/html/sql-abort.html
%{_prefix}/%{major_version}/doc/html/sql-reset.html
%{_prefix}/%{major_version}/doc/html/encryption-options.html
%{_prefix}/%{major_version}/doc/html/sql-alteruser.html
%{_prefix}/%{major_version}/doc/html/app-pgdump.html
%{_prefix}/%{major_version}/doc/html/maintenance.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-proc.html
%{_prefix}/%{major_version}/doc/html/release-7-4-16.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-build-sql-delete.html
%{_prefix}/%{major_version}/doc/html/release-8-0-22.html
%{_prefix}/%{major_version}/doc/html/view-pg-rules.html
%{_prefix}/%{major_version}/doc/html/release-8-2-9.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-cancel-query.html
%{_prefix}/%{major_version}/doc/html/release-7-4-27.html
%{_prefix}/%{major_version}/doc/html/performance-tips.html
%{_prefix}/%{major_version}/doc/html/sql-createtstemplate.html
%{_prefix}/%{major_version}/doc/html/release-8-4.html
%{_prefix}/%{major_version}/doc/html/reference-client.html
%{_prefix}/%{major_version}/doc/html/client-interfaces.html
%{_prefix}/%{major_version}/doc/html/release-8-0-13.html
%{_prefix}/%{major_version}/doc/html/release-8-1-23.html
%{_prefix}/%{major_version}/doc/html/lo-funcs.html
%{_prefix}/%{major_version}/doc/html/plperl-global.html
%{_prefix}/%{major_version}/doc/html/sql-begin.html
%{_prefix}/%{major_version}/doc/html/xoper-optimization.html
%{_prefix}/%{major_version}/doc/html/release-6-3-2.html
%{_prefix}/%{major_version}/doc/html/install-windows.html
%{_prefix}/%{major_version}/doc/html/release-8-1-7.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getvalue.html
%{_prefix}/%{major_version}/doc/html/release-0-02.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-build-sql-update.html
%{_prefix}/%{major_version}/doc/html/sql-altertype.html
%{_prefix}/%{major_version}/doc/html/datatype-pseudo.html
%{_prefix}/%{major_version}/doc/html/fuzzystrmatch.html
%{_prefix}/%{major_version}/doc/html/ecpg-pgtypes.html
%{_prefix}/%{major_version}/doc/html/libpq-async.html
%{_prefix}/%{major_version}/doc/html/spi-spi-pop.html
%{_prefix}/%{major_version}/doc/html/sql-reindex.html
%{_prefix}/%{major_version}/doc/html/error-style-guide.html
%{_prefix}/%{major_version}/doc/html/release-8-0-1.html
%{_prefix}/%{major_version}/doc/html/sql-altertstemplate.html
%{_prefix}/%{major_version}/doc/html/xfunc-overload.html
%{_prefix}/%{major_version}/doc/html/release-7-0-1.html
%{_prefix}/%{major_version}/doc/html/release-8-3-10.html
%{_prefix}/%{major_version}/doc/html/functions-comparisons.html
%{_prefix}/%{major_version}/doc/html/sql-alterdefaultprivileges.html
%{_prefix}/%{major_version}/doc/html/errcodes-appendix.html
%{_prefix}/%{major_version}/doc/html/runtime-config-logging.html
%{_prefix}/%{major_version}/doc/html/contrib-dblink-get-pkey.html
%{_prefix}/%{major_version}/doc/html/release-7-4-8.html
%{_prefix}/%{major_version}/doc/html/sql-alterforeigndatawrapper.html
%{_prefix}/%{major_version}/doc/html/passwordcheck.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-rewrite.html
%{_prefix}/%{major_version}/doc/html/release-8-2-11.html
%{_prefix}/%{major_version}/doc/html/release-6-5-3.html
%{_prefix}/%{major_version}/doc/html/nls-translator.html
%{_prefix}/%{major_version}/doc/html/sql-creategroup.html
%{_prefix}/%{major_version}/doc/html/ddl-alter.html
%{_prefix}/%{major_version}/doc/html/functions.html
%{_prefix}/%{major_version}/doc/html/spi-spi-pfree.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-largeobject.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-attribute.html
%{_prefix}/%{major_version}/doc/html/pltcl-overview.html
%{_prefix}/%{major_version}/doc/html/release-7-3-15.html
%{_prefix}/%{major_version}/doc/html/release-8-4-4.html
%{_prefix}/%{major_version}/doc/html/sql-droptsdictionary.html
%{_prefix}/%{major_version}/doc/html/intarray.html
%{_prefix}/%{major_version}/doc/html/sql-alterdomain.html
%{_prefix}/%{major_version}/doc/html/release-7-4-4.html
%{_prefix}/%{major_version}/doc/html/runtime-config-locks.html
%{_prefix}/%{major_version}/doc/html/bki-structure.html
%{_prefix}/%{major_version}/doc/html/sql-altergroup.html
%{_prefix}/%{major_version}/doc/html/release-7-3-19.html
%{_prefix}/%{major_version}/doc/html/sql-droptable.html
%{_prefix}/%{major_version}/doc/html/bki.html
%{_prefix}/%{major_version}/doc/html/typeconv-oper.html
%{_prefix}/%{major_version}/doc/html/routine-vacuuming.html
%{_prefix}/%{major_version}/doc/html/release-8-3-3.html
%{_prefix}/%{major_version}/doc/html/infoschema-constraint-column-usage.html
%{_prefix}/%{major_version}/doc/html/sql-droptrigger.html
%{_prefix}/%{major_version}/doc/html/backup.html
%{_prefix}/%{major_version}/doc/html/managing-databases.html
%{_prefix}/%{major_version}/doc/html/gist-examples.html
%{_prefix}/%{major_version}/doc/html/infoschema-foreign-data-wrapper-options.html
%{_prefix}/%{major_version}/doc/html/release-7-3-3.html
%{_prefix}/%{major_version}/doc/html/tutorial-conclusion.html
%{_prefix}/%{major_version}/doc/html/ecpg.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-find.html
%{_prefix}/%{major_version}/doc/html/dynamic-trace.html
%{_prefix}/%{major_version}/doc/html/install-procedure.html
%{_prefix}/%{major_version}/doc/html/ecpg-informix-compat.html
%{_prefix}/%{major_version}/doc/html/sql-droptablespace.html
%{_prefix}/%{major_version}/doc/html/spi-spi-getargtypeid.html
%{_prefix}/%{major_version}/doc/html/tutorial-start.html
%{_prefix}/%{major_version}/doc/html/sql-droprule.html
%{_prefix}/%{major_version}/doc/html/functions-comparison.html
%{_prefix}/%{major_version}/doc/html/dict-int.html
%{_prefix}/%{major_version}/doc/html/release-7-2-5.html
%{_prefix}/%{major_version}/doc/html/sql-alteropfamily.html
%{_prefix}/%{major_version}/doc/html/sql-createlanguage.html
%{_prefix}/%{major_version}/doc/html/release-8-2-5.html
%{_prefix}/%{major_version}/doc/html/spi-spi-exec.html
%{_prefix}/%{major_version}/doc/html/sql-commands.html
%{_prefix}/%{major_version}/doc/html/runtime-config.html
%{_prefix}/%{major_version}/doc/html/install-getsource.html
%{_prefix}/%{major_version}/doc/html/user-manag.html
%{_prefix}/%{major_version}/doc/html/sql-alterfunction.html
%{_prefix}/%{major_version}/doc/html/server-programming.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-attrdef.html
%{_prefix}/%{major_version}/doc/html/backup-file.html
%{_prefix}/%{major_version}/doc/html/protocol.html
%{_prefix}/%{major_version}/doc/html/installation.html
%{_prefix}/%{major_version}/doc/html/runtime-config-compatible.html
%{_prefix}/%{major_version}/doc/html/release-7-0.html
%{_prefix}/%{major_version}/doc/html/ddl-inherit.html
%{_prefix}/%{major_version}/doc/html/sql-show.html
%{_prefix}/%{major_version}/doc/html/tutorial-createdb.html
%{_prefix}/%{major_version}/doc/html/functions-matching.html
%{_prefix}/%{major_version}/doc/html/spi.html
%{_prefix}/%{major_version}/doc/html/views-overview.html
%{_prefix}/%{major_version}/doc/html/client-authentication-problems.html
%{_prefix}/%{major_version}/doc/html/wal-async-commit.html
%{_prefix}/%{major_version}/doc/html/install-windows-full.html
%{_prefix}/%{major_version}/doc/html/sql-createtsconfig.html
%{_prefix}/%{major_version}/doc/html/sql-prepare.html
%{_prefix}/%{major_version}/doc/html/ecpg-connect.html
%{_prefix}/%{major_version}/doc/html/pgstattuple.html
%{_prefix}/%{major_version}/doc/html/index-cost-estimation.html
%{_prefix}/%{major_version}/doc/html/auth-methods.html
%{_prefix}/%{major_version}/doc/html/non-durability.html
%{_prefix}/%{major_version}/doc/html/functions-xml.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-opclass.html
%{_prefix}/%{major_version}/doc/html/catalog-pg-db-role-setting.html
%{_prefix}/%{major_version}/doc/html/release-8-3-7.html
%{_prefix}/%{major_version}/doc/html/infoschema-schemata.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-implementation-info.html
%{_prefix}/%{major_version}/doc/html/sql-droprole.html
%{_prefix}/%{major_version}/doc/html/monitoring.html
%{_prefix}/%{major_version}/doc/html/release-7-3-7.html
%{_prefix}/%{major_version}/doc/html/infoschema-sql-features.html
%{_prefix}/%{major_version}/doc/html/sql-altertsparser.html
%{_prefix}/%{major_version}/doc/html/plpgsql-trigger.html
%{_prefix}/%{major_version}/doc/html/infoschema-views.html
%{_prefix}/%{major_version}/doc/html/tutorial-agg.html
%{_prefix}/%{major_version}/doc/html/runtime-config-file-locations.html
%{_prefix}/%{major_version}/doc/html/sql-dropusermapping.html
%{_prefix}/%{major_version}/doc/html/release-8-0-9.html
%{_prefix}/%{major_version}/doc/html/sql-keywords-appendix.html
%{_prefix}/%{major_version}/doc/html/sql-release-savepoint.html
%{_prefix}/%{major_version}/doc/html/reference-server.html
%{_prefix}/%{major_version}/doc/html/spi-spi-finish.html
%{_prefix}/%{major_version}/doc/html/sql-altertable.html
%{_prefix}/%{major_version}/doc/html/release-6-2.html
%{_prefix}/%{major_version}/doc/html/libpq-connect.html
%{_prefix}/%{major_version}/doc/html/textsearch-controls.html
%{_prefix}/%{major_version}/doc/html/xindex.html
%{_prefix}/%{major_version}/doc/html/sql-dropgroup.html
%{_prefix}/%{major_version}/doc/html/datatype-net-types.html
%{_prefix}/%{major_version}/doc/html/cube.html
%{_prefix}/%{major_version}/doc/html/index-catalog.html
%{_prefix}/%{major_version}/doc/html/release-8-2-19.html
%{_prefix}/%{major_version}/doc/html/app-initdb.html
%{_prefix}/%{major_version}/doc/html/typeconv-union-case.html
%{_prefix}/%{major_version}/doc/html/rule-system.html
%{_prefix}/%{major_version}/doc/html/spi-spi-cursor-fetch.html
%{_prefix}/%{major_version}/doc/html/infoschema-domain-udt-usage.html
%{_prefix}/%{major_version}/doc/html/release-7-4.html
%{_prefix}/%{major_version}/doc/html/sourcerepo.html
%{_prefix}/%{major_version}/doc/html/xfunc-sql.html
%{_prefix}/%{major_version}/doc/html/pltcl.html
%{_prefix}/%{major_version}/doc/html/recovery-target-settings.html
%{_prefix}/%{major_version}/doc/html/creating-cluster.html
%{_prefix}/%{major_version}/doc/html/manage-ag-tablespaces.html
%{_prefix}/%{major_version}/doc/html/release-7-2-1.html
%{_prefix}/%{major_version}/doc/html/sql-comment.html
%{_prefix}/%{major_version}/doc/html/release-8-2-1.html
%{_prefix}/%{major_version}/doc/html/spi-interface.html
%{_prefix}/%{major_version}/doc/html/sql-dropschema.html
%{_prefix}/%{major_version}/doc/html/sql-createusermapping.html
%{_prefix}/%{major_version}/doc/html/mvcc-intro.html
%{_prefix}/%{major_version}/doc/html/app-postmaster.html
%{_prefix}/%{major_version}/doc/html/infoschema-routines.html
%{_prefix}/%{major_version}/man/man1/pg_ctl.1
%{_prefix}/%{major_version}/man/man1/pg_dumpall.1
%{_prefix}/%{major_version}/man/man1/psql.1
%{_prefix}/%{major_version}/man/man1/createuser.1
%{_prefix}/%{major_version}/man/man1/pg_restore.1
%{_prefix}/%{major_version}/man/man1/dropuser.1
%{_prefix}/%{major_version}/man/man1/pg_config.1
%{_prefix}/%{major_version}/man/man1/createdb.1
%{_prefix}/%{major_version}/man/man1/pg_controldata.1
%{_prefix}/%{major_version}/man/man1/postmaster.1
%{_prefix}/%{major_version}/man/man1/vacuumdb.1
%{_prefix}/%{major_version}/man/man1/initdb.1
%{_prefix}/%{major_version}/man/man1/ecpg.1
%{_prefix}/%{major_version}/man/man1/clusterdb.1
%{_prefix}/%{major_version}/man/man1/reindexdb.1
%{_prefix}/%{major_version}/man/man1/pg_resetxlog.1
%{_prefix}/%{major_version}/man/man1/pg_dump.1
%{_prefix}/%{major_version}/man/man1/dropdb.1
%{_prefix}/%{major_version}/man/man1/postgres.1
%{_prefix}/%{major_version}/man/man1/createlang.1
%{_prefix}/%{major_version}/man/man1/droplang.1
%{_prefix}/%{major_version}/man/man3/dblink_fetch.3
%{_prefix}/%{major_version}/man/man3/dblink_connect_u.3
%{_prefix}/%{major_version}/man/man3/dblink.3
%{_prefix}/%{major_version}/man/man3/SPI_prepare.3
%{_prefix}/%{major_version}/man/man3/SPI_getargtypeid.3
%{_prefix}/%{major_version}/man/man3/dblink_send_query.3
%{_prefix}/%{major_version}/man/man3/SPI_connect.3
%{_prefix}/%{major_version}/man/man3/dblink_close.3
%{_prefix}/%{major_version}/man/man3/SPI_palloc.3
%{_prefix}/%{major_version}/man/man3/SPI_execute.3
%{_prefix}/%{major_version}/man/man3/dblink_build_sql_delete.3
%{_prefix}/%{major_version}/man/man3/SPI_prepare_cursor.3
%{_prefix}/%{major_version}/man/man3/SPI_push.3
%{_prefix}/%{major_version}/man/man3/SPI_execp.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_move.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_open.3
%{_prefix}/%{major_version}/man/man3/dblink_error_message.3
%{_prefix}/%{major_version}/man/man3/dblink_disconnect.3
%{_prefix}/%{major_version}/man/man3/SPI_repalloc.3
%{_prefix}/%{major_version}/man/man3/SPI_pfree.3
%{_prefix}/%{major_version}/man/man3/dblink_get_connections.3
%{_prefix}/%{major_version}/man/man3/dblink_cancel_query.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_open_with_paramlist.3
%{_prefix}/%{major_version}/man/man3/SPI_execute_plan_with_paramlist.3
%{_prefix}/%{major_version}/man/man3/dblink_exec.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_find.3
%{_prefix}/%{major_version}/man/man3/dblink_connect.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_open_with_args.3
%{_prefix}/%{major_version}/man/man3/dblink_open.3
%{_prefix}/%{major_version}/man/man3/SPI_copytuple.3
%{_prefix}/%{major_version}/man/man3/SPI_prepare_params.3
%{_prefix}/%{major_version}/man/man3/SPI_execute_plan.3
%{_prefix}/%{major_version}/man/man3/dblink_get_notify.3
%{_prefix}/%{major_version}/man/man3/SPI_scroll_cursor_move.3
%{_prefix}/%{major_version}/man/man3/SPI_fname.3
%{_prefix}/%{major_version}/man/man3/SPI_saveplan.3
%{_prefix}/%{major_version}/man/man3/SPI_getnspname.3
%{_prefix}/%{major_version}/man/man3/dblink_build_sql_update.3
%{_prefix}/%{major_version}/man/man3/dblink_build_sql_insert.3
%{_prefix}/%{major_version}/man/man3/dblink_is_busy.3
%{_prefix}/%{major_version}/man/man3/SPI_freeplan.3
%{_prefix}/%{major_version}/man/man3/SPI_fnumber.3
%{_prefix}/%{major_version}/man/man3/SPI_freetuple.3
%{_prefix}/%{major_version}/man/man3/SPI_getrelname.3
%{_prefix}/%{major_version}/man/man3/SPI_gettypeid.3
%{_prefix}/%{major_version}/man/man3/SPI_pop.3
%{_prefix}/%{major_version}/man/man3/dblink_get_pkey.3
%{_prefix}/%{major_version}/man/man3/SPI_exec.3
%{_prefix}/%{major_version}/man/man3/SPI_gettype.3
%{_prefix}/%{major_version}/man/man3/SPI_returntuple.3
%{_prefix}/%{major_version}/man/man3/SPI_modifytuple.3
%{_prefix}/%{major_version}/man/man3/SPI_finish.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_close.3
%{_prefix}/%{major_version}/man/man3/SPI_getargcount.3
%{_prefix}/%{major_version}/man/man3/SPI_scroll_cursor_fetch.3
%{_prefix}/%{major_version}/man/man3/dblink_get_result.3
%{_prefix}/%{major_version}/man/man3/SPI_is_cursor_plan.3
%{_prefix}/%{major_version}/man/man3/SPI_execute_with_args.3
%{_prefix}/%{major_version}/man/man3/SPI_getvalue.3
%{_prefix}/%{major_version}/man/man3/SPI_freetuptable.3
%{_prefix}/%{major_version}/man/man3/SPI_cursor_fetch.3
%{_prefix}/%{major_version}/man/man3/SPI_getbinval.3
%{_prefix}/%{major_version}/man/man5/CREATE_TEXT_SEARCH_DICTIONARY.5sql
%{_prefix}/%{major_version}/man/man5/DROP_SCHEMA.5sql
%{_prefix}/%{major_version}/man/man5/CLOSE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_USER_MAPPING.5sql
%{_prefix}/%{major_version}/man/man5/PREPARE_TRANSACTION.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TEXT_SEARCH_TEMPLATE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_DATABASE.5sql
%{_prefix}/%{major_version}/man/man5/ANALYZE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_LANGUAGE.5sql
%{_prefix}/%{major_version}/man/man5/LISTEN.5sql
%{_prefix}/%{major_version}/man/man5/VACUUM.5sql
%{_prefix}/%{major_version}/man/man5/SET_CONSTRAINTS.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_DATABASE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_CONSTRAINT_TRIGGER.5sql
%{_prefix}/%{major_version}/man/man5/SHOW.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TRIGGER.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_DOMAIN.5sql
%{_prefix}/%{major_version}/man/man5/COMMIT_PREPARED.5sql
%{_prefix}/%{major_version}/man/man5/DECLARE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_OWNED.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TEXT_SEARCH_DICTIONARY.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_RULE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_CONVERSION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_OPERATOR.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_LARGE_OBJECT.5sql
%{_prefix}/%{major_version}/man/man5/SELECT_INTO.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_FOREIGN_DATA_WRAPPER.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_ROLE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_FOREIGN_DATA_WRAPPER.5sql
%{_prefix}/%{major_version}/man/man5/DROP_SEQUENCE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_SCHEMA.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_SEQUENCE.5sql
%{_prefix}/%{major_version}/man/man5/UPDATE.5sql
%{_prefix}/%{major_version}/man/man5/WITH.5sql
%{_prefix}/%{major_version}/man/man5/DELETE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TEXT_SEARCH_PARSER.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_SERVER.5sql
%{_prefix}/%{major_version}/man/man5/LOCK.5sql
%{_prefix}/%{major_version}/man/man5/START_TRANSACTION.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TYPE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_USER.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TABLESPACE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_GROUP.5sql
%{_prefix}/%{major_version}/man/man5/DROP_OPERATOR_CLASS.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_GROUP.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_INDEX.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_VIEW.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TYPE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_CAST.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_FUNCTION.5sql
%{_prefix}/%{major_version}/man/man5/DROP_FUNCTION.5sql
%{_prefix}/%{major_version}/man/man5/EXPLAIN.5sql
%{_prefix}/%{major_version}/man/man5/REVOKE.5sql
%{_prefix}/%{major_version}/man/man5/SAVEPOINT.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_USER.5sql
%{_prefix}/%{major_version}/man/man5/DROP_DOMAIN.5sql
%{_prefix}/%{major_version}/man/man5/GRANT.5sql
%{_prefix}/%{major_version}/man/man5/TRUNCATE.5sql
%{_prefix}/%{major_version}/man/man5/REASSIGN_OWNED.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_USER_MAPPING.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TABLE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TABLE.5sql
%{_prefix}/%{major_version}/man/man5/RESET.5sql
%{_prefix}/%{major_version}/man/man5/ABORT.5sql
%{_prefix}/%{major_version}/man/man5/CLUSTER.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TABLESPACE.5sql
%{_prefix}/%{major_version}/man/man5/BEGIN.5sql
%{_prefix}/%{major_version}/man/man5/DROP_OPERATOR_FAMILY.5sql
%{_prefix}/%{major_version}/man/man5/SET.5sql
%{_prefix}/%{major_version}/man/man5/COMMIT.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_DEFAULT_PRIVILEGES.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_USER_MAPPING.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TEXT_SEARCH_PARSER.5sql
%{_prefix}/%{major_version}/man/man5/DO.5sql
%{_prefix}/%{major_version}/man/man5/VALUES.5sql
%{_prefix}/%{major_version}/man/man5/PREPARE.5sql
%{_prefix}/%{major_version}/man/man5/LOAD.5sql
%{_prefix}/%{major_version}/man/man5/SET_ROLE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_VIEW.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TEXT_SEARCH_PARSER.5sql
%{_prefix}/%{major_version}/man/man5/DROP_CAST.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_OPERATOR.5sql
%{_prefix}/%{major_version}/man/man5/UNLISTEN.5sql
%{_prefix}/%{major_version}/man/man5/COPY.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TRIGGER.5sql
%{_prefix}/%{major_version}/man/man5/COMMENT.5sql
%{_prefix}/%{major_version}/man/man5/DROP_OPERATOR.5sql
%{_prefix}/%{major_version}/man/man5/ROLLBACK_PREPARED.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TEXT_SEARCH_TEMPLATE.5sql
%{_prefix}/%{major_version}/man/man5/RELEASE_SAVEPOINT.5sql
%{_prefix}/%{major_version}/man/man5/DROP_SERVER.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TABLESPACE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_VIEW.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TYPE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_DOMAIN.5sql
%{_prefix}/%{major_version}/man/man5/DROP_TEXT_SEARCH_CONFIGURATION.5sql
%{_prefix}/%{major_version}/man/man5/INSERT.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_USER.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TEXT_SEARCH_DICTIONARY.5sql
%{_prefix}/%{major_version}/man/man5/SELECT.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TEXT_SEARCH_CONFIGURATION.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_LANGUAGE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_LANGUAGE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TEXT_SEARCH_CONFIGURATION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_DATABASE.5sql
%{_prefix}/%{major_version}/man/man5/DEALLOCATE.5sql
%{_prefix}/%{major_version}/man/man5/REINDEX.5sql
%{_prefix}/%{major_version}/man/man5/ROLLBACK.5sql
%{_prefix}/%{major_version}/man/man5/EXECUTE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_FUNCTION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TABLE_AS.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_OPERATOR_CLASS.5sql
%{_prefix}/%{major_version}/man/man5/CHECKPOINT.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_SCHEMA.5sql
%{_prefix}/%{major_version}/man/man5/DROP_ROLE.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_OPERATOR_CLASS.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_OPERATOR_FAMILY.5sql
%{_prefix}/%{major_version}/man/man5/DROP_FOREIGN_DATA_WRAPPER.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_AGGREGATE.5sql
%{_prefix}/%{major_version}/man/man5/SET_TRANSACTION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_SERVER.5sql
%{_prefix}/%{major_version}/man/man5/DROP_RULE.5sql
%{_prefix}/%{major_version}/man/man5/DISCARD.5sql
%{_prefix}/%{major_version}/man/man5/TABLE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_AGGREGATE.5sql
%{_prefix}/%{major_version}/man/man5/FETCH.5sql
%{_prefix}/%{major_version}/man/man5/DROP_INDEX.5sql
%{_prefix}/%{major_version}/man/man5/SET_SESSION_AUTHORIZATION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_SEQUENCE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_GROUP.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_INDEX.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_CONVERSION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TEXT_SEARCH_TEMPLATE.5sql
%{_prefix}/%{major_version}/man/man5/DROP_CONVERSION.5sql
%{_prefix}/%{major_version}/man/man5/CREATE_TRIGGER.5sql
%{_prefix}/%{major_version}/man/man5/END.5sql
%{_prefix}/%{major_version}/man/man5/NOTIFY.5sql
%{_prefix}/%{major_version}/man/man5/DROP_AGGREGATE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_TABLE.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_OPERATOR_FAMILY.5sql
%{_prefix}/%{major_version}/man/man5/MOVE.5sql
%{_prefix}/%{major_version}/man/man5/ROLLBACK_TO_SAVEPOINT.5sql
%{_prefix}/%{major_version}/man/man5/ALTER_ROLE.5sql
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/doc/contrib
%{_prefix}/%{major_version}/doc/contrib/autoinc.example
%{_prefix}/%{major_version}/doc/contrib/insert_username.example
%{_prefix}/%{major_version}/doc/contrib/moddatetime.example
%{_prefix}/%{major_version}/doc/contrib/refint.example
%{_prefix}/%{major_version}/doc/contrib/timetravel.example


%files -n postgres-90-server
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/timezonesets
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%dir %attr (0755, postgres, postgres) %{_var_prefix}
%dir %attr (0755, postgres, postgres) %{_var_prefix}/%{major_version}
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/backups
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data
%dir %attr (0700, postgres, postgres) %{_var_prefix}/%{major_version}/data_64
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/security
%dir %attr (0755, root, sys) /etc/security/auth_attr.d
%dir %attr (0755, root, sys) /etc/security/exec_attr.d
%dir %attr (0755, root, sys) /etc/security/prof_attr.d
%dir %attr (0755, root, sys) /etc/user_attr.d
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/application
%dir %attr (0755, root, sys) /var/svc/manifest/application/database
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hungarian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/hunspell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.affix
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/ispell_sample.dict
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/italian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/norwegian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/portuguese.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/russian.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/spanish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/swedish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/synonym_sample.syn
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/thesaurus_sample.ths
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/turkish.stop
%attr (0555, root, bin) /lib/svc/method/postgres_90
%attr (0644, root, sys) /etc/security/auth_attr.d/service\%2Fdatabase\%2Fpostgres-90
%attr (0644, root, sys) /etc/security/exec_attr.d/service\%2Fdatabase\%2Fpostgres-90
%attr (0644, root, sys) /etc/security/prof_attr.d/service\%2Fdatabase\%2Fpostgres-90
%attr (0644, root, sys) /etc/user_attr.d/service\%2Fdatabase\%2Fpostgres-90
%attr (0444, root, sys) /var/svc/manifest/application/database/postgresql_90.xml
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/initdb
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_controldata
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_ctl
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/pg_resetxlog
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postgres
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/amd64/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/bin/postmaster
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/ascii_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/cyrillic_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/dict_snowball.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_cn_and_mic.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jis_2004_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_jp_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_kr_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc_tw_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin2_and_win1250.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/latin_and_mic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpgsql.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_ascii.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_big5.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_cyrillic.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_cn.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_jp.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_kr.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc_tw.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gb18030.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_gbk.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_iso8859_1.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_johab.so
#%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_shift_jis_2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_uhc.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_win.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/libpqwalreceiver.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_euc2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/utf8_and_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/euc2004_sjis2004.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/plpython2.so
%attr (0555, root, bin) %{_prefix}/%{major_version}/lib/amd64/libpqwalreceiver.so

%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/cs/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/de/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/es/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/fr/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/it/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ja/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ko/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/pt_BR/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/plperl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/plpython-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ro/LC_MESSAGES/pltcl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ru/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/sv/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/ta/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/initdb-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pg_controldata-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pg_ctl-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/pg_resetxlog-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/postgres-%{major_version}.mo
%attr (0644, root, other) %{_prefix}/%{major_version}/share/locale/tr/LC_MESSAGES/plpgsql-%{major_version}.mo
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/conversion_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/information_schema.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_hba.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_ident.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/pg_service.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.bki
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.description
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgres.shdescription
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/postgresql.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/recovery.conf.sample
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/snowball_create.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/sql_features.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/system_views.sql
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Africa.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/America.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Antarctica.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Asia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Atlantic.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Australia.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Default
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Etc.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Europe.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/India
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Indian.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/timezonesets/Pacific.txt
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/danish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/dutch.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/english.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/finnish.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/french.stop
%attr (0444, root, bin) %{_prefix}/%{major_version}/share/tsearch_data/german.stop

%files -n postgres-90-contrib
%defattr (-, root, bin)

%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/bin
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/lib/amd64
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/locale
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share
%dir %attr (0755, root, other) %{_prefix}/%{major_version}/share/contrib
%dir %attr (0755, root, bin) %{_prefix}/%{major_version}/share/tsearch_data
%{_prefix}/%{major_version}/lib/adminpack.so
%{_prefix}/%{major_version}/lib/auto_explain.so
%{_prefix}/%{major_version}/lib/btree_gin.so
%{_prefix}/%{major_version}/lib/btree_gist.so
%{_prefix}/%{major_version}/lib/chkpass.so
%{_prefix}/%{major_version}/lib/citext.so
%{_prefix}/%{major_version}/lib/cube.so
%{_prefix}/%{major_version}/lib/dblink.so
%{_prefix}/%{major_version}/lib/dict_int.so
%{_prefix}/%{major_version}/lib/dict_xsyn.so
%{_prefix}/%{major_version}/lib/earthdistance.so
%{_prefix}/%{major_version}/lib/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/hstore.so
%{_prefix}/%{major_version}/lib/_int.so
%{_prefix}/%{major_version}/lib/isn.so
%{_prefix}/%{major_version}/lib/lo.so
%{_prefix}/%{major_version}/lib/ltree.so
%{_prefix}/%{major_version}/lib/pageinspect.so
%{_prefix}/%{major_version}/lib/passwordcheck.so
%{_prefix}/%{major_version}/lib/pg_buffercache.so
%{_prefix}/%{major_version}/lib/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/pg_trgm.so
%{_prefix}/%{major_version}/lib/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/pgcrypto.so
%{_prefix}/%{major_version}/lib/pgrowlocks.so
%{_prefix}/%{major_version}/lib/pgstattuple.so
%{_prefix}/%{major_version}/lib/seg.so
%{_prefix}/%{major_version}/lib/autoinc.so
%{_prefix}/%{major_version}/lib/insert_username.so
%{_prefix}/%{major_version}/lib/moddatetime.so
%{_prefix}/%{major_version}/lib/refint.so
%{_prefix}/%{major_version}/lib/timetravel.so
%{_prefix}/%{major_version}/lib/tablefunc.so
%{_prefix}/%{major_version}/lib/test_parser.so
%{_prefix}/%{major_version}/lib/tsearch2.so
%{_prefix}/%{major_version}/lib/unaccent.so
%{_prefix}/%{major_version}/lib/sslinfo.so
%{_prefix}/%{major_version}/lib/pgxml.so
%{_prefix}/%{major_version}/lib/amd64/autoinc.so
%{_prefix}/%{major_version}/lib/amd64/adminpack.so
%{_prefix}/%{major_version}/lib/amd64/auto_explain.so
%{_prefix}/%{major_version}/lib/amd64/btree_gin.so
%{_prefix}/%{major_version}/lib/amd64/btree_gist.so
%{_prefix}/%{major_version}/lib/amd64/chkpass.so
%{_prefix}/%{major_version}/lib/amd64/citext.so
%{_prefix}/%{major_version}/lib/amd64/cube.so
%{_prefix}/%{major_version}/lib/amd64/dblink.so
%{_prefix}/%{major_version}/lib/amd64/dict_int.so
%{_prefix}/%{major_version}/lib/amd64/dict_xsyn.so
%{_prefix}/%{major_version}/lib/amd64/earthdistance.so
%{_prefix}/%{major_version}/lib/amd64/fuzzystrmatch.so
%{_prefix}/%{major_version}/lib/amd64/hstore.so
%{_prefix}/%{major_version}/lib/amd64/_int.so
%{_prefix}/%{major_version}/lib/amd64/insert_username.so
%{_prefix}/%{major_version}/lib/amd64/isn.so
%{_prefix}/%{major_version}/lib/amd64/lo.so
%{_prefix}/%{major_version}/lib/amd64/ltree.so
%{_prefix}/%{major_version}/lib/amd64/moddatetime.so
%{_prefix}/%{major_version}/lib/amd64/pageinspect.so
%{_prefix}/%{major_version}/lib/amd64/passwordcheck.so
%{_prefix}/%{major_version}/lib/amd64/pg_buffercache.so
%{_prefix}/%{major_version}/lib/amd64/pg_freespacemap.so
%{_prefix}/%{major_version}/lib/amd64/pg_stat_statements.so
%{_prefix}/%{major_version}/lib/amd64/pg_trgm.so
%{_prefix}/%{major_version}/lib/amd64/pg_upgrade_support.so
%{_prefix}/%{major_version}/lib/amd64/pgcrypto.so
%{_prefix}/%{major_version}/lib/amd64/pgrowlocks.so
%{_prefix}/%{major_version}/lib/amd64/pgstattuple.so
%{_prefix}/%{major_version}/lib/amd64/pgxml.so
%{_prefix}/%{major_version}/lib/amd64/refint.so
%{_prefix}/%{major_version}/lib/amd64/seg.so
%{_prefix}/%{major_version}/lib/amd64/sslinfo.so
%{_prefix}/%{major_version}/lib/amd64/tablefunc.so
%{_prefix}/%{major_version}/lib/amd64/test_parser.so
%{_prefix}/%{major_version}/lib/amd64/timetravel.so
%{_prefix}/%{major_version}/lib/amd64/tsearch2.so
%{_prefix}/%{major_version}/lib/amd64/unaccent.so
%{_prefix}/%{major_version}/share/contrib/uninstall_adminpack.sql
%{_prefix}/%{major_version}/share/contrib/adminpack.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_btree_gin.sql
%{_prefix}/%{major_version}/share/contrib/btree_gin.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_btree_gist.sql
%{_prefix}/%{major_version}/share/contrib/btree_gist.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_chkpass.sql
%{_prefix}/%{major_version}/share/contrib/chkpass.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_citext.sql
%{_prefix}/%{major_version}/share/contrib/citext.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_cube.sql
%{_prefix}/%{major_version}/share/contrib/cube.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_dblink.sql
%{_prefix}/%{major_version}/share/contrib/dblink.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_dict_int.sql
%{_prefix}/%{major_version}/share/contrib/dict_int.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_dict_xsyn.sql
%{_prefix}/%{major_version}/share/contrib/dict_xsyn.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_earthdistance.sql
%{_prefix}/%{major_version}/share/contrib/earthdistance.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_fuzzystrmatch.sql
%{_prefix}/%{major_version}/share/contrib/fuzzystrmatch.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_hstore.sql
%{_prefix}/%{major_version}/share/contrib/hstore.sql
%{_prefix}/%{major_version}/share/contrib/int_aggregate.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_int_aggregate.sql
%{_prefix}/%{major_version}/share/contrib/uninstall__int.sql
%{_prefix}/%{major_version}/share/contrib/_int.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_isn.sql
%{_prefix}/%{major_version}/share/contrib/isn.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_lo.sql
%{_prefix}/%{major_version}/share/contrib/lo.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_ltree.sql
%{_prefix}/%{major_version}/share/contrib/ltree.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pageinspect.sql
%{_prefix}/%{major_version}/share/contrib/pageinspect.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pg_buffercache.sql
%{_prefix}/%{major_version}/share/contrib/pg_buffercache.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pg_freespacemap.sql
%{_prefix}/%{major_version}/share/contrib/pg_freespacemap.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pg_stat_statements.sql
%{_prefix}/%{major_version}/share/contrib/pg_stat_statements.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pg_trgm.sql
%{_prefix}/%{major_version}/share/contrib/pg_trgm.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pgcrypto.sql
%{_prefix}/%{major_version}/share/contrib/pgcrypto.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pgrowlocks.sql
%{_prefix}/%{major_version}/share/contrib/pgrowlocks.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pgstattuple.sql
%{_prefix}/%{major_version}/share/contrib/pgstattuple.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_seg.sql
%{_prefix}/%{major_version}/share/contrib/seg.sql
%{_prefix}/%{major_version}/share/contrib/autoinc.sql
%{_prefix}/%{major_version}/share/contrib/insert_username.sql
%{_prefix}/%{major_version}/share/contrib/moddatetime.sql
%{_prefix}/%{major_version}/share/contrib/refint.sql
%{_prefix}/%{major_version}/share/contrib/timetravel.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_tablefunc.sql
%{_prefix}/%{major_version}/share/contrib/tablefunc.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_test_parser.sql
%{_prefix}/%{major_version}/share/contrib/test_parser.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_tsearch2.sql
%{_prefix}/%{major_version}/share/contrib/tsearch2.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_unaccent.sql
%{_prefix}/%{major_version}/share/contrib/unaccent.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_sslinfo.sql
%{_prefix}/%{major_version}/share/contrib/sslinfo.sql
%{_prefix}/%{major_version}/share/contrib/uninstall_pgxml.sql
%{_prefix}/%{major_version}/share/contrib/pgxml.sql
%{_prefix}/%{major_version}/share/tsearch_data/xsyn_sample.rules
%{_prefix}/%{major_version}/share/tsearch_data/unaccent.rules
%{_prefix}/%{major_version}/bin/oid2name
%{_prefix}/%{major_version}/bin/pg_archivecleanup
%{_prefix}/%{major_version}/bin/pg_standby
%{_prefix}/%{major_version}/bin/pg_upgrade
%{_prefix}/%{major_version}/bin/pgbench
%{_prefix}/%{major_version}/bin/vacuumlo
%{_prefix}/%{major_version}/bin/amd64/oid2name
%{_prefix}/%{major_version}/bin/amd64/pg_archivecleanup
%{_prefix}/%{major_version}/bin/amd64/pg_standby
%{_prefix}/%{major_version}/bin/amd64/pg_upgrade
%{_prefix}/%{major_version}/bin/amd64/pgbench
%{_prefix}/%{major_version}/bin/amd64/vacuumlo

%changelog
* Tue Jan 25 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision
