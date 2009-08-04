#
# spec file for package SFEemacs
#
# includes module(s): GNU emacs
#
%include Solaris.inc

Name:                    SFEemacs
Summary:                 GNU Emacs - an operating system in a text editor
Version:                 23.1
%define emacs_version    23.1
Source:                  http://ftp.gnu.org/pub/gnu/emacs/emacs-%{emacs_version}.tar.gz
URL:                     http://www.gnu.org/software/emacs/emacs.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define _with_gtk 1

Requires: SUNWTiff
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWperl584core
Requires: SUNWtexi
Requires: SUNWdbus                                                                                                                                                        
Requires: %{name}-root
%if %{?_with_gtk:1}%{?!_with_gtk}
%define toolkit gtk
Requires: SUNWgtk2                                                                                                                                                                 
Requires: SUNWglib2
Requires: SUNWcairo
%else
%define toolkit motif
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
%endif

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n emacs-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPP="cc -E -Xs"
export CFLAGS='-i -xO3 -xspace -xstrconst -xpentium -mr -xregs=no%frameptr '
export PERL=/usr/perl5/bin/perl

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --without-sound                  \
            --localstatedir=%{_localstatedir}   \
            --with-gif=no \
            --with-x-toolkit=%toolkit \
            --enable-python \
            --enable-font-backend \
            --with-xft \
            --with-freetype

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
        infodir=$RPM_BUILD_ROOT%{_infodir} \
        localstatedir=$RPM_BUILD_ROOT%{_localstatedir}

rm -f $RPM_BUILD_ROOT%{_bindir}/ctags
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/emacs
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/emacs.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/emacs/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%attr (0755, root, bin) %{_infodir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/games
%dir %attr (0755, root, sys) %{_localstatedir}/games/emacs
%{_localstatedir}/games/emacs/*

%changelog
* Tue Aug 04 2009 - jedy.wang@sun.com
- Bump to 23.1
* Thu Oct 2 2008 - markwright@internode.on.net
- Bump to 22.3
* Wed Oct 17 2007 - laca@sun.com
- change /var/games owner to root:bin to match Maelstrom
* Tue Oct 16 2007 - laca@sun.com
- enable building with gtk if the --with-gtk build option is used (default
  remains motif)
- disable sound support (alsa breaks the build currently)
* Wed Jul 24 2007 - markwright@internode.on.net
- Bump to 22.1, change CPP="cc -E -Xs", add --with-gcc=no --with-x-toolkit=motif, add %{_localstatedir}/games/emacs.
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEemacs
- add missing deps
* Wed Oct 12 2005 - laca@sun.com
- create
