#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')

%use goocanvas = goocanvas.spec

Name:           SFEgoocanvas
Summary:        %{goocanvas.summary}
Version:        %{default_pkg_version}
License:	LGPL
URL:		http://live.gnome.org/GooCanvas
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWgnome-base-libs
BuildRequires:  SUNWgnome-base-libs-devel

%if %(expr %{osbuild} '>=' 134)
Requires:	data/docbook
BuildRequires:	developer/documentation-tool/gtk-doc
%else
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml
%endif

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%goocanvas.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export RPM_OPT_FLAGS="$CFLAGS"
%goocanvas.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%goocanvas.install -d %name-%version
cd %{_builddir}/%name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%{_datadir}/gtk-doc
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* May 02 2010 - Gilles Dauphin
- get ready for next release
* Fri Apr 30 2010 - Milan Jurik
- added missing build dependencies
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
