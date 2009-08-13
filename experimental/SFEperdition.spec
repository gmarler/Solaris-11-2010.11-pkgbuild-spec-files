
# spec file for package SFEperdition

##TODO## add database modules, unisodbc, postgres, mysql, gdbm, others ...

##TODO## migrate the pam settings from the file /etc/perdition/pam.d/perdition over to /etc/pam.conf to the format used in Solaris

%define src_name perdition
%define perditionparentversion 1.17.1

%include Solaris.inc

Name:                    SFEperdition
Summary:                 perdition - POP3/IMAP proxy to route requests based on tables (migrations, server grouping, load balancing)
URL:                     http://www.vergenet.net/linux/perdition/
Version:                 %{perditionparentversion}
Source:                  http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/perdition-%{version}.tar.gz
Patch1:			perdition-01-Makefile_in_am-LDFLAGS.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFElibvanessa-logger
Requires: SFElibvanessa-adt
Requires: SFElibvanessa-socket
BuildRequires: SFElibvanessa-logger
Requires: SFElibvanessa-adt
Requires: SFElibvanessa-socket

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"

export LDFLAGS="%{_ldflags}"

#from perdition.spec (source tarball)
aclocal
libtoolize --force --copy
autoheader
automake
autoconf

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --disable-static     \
            --disable-odbc

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT 

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/perdition.imaps
%{_sbindir}/perdition.pop3s
%{_sbindir}/perdition.imap4s
%{_sbindir}/perdition.imap4
%{_sbindir}/perdition.pop3
%{_sbindir}/perdition
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

##TODO## below: /etc/perdition/pam.d/perdition not in Solaris format and location
%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*

%changelog
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
