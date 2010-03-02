#
# spec file for package SFEvorbis-tools
#
# includes module(s): vorbis-tools
#

%include Solaris.inc

%define src_name vorbis-tools

Name:		SFEvorbis-tools
Version:	1.2.0
Release:	1
Summary:	Several Ogg Vorbis Tools

Group:		Applications/Multimedia
License:	GPL
URL:		http://xiph.org/
Vendor:		Xiph.Org Foundation <team@xiph.org>
Source:         http://downloads.xiph.org/releases/vorbis/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

Requires:       SUNWogg-vorbis
BuildRequires:	SUNWogg-vorbis-devel
Requires:       SUNWflac
BuildRequires:	SUNWflac-devel
Requires:       SUNWspeex
BuildRequires:	SUNWspeex-devel
Requires:       SFElibao
BuildRequires:	SFElibao-devel
Requires:       SUNWcurl
BuildRequires:	SUNWcurl

%description
vorbis-tools contains oggenc (an encoder) and ogg123 (a playback tool).
It also has vorbiscomment (to add comments to Vorbis files), ogginfo (to
give all useful information about an Ogg file, including streams in it),
oggdec (a simple command line decoder), and vcut (which allows you to 
cut up Vorbis files).

%prep
%setup -q -n %{src_name}-%{version}

%build
export CFLAGS="%optflags"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --enable-vcut
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%doc COPYING
%doc README
%{_bindir}/oggenc
%{_bindir}/oggdec
%{_bindir}/ogg123
%{_bindir}/ogginfo
%{_bindir}/vorbiscomment
%{_bindir}/vcut
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/ogg123.1*
%{_mandir}/man1/oggenc.1*
%{_mandir}/man1/oggdec.1*
%{_mandir}/man1/ogginfo.1*
%{_mandir}/man1/vorbiscomment.1*
%{_mandir}/man1/vcut.1*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/{%src_name}-{%version}/ogg123rc-example
%attr (-, root, other) %{_datadir}/locale


%changelog
* Tue Mar 02 2010 Milan Jurik
- SFE port
* Tue Jan 25 2008 Ivo Emanuel Goncalves <justivo@gmail.com>
- update for 1.2.0 release
* Tue Oct 07 2003 Warren Dukes <shank@xiph.org>
- update for 1.0.1 release
* Fri Jul 19 2002 Michael Smith <msmith@xiph.org>
- Added oggdec and oggdec manpage.
* Sun Jul 14 2002 Thomas Vander Stichele <thomas@apestaart.org>
- updated for 1.0 release
- added vcut, vcut man and vorbiscomment man
- added LC_MESSAGES
- removed libogg and libogg-devel from requires since libvorbis pulls that in
* Fri Jul 12 2002 Michael Smith <msmith@xiph.org>
- Version number updates for 1.0 release.
* Fri May 23 2002 Thomas Vander Stichele <thomas@apestaart.org>
- Added more BuildRequires: for obvious packages
* Fri Mar 22 2002 Jack Moffitt <jack@xiph.org>
- Update curl dependency info (Closes bug #130)
* Mon Dec 31 2001 Jack Moffitt <jack@xiph.org>
- Update for rc3 release.
* Sun Oct 07 2001 Jack Moffitt <jack@xiph.org>
- Updated for configurable prefix
* Sun Aug 12 2001 Greg Maxwell <greg@linuxpower.cx>
- updated for rc2
* Sun Jun 17 2001 Jack Moffitt <jack@icecast.org>
- updated for rc1
- added ogginfo
* Mon Jan 22 2001 Jack Moffitt <jack@icecast.org>
- updated for prebeta4 builds
* Sun Oct 29 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
