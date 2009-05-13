#
# spec file for package SFEpython-xlib
#
# includes module(s): python-xlib
#
%include Solaris.inc

%define python_version  2.4

Name:                   SFEistanbul
Summary:                Desktop Session Recorder
URL:                    http://live.gnome.org/Istanbul
Version:                0.2.2
Source:                 http://zaheer.merali.org/istanbul-%{version}.tar.bz2
# Reported as bug #573063.
Patch1:                 istanbul-01-fixgst.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
Requires:               SUNWgst-python
Requires:               SUNWgnome-media
Requires:               SUNWgnome-python-libs
Requires:               SUNWgnome-python-extras
Requires:               SFEpython-xlib
BuildRequires:          SUNWPython-devel
BuildRequires:          SUNWgst-python
BuildRequires:          SUNWgnome-media-devel
BuildRequires:          SUNWgnome-python-libs-devel
BuildRequires:          SUNWgnome-python-extras
BuildRequires:          SFEpython-xlib

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SFEistanbul

%prep
%setup -q -n istanbul-%{version}
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
export PKG_CONFIG_PATH=/usr/lib/python2.4/pkgconfig
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.la


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post root
%include gconf-install.script

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/istanbul.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/gstreamer-0.10/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%attr (-, root, other) %{_datadir}/locale
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/istanbul.schemas


%changelog
* Wed May 13 2009 - brian.cameron@sun.com
- Set PKG_CONFIG_PATH to point to the Python 2.4 libraries.  Otherwise it
  fails to configure.  Probably could use Python 2.6, but would need to make
  python-xlib install as Python 2.6 and also would need to modify the 
  istanbul common/as-python.m4 file to find python 2.6, which it does not
  currently.
* Tue Feb 24 2009 - brian.cameron@sun.com
- Initial 0.2.2 version
