#
# spec file for package SFEgajim.spec
#
# includes module(s): gajim
#

%include Solaris.inc

Name:		SFEgajim
Summary:	Gajim Jabber client
Group:		Applications/Internet
Version:	0.14.1
URL:		http://www.gajim.org/
Source:		http://www.gajim.org/downloads/0.14/gajim-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWPython26
Requires:	SUNWgtkspell
BuildRequires:	SUNWPython26-devel
BuildRequires:	SUNWgtkspell-devel
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWperl-xml-parser

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n gajim-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"


./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# REMOVE doc FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/gajim/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*
%{_mandir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Dec 04 2010 - Milan Jurik
- update to 0.14.1, move to python 2.6
* Sat Mar 23 2008 - nicolas@slubman.info
- Bumped version
* Wed Oct 11 2006 - laca@sun.com
- add gtkspell deps
* Wed Jul 26 2006 - lin.ma@sun.com
- Initial spec file
