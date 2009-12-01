#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:		SFElynx
Summary:	Text mode browser
Version:	2.8.6
Source:		http://lynx.isc.org/lynx%{version}/lynx%{version}.tar.bz2
Patch1:		lynx-01-color.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SFEncurses
Requires:	SUNWopenssl-libraries
Requires:   SUNWbzip
Requires:   SUNWzlib
BuildRequires:	SFEncurses-devel
BuildRequires:	SUNWopenssl-include


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n lynx2-8-6
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include -I/usr/sfw/include"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir}	\
	    --with-ssl			\
	    --with-screen=ncurses	\
	    --enable-color-style	\
	    --enable-scrollbar		\
	    --enable-nested-tables	\
	    --with-bzlib		\
	    --with-zlib

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun Sep 16 2007 - trisk@acm.jhu.edu
- Fix LDFLAGS
* Sat May 26 2007 - Thomas Wagner
- version bump to 2.8.6, new download-URL since not in /current/-diry
* Fri Apr 20 2007 - Doug Scott
- Initial spec
