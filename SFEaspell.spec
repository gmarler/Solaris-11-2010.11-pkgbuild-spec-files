#
# spec file for package SFEaspell
#
# includes module(s): aspell
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc
%use aspell = aspell.spec

Name:          SFEaspell
Summary:       A Spell Checker
Version:       %{aspell.version}
SUNW_BaseDir:  %{_prefix}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWlibC
Requires:      SUNWlibms
Requires:      SUNWlibmsr
Requires:      SUNWperl584core
BuildConflicts:	SUNWaspell

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:      SFEaspell

%prep
rm -rf %name-%version
mkdir -p %name-%version
%aspell.prep -d %name-%version

%build
# Need to set LD_NOEXEC_64 and add -xannotate=no to deal with doo bug #9720.
# and bugster #6823945/#6865312.
export LD_NOEXEC_64=1
export CFLAGS="%optflags -xannotate=no"
export CXXFLAGS="%cxx_optflags -staticlib=stlport4 -xannotate=no"
export CXX="$CXX -norunpath"
export LDFLAGS="%_ldflags -lCrun -lm"
export MSGFMT="/usr/bin/msgfmt"
%aspell.build -d %name-%version

%install

# Need to set LD_NOEXEC_64 and add -xannotate=no to deal with doo bug #9720.
# and bugster #6823945/#6865312.
export LD_NOEXEC_64=1
export CFLAGS="%optflags -xannotate=no"
export CXXFLAGS="%cxx_optflags -staticlib=stlport4 -xannotate=no"

%aspell.install -d %name-%version
mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_libdir}/aspell/
rm -rf $RPM_BUILD_ROOT%{_bindir}

# The only stuff in datadir is doc, info and man which we do not want
# to package.  
#
rm -rf $RPM_BUILD_ROOT%{_datadir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/aspell

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Mar 05 2010 - Brian Cameron <brian.cameron>
- Need to set LD_NOEXEC_64 and add -xannotate=no to deal with doo bug #9720.
  and bugster #6823945/#6865312.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added BuildConflicts: SUNWaspell
* Tue Mar 13 2007 - jeff.cai@sun.com
- Move to sourceforge from opensolaris.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Apr 21 2006 - halton.huo@sun.com
- Move all things under %{_bindir} to %{_libdir}/aspell,
  requested by ARC change.
* Thu Apr 20 2006 - halton.huo@sun.com
- Change aspell lib dir from %{_libdir}/aspell-0.60 to 
  %{_libdir}/aspell, request by LSARC/2006/231.
* Thu Feb  2 2006 - damien.carbery@sun.com
- Add SUNWlibmsr to fix 6318910.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Remove '-library=stlport' from CXXFLAGS so it the library is not dynamically 
  linked into /usr/bin/aspell.
* Thu Oct 06 2005 - damien.carbery@sun.com
- Fix 6208701 (missing dependencies).
* Tue Sep 06 2005 - laca@sun.com
- fix build with new automake and libtool; remove unpackaged files
* Tue Jun 28 2005 - laca@sun.com
- fix stlport4 static linking with Vulcan FCS
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
