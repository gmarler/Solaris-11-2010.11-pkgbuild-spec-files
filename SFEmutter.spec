#
# spec file for package SFEmutter
#
# includes module(s): mutter
#
%include Solaris.inc

%define pythonver 2.6

Name:                    SFEmutter
Summary:                 Clutter enabled metacity window manager
Version:                 2.91.0
Source:	                 http://ftp.gnome.org/pub/GNOME/sources/mutter/2.91/mutter-%{version}.tar.bz2
Patch1:                  mutter-01-suncc-xc99.diff
# Bug #612506.
Patch2:                  mutter-02-wait.diff
Patch3:                  mutter-03-compile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWlibgtk3-devel
BuildRequires:           SUNWclutter-devel
BuildRequires:           SUNWgobject-introspection-devel
BuildRequires:           SFEgjs-devel
Requires:                SUNWPython26
Requires:                SUNWlibgtk3
Requires:                SUNWclutter
Requires:                SUNWgobject-introspection
Requires:                SFEgjs
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n mutter-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export CFLAGS="%optflags"
export PYTHON=/usr/bin/python%{pythonver}

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --mandir=%{_mandir} \
   --sysconfdir=%{_sysconfdir} \
   --with-clutter --with-gtk=3.0
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%post root
cat >> $BASEDIR/var/svc/profile/upgrade <<\EOF

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mutter
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/wm-properties
%{_datadir}/mutter
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/mutter.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Oct 22 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 2.91.0.
* Tue Jun 01 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 2.31.2.
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.1.
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.0.
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.28.0.
* Wed Sep 16 2009 - Halton Huo <halton.huo@sun.com>
- Bump to 2.27.5.
* Sat Sep 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.4.
* Sat Aug 29 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.3.
* Tue Aug 04 2009 - Halton Huo <halton.huo@sun.com>
- Add patch suncc-xc99.diff to fix suncc build issue.
- Add patch solaris-shell.diff to fix bugzilla #590719.
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Update to build against 2.27.1 tarball.
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove upstream patch mutter-01-xopen-source.diff.
* Sat Apr 06 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
