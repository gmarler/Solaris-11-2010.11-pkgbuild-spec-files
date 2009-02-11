#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEsamba4
Summary:             samba - CIFS Server and Domain Controller v4
Version:             4.0.0
Source:              http://us5.samba.org/samba/ftp/samba4/samba-4.0.0alpha6.tar.gz
Patch1:              samba4-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -n samba-4.0.0alpha6/
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
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
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}
%{_datadir}/perl5/*
%{_datadir}/samba/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) /var
%dir %attr (0775, root, other) /var/lib
%dir %attr (0775, root, sys) /var/lib/samba/private
%dir %attr (0775, root, sys) /var/lib/samba/private/tls
%dir %attr (0755, root, sys) /var/log
%dir %attr (0775, root, sys) /var/log/samba

%changelog
* Tue Feb 11 2009 - jedy.wang@sun.com
- Initial spec
