#
# spec file for package SFEsdl-image
#
# includes module(s): SDL
#

%define src_name	SDL_image
%define src_url		http://www.libsdl.org/projects/%{src_name}/release

Name:			sdl-image
Summary: 		Simple DirectMedia Layer - Sample Image Loading Library
Version:		1.2.10
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags" 
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
* Tue Mar 02 2010 - matt@greenviolet.net
- Bump version to 1.2.10
* Sun Aug 16 2009 - Milan Jurik
- update to 1.2.7
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 1.2.6
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Sun Apr 01 2007 Jeff Cai
- Initial version
