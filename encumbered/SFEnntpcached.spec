#
# spec file for package SFEnntpcache
#
# includes module(s): nntpcache
#
%include Solaris.inc

#TODO# if possible, solve the automake/* stuff - to have Makefile.am patchable
#TODO# move cp sysconf/*dist syscon/* into postinstall class action script and mark as editable

%define	src_name nntpcache
#%define	src_url	ftp://ftp.nntpcache.com/pub/nntpcache
%define	src_url	http://fresh.t-systems-sfr.com/unix/src/privat2

Name:                SFEnntpcache
License:		Other (read License carefully)
Summary:             nntpcache daemon - not sure if actively maintened
Version:             3.0.2
#Source:              %{src_url}/%{src_name}.tar.gz
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     nntpcache-01-3.0.2_3.0.2a_gn_s11_pointer.diff
Patch5:		     nntpcache-05-Makefile.in_DESTDIR.diff
Patch6:		     nntpcache-06-list.h.diff
Patch7:			nntpcache-07-list.c.diff
Patch8:			nntpcache-08-libproff.h.diff
Patch9:			nntpcache-09-list.ext.diff
#Patch10:		nntpcache-10-Makefile.am_debuginstall.diff 
Patch11:		nntpcache-11-Makefile.in_debuginstall.diff 


SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q  -n %{src_name}-%{version}
%patch1 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
#%patch10 -p1
%patch11 -p1

mv libproff/list.h libproff/nn_list.h

#TODO# is this the right thing to do?
# perl -w -pi.bak_nn_list.h -e "s/list.h/nn_list.h/g" libproff/Makefile.in libproff/Makefile.am

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

#aclocal
#automake

./configure --prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir}              \
	--libexecdir=%{_prefix}/%{src_name}/libexec      \
	--sysconfdir=%{_sysconfdir}      \
        --localstatedir=%{_localstatedir}/%{src_name} \

#	--libexecdir=%{_libexecdir}      \

make

%install
rm -rf $RPM_BUILD_ROOT

#mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/nntpcache/
make install DESTDIR=$RPM_BUILD_ROOT

#clean unwanted files
rm -r $RPM_BUILD_ROOT/%{_prefix}/include


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/%{src_name}
%dir %attr (0755, root, bin) %{_prefix}/%{src_name}/libexec
%{_prefix}/%{src_name}/libexec/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/nntpcache
%{_sysconfdir}/nntpcache/*
#TODO# mark this as volatile /var/nntpache/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/%{src_name}
%{_localstatedir}/%{src_name}/*
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/*


%changelog
* Sat Mai 02 2009 - Thomas Wagner
- add SMF manifest for auto-start
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Added a missing pathname to files section
* Sat Nov 24 2007 - Thomas Wagner
- Initial spec
- list.h from system is included, names/struct redefine errors
