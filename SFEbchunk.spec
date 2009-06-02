#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name bchunk

Name:                SFEbchunk
Summary:             bchunk - Convert ".bin/.cue" files into ISO 9660 images
Version:             1.2.0
Source:              http://he.fi/bchunk/%{src_name}-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
make CC="$CC" LD="$CC" CFLAGS="%optflags" LDFLAGS="%{_ldflags}"

%install
rm -rf $RPM_BUILD_ROOT

/usr/ucb/install -d -m 0755 $RPM_BUILD_ROOT/%{_prefix}/bin
/usr/ucb/install -o root -g sys -m 0755 bchunk $RPM_BUILD_ROOT/%{_prefix}/bin
/usr/ucb/install -d -m 0755 $RPM_BUILD_ROOT/%{_mandir}/man1
/usr/ucb/install -o root -g bin -m 0755 bchunk.1 $RPM_BUILD_ROOT/%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Mon Jun 01 2009 - Albert Lee <trisk@forkgnu.org>
- Initial spec
