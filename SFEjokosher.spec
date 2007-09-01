#
# spec file for package SFEjokosher
#
# includes module(s): jokosher
#
%define pythonver 2.4

%include Solaris.inc

Name:		SFEjokosher
Summary:	Jokosher is a multi-track studio application
Version:	0.9
URL:		http://jokosher.org
Source0:	http://www.jokosher.org/downloads/source/jokosher-%{version}.tar.gz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/jokosher-%{version}-build
Requires:	SUNWgnome-python-libs
Requires:	SUNWdbus-bindings
Requires:	SUNWgnome-media
Requires:	SFEgst-python
Requires:	SFEgnonlin
BuildRequires:	SUNWPython-devel >= %{pythonver}
BuildRequires:	SFEgst-python
BuildRequires:	SFEgnonlin

%include default-depend.inc

%description
Jokosher is a simple yet powerful multi-track studio. 

%prep
%setup -q -n jokosher-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=%{buildroot}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="AudioVideo" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
find $RPM_BUILD_ROOT%{_datadir}/gnome/help/jokosher/* -type d ! -name 'C' -prune \
    | xargs rm -rf
find $RPM_BUILD_ROOT%{_datadir}/omf/jokosher/* -type f ! -name '*-C.omf' \
    | xargs rm -f
%endif

%clean
rm -rf %{buildroot}

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo '/usr/bin/gtk-update-icon-cache --force %{_datadir}/icons/hicolor'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -t 5
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/jokosher

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/Jokosher

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%attr (-, root, other) %{_datadir}/icons
%{_datadir}/jokosher
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/jokosher/C
%{_datadir}/omf/jokosher/*-C.omf

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/jokosher/[a-z]*
%{_datadir}/omf/jokosher/*-[a-z]*.omf
%endif

%changelog
* Sat Sep 01 2007 - trisk@acm.jhu.edu
- Fix help and l10n install rules
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Update dependencies and paths
* Tue Jul 10 2007 Brian Cameron <brian.cameron@sun.com>
- New spec file.
