#
# spec file for package SFElbreakout
#
#
%include Solaris.inc

Name:		SFElbreakout2
Summary:	LBreakout2 is a successor to LBreakout a breakout-style arcade game
Version:	2.6.1
Source:		%{sf_download}/lgames/lbreakout2-%{version}.tar.gz
Source1:	lbreakout2.desktop
Patch1:		lbreakout2-01-locale.diff
URL:		http://lgames.sourceforge.net/index.php?project=LBreakout2
License:	GPLv2
Group:		Amusements/Games
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWcsu
Requires: SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: %{name}-root
BuildRequires: SFElibiconv-devel
Requires: SFElibiconv
BuildRequires: SUNWaudh
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer

%package root
Summary:                 %{summary} - / filesystem components
SUNW_BaseDir:            /
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n lbreakout2-%version
%patch1 -p1

%build
export CFLAGS="%optflags -I%{gnu_inc} -DINSTALLPREFIX=\\\"%{_prefix}\\\""
export LDFLAGS="%_ldflags %{gnu_lib_path} -liconv -lintl -lsocket -lnsl"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --localstatedir=%{_localstatedir}/lbreakout2 \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --with-docdir=%{_datadir}/doc
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf ${RPM_BUILD_ROOT}/usr/var
rm -rf ${RPM_BUILD_ROOT}/usr/doc
rm -f ${RPM_BUILD_ROOT}/var/lbreakout2/lbreakout2.hscr

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp ${RPM_BUILD_ROOT}%{_datadir}/lbreakout2/gfx/win_icon.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/lbreakout2.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lbreakout2
%{_datadir}/lbreakout2/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*

%files root
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lbreakout2
#%{_localstatedir}/lbreakout2/*

%changelog
* Mon May 17 2010 - Milan Jurik
- update to 2.6.1
* Wed Feb  6 pradhap (at) gmail.com
- Initial lbreakout spec file.

