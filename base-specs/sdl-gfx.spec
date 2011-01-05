#
# spec file for package SFEsdl-gfx
#
# includes module(s): SDL
#

%define src_name	SDL_gfx

Name:			SFEsdl-gfx
Summary: 		Graphics library for SDL
Version:		2.0.22
URL:			http://www.ferzkopp.net/Software/SDL_gfx-2.0/
License:		LGPL
Source: 		http://www.ferzkopp.net/Software/%{src_name}-2.0/%{src_name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
# workaround for wrong Makefile
mkdir -p m4

export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags" 
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}		\
            --enable-shared			\
	    --disable-static			\
	    %mmx_option

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 05 2011 - Milan Jurik
- bump to 2.0.22
* Sun Apr 11 2010 - Milan Jurik
- minor cleanup
* Tue Mar 02 2010 - matt@greenviolet.net
- Bump version to 2.0.20
- Update configure script to cooperate with Solaris sh
* Fri Aug 21 2009 - Milan Jurik
- update to 2.0.19
* Wed Oct  3 2007 - daymobrew@users.sourceforge.net
- Move src_url into Source so that the --download option works.
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Tue May  8 2007 - Doug Scott
- Initial version
