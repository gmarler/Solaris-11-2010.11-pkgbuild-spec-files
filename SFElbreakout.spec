#
# spec file for package SFElbreakout
#
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_version 010315

Name:		SFElbreakout
Summary:	LBreakout is a breakout-style arcade game in the manner of Arkanoid.
Version:	0.10315
Source:		%{sf_download}/lgames/lbreakout-%{src_version}.tar.gz
URL:		http://lgames.sourceforge.net/index.php?project=LBreakout
Group:		Amusements/Games
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{src_version}-build

%include default-depend.inc
Requires: SUNWcsu
Requires: SUNWlibsdl
BuildRequires: SUNWlibsdl-devel

%prep
%setup -q -n lbreakout-%{src_version}

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%{gcc_cxx_optflags}"
export LDFLAGS="%{_ldflags}"
mkdir -p $RPM_BUILD_ROOT/var/lib/games
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} 
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*


%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, other) /var/lib
%dir %attr (0755, root, other) /var/lib/games
/var/lib/games/*


#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1/*

%changelog
* Mon May 17 2010 - Milan Jurik
- cleanup of spec and dependencies 
* Wed Feb  6 pradhap (at) gmail.com
- Initial lbreakout spec file.

