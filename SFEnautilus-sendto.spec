#
# spec file for package SFEnautilus-sendto
#
# includes module(s): nautilus-sendto
#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use nst = nautilus-sendto.spec

Name:               SFEnautilus-sendto
Summary:            nst.- Nautilus context menu for sending files
Version:            %{nst.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWglib2
BuildRequires:      SUNWglib2-devel
Requires:           SUNWgtk2
BuildRequires:      SUNWgtk2-devel
Requires:           SUNWgnome-config
BuildRequires:      SUNWgnome-config
Requires:           SUNWgnome-file-mgr
Requires:           SUNWgnome-file-mgr-devel
Requires:           SUNWdbus-glib
BuildRequires:      SUNWdbus-glib-devel
Requires:           SUNWevolution-data-server
BuildRequires:      SUNWevolution-data-server-devel

%if %build_l10n
%package l10n
Summary:            %{summary} - l10n files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires:           %{name}
%endif

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%nst.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%nst.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%nst.install -d %name-%version

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
%{_bindir}/nautilus-sendto
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/nautilus
%{_libdir}/nautilus-sendto
%{_libdir}/pidgin
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/nautilus-sendto
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/nst.schemas

%changelog
* Wed Aug 05 2009 - halton.huo@sun.com
- Initial spec
