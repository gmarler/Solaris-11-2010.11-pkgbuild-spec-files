#
# spec file for package SFEzeitgeist
#
# includes module(s): zeitgeist
#
%define pythonver 2.6

%include Solaris.inc
Name:                    SFEzeitgeist
Summary:                 Zeitgeist Engine
Version:                 0.0.1
Patch1:                  zeitgeist-01-python.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
# SFEbzr is needed since there isn't a release yet, and the spec-file
# pulls the data directly from bzr.
BuildRequires:           SFEbzr
BuildRequires:           SUNWdbus-python26
BuildRequires:           SUNWgnome-python26-libs-devel
BuildRequires:           SUNWgnome-python26-desktop
Requires:                SUNWdbus-python26
Requires:                SUNWgnome-python26-libs
Requires:                SUNWgnome-python26-desktop

%include default-depend.inc

%prep
mkdir -p zeitgeist-%version
cd zeitgeist-%version
rm -fR zeitgeist
bzr branch lp:zeitgeist
cd zeitgeist
%patch1 -p1

%build
export PYTHON="/usr/bin/python2.6"
cd zeitgeist-%version
cd zeitgeist
./autogen.sh \
   --prefix=%{_prefix} \
   --mandir=%{_mandir} 
make

%install
export PYTHON="/usr/bin/python2.6"
rm -rf $RPM_BUILD_ROOT
cd zeitgeist-%version
cd zeitgeist
make install DESTDIR=$RPM_BUILD_ROOT

# move to verndor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/zeitgeist/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.gnome.zeitgeist.service
%{_datadir}/zeitgeist
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
