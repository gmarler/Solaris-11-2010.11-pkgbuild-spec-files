
# spec file for package SFEperdition

# NOTE version bumpers:  if SFEperdition does not compile well, you *might* have missed updates
#                        to the necessary SFElibvanessa-* tools !!!
#                        go uninstall the old ones first: pkgtool uninstall-pkgs SFElibvanessa-*

# NOTE version bumpers:  change the base version number in the *include* file here:
#                           include/perditionparentversion.inc

# help needed:
##TODO## add database modules, unisodbc, postgres, mysql, gdbm, others ...

##TODO## migrate the pam settings from the file /etc/perdition/pam.d/perdition over to /etc/pam.conf to the format used in Solaris - is this correct?

##TODO## might love a refresh of the patch1 for the more recent Makefile.am/Makefile.in

%define src_name perdition

#set the base version number (->download dir libvanessa-* and ->perdition version)
%include perditionparentversion.inc

%define src_version %{perditionparentversion}

#be carefull with setting IPS_component_version to a valid numeric setting!!!
#make the string 1.19-rc1 reading 1.19.0.1 or forget about it and change nothing
IPS_component_version: $( echo %{perditionparentversion} | sed -e '/-rc[0-9][0-9]*/ s/-rc/.0./' )




%include Solaris.inc

#%define cc_is_gcc 1
#%define _gpp /usr/sfw/bin/g++
#%include base.inc


Name:                    SFEperdition
Summary:                 perdition - POP3/IMAP proxy to route requests based on tables (migrations, server grouping, load balancing)
URL:                     http://www.vergenet.net/linux/perdition/
#remember: version is set for all required specs in the include file 
#include/perditionparentversion.inc
Version:                 %{src_version}
Source:                  http://www.vergenet.net/linux/perdition/download/%{src_version}/perdition-%{version}.tar.gz
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
##TODO## Add buildrequires to mysql (optional Requires mysql)
##TODO## parametrize path to mysql/version.version

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

export LDFLAGS="%{_ldflags} -lsocket -lxnet"

#spyed on perdition.spec (from source tarball)
aclocal
libtoolize --force --copy
autoheader
automake
autoconf

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --disable-static     \
            --disable-odbc       \
            --with-mysql-includes=/usr/mysql/5.1/include/mysql \
            --with-mysql-libraries=/usr/mysql/5.1/lib


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
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*
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
* Fri Jul  9 2010 - Thomas Wagner
- missing symbol inet_*, add to LDFLAGS (-lsocket) -lxnet 
- automate IPS version numbers if you insist on using release candidates
  like 1.19-rc1 -> 1.19.0.1 is then the automatic IPS version number
- experimental add mysql (does this work at the moment, I think not)
* Fri Jul  9 2010 - Thomas Wagner
- bump to 1.18
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
