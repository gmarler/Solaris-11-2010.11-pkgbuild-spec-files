#
# spec file for package SFEpidgin-facebookchat
#

%include Solaris.inc

Name:                    SFEtwitux
Summary:                 Follow tweets
Group:                   Network/InstantMessaging
Version:                 0.69
Source:                  http://ufpr.dl.sourceforge.net/sourceforge/twitux/twitux-%{version}.tar.bz2 
BuildRoot:               %{_tmppath}/%{name}-%{version}
Patch1:			 patches/twitux-01-locale.diff
SUNW_Copyright:          %{name}.copyright

%include default-depend.inc

Requires:    SUNWgnome-libs
BuildRequires:    SUNWgnome-common-devel

%prep
%setup -q -n twitux-%{version}
%patch1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export LDFLAGS="%_ldflags"
export LIBTWITUX_LIBS="-R/usr/X11/lib -R/lib -L/usr/X11/lib -L/lib -lxml2 -lgtk-x11-2.0 -lgdk-x11-2.0 -lXi -lXext -lX11 -latk-1.0 -lpangoft2-1.0 -lgdk_pixbuf-2.0 -lm -lmlib -lpangocairo-1.0 -lgio-2.0 -lXrandr -lXcursor -lXcomposite -lXdamage -lcairo -lXfixes -lpango-1.0 -lfreetype -lfontconfig -lgmodule-2.0 -lgobject-2.0 -lgconf-2 -lgnome-keyring -lglib-2.0 -lgthread-2.0"


./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
	    --includedir=%{_includedir}	\
	    --mandir=%{_mandir} 	\
	    --infodir=%{_infodir}	\
	    --sysconfdir=%{_sysconfdir}

make -j $CPUS



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %{_datadir}/gnome/help
%dir %{_datadir}/omf
%defattr (-, root, sys)
%dir /usr
%dir /usr/share
%{_sysconfdir}
%defattr (-, root, other)
%{_datadir}/applications/twitux.desktop
%{_datadir}/gnome/help/twitux
%{_datadir}/icons/hicolor/48x48/apps/twitux.png
%{_datadir}/icons/hicolor/scalable/apps/twitux.svg
%{_datadir}/locale/de/LC_MESSAGES/twitux.mo
%{_datadir}/locale/es/LC_MESSAGES/twitux.mo
%{_datadir}/locale/fr/LC_MESSAGES/twitux.mo
%{_datadir}/locale/ja/LC_MESSAGES/twitux.mo
%{_datadir}/locale/pt/LC_MESSAGES/twitux.mo
%{_datadir}/locale/sv/LC_MESSAGES/twitux.mo
%{_datadir}/omf/twitux
%{_datadir}/twitux

%changelog
* Fri Jan 31 2009 - Sergio Schvezov <sergiusens@ieee.org>
- Initial spec
