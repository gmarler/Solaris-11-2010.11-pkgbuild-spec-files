#
# spec file for package SFEsdl-ttf
#
# includes module(s): SDL
#

%define src_name	SDL_ttf
%define src_url		http://www.libsdl.org/projects/%{src_name}/release

Name:			sdl-ttf
Summary: 		True Type Font library for SDL
Version:		2.0.10
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
export PATH=/usr/gnu/bin/%{bld_arch}:%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags -lm"
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 05 2011 - Milan Jurik
- bump to 2.0.10
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 2.0.9
- Remove sdl-ttf-01-internal_h.diff - applied upstream
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Sun Apr 22 2007 - Doug Scott
- Initial version
