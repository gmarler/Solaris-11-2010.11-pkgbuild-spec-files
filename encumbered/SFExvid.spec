#
# spec file for package SFExvid
#
# includes module(s): xvid
#

# want this? compile with: pkgtool --with-gcc4 build <specfile>
%define use_gcc4 %{?_with_gcc4:1}%{?!_with_gcc4:0}

%include Solaris.inc
%define cc_is_gcc 1
%if %use_gcc4
%define _gpp /usr/gnu/bin/g++
%else
%define _gpp /usr/sfw/bin/g++
%endif


%ifarch amd64 sparcv9
%include arch64.inc
%use xvid_64 = xvid.spec
%endif

%include base.inc
%use xvid = xvid.spec

Name:		SFExvid
Summary:	%{xvid.summary}
Version:	%{xvid.version}
License:	GPL
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

#BuildConflicts: SFEyasm
%ifarch i386 amd64
BuildRequires: SFEnasm
%endif

%if %use_gcc4
BuildRequires: SFEgcc
Requires: SFEgccruntime
%else
BuildRequires: SUNWgcc
Requires: SUNWgccruntime
%endif


%description
ISO MPEG-4 compliant video codec. You can play OpenDivX and DivX4 videos
with it, too.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%xvid_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%xvid.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%xvid_64.build -d %name-%version/%_arch64
%endif

%xvid.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%xvid_64.install -d %name-%version/%_arch64
%endif

%xvid.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Wed Mar 03 2010 - Milan Jurik
- use_gcc4 support
* Sat Aug 22 2009 - Milan Jurik
- multiarch support
* Sun Aug 09 2009 - Thomas Wagner
- switch to gcc4
- (Build)Requires: SFEgcc/SFEgccruntime
* Aug 04 2009 - Gilles Dauphin
- One patch for configure.in, add -mimpure-text and -shared because of nasm
- don't use yasm. option in configure. enable build with yasm installed
* Sat Jun 13 2009 - Milan Jurik
- upgradde to 1.2.2
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 1.2.1, nasm build support
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc, Remove non-standard CFLAGS (pentiumpro,sse2)
* Sat May 31 2008 - trisk@acm.jhu.edu
- Use default gcc and linker, fix arch options
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- use SFW gcc
- use SFW gld
- changes thanks to Giles Dauphin
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Removed redundant CFLAGS setting that was overwriting the earlier value.
* Mon Dec 31 2007 - markwright@internode.on.net
- Use SFEgcc 4.2.2.  Add sed hack to change -Wl,-M back to
- -Wl,--version-script for /usr/gnu/bin/ld.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
