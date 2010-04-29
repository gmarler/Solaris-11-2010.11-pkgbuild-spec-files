#
# spec file for package: SFEgreasymouse.spec
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): greasymouse

%include Solaris.inc

Name:              SFEgreasymouse
Summary:           greasymouse - mouse greaser
Version:           0.0
URL:               http://ftp.x.org/contrib/amusements/
Source:            http://ftp.x.org/contrib/amusements/greasymouse-%{version}.tar.gz
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
License:           GPLv2
SUNW_Copyright:    %{sname}.copyright
Distribution:      OpenSolaris
Vendor:            OpenSolaris Community

# OpenSolaris IPS Manifest Fields
Meta(info.upstream):            Edward Rosten <edward.rosten@stcatz.ox.ac.uk>
Meta(info.maintainer):          Matt Lewandowsky <matt@greenviolet.net>
Meta(info.classification):      org.opensolaris.category.2008:Applications/Games

%include default-depend.inc

Requires: SUNWxwplt

%description
Greasy mouse does just that. It greases your mouse - it makes it slide around 
the screen and bounce off the edges. It was supposed to serve no useful purpose
whatsoever, but unfortunately I came across a computer with a very bad mouse 
that moved very slowly. Increasing the speed setting made it move with very low
resolution, so I ran greasymouse and it worked fine.

Esentially, it calculates the speed of the mouse and keeps moving the mouse at 
that speed. It also divides the speed by a `greasyness' factor each iteration, 
so it usually slows down, unless you set the greasyness to less than unity.

%prep
%setup -c -n greasymouse-%version

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp greasymouse $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/greasymouse
%doc README
%doc(bzip2) LICENSE
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Thu Apr 29 2010 - Matt Lewandowsky <matt@greenviolet.net>
- Initial spec file.
