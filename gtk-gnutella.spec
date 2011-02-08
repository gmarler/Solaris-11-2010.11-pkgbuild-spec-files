#
# spec file for package: gtk-gnutella
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): NONE
#

%include Solaris.inc

%define short_name gtk-gnutella

Name:           SFE%{short_name}
Summary:        Gtk-Gnutella - Graphical Gnutella Client
Version:        0.96.8
License:        GPLv2
URL:            http://gtk-gnutella.sourceforge.net/
Source:         http://downloads.sourceforge.net/project/%{short_name}/%{short_name}/%{version}/%{short_name}-%{version}.tar.bz2
Distribution:   OpenSolaris
Vendor:		      OpenSolaris Community
BuildRoot:      %{_tmppath}/%{short_name}-%{version}-build
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: %{short_name}.copyright

%include default-depend.inc

# Very likely that OpenSolaris only supports GTK v2 anyway...
%define gtkver 2

#
# BuildRequires: (configuration/compile time requirements)
#
BuildRequires:    SUNWbtool
BuildRequires:    SUNWgcc
BuildRequires:    SUNWgnu-coreutils
BuildRequires:    SUNWxwinc
BuildRequires:    SUNWxorg-headers
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWgnome-base-libs
BuildRequires:    SUNWfreetype2
BuildRequires:    SUNWfontconfig
BuildRequires:    SUNWlxml
BuildRequires:    SUNWdbus-libs
BuildRequires:    SUNWgnutls
BuildRequires:    SUNWzlib
BuildRequires:    SUNWpixman
BuildRequires:    SUNWpng
BuildRequires:    SUNWgmake
#
# Requires: (runtime requirements)
#
Requires:         SUNWcsl
Requires:         SUNWgnome-base-libs
Requires:         SUNWlibms
Requires:         SUNWmlib
Requires:         SUNWxwplt
Requires:         SUNWxorg-clientlibs
Requires:         SUNWfreetype2
Requires:         SUNWfontconfig
Requires:         SUNWlxml
Requires:         SUNWdbus-libs
Requires:         SUNWgnutls
Requires:         SUNWzlib
Requires:         SUNWpixman
Requires:         SUNWpng
Requires:         SUNWlexpt
Requires:         SUNWlibgcrypt
Requires:         SUNWlibtasn1
Requires:         SUNWlibgpg-error


%description
gtk-gnutella is a GUI based Gnutella p2p servent. It's a fully featured  
servent designed to share any type of file.  gtk-gnutella implements 
compressed gnutella net connections, ultrapeer and leaf nodes and uses 
Passive/Active Remote Queueing (PARQ) and other modern gnutella network
features.

%prep
rm -rf %{short_name}-%{version}
#mkdir %{short_name}-%{version}
#cd %{_builddir}/%{short_name}-%{version}

%setup -n %{short_name}-%{version}

%build
CPUS=$(/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' ')
if [[ -z "$CPUS" || "$CPUS" == "0" ]]; then
  CPUS=1
fi 

# Pity, seems like the configuration script is gcc specific
MAKE=/bin/gmake \
./build.sh \
          --gtk%{gtkver} \
          --prefix=%{_prefix} \
          --bindir=%{_bindir} \
          --datadir=%{_datadir}/%{short_name} \
          --mandir=%{_mandir}/man1 \
          --cc=gcc \
          --ldflags="-lnsl -lsocket" \
          --configure-only

(( $? != 0 )) && exit 1  # Early exit error

/bin/gmake -j${CPUS}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -d -m 755 $RPM_BUILD_ROOT/%{_bindir}
%{__make} install INSTALL_PREFIX=$RPM_BUILD_ROOT
%{__install} -d -m 755 $RPM_BUILD_ROOT/%{_mandir}/man1
%{__make} install.man INSTALL_PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

#
# NOT SURE HOW TO GET THESE WORKING FOR IPS
#Tha
#%post
#%restart_fmri desktop-mime-cache gconf-cache

#%postun
#%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%doc README TODO AUTHORS ChangeLog LICENSE
%dir %attr(0755, root, bin) %{_bindir}
%attr(0555, root, bin) %{_bindir}/*

%dir %attr(0755, root, other) %{_prefix}/share/locale

%dir %attr(0755, root, other) %{_prefix}/share/locale/de
%dir %attr(0755, root, other) %{_prefix}/share/locale/de/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/el
%dir %attr(0755, root, other) %{_prefix}/share/locale/el/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/hu
%dir %attr(0755, root, other) %{_prefix}/share/locale/hu/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/es
%dir %attr(0755, root, other) %{_prefix}/share/locale/es/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/nb
%dir %attr(0755, root, other) %{_prefix}/share/locale/nb/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/fr
%dir %attr(0755, root, other) %{_prefix}/share/locale/fr/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/zh_CN
%dir %attr(0755, root, other) %{_prefix}/share/locale/zh_CN/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/nl
%dir %attr(0755, root, other) %{_prefix}/share/locale/nl/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/uk
%dir %attr(0755, root, other) %{_prefix}/share/locale/uk/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/ja
%dir %attr(0755, root, other) %{_prefix}/share/locale/ja/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/tr
%dir %attr(0755, root, other) %{_prefix}/share/locale/tr/LC_MESSAGES
%dir %attr(0755, root, other) %{_prefix}/share/locale/it
%dir %attr(0755, root, other) %{_prefix}/share/locale/it/LC_MESSAGES
%attr(0444, root, other) %{_prefix}/share/locale/de/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/el/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/hu/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/es/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/nb/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/fr/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/zh_CN/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/nl/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/uk/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/ja/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/tr/LC_MESSAGES/*
%attr(0444, root, other) %{_prefix}/share/locale/it/LC_MESSAGES/*

%dir %attr(0755, root, bin) %{_mandir}
%attr(0444, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_prefix}/share/%{short_name}
%attr(0444, root, other) %{_prefix}/share/%{short_name}/*.txt
%attr(0444, root, other) %{_prefix}/share/%{short_name}/*.png
%dir %attr(0755, root, other) %{_prefix}/share/%{short_name}/en
%attr(0444, root, other) %{_prefix}/share/%{short_name}/en/FAQ
%dir %attr(0755, root, other) %{_prefix}/share/%{short_name}/ja
%attr(0444, root, other) %{_prefix}/share/%{short_name}/ja/FAQ
%dir %attr(0755, root, other) %{_prefix}/share/%{short_name}/el
%attr(0444, root, other) %{_prefix}/share/%{short_name}/el/FAQ
%dir %attr(0755, root, bin) %{_prefix}/share/%{short_name}/pixmaps
%attr(0444, root, bin) %{_prefix}/share/%{short_name}/pixmaps/*
%dir %attr(0755, root, other) %{_prefix}/share/applications
%attr(0444, root, bin) %{_prefix}/share/applications/*
%dir %attr(0755, root, other) %{_prefix}/share/pixmaps
%attr(0444, root, bin) %{_prefix}/share/pixmaps/*

%changelog
* Fri Feb 04, 2011 - gmarler@gmarler.com
- Use new S11 Express naming scheme
- use of short_name
* Thu Aug 27 - gmarler@gmarler.com
Initial spec file, all %files directives
Fix Source location
* Thu Aug 28 - gmarler@gmarler.com
Add entries for %{_prefix}/share/pixmaps/
Fix several dir perms so we won't have conflicts with other packages
Fix locale dir perms
Properly compute the number of CPUs for building, and use in gmake invocation
* Tue Sep 1 - gmarler@gmarler.com
Add Requires runtime packages
Add all remaining BuildRequires statements
Substitute %{name} and %{version} where appropriate
* Wed Sep 2 - gmarler@gmarler.com
Fix line endings from DOS to Unix
* Thu Sep 3 - gmarler@gmarler.com
add changelog back in
Eliminate Group field
Fix Meta(info.classification) field
## Re-build 24/09/09
