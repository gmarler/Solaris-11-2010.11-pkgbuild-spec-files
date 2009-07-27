#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use ncursesw_64 = ncursesw.spec
%endif

%include base.inc
%use ncursesw = ncursesw.spec

Name:                SFEncursesw
Summary:             Emulation of SVR4 curses with wide-character support
Version:             5.6
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWncurses
Requires: SUNWncurses-devel


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%ncursesw_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%ncursesw.prep -d %name-%version/%{base_arch}

%build
if [ "x`basename $CC`" != xgcc ]
then
        FLAG64="-xarch=generic64"
else
        FLAG64="-m64"
fi

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
%ncursesw_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS=
%ncursesw.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%ncursesw_64.install -d %name-%version/%_arch64
# 64-bit binaries are of no benefit
rm -rf $RPM_BUILD_ROOT%{_bindir}/%_arch64
%endif

%ncursesw.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* jul 27 2009 - Gilles Dauphin
- s/SFEncurses/SUNWncurses/
- s/SFEncurses-data/SUNWncurses-devel/
* Sun Aug 10 2008 - andras.barna@gmail.com
- Copied from SFEncurses
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Added proper 64-bit link flags to work with Sun Studio 11 and gcc
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 5.6.  Set LDFLAGS=-m64 for 64 bit build.
* Tue Mar 20 2007 - dougs@truemail.co.th
- Move build to a base spec. Added 64bit build
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
