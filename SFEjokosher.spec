#
# spec file for package SFEjokosher
#
# includes module(s): jokosher
#
%define pythonver 2.6

%include Solaris.inc

Name:		SFEjokosher
Summary:	Jokosher is a multi-track studio application
Version:	0.11.1
URL:		http://jokosher.org
Source0:	http://launchpad.net/jokosher/0.11/%{version}/+download/jokosher-%{version}.tar.gz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/jokosher-%{version}-build
Requires:       SUNWPython
Requires:	SUNWdbus-python26
Requires:	SUNWgnome-media
Requires:	SUNWgnome-python26-libs
Requires:	SUNWgst-python26
Requires:	SFEgnonlin
Requires:	SUNWpython26-setuptools
BuildRequires:	SUNWPython26-devel
BUildRequires:	SUNWdbus-python26-devel
BuildRequires:	SUNWgnome-media-devel
BuildRequires:	SUNWgnome-python26-libs-devel
BuildRequires:	SUNWgst-python26-devel
BuildRequires:  SUNWpython26-setuptools
BuildRequires:	SFEgnonlin

%include default-depend.inc

%description
Jokosher is a simple yet powerful multi-track studio. 

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n jokosher-%version

%build
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --root=%{buildroot}

desktop-file-install \
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
%{_libdir}/python%{pythonver}/vendor-packages/jokosher*egg-info

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
* Tue May 12 2009 - brian.cameron@sun.com
- Now build with Python 2.6.
* Thu Mar 19 2009 - brian.cameron@sun.com
- Bump to 0.11.1.
* Sun Mar 01 2009 - brian.cameron@sun.com
- Bump to 0.11.
* Tue Sep 30 2008 - brian.cameron@sun.com
- Bump to 0.10.1
* Fri Aug 29 2008 - brian.cameron@sun.com
- Bump to 0.10.  Yay!  Remove patch jokosher-01-fixdesktop.diff as it is no
  longer needed.
* Thu Apr 10 2008 - brian.cameron@sun.com
- Change SFEgst-python to SUNWgst-python.
* Thu Feb 07 2008 - brian.cameron@sun.com.
- Add jokosher-01-fixdesktop.diff file so package builds.
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Sat Sep 01 2007 - trisk@acm.jhu.edu
- Fix help and l10n install rules
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Update dependencies and paths
* Tue Jul 10 2007 Brian Cameron <brian.cameron@sun.com>
- New spec file.
