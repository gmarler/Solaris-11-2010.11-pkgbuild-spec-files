#
# spec file for package SFElxlauncher
#
# includes module(s): lxlauncher
#
%include Solaris.inc

Name:                    SFElxlauncher
Summary:                 LXDE application launcher
Version:                 0.2.1
Source:                  http://downloads.sourceforge.net/lxde/lxlauncher-%{version}.tar.gz
URL:                     http://sourceforge.net/projects/lxde/

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEmenu-cache
BuildRequires: SFEmenu-cache

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n lxlauncher-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir}

# Works around an inifite loop issue.
touch -r po/Makefile po/stamp-it

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/desktop-directories
%{_datadir}/desktop-directories/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.2.1.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
