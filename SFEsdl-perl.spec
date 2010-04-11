#
# spec file for package SFEsdl-perl
#
# includes module(s): sdl-perl
#
%include Solaris.inc

%define SFEsdl  %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)

Name:                    SFEsdl-perl
Summary:                 SDL Perl is a multimedia binding for Perl, using the Simple DirectMedia Layer and OpenGL.
Version:                 1.20.0
Source:                  http://zarb.org/~gc/t/SDL_perl-%{version}.tar.gz
URL:                     http://sdl.perl.org/

# owner:alfred date:2009-01-12 type:bug
# https://sourceforge.net/tracker/index.php?func=detail&aid=2500626&group_id=11529&atid=361529
Patch1:                  sdl-perl-01-solaris.diff

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
BuildRequires:	SUNWperl584usr

%prep
%setup -q -n SDL_perl-%{version}
%patch1 -p1

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/perl5
%{_basedir}/perl5/*

%changelog
* Sun Apr 11 2010 - Milan Jurik
- adding missing build deps
* Mon Jan 12 2009 - alfred.peng@sun.com
- Initial version
