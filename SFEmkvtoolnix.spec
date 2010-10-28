#
# spec file for package SFEmkvtoolnix
#
# includes module: mkvtoolnix
#

# NOTE: This must be built using Solaris Studio 12.2, since the compiler
# option "-library=stdcxx4" used by the spec is new to that release.

# NOTE: The current version of the boost-stdcxx spec file must be modified to
# use Boost 1.44.  This is because with version 1.43, the filessystem library
# does not get built.
# The reason SFEboost-stdcxx is used instead of SFEboost is that the filesystem
# library is apparently broken when it is linked against stlport.

# TODO: Get mmg (the GUI front end) to build

%include Solaris.inc
%define srcname mkvtoolnix

Name:		SFEmkvtoolnix
Summary:	Tools for the Matroska video container
URL:		http://www.bunkus.org/videotools/mkvtoolnix
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	4.3.0
License:	GPLv2
Source:		http://www.bunkus.org/videotools/%srcname/sources/%{srcname}-%{version}.tar.bz2
Patch1:		mkvtoolnix-01-git-version.diff.bz2
Patch2:		mkvtoolnix-02-guide-install.diff
Patch3:		mkvtoolnix-03-rmff.diff
Patch4:		mkvtoolnix-04-mpegparser.diff
Patch5:		mkvtoolnix-05-bug-567-patch.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWruby18r

Requires: SFElibebml
Requires: SFElibmatroska
Requires: SFEboost-stdcxx
Requires: SUNWlexpt
Requires: SUNWzlib
Requires: SUNWogg-vorbis
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
# Bring MKVToolnix up to the Git version as of 2010-09-28.
# Version 4.3.0 does not build on Solaris.
%patch1 -p1
# Based on https://build.opensuse.org/package/view_file?file=mkvtoolnix-4.3.0-guide_install.patch&package=mkvtoolnix&project=multimedia%3Aapps&srcmd5=6156e051db15cd8c196f83e4877192df#
# Also removes GNU compiler warning flags
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export USER_CXXFLAGS="-library=stdcxx4 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ \
-D_POSIX_PTHREAD_SEMANTICS -erroff=identexpected,badargtype2w,storenotokw"
export OPTIMIZATION_CFLAGS=-xO4
export USER_LDFLAGS=-library=stdcxx4

CXXFLAGS=$USER_CXXFLAGS LDFLAGS=$USER_LDFLAGS ./configure --prefix=%{_prefix}
./drake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

./drake install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
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
* Thu Oct 21 2010 - Alex Viskovatoff
- Add patch kindly provided by Moritz Bunkus to fix runtime bug (number 567)
- Move out of experimental
* Sun Oct 10 2010 - Alex Viskovatoff
- Initial spec
