#
#
# spec file for package SFEgeeqie 
#
# includes module(s): geeqie 
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jouby

%include Solaris.inc
%use geeqie = geeqie.spec
Name:                    SFEgeeqie 
Summary:                 Geeqie - Image browser forked from gqview
URL:                     http://geeqie.sourceforge.net/
Version:                 %{geeqie.version}
Source:                  http://sourceforge.net/projects/geeqie/files/geeqie/geeqie-%{version}/geeqie-%{version}.tar.gz/download 
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SFEgeeqie.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWuiu8
Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-common-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%geeqie.prep -d %name-%version

%build
export CFLAGS="%optflags -DEDITOR_GIMP"
export LDFLAGS="-lX11 -lsocket"
%geeqie.build -d %name-%version

%install
%geeqie.install -d %name-%version
if [ -d $RPM_BUILD_ROOT/%{_libdir}/locale ]; then
  mv $RPM_BUILD_ROOT/%{_libdir}/locale $RPM_BUILD_ROOT/%{_datadir}/
  rm -r  $RPM_BUILD_ROOT/%{_libdir}
fi
%if %{build_l10n}
mv $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN.GB2312 $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN 
%else
rm -r  $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d geeqie-%{geeqie.version} README AUTHORS
%doc(bzip2) -d geeqie-%{geeqie.version} COPYING ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#%dir %attr (0755, root, other) %{_datadir}/applications/
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/geeqie
%{_datadir}/geeqie/template.desktop
%{_datadir}/geeqie/applications/
%{_datadir}/doc/geeqie-%{geeqie.version}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Aug 24 2009 - yuntong.jin@sun.com 
- Initial build.

