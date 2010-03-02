#
# spec file for package SFEsdl-sound
#
# includes module(s): SDL
#

%define src_name	SDL_sound
%define src_url		http://icculus.org/%{src_name}/downloads

Name:			sdl-image
Summary: 		Sound decoding library for SDL
Version:		1.0.3
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
URL:                    http://icculus.org/SDL_sound/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags" 
# mpglib must be disabled due to MP3 patent
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}		\
            --disable-flac			\
            --disable-smpeg			\
            --disable-mpglib			\
            --disable-mikmod			\
            --disable-modplug			\
            --disable-speex			\
            --disable-physfs

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 02 2010 - matt@greenviolet.net
- Bump version to 1.0.3
* Mon Feb 25 2008 - Albert Lee
- Initial spec
