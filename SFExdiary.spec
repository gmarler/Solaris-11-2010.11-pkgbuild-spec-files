#
# spec file for package: SFExdiary.spec
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): xdiary


# XXX: KNOWN ISSUES:
#  *** EXTRA_DEFINES doesn't seem to be getting passed to the Makefile
#      when you run xmkmf.
#  *** Program's about box reports version 3.0.1. (Not really a bug...)

%include Solaris.inc

Name:              SFExdiary
Summary:           xdiary - Personal Organizer
Version:           3.0.3
URL:               http://ftp.x.org/contrib/office/
Source:            http://ftp.x.org/contrib/office/xmdiary-%{version}.tar.gz
Patch1:            xdiary-01-tmpl.diff
Patch2:            xdiary-02-fixups.diff
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
License:           Public Domain
SUNW_Copyright:    %{name}.copyright
Distribution:      OpenSolaris
Vendor:            OpenSolaris Community

# OpenSolaris IPS Manifest Fields
Meta(info.upstream):            Roger Larsson <llg@ubszh.net.ch>
Meta(info.maintainer):          Matt Lewandowsky <matt@greenviolet.net>
Meta(info.classification):      org.opensolaris.category.2008:System/X11

%include default-depend.inc

BuildRequires: SUNWscpu
Requires:      SUNWmfrun

%description
XDiary is your personal organizer that combines the functions of 
a desktop calendar, an appointment book and an alarm clock. XDiary 
will help you keep track of your meetings, appointments and plan 
your time.

XDiary is a Motif/X Windows application which allows you to manage 
one or more calendars with a 'few clicks with the mouse'.

XDiary can be used as a stand-alone tool but it also contains all 
the functions necessary to be used as a group calendar. As a group 
calendar, XDiary will help you to plan meetings, distribute information 
to specific groups etc.

%prep
%setup -q -n xmdiary-%version
%patch1
%patch2

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
xmkmf -a
make includes
make depend
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install.man
rmdir $RPM_BUILD_ROOT/usr/include

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xdalarm
%{_bindir}/xddump
%{_bindir}/xdinitdb
%{_bindir}/xdlocation
%{_bindir}/xdprformat
%{_bindir}/xdremind
%{_bindir}/xdremove
%{_bindir}/xdaclunix
%{_bindir}/xdcustom
%{_bindir}/xdiary
%{_bindir}/xdlight
%{_bindir}/xdnotify
%{_bindir}/xdprint
%{_bindir}/xdremote
%{_bindir}/xdrestore
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/libTools.a
%{_libdir}/libXdiary.a
%{_libdir}/libXdndbm.a
%{_libdir}/libXtools.a
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/XDiary
%{_datadir}/X11/app-defaults/XDiary.map
%dir %attr(0755, root, sys) %{_datadir}/xdiary
%attr(-, root, sys) %{_datadir}/xdiary/*
%attr(-, root, bin) %{_mandir}/man1


%changelog
* Wed Apr 28 2010 - Matt Lewandowsky <matt@greenviolet.net>
- Initial spec file.
