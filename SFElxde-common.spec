#
# spec file for package SFElxde-common
#
# includes module(s): lxde-common
#
%include Solaris.inc

Name:                    SFElxde-common
Summary:                 the default settings configuration file for LXDE
Version:                 0.5.0
Source:                  http://downloads.sourceforge.net/lxde/lxde-common-%{version}.tar.gz
Patch1:                  lxde-common-01-startlxde.diff
URL:                     http://sourceforge.net/projects/lxde/

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n lxde-common-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lxde
%{_datadir}/lxde/*
%dir %attr (0755, root, other) %{_datadir}/lxpanel
%{_datadir}/lxpanel/*
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg/*

%changelog
* Mon Feb 15 2010 - brian.cameron@sun.com
- Bump to 0.5.0.
* Thu Aug 06 2009 - brian.cameron@sun.com
- Add lxde-common-02-startlxde.diff patch so that the script works with 
  Nevada bourne shell.
* Thu Aug 06 2009 - alfred.peng@sun.com
- Add patch01 to use GNU cp.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.4.2.
* Sun Mar 16 2009 - alfred.peng@sun.com
- Initial version.
