#
# spec file for package SFEsupertuxkart.spec
#
%include Solaris.inc

%define src_name supertuxkart
%define src_version 0.6.2a

%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)


Name:           SFEsupertuxkart
Version:        0.6.2.0.1
Summary:        Kids 3D go-kart racing game featuring Tux
Group:          Amusements/Games
License:        GPLv2+ and GPLv3 and CC-BY-SA
URL:            http://supertuxkart.sourceforge.net/
Source0:        %{sf_download}/%{src_name}/%{src_name}-%{src_version}-src.tar.bz2
Source2:	%{sf_download}/%{src_name}/addon0.6.1-1.zip
Patch1:		supertuxkart-01-sunstudio.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  SFEplib-devel
BuildRequires:  SUNWlibsdl-devel
BuildRequires:	SFElibmikmod-devel
BuildRequires:  SUNWogg-vorbis
BuildRequires:	SFEfreeglut-devel
BuildRequires:  SFEopenal-devel
BuildRequires:	SFEfreealut-devel
BuildRequires:	SUNWgawk
Requires:	%{name}-data = %{version}

%description
3D go-kart racing game for kids with several famous OpenSource mascots
participating. Race as Tux against 3 computer players in many different fun
race courses (Standard race track, Dessert, Mathclass, etc). Full information
on how to add your own race courses is included. During the race you can pick
up powerups such as: (homing) missiles, magnets and portable zippers.

%package data
Summary:	%{summary}
Group:		Amusements/Games
Requires:	%{name} = %{version}
BuildArch:	noarch

%description data
This package contains the data files for SuperTuxKart, as well as the add-on pack.

%prep
%setup -q -n %{src_name}-%{src_version}
%patch1 -p1
# some cleanups
chmod -x AUTHORS COPYING ChangeLog README TODO
chmod -x `find -name "*.cpp" -o -name "*.hpp"`
rm -fr data/karts/*/.svn data/karts/.svn

unzip %{SOURCE2} -d data/ -x karts/mriceblock*

%build
autoconf

export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lGLU -lnsl -lsocket"

./configure --prefix=%{_prefix} --mandir=%{_mandir}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# easier then patching all the Makefile's
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_prefix}/games/%{src_name} $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/games/%{src_name}/data/po $RPM_BUILD_ROOT%{_datadir}/locale
rm $RPM_BUILD_ROOT%{_datadir}/locale/*.po
rm $RPM_BUILD_ROOT%{_datadir}/locale/%{src_name}.pot
ln -s ../../locale $RPM_BUILD_ROOT%{_datadir}/games/%{src_name}/data/po
rmdir $RPM_BUILD_ROOT%{_prefix}/games

%find_lang %{src_name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.xpm
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files data
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/games/%{src_name}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Sun May 09 2010 Milan Jurik
- initial SFE import
* Thu Jan 14 2010 Jon Ciesla <limb@jcomserv.net> - 0.6.2-3
- Rebuild for new irrlicht.

* Thu Nov 19 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.2-2
- Add in addon pack.
- Split data to noarch subpackage.

* Thu Sep 10 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.2-1
- Bugfix release.

* Sun Aug 16 2009 Hans de Goede <hdegoede@redhat.com> - 0.6.1a-3
- Switch to openal-soft

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Jon Ciesla <limb@jcomserv.net> - 0.6.1a-1
- Patch release.
- Fixed symlink/dir replacement, BZ 506245.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Hans de Goede <hdegoede@redhat.com> 0.6.1-1
- New upstream release 0.6.1

* Sun Jan 25 2009 Hans de Goede <hdegoede@redhat.com> 0.6-1
- New upstream release 0.6

* Sun Sep  7 2008 Hans de Goede <hdegoede@redhat.com> 0.5-2
- Fix patch fuzz build failure

* Tue Jun  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5-1
- New upstream release 0.5

* Tue May 13 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-2
- Rebuild for new plib

* Mon Mar 10 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-1
- New upstream release 0.4
- Note this version includes a build in copy of the bullet physics library,
  this is a patched copy making use if a system version impossible

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3-4
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-3
- Fix compilation with gcc 4.3

* Mon Sep 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-2
- Use opengl-games-utils wrapper to show error dialog when DRI is missing

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-1
- New upstream release 0.3
- Drop most patches (all fixed upstream)
- Update License tag for new Licensing Guidelines compliance

* Fri Oct  6 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-3
- replace some more coprighted images and sounds
- fix a bunch of joystick related bugs

* Mon Sep 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-2
- rename images-legal.txt to supertuxkart-images-legal.txt
- add a changelog entry for the previous release (and this one)

* Mon Sep 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-1
- initial Fedora Extras package (replacing regular tuxkart)
