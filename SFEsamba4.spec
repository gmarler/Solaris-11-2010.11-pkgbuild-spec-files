#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define source_name samba-4.0.0alpha11

Name:                SFEsamba4
Summary:             samba - CIFS Server and Domain Controller v4
Version:             4.0.0
Source:              http://us5.samba.org/samba/ftp/samba4/%{source_name}.tar.gz

Patch1: samba4-01-create-symbol-link.diff
Patch2: samba4-02-remove-HAVE_IMMEDIATE_STRUCT.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
rm -rf %name-%version
%setup -q -c -n %name-%version
%patch1 -p0
%patch2 -p0


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-g -mt %optflags"
export LDFLAGS="-z ignore %_ldflags"

cd %{source_name}/source4
./autogen.sh
./configure.developer \
            --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir}	\
            --enable-debug \
            --enable-fhs \
            --enable-static=no

gmake idl_full && gmake

%install
rm -rf $RPM_BUILD_ROOT

cd %{source_name}/source4

gmake install DESTDIR=$RPM_BUILD_ROOT

rmdir $RPM_BUILD_ROOT/var/run/samba
rmdir $RPM_BUILD_ROOT/var/run

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

#The files whose name is with "cn=" have problem.
find $RPM_BUILD_ROOT -type f -name "cn=replicator.ldif" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "cn=samba-admin.ldif" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "cn=samba.ldif" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%{_libdir}/python2.6
%{_libdir}/5.8.4
%{_libdir}/i86pc-solaris-64int
%{_libdir}/samba
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/perl5/*
%{_datadir}/samba/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, other) /var/lib
%dir %attr (0775, root, sys) /var/lib/samba/private
%dir %attr (0775, root, sys) /var/lib/samba/private/tls
%dir %attr (0755, root, sys) /var/log
%dir %attr (0775, root, sys) /var/log/samba

%changelog
* Tue Mar 16 2010 - brian.lu@sun.com
- Add patches: samba4-01-create-symbol-link.diff
  and samba4-02-remove-HAVE_IMMEDIATE_STRUCT.diff 
* Sat Mar 13 2010 - brian.lu@sun.com
- Build samba4 under SUNWsamba4-4.0.0 directory
* Wed Dec 02 2009 - brian.lu@sun.com
- Bump to Samba4 alpha9
* Thu Nov 19 2009 - brian.lu@sun.com
- Add patch samba4-03-checking-suncc.diff
* Thu Aug 27 2009 - brian.lu@sun.com
- Add "-mt" to CFLAGS to set errno correctly in MT environment
* Thu Jun 04 2009 - brian.lu@sun.com
- Remove patch samba4-03-FUNCTION-macro.diff
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fix file attribute problem of /usr/lib/*.
* Tue Feb 11 2009 - jedy.wang@sun.com
- Fix file attribute problem of /usr/share.
* Tue Feb 11 2009 - jedy.wang@sun.com
- Initial spec
