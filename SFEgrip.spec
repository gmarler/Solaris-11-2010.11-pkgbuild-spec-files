#
# spec file for package SFEgrip
#

%include Solaris.inc
Name:                    SFEgrip
Summary:                 Cd-player and cd-ripper for the Gnome desktop
URL:                     http://nostatic.org/grip/
Version:                 3.3.1
Source:                  %{sf_download}/grip/grip-%{version}.tar.gz
Patch1:			 grip-01-i386.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWcurl
Requires:      SUNWcurl
BuildRequires: SUNWfontconfig
Requires:      SUNWfontconfig
BuildRequires: SUNWfreetype2
Requires:      SUNWfreetype2
BuildRequires: SUNWgnome-base-libs-devel
Requires:      SUNWgnome-base-libs
BuildRequires: SUNWgnome-component-devel
Requires:      SUNWgnome-component
BuildRequires: SUNWgnome-config-devel
Requires:      SUNWgnome-config
BuildRequires: SUNWgnome-libs-devel
Requires:      SUNWgnome-libs
BuildRequires: SUNWgnome-terminal-devel
Requires:      SUNWgnome-terminal
BuildRequires: SUNWgnome-vfs-devel
Requires:      SUNWgnome-vfs
BuildRequires: SUNWgnu-idn
Requires:      SUNWgnu-idn
Requires:      SUNWgss
Requires:      SUNWlibmsr
BuildRequires: SUNWlibpopt-devel
Requires:      SUNWlibpopt
BuildRequires: SUNWmlibe
BuildRequires: SUNWmlibh
Requires:      SUNWmlib
BuildRequires: SUNWopenssl-include
Requires:      SUNWopensslr
Requires:      SUNWxorg-clientlibs
Requires:      SUNWxwice
Requires:      SUNWxwplt
BuildRequires: SUNWxwxft
Requires:      SUNWxwxft
BuildRequires: SUNWzlib
Requires:      SUNWzlibr

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n grip-%version
%patch1 -p1

%build
export LDFLAGS="-lX11"
./configure --prefix=%{_prefix} --disable-shared-cdpar --disable-shared-id3
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
# Rename pl_PL dir to pl as pl_PL is a symlink to pl and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv pl_PL pl
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/grip
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/grip.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/grip
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png
%dir %attr (0755, root, other) %{_docdir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Mon Feb 25 2009 - Thomas Wagner
- fix permission problem with newer pkgbuild (honouring %doc)
- add dependencies
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix broken spec
* Thu July 24 2008 - jijun.yu@sun.com
- Modify the dependency's name.
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Rename pl_PL dir to pl in %install as pl_PL is a symlink to pl and causing
  installation problems as a dir.
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Correct %files perms and add l10n package for l10n.
* Fri Mar 16 2007  - irene.huang@sun.com
- created
