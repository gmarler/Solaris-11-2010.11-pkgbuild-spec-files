#
# spec file for package SFElxappearance
#
# includes module(s): lxappearance
#
%include Solaris.inc

Name:                    SFElxappearance
Summary:                 LXDE theme switcher
Version:                 0.4.0
Source:                  http://downloads.sourceforge.net/lxde/lxappearance-%{version}.tar.gz
Patch1:                  lxappearance-01-makefile.diff
URL:                     http://sourceforge.net/projects/lxde/

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n lxappearance-%version
%patch1 -p1

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
./configure --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir}

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
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/lxappearance
%{_datadir}/lxappearance/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Feb 15 2010 - brian.cameron@sun.co
- Bump to 0.4.0.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.2.1.
* Sun Mar 16 2009 - alfred.peng@sun.com
- Initial version.
