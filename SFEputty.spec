#
# spec file for package SFEputty
#
# use gcc to compile
# works: snv104 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22
# works: snv104 / pkgbuild 1.2.0  / Sun C 5.9 SunOS_i386 Patch 124868-02 2007/11/27
# works: snv103 / pkgbuild 1.3.0  / Sun C 5.9 SunOS_i386 Patch 124868-02 2007/11/27
# works: snv96  / pkgbuild 1.3.1  / Sun Ceres C 5.10 SunOS_i386 2008/07/10


%define CC gcc

%include Solaris.inc
Name:                    SFEputty
Summary:                 putty - A graphical SSH Client
URL:                     http://www.chiark.greenend.org.uk/~sgtatham/putty/
Version:                 0.60
Source:                  http://the.earth.li/~sgtatham/putty/latest/putty-%{version}.tar.gz
Patch1:			 putty-01-gtk.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

##TODO## all Requirements
BuildRequires: CBEenv
# if your are < b134
#Requires:	SUNWGtk
#Requires:	SUNWGlib
Requires:	library/desktop/gtk1
Requires:	library/glib1


%prep
%setup -q -n putty-%version
%patch1 -p1

%build

export CC=gcc
export CXX=g++
#be carefull *not* to set wired LDFLAGS in your compile-environment!
export LDFLAGS="${LDFLAGS} -lsocket -lxnet -L/usr/sfw/lib -R/usr/sfw/lib"
export INSTALL="`pkgparam CBEenv BASEDIR`/bin/install -c -D"


cd unix

./configure --prefix=%{_prefix} \

make all-gtk all-cli

%install
rm -rf $RPM_BUILD_ROOT
cd unix
make install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc LICENCE README CHECKLST.txt LATEST.VER
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*


%changelog
* Tue Dec 23 2008 - Thomas Wagner
- create %{_docdir} in case old pkgbuild doesn't
* Tue Dec 23 2008 - Thomas Wagner
- %doc adjusted - pkgbuild starting with 1.3.2 honours %doc and all files must be listed exactly
- make INSTALL depending of install location of pkgparam CBEenv BASEDIR
- add BuildRequires CBEenv to make sure "install" is installed
* Tue Dec 16 2008 - Gilles Dauphin
- remove %doc , files does not exits
* Fri Jan 04 2008 - Thomas Wagner
- remove l10n package definition, remove debug call to bash
* Fri Jan 04 2008 - Thomas Wagner
- add patch1 emailed by Takao.Fujiwara@Sun.COM (16 Nov 2007, putty-xx-my-build.diff)
* Fri July 20 2007  - Thomas Wagner
- Initial spec
