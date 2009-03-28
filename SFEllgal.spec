#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define perl_version 5.8.4

Name:           SFEllgal
Summary:        Command-line online gallery generator
Version:        0.13.15
URL:            http://home.gna.org/llgal/
Source:         http://download.gna.org/llgal/llgal-%{version}.tar.bz2
Patch1:         llgal-01-solaris-build.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWperl584core
Requires:       SFEperl-image-exiftool
Requires:       SFEperl-image-size
Requires:       SFEperl-uri
Requires:       SFEperl-gettext

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n llgal-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_prefix}/etc

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/site_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/site_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/site_perl/%{perl_version}/Llgal
%{_prefix}/perl5/site_perl/%{perl_version}/Llgal/*
%dir %attr(0755, root, bin) %{_prefix}/perl5/site_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/site_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/llgal

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Mar 28 2009 - halton.huo@sun.com
- Bump to 0.13.15
* Wed Sep 12 2007 - nonsea@users.sourceforge.net
- Initial spec
