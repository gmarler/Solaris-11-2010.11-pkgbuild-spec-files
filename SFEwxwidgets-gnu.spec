#
# spec file for package SFEwxwidgets-gnu
#
# includes module(s): wxWidgets
#

%include Solaris.inc
%include usr-gnu.inc

%define pkg_src_name	wxWidgets
%define	src_ver 2.8.10
%define	src_name        wxwidgets-gnu

%define using_gld %(gcc -v 2>&1 | /usr/xpg4/bin/grep -q with-gnu-ld && echo 1 || echo 0)
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define cc_is_gcc 1
%ifarch amd64 sparcv9
%include arch64.inc
%define is64 1
%use wxwidgets_gnu_64 = wxwidgets-gnu.spec
%endif
%include base.inc
%define is64 0
%use wxwidgets_gnu = wxwidgets-gnu.spec

Name:                    SFEwxwidgets-gnu
Summary:                 wxWidgets - Cross-Platform GUI Library (g++)
URL:                     http://wxwidgets.org/
Version:                 %{src_ver}
Source:			 %{sf_download}/wxwindows/%{pkg_src_name}-%{src_ver}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Requires:      SUNWgnome-vfs
%if %SUNWlibsdl
Requires:      SUNWlibsdl
%else
Requires:      SFEsdl
%endif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
%else
BuildRequires: SFEsdl-devel
%endif

%if %{is_s10}
# There is no gtk2 on solaris 10, hence necessary to build it from the
# KDE4 Solaris project:
# http://techbase.kde.org/index.php?title=Projects/KDE_on_Solaris
# Also after noticing that there are no 64 bit gtk v1 libs on solaris 10u8,
# I gave in on trying to make it work with gtk v1 on Solaris 10u8.
Requires:      FOSSgtk2
Requires:      FOSSexpat
BuildRequires: FOSSgtk2
BuildRequires: FOSSexpat
%endif

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%define is64 1
%wxwidgets_gnu_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir %{name}-%{version}/%{base_arch}
%define is64 0
%wxwidgets_gnu.prep -d %{name}-%{version}/%{base_arch}


%build
%ifarch amd64 sparcv9
%define is64 1
%wxwidgets_gnu_64.build -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%wxwidgets_gnu.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%define is64 1
%wxwidgets_gnu_64.install -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%wxwidgets_gnu.install -d %{name}-%{version}/%{base_arch}

%clean
%ifarch amd64 sparcv9
%define is64 1
%wxwidgets_gnu_64.clean -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%wxwidgets_gnu.clean -d %{name}-%{version}/%{base_arch}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wx*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%{_libdir}/wx

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/wx*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*
%{_libdir}/%{_arch64}/wx*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/bakefile
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Jun 21 2009 - brian.cameron@sun.com
- Bump to 2.8.10.  Remove upstream ptach wxwidgets-02-fixcompile.diff.
  Add patch wxwidgets-02-Tmacro.diff to resolve compile issue when building
  with the latest Sun Studio patches.
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 2.8.8
- Add patch fixcompile.diff (copy from SFEwxwidgets.spec)
* Thu Feb 21 2008 - trisk@acm.jhu.edu
- Bump to 2.8.7
- Add SFEsdl dependency, add --with-gnomevfs, fix building subdirs
* Sat Sep 22 2007 - dougs@truemail.co.th
- Modified for GNU ld with gcc
* Tue Sep 18 2007 - brian.cameron@sun.com
- Bump to 2.8.5.  Remove upstream patch wxwidgets-02-sqrt.diff.
* Wed Aug 15 2007 - dougs@truemail.co.th
- removed -pthreads from wx-config to stop it infecting other builds
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Bump to 2.8.4 for compatibility with SFEwxwidgets
- Use CC=gcc to be consistent and not confuse build system
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFEwxwidgets.spec
