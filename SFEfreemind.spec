#
# spec file for package SFEfreemind
#
# Owner: dkenny
#
%include Solaris.inc

%define src_version	0.9.0_RC_7

Name:		    SFEfreemind
Summary:	    FreeMind - free mind-mapping software.
Version:	    0.9.0.1.7
License:	    GPLv2
Group:		    Applications
Source:         http://heanet.dl.sourceforge.net/sourceforge/freemind/freemind-src-%{src_version}.tar.gz
Source1:        freemind.desktop
Patch0:         freemind-01-use_bash.diff
URL:		    http://freemind.sourceforge.net/wiki/index.php/Main_Page
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:	    %{_tmppath}/%{name}-%{src_version}-build
BuildRequires:  SUNWant
BuildRequires:  SUNWj6dev
Requires:       SUNWj6rt

%include default-depend.inc

%prep
%setup -c -q -n %{name}-%{src_version} 
cd  freemind
%patch0 -p1

%build
cd  freemind
ant build


%install
rm -rf $RPM_BUILD_ROOT/
cd freemind
ant -Ddist=$RPM_BUILD_ROOT%{_libdir}/freemind dist

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s ../lib/freemind/freemind.sh $RPM_BUILD_ROOT%{_bindir}/freemind
chmod 755 $RPM_BUILD_ROOT%{_bindir}/freemind

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp images/FreeMindWindowIcon.png  $RPM_BUILD_ROOT%{_datadir}/pixmaps
chmod 644 $RPM_BUILD_ROOT%{_datadir}/pixmaps/FreeMindWindowIcon.png  

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp %{SOURCE1}  $RPM_BUILD_ROOT%{_datadir}/applications
chmod 644 $RPM_BUILD_ROOT%{_datadir}/applications/freemind.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr(-,root,bin)
%{_bindir}
%{_libdir}/freemind
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/pixmaps/FreeMindWindowIcon.png
%{_datadir}/applications/freemind.desktop

%changelog
* Sun May 09 2010 - Milan Jurik
- update to 0.9.0_RC7
* Mon Jun 16 2008 - darren.kenny@sun.com
- Initial version
