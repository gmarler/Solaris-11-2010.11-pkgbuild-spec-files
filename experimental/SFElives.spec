#
# spec file for package SFElives.spec
#
# includes module(s): lives
#
%include Solaris.inc

%define src_name	LiVES
%define src_url		http://www.xs4all.nl/~salsaman/lives/current

Name:                   SFElives
License:		GPL v3
Summary:                Video Editing System
Version:                1.1.2
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			lives-01-fionread.diff
Patch2:			lives-02-w_memcpy.diff
Patch3:			lives-03-defines.diff
Patch4:			lives-04-inline.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	SFEmplayer
BuildRequires:	SUNWjpg-devel
Requires:	SUNWjpg
BuildRequires:	SFEsox-devel
Requires:	SFEsox
Requires:	SUNWimagick
Requires:	SFEjack
BuildRequires:	SFEjack-devel
Requires:	SFEmjpegtools

%prep
%setup -q -n lives-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


LDFLAGS="-lsocket -lresolv -lnsl"	\
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_bindir}/lives
cd $RPM_BUILD_ROOT/%{_bindir}/ && ln -s lives-exe lives
cd $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_datadir} && mv locale/nl_NL locale/nl && mv locale/de_DE locale/de

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/lives
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Fri Sep 18 2009 - Milan Jurik
- Initial version
