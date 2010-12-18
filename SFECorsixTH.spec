#
# spec file for package SFECorsixTH.spec
#
# includes module(s): CorsixTH
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name CorsixTH
%define src_version Beta4

Name:		SFECorsixTH
Version:	0.0.0.4
Summary:	Theme Hospital reimplementation
Group:		Games/Strategy
License:	MIT
URL:		https://code.google.com/p/corsix-th/
Source:		http://corsix-th.googlecode.com/files/%{src_name}-%{src_version}-Source.tar.gz
Source1:	corsixth.txt
Source2:	CorsixTH-16.png
Source3:	CorsixTH-32.png
Source4:	CorsixTH-64.png
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWlibsdl-devel
Requires:	SUNWlibsdl
BuildRequires:	SUNWlua
Requires:	SUNWlua
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer
BuildRequires:	SUNWwxwidgets-devel
Requires:	SUNWwxwidgets
BuildRequires:	SUNWcmake

%description
This project aims to reimplement the game engine of Theme Hospital, and be able to load the original game data files

%prep
%setup -q -n %{src_name}-%{src_version}-Source
cp %{SOURCE1} CorsixTH/config.txt

%build
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
cd CorsixTH
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make

%install
rm -rf %{buildroot}
cd CorsixTH
make install

mkdir -p %{buildroot}%{_datadir}
mv sfw_stage/%{src_name} %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{src_name} << EOF
#!/bin/sh
%{_datadir}/%{src_name}/%{src_name}
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,64x64}/apps
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{src_name}.png
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{src_name}.png
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{src_name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{src_name}.desktop << EOF
[Desktop Entry]
Name=CorsixTH
Comment=Open source clone of Theme Hospital game
Exec=%{_bindir}/%{src_name}
Path=%{_datadir}/%{src_name}
Icon=%{src_name}
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, bin)
%attr(755, root, bin) %{_bindir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/%{src_name}.png
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/%{src_name}.png
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/%{src_name}.png



%changelog
* Sat Dec 18 2010 - Milan Jurik
- initial spec with inspiration from Mandriva
