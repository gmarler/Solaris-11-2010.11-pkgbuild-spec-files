#
# spec file for package SFEmkvtoolnix
#
# includes module: mkvtoolnix
#

# SFEboost-stdcxx is used instead of SFEboost because the filesystem
# library is apparently broken when it is linked against stlport4.

# TODO: Get mmg (the GUI front end) to build

%include Solaris.inc
%define srcname mkvtoolnix
%define with_SUNWruby %(pkginfo -q SFEruby && echo 0 || echo 1)

Name:		SFEmkvtoolnix
Summary:	Tools for the Matroska video container
URL:		http://www.bunkus.org/videotools/mkvtoolnix
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	4.4.0
License:	GPLv2
Source:		http://www.bunkus.org/videotools/%srcname/sources/%{srcname}-%{version}.tar.bz2
# Based on https://build.opensuse.org/package/view_file?file=mkvtoolnix-4.3.0-guide_install.patch&package=mkvtoolnix&project=multimedia%3Aapps&srcmd5=6156e051db15cd8c196f83e4877192df#
# Also removes GNU compiler warning flags
Patch2:		mkvtoolnix-02-guide-install.diff
Patch3:		mkvtoolnix-03-rmff.diff
Patch4:		mkvtoolnix-04-mpegparser.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %with_SUNWruby
BuildRequires: SUNWruby18r
%endif

BuildRequires: SFElibebml-devel
Requires: SFElibebml
BuildRequires: SFElibmatroska-devel
Requires: SFElibmatroska
BuildRequires: SFEboost-stdcxx-devel
Requires: SFEboost-stdcxx
BuildRequires: SUNWlexpt
Requires: SUNWlexpt
BuildRequires: SUNWzlib
Requires: SUNWzlib
BuildRequires: SUNWogg-vorbis
Requires: SUNWogg-vorbis
BuildRequires: SUNWflac
Requires: SUNWflac

%description

MKVToolnix is a set of tools to create, alter and inspect Matroska files under
Linux, other Unices and Windows. They do for Matroska what the OGMtools do for
the OGM format and then some.

MKVToolnix consists of the tools mkvmerge, mkvinfo, mkvextract, and mkvpropedit.

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
%setup -q -n %srcname-%version
%patch2 -p0
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export USER_CXXFLAGS="%cxx_optflags -library=stdcxx4 \
  -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -D_POSIX_PTHREAD_SEMANTICS \
  -erroff=identexpected,badargtype2w,storenotokw"
export USER_LDFLAGS="%_ldflags -library=stdcxx4 -L/usr/stdcxx/lib -R/usr/stdcxx/lib"

CXXFLAGS=$USER_CXXFLAGS LDFLAGS=$USER_LDFLAGS ./configure --prefix=%_prefix \
--with-extra-includes=/usr/stdcxx/include --with-boost-libdir=/usr/stdcxx/lib
./drake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

./drake install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/locale
rm -rf $RPM_BUILD_ROOT%_docdir/%srcname/guide/zh_CN
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir
%dir %attr (-, root, sys) %_datadir
%_mandir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (-, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Sun Nov 21 2010 - Alex Viskovatoff
- Update to 4.4.0, with two patches no longer required
- Accommodate to stdcxx libs and headers residing in /usr/stdcxx
- Do not use -library=stdcxx4, which Sun Studio 12u1 does not understand
* Thu Oct 21 2010 - Alex Viskovatoff
- Add patch kindly provided by Moritz Bunkus to fix runtime bug (number 567)
- Move out of experimental
* Sun Oct 10 2010 - Alex Viskovatoff
- Initial spec
