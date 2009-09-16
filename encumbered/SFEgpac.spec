#
# spec file for package SFEgpac
#
# includes module(s): gpac
#
%include Solaris.inc

%define with_wxw_gcc %(pkginfo -q SFEwxwidgets-gnu && echo 1 || echo 0)
# disable jack and pulseaudio support for now
%define with_jack 0
%define with_pulseaudio 0

%if %with_wxw_gcc
%define cc_is_gcc 1
export CC=gcc
export CXX=g++
%endif

%ifarch amd64 sparcv9
%include arch64.inc
%use gpac_64 = gpac.spec
%endif

%include base.inc
%use gpac = gpac.spec

Name:                SFEgpac
Summary:             %{gpac.summary}
Version:             %{gpac.version}
URL:                 http://gpac.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEliba52-devel
Requires: SFEliba52
Requires: SUNWfreetype2
# Check whether the user has installed the Sun Studio or GCC
# version of wxWidgets, and build with GCC if using the GCC
# version
%if %with_jack
BuildRequires: SFEjack-devel
Requires: SFEjack
%endif
%if %with_pulseaudio
BuildRequires: SFEpulseaudio-devel
Requires: SFEpulseaudio
%endif
%if %with_wxw_gcc
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEwxwidgets-gnu
%else
BuildRequires: SUNWwxwidgets-devel
Requires: SUNWwxwidgets
%endif
BuildRequires: SFExvid-devel
Requires: SFExvid

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%gpac_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gpac.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%gpac_64.build -d %name-%version/%_arch64
%endif

%gpac.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gpac_64.install -d %name-%version/%_arch64
%endif

%gpac.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gpac
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gpac
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_datadir}/gpac
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Wed Sep 16 2009 - trisk@forkgnu.org
- Add (disabled) support for jack and pulseaudio
* Wed Sep 02 2009 - trisk@forkgnu.org
- Add dependency on SFEliba52
* Sun Aug 24 2009 - Milan Jurik
- multiarch support, update to 0.4.5
* Sun Nov 30 2008 - dauphin@enst.fr
- SUNWwxwigets is on b101
* Fri Nov 21 2008 - dauphin@enst.fr
- gpac with Studio12 and new freeglut
- TODO: check ffmepg option (build with)
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEfreetype/SUNWfreetype2
* Thu Jun 19 2008 - river@wikimedia.org
- need to unset P4PORT during %setup or gpatch behaves oddly
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- rights change for mandir, fix by Giles Dauphin
* Mon Dec 31 6 2007 - markwright@internode.on.net
- Add patch 4 to fix trivial compiler error missing INADDR_NONE.
- Add --extra-libs="-lrt -lm".
* Mon Jul 30 2007 - dougs@truemail.co.th
- Install headers
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
