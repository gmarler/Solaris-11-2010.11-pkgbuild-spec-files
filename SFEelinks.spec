#
# spec file for package SFEelinks
#
#
# IMPORTANT: This spec is GCC only at the moment. Suggestions welcome.
#
# on Sparc *and* x86 compile this spec with: 
#
# CXX=/usr/sfw/bin/g++ CC=/usr/sfw/bin/gcc pkgtool --interactive build-only SFEelinks.spec
# 
#

%include Solaris.inc

Name:                    SFEelinks
Summary:                 Elinks - textbased webbrowser
Version:                 0.11.4rc1
Source:			 http://elinks.or.cz/download/elinks-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
##TODO## patch need reworking (linker/sunstudio)
#Patch1:			 elinks-01-remove_-rdynamic
%include default-depend.inc

BuildRequires: SUNWxwrtl
BuildRequires: SUNWxwplt
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWzlib
BuildRequires: SUNWbzip

Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWopenssl-libraries
Requires: SUNWzlibr
Requires: SUNWbzip


%prep
%setup -q -n elinks-%version
#%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -L/usr/gnu/lib -R/usr/gnu/lib
export CXXFLAGS="%cxx_optflags
export LDFLAGS="%{_ldflags} -L/usr/gnu/lib -R/usr/gnu/lib"

#Okay, a bit hard way to achieve that. Suggestions welcome. List only files relying on "bash"?
SHELLREPLACE=`find . -type f -exec grep -l "^#\!.*/bin/sh" {} \; -print`
perl -pi -e 's?^#!.*/bin/sh?#!/bin/bash?' $SHELLREPLACE

./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
	    --datadir=%{_datadir}               \
            --enable-bittorrent                 \
            --infodir=%{_infodir}

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_localedir}/locale.alias
rmdir $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%defattr (-, root, other)
%{_datadir}/locale/*


%changelog
* Sat May 10 2008 - Thomas Wagner
- add (Build-)Requires, bump version to 0.11.4rc1
- Sorry this is gcc only at the moment. Suggestions welcome.
- add this your .mailcap to have SFEmutt use elinks for great html rendering:
  text/html; elinks -dump %s; needsterminal; copiousoutput;
* Mon Nov 20 2006 - Thomas Wagner
- initial spec stored savely on the darkest end of my harddisk
