#
# spec file for package SFEunclutter
#
# includes module(s): unclutter
#
%include Solaris.inc

Name:		SFEunclutter
Version:	9
Summary:	Hide mouse cursor when idle
Group:		User Interface/X
License:	Public Domain
URL:		http://unclutter.sourceforge.net/
Source:		%{sf_download}/unclutter/unclutter-1.0%{version}.tar.gz
Patch1:		unclutter-01-install.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	SUNWxwplt
BuildRequires:	SUNWxwinc
BuildRequires:	SUNWxwopt

%description
Unclutter hides the mouse cursor image from the screen so that it does not
obstruct the area you are looking at. It hides the mouse cursor when it is not
moved for a specified amount of time or no buttons are pressed on the mouse.
Cursor image will be restored once the mouse is moved again.  

%prep
%setup -q -n unclutter-1.0%{version}
%patch1 -p1

%build
xmkmf
make CFLAGS="%optflags"

%install
rm -rf $RPM_BUILD_ROOT
make install-csw INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README
%{_bindir}/unclutter
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man1/unclutter.1

%changelog
* Sun Aug 08 2010
- initial spec
