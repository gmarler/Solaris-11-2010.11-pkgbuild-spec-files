#
# spec file for package SFEatomix
#
# includes module(s): atomix
#
%include Solaris.inc

Name:                    SFEatomix
Group:                   applications/games
Summary:                 Atomix - puzzle game in which you build molecules from atoms
Version:                 2.14.0
Source:                  http://download.gnome.org/sources/atomix/2.14/atomix-%{version}.tar.gz
Patch1:                  atomix-01-Wall.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWlibms
Requires: SUNWlxml
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%endif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWperl-xml-parser
BuildRequires: SUNWgnome-common-devel


%prep
%setup -q -n atomix-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --localstatedir=%{_localstatedir}   \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_localstatedir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/atomix
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/gnome-2.0
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Sun May 09 2010 - Milan Jurik
- added missing build dependency
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEatomix
- change to root:bin to follow other JDS pkgs.
* Fri Mar 10 2006 - laca@sun.com
- Initial spec
