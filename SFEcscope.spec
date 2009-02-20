#
# spec file for package SFEcscope
#
# includes module(s): cscope
#
%include Solaris.inc

Name:                    SFEcscope
License:                 BSD
Summary:                 Cscope - interactive source code examiner
Version:                 15.7
Source:                  %{sf_download}/cscope/cscope-%{version}.tar.bz2
URL:                     http://cscope.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildConflicts:      SPROsslnk
BuildRequires:       SUNWbison
BuildRequires:       SUNWncurses-devel
Requires:            SUNWncurses
Requires:            SFEctags

%prep
%setup -q -n cscope-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/include/ncurses"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}
	    
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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Fri Feb 20 2009 - halton.huo@sun.com
- Bump to 15.7
- Add ncurses dependency.
* Sat Feb 02 2008 - moinak.ghosh@sun.com
- Slight tweaks and add dependency on ctags and bison.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added BuildConflicts: SPROsslnk
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Bump to 15.6.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEcscope
- update file attributes to match JDS
- delete -share subpkg
* Tue Nov 29 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
