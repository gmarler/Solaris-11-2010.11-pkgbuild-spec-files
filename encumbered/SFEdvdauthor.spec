#
# spec file for package SFEdvdauthor
#
# includes module(s): SFEdvdauthor
#
%include Solaris.inc

Name:                    SFEdvdauthor
Summary:                 dvdauthor a program that will generate a DVD movie
Version:                 0.6.14
Source:                  %{sf_download}/dvdauthor/dvdauthor-%{version}.tar.gz
Patch2:			 dvdauthor-02-wall.diff
Patch4:                  dvdauthor-04-decl.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel

%prep
%setup -q -n dvdauthor-%version
%patch2 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

LDFLAGS="-L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib:/usr/sfw/lib" \
CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Aug 21 2009 - Milan Jurik
- update to 0.6.14
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
