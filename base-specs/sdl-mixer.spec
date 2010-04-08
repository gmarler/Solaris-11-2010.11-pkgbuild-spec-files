#
# spec file for package SFEsdl-mixer
#
# includes module(s): SDL
#

%define src_name	SDL_mixer
%define src_url		http://www.libsdl.org/projects/%{src_name}/release

Name:			SFEsdl-mixer
Summary: 		Sound Mixer library for SDL
Version:		1.2.11
URL:			http://www.libsdl.org/projects/SDL_mixer/
License:		LGPLv2.1
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			sdl-mixer-01-cflags.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags -lm" 
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}

gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Apr 08 2010 - Milan Jurik
- cleanup
* Fri Mar 05 2010 - brian.cameron@sun.com
- Bump to 1.2.11.
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 1.2.8
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Sun Apr 22 2007 - Doug Scott
- Initial version
