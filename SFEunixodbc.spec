#####
# Spec File
####
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

####
# Software specific defines
####
%define vpkg odbc
%{!?_sysconfdir: %define _sysconfdir /etc}
# default location for drivers is libdir
%{!?drvlibdir: %define drvlibdir %{_libdir}}

%define configure_options --enable-shared --enable-static
# defaults below can be overridden during build
# e.g. rpmbuild --define 'build_gui_gtk 1'
%{!?build_drivers: %define build_drivers 1}
%{!?build_gui_qt:  %define build_gui_qt  0}
%{!?build_gui_gtk: %define build_gui_gtk 0}

# define macros if they are not defined
%{!?__ldconfig:%define __ldconfig /sbin/ldconfig}
%{!?_pkglibdir:%define _pkglibdir %{_libdir}/%{name}}
%{!?__libtool:%define __libtool /usr/bin/libtool}
%{!?__cut:%define __cut /usr/bin/cut}
%{!?__cat:%define __cat /bin/cat}

%define src_name unixodbc
%define src_version 2.2.14
%define pkg_release 1
#######
# Tag definitions
#######
%define prefix   /usr
%define sysconfdir	/etc

Name: SFEunixodbc
Summary: ODBC driver manager and drivers for PostgreSQL, MySQL, etc.
Version: %{src_version}
Release: %{pkg_release}
Copyright: LGPL and GPL
SUNW_BaseDir:/
BuildRoot: %{_tmppath}/%{src_name}-%{src_version}-build
URL: http://www.unixodbc.org/
Docdir: %{prefix}/doc
Prefix: %prefix
%include default-depend.inc

%description
ODBC driver manager and drivers for PostgreSQL, MySQL, etc.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc


# --- Sub-Packages ---

%if %{build_gui_qt}
%package gui-qt
Summary:        ODBC configurator, Data Source browser and ODBC test tool based on Qt
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
#BuildPrereq:   qt[23]-devel
Requires:       %{name} = %{version}
#Requires:      %{name} = %{version}, qt[23]
Provides:       %{name}-gui, %{vpkg}-gui
%endif # build_gui_qt

%if %{build_gui_gtk}
%package gui-gtk
Summary:        ODBC configurator based on GTK+ and GTK+ widget for gnome-db
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
#BuildPrereq:   gnome-libs-devel, gtk-devel
Requires:       %{name} = %{version}
#Requires:      %{name} = %{version}, gnome-libs, gtk
Provides:       %{name}-gui, %{vpkg}-gui
%endif

%if %{build_drivers}
%package drivers
Summary:        Database Drivers and Setup libraries for unixODBC
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name} = %{version} 
Provides:       %{name}-drivers, %{vpkg}-drivers
Summary:        Static library versions of Drivers and Setup libraries for uni
%description drivers
This package contains unixODBC drivers and setup libraries
for various database systems
%package drivers-devel
Summary:        Static library versions of Drivers and Setup libraries for unixODBC
Group:          %{?group}%{!?group:Applications/Databases}
Requires:       %{name}-devel = %{version} 
Provides:       %{name}-drivers-devel, %{vpkg}-drivers-devel
%description drivers-devel
This package contains static versions of unixODBC drivers and setup libraries
%endif # build_drivers

%ifarch amd64 sparcv9
%define is64 1
%use unixodbc64 = unixodbc-sr.spec
%endif
%include base.inc
%define is64 0
%use unixodbc = unixodbc-sr.spec

%prep
rm -rf unixODBC-%{src_version}
mkdir unixODBC-%{src_version}
%ifarch amd64 sparcv9
mkdir unixODBC-%{src_version}/%_arch64
%define is64 1
%unixodbc64.prep -d unixODBC-%{src_version}/%_arch64
%endif
mkdir unixODBC-%{src_version}/%{base_arch}
%define is64 0
%unixodbc.prep -d unixODBC-%{src_version}/%{base_arch}

# and apply patch(es) if any
#%patch
%if %{build_gui_gtk}
  # fix depcomp in GTK GUI (libtool needs it for relinking)
  ( cd gODBCConfig; if test ! -f ./depcomp; then ln -s ../depcomp .; fi )
%endif
# --- end of prep scriptlet ---


%build
%ifarch amd64 sparcv9
export CFLAGS=-m64
export LDFLAGS=-m64
export CXXFLAGS=-m64
%define is64 1
%unixodbc64.build -d unixODBC-%{src_version}/%_arch64
%endif
export LDFLAGS=
export CFLAGS=
export CXXFLAGS=
%define is64 0
%unixodbc.build -d unixODBC-%{src_version}/%{base_arch}

%install

%ifarch amd64 sparcv9
%define is64 1
%unixodbc64.install -d unixODBC-%{src_version}/%{_arch64}
%endif
%define is64 0
%unixodbc.install -d unixODBC-%{src_version}/%{base_arch}

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

# remove empty configuration files from buildroot
# (they will be created on-the-fly by the post scriptlet)
%{__rm} -f ${RPM_BUILD_ROOT}%{_sysconfdir}/odbcinst.ini
%{__rm} -f ${RPM_BUILD_ROOT}%{_sysconfdir}/odbc.ini

%pre
if [ -f %{sysconfdir}/odbc.ini ]; then
	mv -f %{sysconfdir}/odbc.ini %{sysconfdir}/odbc.ini.rpmsave
fi
if [ -f %{sysconfdir}/odbcinst.ini ]; then
	mv -f %{sysconfdir}/odbcinst.ini %{sysconfdir}/odbcinst.ini.rpmsave
fi

%files
# --- files section ---
%defattr(-, root, bin)
%doc    AUTHORS COPYING ChangeLog NEWS README README.* doc
%dir %attr (0755, root, sys) %{prefix}
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/ODBCDataSources
# system config files not included - created on the fly by post
#config %{_sysconfdir}/odbcinst.ini
#config %{_sysconfdir}/odbc.ini
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/odbcinst
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_libdir}/libodbc.so*
# driver manager configuration
%{_libdir}/libodbcinst.so*
# generic cursors library
%{_libdir}/libodbccr.so*
# testing
%{_libdir}/libgtrtst.so*
%{_libdir}/libboundparam.so*
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/isql
%{_bindir}/%{_arch64}/dltest
%{_bindir}/%{_arch64}/odbcinst
%{_bindir}/%{_arch64}/iusql
%{_bindir}/%{_arch64}/odbc_config
%{_libdir}/%{_arch64}/libodbc.so*
# driver manager configuration
%{_libdir}/%{_arch64}/libodbcinst.so*
# generic cursors library
%{_libdir}/%{_arch64}/libodbccr.so*
# testing
%{_libdir}/%{_arch64}/libgtrtst.so*
%{_libdir}/%{_arch64}/libboundparam.so*
%endif # amd64 sparcv9

%files devel
%defattr(-, root, bin)
%{_libdir}/libodbcinst.la
%{_libdir}/libodbcinst.a
%{_libdir}/libodbc.la
%{_libdir}/libodbc.a
%{_libdir}/libodbccr.la
%{_libdir}/libodbccr.a
%{_libdir}/libgtrtst.la
%{_libdir}/libgtrtst.a
%{_libdir}/libboundparam.la
%{_libdir}/libboundparam.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/unixODBC.pc
%{_includedir}/odbc/*.h
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libodbcinst.la
%{_libdir}/%{_arch64}/libodbcinst.a
%{_libdir}/%{_arch64}/libodbc.la
%{_libdir}/%{_arch64}/libodbc.a
%{_libdir}/%{_arch64}/libodbccr.la
%{_libdir}/%{_arch64}/libodbccr.a
%{_libdir}/%{_arch64}/libgtrtst.la
%{_libdir}/%{_arch64}/libgtrtst.a
%{_libdir}/%{_arch64}/libboundparam.la
%{_libdir}/%{_arch64}/libboundparam.a
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/unixODBC.pc
%endif

%if %{build_gui_qt}
%files gui-qt
%defattr(-, root, bin)
%{_bindir}/ODBCConfig
%{_bindir}/DataManager
%{_bindir}/DataManagerII
%if "%{_vendor}" == "suse"
%{_bindir}/ODBCTest
%else
%{_bindir}/odbctest
%endif
%{_libdir}/libodbcinstQ.so*
%endif

%if %{build_gui_gtk}
%defattr(-, root, bin)
%files gui-gtk
%{_bindir}/gODBCConfig
%{_libdir}/libgtkodbcconfig.so*
%endif

%if %{build_drivers}
%files drivers
%defattr(-, root, bin)
%{drvlibdir}/libesoobS.so*
%{drvlibdir}/libmimerS.so*
%{drvlibdir}/libnn.so*
%{drvlibdir}/libodbcdrvcfg1S.so*
%{drvlibdir}/libodbcdrvcfg2S.so*
%{drvlibdir}/libodbcminiS.so*
%{drvlibdir}/libodbcmyS.so*
%{drvlibdir}/libodbcnnS.so*
%{drvlibdir}/libodbcpsql.so*
%{drvlibdir}/libodbcpsqlS.so*
%{drvlibdir}/libodbctxtS.so*
%{drvlibdir}/liboplodbcS.so*
%{drvlibdir}/liboraodbcS.so*
%{drvlibdir}/libsapdbS.so*
%{drvlibdir}/libtdsS.so*
%{drvlibdir}/libtemplate.so*
%ifarch amd64 sparcv9
%{drvlibdir}/%{_arch64}/libesoobS.so*
%{drvlibdir}/%{_arch64}/libmimerS.so*
%{drvlibdir}/%{_arch64}/libnn.so*
%{drvlibdir}/%{_arch64}/libodbcdrvcfg1S.so*
%{drvlibdir}/%{_arch64}/libodbcdrvcfg2S.so*
%{drvlibdir}/%{_arch64}/libodbcminiS.so*
%{drvlibdir}/%{_arch64}/libodbcmyS.so*
%{drvlibdir}/%{_arch64}/libodbcnnS.so*
%{drvlibdir}/%{_arch64}/libodbcpsql.so*
%{drvlibdir}/%{_arch64}/libodbcpsqlS.so*
%{drvlibdir}/%{_arch64}/libodbctxtS.so*
%{drvlibdir}/%{_arch64}/liboplodbcS.so*
%{drvlibdir}/%{_arch64}/liboraodbcS.so*
%{drvlibdir}/%{_arch64}/libsapdbS.so*
%{drvlibdir}/%{_arch64}/libtdsS.so*
%{drvlibdir}/%{_arch64}/libtemplate.so*
%endif # amd64 sparcv9

%files drivers-devel
%defattr(-, root, bin)
%{drvlibdir}/libesoobS.*a
%{drvlibdir}/libmimerS.*a
%{drvlibdir}/libnn.*a
%{drvlibdir}/libodbcdrvcfg1S.*a
%{drvlibdir}/libodbcdrvcfg2S.*a
%{drvlibdir}/libodbcminiS.*a
%{drvlibdir}/libodbcmyS.*a
%{drvlibdir}/libodbcnnS.*a
%{drvlibdir}/libodbcpsql.*a
%{drvlibdir}/libodbcpsqlS.*a
%{drvlibdir}/libodbctxtS.*a
%{drvlibdir}/liboplodbcS.*a
%{drvlibdir}/liboraodbcS.*a
%{drvlibdir}/libsapdbS.*a
%{drvlibdir}/libtdsS.*a
%{drvlibdir}/libtemplate.*a
%ifarch amd64 sparcv9
%files drivers-devel
%{drvlibdir}/%{_arch64}/libesoobS.*a
%{drvlibdir}/%{_arch64}/libmimerS.*a
%{drvlibdir}/%{_arch64}/libnn.*a
%{drvlibdir}/%{_arch64}/libodbcdrvcfg1S.*a
%{drvlibdir}/%{_arch64}/libodbcdrvcfg2S.*a
%{drvlibdir}/%{_arch64}/libodbcminiS.*a
%{drvlibdir}/%{_arch64}/libodbcmyS.*a
%{drvlibdir}/%{_arch64}/libodbcnnS.*a
%{drvlibdir}/%{_arch64}/libodbcpsql.*a
%{drvlibdir}/%{_arch64}/libodbcpsqlS.*a
%{drvlibdir}/%{_arch64}/libodbctxtS.*a
%{drvlibdir}/%{_arch64}/liboplodbcS.*a
%{drvlibdir}/%{_arch64}/liboraodbcS.*a
%{drvlibdir}/%{_arch64}/libsapdbS.*a
%{drvlibdir}/%{_arch64}/libtdsS.*a
%{drvlibdir}/%{_arch64}/libtemplate.*a
%endif # amd64 sparcv9
%endif # build_drivers

# --- Pre/Post/Un/Install/Verify scripts ---

%post
%{__ldconfig}
if test "$1" = 1 ; then # first instance of the package
  # find configuration utility
  odbcinst=odbcinst # last resort - rely on path
  for dir in ${RPM_INSTALL_PREFIX}/bin %{_bindir}; do
    test -x $dir/$odbcinst || continue # not here
    odbcinst=$dir/$odbcinst # found 
    break # out of loop 
  done
  # create/remove default entries in configuration files
  # if they do not exist (creates config files):
  # driver configuration file odbcinst.ini
  $odbcinst -q -d -n 'ODBC' 1>&- 2>&- # exists ?
  if test $? -gt 0 ; then # no, create
    echo '[ODBC]' | $odbcinst  -i -d -r 1>&- 2>&- # install
    $odbcinst -u -d -n 'ODBC' 1>&- 2>&- # remove
  fi
  # system data source configuration file odbc.ini
  $odbcinst -q -s -l -n 'DEFAULT' 1>&- 2>&- # exists ?
  if test $? -gt 0 ; then # no, create
    echo '[DEFAULT]' | $odbcinst  -i -s -l -r 1>&- 2>&- # install
    $odbcinst -u -s -l -n 'DEFAULT' 1>&- 2>&- # remove
  fi
fi
%preun
# configuration files in %{_sysconfdir} stay in place (even if empty)
# they might be needed by another driver manager

%postun -p %{__ldconfig}

%changelog
* Thu Aug 21 2008 Michal Bielicki <michal.bielicki <at> voiceworks.pl>
- More Permission fixes
* Wed Jun 25 2008 Michal Bielicki <michal.bielicki <at> voiceworks.pl> 
- Permission fixes
* Sun Dec 02 2007 Michal Bielicki <michal.bielicki <at> voiceworks.pl> 2.2.12
- First instance of SFE spec file
- Disabled GUI stuff, will add in next version of spec file
