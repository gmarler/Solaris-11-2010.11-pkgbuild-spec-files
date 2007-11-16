#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%use gio = gio.spec

Name:           SFEgio
Summary:        gio - a set of daemons handling access to various file resources
Version:        %{default_pkg_version}
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWlibmsr
Requires:       SUNWcslr
Requires:       SUNWgnome-base-libs
Requires:       SUNWgamin
BuildRequires:  SUNWgnome-base-libs-devel
BUildRequires:  SUNWgamin-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gio.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export RPM_OPT_FLAGS="$CFLAGS"
%gio.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gio.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/gio

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gio


%changelog
* Thu Nov 08 2007 - daymobrew@users.sourceforge.net
- Remove l10n package as no l10n files are installed.

* Wed Nov 07 2007 - nonsea@users.sourceforge.net
- Initial spec
