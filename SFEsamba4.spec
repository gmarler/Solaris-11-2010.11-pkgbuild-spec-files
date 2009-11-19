#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEsamba4
Summary:             samba - CIFS Server and Domain Controller v4
Version:             4.0.0
Source:              http://us5.samba.org/samba/ftp/samba4/samba-4.0.0alpha7.tar.gz
Patch1:              samba4-01-solaris.diff
Patch2:              samba4-02-map-rename.diff
Patch3:              samba4-03-checking-suncc.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -n samba-4.0.0alpha7/
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
export CFLAGS="-g -mt"
export LDFLAGS="%_ldflags"

cd source4/
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

cd source4/
gmake install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT/%{_libdir}
ln -s -f libdcerpc.so.0.0.1 libdcerpc.so.0
ln -s -f libdcerpc_atsvc.so.0.0.1 libdcerpc_atsvc.so.0
ln -s -f libdcerpc_samr.so.0.0.1 libdcerpc_samr.so.0
ln -s -f libgensec.so.0.0.1 libgensec.so.0
ln -s -f libldb.so.0.0.1 libldb.so.0
ln -s -f libndr.so.0.0.1 libndr.so.0
ln -s -f libregistry.so.0.0.1 libregistry.so.0
ln -s -f libsamba-hostconfig.so.0.0.1 libsamba-hostconfig.so.0
ln -s -f libtorture.so.0.0.1 libtorture.so.0
cd -

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
%{_sbindir}/samba
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%{_libdir}/python2.4
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
