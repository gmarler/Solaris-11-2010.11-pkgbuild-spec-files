#
# spec file for package SFEmednafen.spec
#

%include Solaris.inc

# Latest release:
# (Converting hex into decimal)
#%define version 0.8.12
#%define real_version 0.8.C

# Latest release candidate:
# (Appending next release number, followed by release candidate number)
%define version 0.8.12.13.1
%define real_version 0.8.D-rc1

Name:                    SFEmednafen
Summary:                 Mednafen - My Emulator Doesn't Need a Frickin' Excellent Name! - Multi-console emulator
Version:                 %{version}
#Source:                  %{sf_download}/mednafen/mednafen-%{real_version}.tar.bz2
Source:                  http://www.greenviolet.net/Solaris/SFE/mednafen-%{real_version}.tar.bz2
Patch1:                  mednafen-01-tremor.diff
Patch2:                  mednafen-02-madvise.diff
Copyright:               mednafen.copyright
License:                 GPL
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SFEgcc
BuildRequires:           SFElibcdio-devel
BuildRequires:           SFElibiconv-devel
BuildRequires:           SFEsdl-net-devel
BuildRequires:           SUNWlibsdl-devel
Requires:                SFEgccruntime
Requires:                SFElibcdio
Requires:                SFElibiconv
Requires:                SFEsdl-net
Requires:                SUNWlibmsr
Requires:                SUNWlibsdl
Requires:                SUNWlibsndfile
Requires:                SUNWlibzr

%description
Mednafen is a portable, utilizing OpenGL and SDL, argument(command-line)-driven multi-system emulator with many advanced features. The Atari Lynx, GameBoy (Color), GameBoy Advance, NES, PC Engine(TurboGrafx 16), SuperGrafx, Neo Geo Pocket (Color), and PC-FX are emulated. Mednafen has the ability to remap hotkey functions and virtual system inputs to a keyboard, a joystick, or both simultaneously. Save states are supported, as is real-time game rewinding. Screen snapshots may be taken at the press of a button, and are saved in the popular PNG file format.

%prep
%setup -q -c
cd %sname
%patch1
%patch2

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC="/usr/gnu/bin/gcc"
export CXX="/usr/gnu/bin/g++"
# Solaris requires a Pentium, hence -march=i586.
# Most desktop users on OpenSolaris probably have a recent Intel. Hence -mtune=prescott.
export CFLAGS="-g -Os -march=i586 -mtune=prescott -pipe -fno-omit-frame-pointer -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -i" 
export CXXFLAGS="-g -Os -march=i586 -mtune=prescott -pipe -fno-omit-frame-pointer -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -i" 
export LDFLAGS="-L/lib -R/lib -L/usr/lib -R/usr/lib -liconv %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
export LD=/usr/ccs/bin/ld
cd %sname
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-threads=solaris    \
            --enable-gb                 \
            --enable-gba                \
            --enable-lynx               \
            --enable-nes                \
            --enable-ngp                \
            --enable-pce                \
            --enable-pcfx               \
            --enable-sms                \
            --disable-wswan
# Compilation errors in:
# wswan: src/wswan/debug.h:17: expected ',' or '...' before numeric constant


#false
make -j$CPUS || make

%install
rm -rf $RPM_BUILD_ROOT
cd %sname
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Mon Mar 22 2010 - matt@greenviolet.net
- Initial spec file.
