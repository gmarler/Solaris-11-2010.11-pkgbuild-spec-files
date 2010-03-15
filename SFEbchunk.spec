#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name bchunk

Name:                SFEbchunk
Summary:             bchunk - Convert ".bin/.cue" files into ISO 9660 images
Version:             1.2.0
License:             GPLv2+
Source:              http://he.fi/bchunk/%{src_name}-%{version}.tar.gz
URL:                 http://he.fi/bchunk/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
make CC="$CC" LD="$CC" CFLAGS="%optflags" LDFLAGS="%{_ldflags}"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin
cp -p bchunk $RPM_BUILD_ROOT/%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -p bchunk.1 $RPM_BUILD_ROOT/%{_mandir}/man1

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
* Mon Mar 15 2010 - Albert Lee <trisk@opensolaris.org>
- Update to not require /usr/ucb install
- Add URL and License
* Mon Jun 01 2009 - Albert Lee <trisk@forkgnu.org>
- Initial spec
