#
# spec file for package SFElxinput
#
# includes module(s): lxinput
#
%include Solaris.inc

Name:                    SFElxinput
Summary:                 LXInput (Kbd & mouse config)
Version:                 0.3.0
Source:                  http://nchc.dl.sourceforge.net/sourceforge/lxde/lxinput-%{version}.tar.gz
URL:                     http://sourceforge.net/projects/lxde/

# owner:alfred date:2009-05-27 type:bug
Patch1:                  lxinput-01-Werror.diff

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
%setup -q -n lxinput-%version
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
%dir %attr (0755, root, other) %{_datadir}/lxinput
%{_datadir}/lxinput/*
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
* Tue Aug 17 2010 - brian.cameron@oracle.com
- Bump to 0.3.0.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.1.1
* Wed May 27 2009 - alfred.peng@sun.com
- Initial version
