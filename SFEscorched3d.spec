#
# spec file for package SFEscorched3d.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)
%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)
%define SFEwxwidgets %(/usr/bin/pkginfo -q SFEwxwidgets && echo 1 || echo 0)


%define src_version 43.1c

Name:                    SFEscorched3d
Summary:                 A 3D game based on the classic DOS game, Scorched Earth
Version:                 43.1.0.3
Source:                  %{sf_download}/scorched3d/Scorched3D-%{src_version}-src.tar.gz
Source1:                 scorched3d.png
Source2:                 scorched3d.desktop
URL:                     http://www.scorched3d.co.uk/
License:                 GPL
Group:                   Amusements/Games
Patch1:                  scorched3d-01-securid.diff
Patch2:                  scorched3d-02-sunpro.diff
Patch3:                  scorched3d-03-const.diff
Patch4:                  scorched3d-04-prototype.diff
Patch5:                  scorched3d-05-openal.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SFEsdl
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%else
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%endif
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%if %SFEfreetype
BuildRequires: SFEfreetype-devel
Requires: SFEfreetype
%else
BuildRequires: SUNWfreetype2
Requires: SUNWfreetype2
%endif
Requires: SFEfftw
BuildRequires: SFEfftw-devel
%if %SFEwxwidgets
Requires: SFEwxwidgets
BuildRequires: SFEwxwidgets-devel
%else
BuildRequires: SUNWwxwidgets-devel
Requires: SUNWwxwidgets
%endif
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-net-devel

%prep
%setup -q -n scorched
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="%cxx_optflags"
export CFLAGS="%optflags -I%{sfw_inc}"
export MSGFMT="/usr/bin/msgfmt"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%{_ldflags} -z ignore -z combreloc -z direct -lsocket -lnsl %{sfw_lib_path}"
export LIBS=${LDFLAGS}

aclocal
automake --foreign
autoconf

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --datadir=%{_datadir}		\
            --with-wx-config=%{_prefix}/bin/wx-config

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/applications


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Sat May 08 2010 - Milan Jurik
- update to 43.1c
* Fri Feb 22 2008 - trisk@acm.jhu.edu
- Use SFEwxwidgets instead of SFEwxwidgets-gnu
- Fix linking
- Add patch2, patch3, patch4
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
