#
# spec file for package SFElibfribidi.spec
#
# includes module(s): libfribidi
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use fribidi = fribidi.spec

Name:                   SFElibfribidi
Summary:                %{fribidi.summary}
URL:			%{fribidi.url}
Version:                %{fribidi.version}
License:		%{fribidi.license}
Group:			%{fribidi.group}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
A library to handle bidirectional scripts (eg. hebrew, arabic), so that
the display is done in the proper way; while the text data itself is
always written in logical order.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%fribidi.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%fribidi.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%fribidi.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Apr 11 2010 - Milan Jurik
- cleanup for the latest pkgtool
* Sun Aug 17 2008 - nonsea@users.sourceofrge.net
- Add man page to %files
* Mon Oct 22 2007 - nonsea@users.sourceforge.net
- Spilit into fribidi.spec
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
