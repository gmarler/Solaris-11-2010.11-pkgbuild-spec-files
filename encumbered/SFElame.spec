#
# spec file for package SFElame.spec
#
# includes module(s): lame, toolame
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
%use lame_64 = lame.spec
%use toolame_64 = toolame.spec
%endif

%include base.inc

%use lame = lame.spec
%use toolame = toolame.spec

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)


Name:                    SFElame
Summary:                 MP3 Encoders - lame and toolame
Version:                 %{lame.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibms
Requires: SUNWlibms

%if %use_gcc4
BuildRequires: SFEgcc
Requires: SFEgccruntime
%else
BuildRequires: SUNWgcc
Requires: SUNWgccruntime
%endif

%if %SFElibsndfile
BuildRequires:	SFElibsndfile-devel
Requires:	SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

BuildRequires: SUNWncurses-devel
Requires: SUNWncurses

# we don't build the GTK frontend but autotools needs the macros
BuildRequires: SUNWgnome-common-devel

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
%lame_64.prep -d %name-%version/%_arch64
%toolame_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%lame.prep -d %name-%version/%{base_arch}
%toolame.prep -d %name-%version/%{base_arch}

%build

%ifarch amd64 sparcv9
%lame_64.build -d %name-%version/%_arch64
%toolame_64.build -d %name-%version/%_arch64
%endif

%lame.build -d %name-%version/%{base_arch}
%toolame.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%lame_64.install -d %name-%version/%_arch64
%toolame_64.install -d %name-%version/%_arch64
%endif

%lame.install -d %name-%version/%{base_arch}
%toolame.install -d %name-%version/%{base_arch}

%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/lame $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/toolame $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%if %can_isaexec
%post
ln ${BASEDIR}/lib/isaexec ${BASEDIR}/bin/lame
ln ${BASEDIR}/lib/isaexec ${BASEDIR}/bin/toolame
installf $PKGINST %{_bindir}/lame || exit 2
installf $PKGINST %{_bindir}/toolame || exit 2
installf -f $PKGINST || exit 2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}
%else
%{_bindir}/lame
%{_bindir}/toolame
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc/*

%changelog
* Wed Mar 24 2010 - Milan Jurik
- update for 3.98.4
* Wed Mar 03 2010 - Milan Jurik
- update for 3.98.3
* Tue Sep 15 2009 - Thomas Wagner
- make (Build)Requires a build-time --with-gcc4 switch defaulting to off (which is then: use SUNWgcc, gcc3)
- %define cc_is_gcc 1  to use gcc include settings to avoid -Kpic unknown switch error of gcc3 and gcc4 compiler 
- remove one too much #include base.inc
* Tue Sep 15 2009 - Albert Lee
- Drop SUNWgnome-common and SFEgccruntime dependencies
* Sun Aug 09 2009 - Thomas Wagner
- (Build)Requires: SUNWlibms SFEgcc/SFEgccruntime
* Sun Aug 02 2009 - Adam Retter
- add required dependency on SUNWgnome-common-devel
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 3.98.2 
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Sat Nov 29 2008 - dauphin@enst.fr
- SUNWncurses exist in b101
* Thu Oct 23 2008 - dick@nagual.nl
- s/SUNWncurses/SFEncurses for the time being.
- add dependency on SFElibsndfile for better/more audio formats
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEncurses/SUNWncurses since it goes into vermillion
* Tue Mar 20 2007 - dougs@truemail.co.th
- Moved lame and toolame to base spec. Added 64bit and x86_sse2 builds
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
