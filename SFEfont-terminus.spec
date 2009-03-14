#
# spec file for package SFEfont-terminus
#

%include Solaris.inc
Name:                    SFEfont-terminus
Summary:                 terminus - font terminus
URL:                     http://www.is-vn.bg/hamster
Version:                 4.28
Source:                  http://www.is-vn.bg/hamster/terminus-font-%{version}.tar.gz
Patch1:                  terminus-font-01-x11dir.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n terminus-font-%version
%patch1 -p1

%build

# CXXFLAGS='-library=stlport4')

PATH=$PATH:/usr/openwin/bin:/usr/X11/bin

./configure --prefix=%{_prefix}  \
            --x11dir=%{_prefix}/openwin/lib/X11/fonts/pcf

#make psf
#make txt
#make raw
make pcf


%install
rm -rf $RPM_BUILD_ROOT


make install DESTDIR=$RPM_BUILD_ROOT

#make install-acm DESTDIR=$RPM_BUILD_ROOT
#make install-psf DESTDIR=$RPM_BUILD_ROOT
#make install-uni DESTDIR=$RPM_BUILD_ROOT
#make install-ref DESTDIR=$RPM_BUILD_ROOT
#make install.raw DESTDIR=$RPM_BUILD_ROOT
#make install-raw DESTDIR=$RPM_BUILD_ROOT
make install-pcf DESTDIR=$RPM_BUILD_ROOT
#make install-12b DESTDIR=$RPM_BUILD_ROOT

#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT


### TODO: post-intall-script with cd /usr/openwin/lib/X11/fonts/pcf; mkfontdir `pwd`
###make fontdir 


%files
%defattr(-, root, bin)
%doc README
%dir %attr (0755, root, bin) %{_basedir}/X11/lib/X11/fonts
%{_basedir}/X11/lib/X11/fonts/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/consolefonts/*
%dir %attr (0755, root, other) %{_docdir}


%changelog
* Sat May 07 2009 - Thomas Wagner
- bump to 4.28
- rework patch1 new font path, adjust %files
- create %{_docdir} in case old pkgbuild doesn't
- adjust %doc files
* Sun Oct 14 2007 - laca@sun.com
- add /usr/X11/bin to PATH for FOX build
* Sat May 12 2007 - Thomas Wagner
- Initial spec
