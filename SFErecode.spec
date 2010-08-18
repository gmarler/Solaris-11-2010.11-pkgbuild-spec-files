#
# spec file for package SFErecode
#
# includes module(s): GNU recode
#
%include Solaris.inc

Name:                SFErecode
Summary:             library that converts files between character sets and usages
Version:             3.6
Source:              ftp://ftp.gnu.org/pub/gnu/recode/recode-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Patch1:		     recode.01.diff
%include default-depend.inc
Requires: SUNWpostrun
BuildRequires:	SUNWtexi

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n recode-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%if %build_l10n
nlsopt=--enable-nls
%else
nlsopt=--disable-nls
%endif

./configure --prefix=%{_prefix}        \
            --mandir=%{_mandir}         \
            --infodir=%{_infodir}       \
            --disable-static            \
              $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm $RPM_BUILD_ROOT%{_infodir}/dir
rm $RPM_BUILD_ROOT%{_libdir}/librecode.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
 echo 'infos="';
 echo ' recode.info recode.info-1 recode.info-2 recode.info-3 recode.info-4 recode.info-5 recode.info-6 recode.info-7' ;
 echo '"';
 echo 'retval=0';
 echo 'for info in $infos; do';
 echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
 echo 'done';
 echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
 echo 'infos="';
 echo ' recode.info recode.info-1 recode.info-2 recode.info-3 recode.info-4 recode.info-5 recode.info-6 recode.info-7' ;
 echo '"';
 echo 'for info in $infos; do';
 echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
 echo 'done';
 echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/librecode*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* 
* Mon Mar 31 2008 - Pradhap Devarajan < pradhap (at) sun.com>
- fix error undef symbol issue (recode.01.diff)
* Sun Mar 04 2007 - Eric Boutilier
- Initial spec
