#
# spec file for package SFErtorrent
#
# includes module(s): rtorrent
#
%include Solaris.inc

# Studio support is experimental
#%define cc_is_gcc 1

%include base.inc

%use rtorrent = rtorrent.spec
%use rlibtorrent = rlibtorrent.spec

Name:		SFErtorrent
Summary:	%{rtorrent.summary}
Version:	%{rtorrent.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %cc_is_gcc
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
%else
Requires: SUNWsigcpp
BuildRequires: SUNWsigcpp-devel
%endif
Requires: SFExmlrpc-c
BuildRequires: SFExmlrpc-c-devel
Requires: SUNWcurl
Requires: SUNWncurses
BuildRequires: SUNWncurses-devel

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%rlibtorrent.prep -d %name-%version/%{base_arch}
%rtorrent.prep -d %name-%version/%{base_arch}

%build
LIBTORRENT_ROOT=%{_builddir}/%name-%version/%{base_arch}/%{rlibtorrent.name}-%{rlibtorrent.version}
%if %cc_is_gcc
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags} \
 -I%{sfw_inc} -I/usr/include/ncurses -I$LIBTORRENT_ROOT/src"
export LDFLAGS="%_ldflags %{sfw_lib_path} %{gnu_lib_path} \
 -L%{_cxx_libdir} -R%{_cxx_libdir} -L$LIBTORRENT_ROOT/src/.libs"
%else
# __attribute__((unused)) test uses $CC
export CC="$CXX"
# Need -xO2 to work around some sigc++ issues
export CXXFLAGS="%cxx_optflags -xO2 \
 -I%{sfw_inc} -I/usr/include/ncurses -I$LIBTORRENT_ROOT/src"
export LDFLAGS="%_ldflags %{sfw_lib_path} %{gnu_lib_path} \
 -L$LIBTORRENT_ROOT/src/.libs"
%endif

export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig:%{_sfw_libdir}/pkgconfig:$LIBTORRENT_ROOT"
%rlibtorrent.build -d %name-%version/%{base_arch}
%if %cc_is_gcc
%else
# Need -xO2 to work around some sigc++ issues
export CXXFLAGS="%cxx_optflags -xO1 \
 -I%{sfw_inc} -I/usr/include/ncurses -I$LIBTORRENT_ROOT/src"
%endif
%rtorrent.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%rtorrent.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rtorrent
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/rtorrent.1

%changelog
* Fri Jul 04 2008 - trisk@acm.jhu.edu
- Fix gcc compilation
* Tue Jun 24 2008 - trisk@acm.jhu.edu
- Allow building with Studio
- Rename SFExmlrpc-c-gpp dependency, add SUNWsigcpp
* Sat May 24 2008 - trisk@acm.jhu.edu.
- Add SFExmlrpc-c-gpp dependencies
* Fri May  9 2008 - laca@sun.com
- Initial version
