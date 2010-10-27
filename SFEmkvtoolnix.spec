#
# spec file for package SFEmkvtoolnix
#
# includes module: mkvtoolnix
#

################################################################################
###									     ###
###				  EXPERIMENTAL				     ###
###									     ###
### The main functionality of MKVtoolNix - to create Matroska files	     ###
### containing H.264 video streams from avi files or from raw x264 video     ###
### files - is absent.  This is because mkvmerge CRASHES with a	segmentation ###
### fault when it attempts to read H.264 streams from such files.	     ###
### Otherwise, everything else seems to work.  Thus, mkvmerge is able to     ###
### remux H.264 video from Matroska or mp4 files.			     ###
###									     ###
### It is hoped that a proficient C++ programmer will be able to find and    ###
### fix this bug in mkvmerge.						     ###
###									     ###
### Bug report: https://www.bunkus.org/bugzilla/show_bug.cgi?id=567	     ###
################################################################################

# NOTE: This must be built using Solaris Studio 12.2, since the compiler
# option "=-library=stdcxx4" used by the spec is new to that release.

# NOTE: The current version of the boost-stdcxx spec file must be modified to
# to use Boost 1.44.  This is because with version 1.43, the filessystem library
# does not get built.
# The reason SFEboost-stdcxx is used instead of SFEboost is that the filesystem
# library is apparently broken when it is linked against stlport.

# NOTE: Compilation using g++ is not an option at this point, since MKVtoolNix
# links against the icu (International Components for Unicode) library.

# The mkvtoolnix-01-git-version.diff patch brings MKVtoolNix up to the Git
# version as of 2010-09-28.  Version 4.3.0 does not build on Solaris.

%include Solaris.inc

%define srcname mkvtoolnix

Name:		SFEmkvtoolnix
Summary:	Tools for the Matroska video container
URL:		http://www.bunkus.org/videotools/mkvtoolnix
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	4.3.0
License:	GPL
Source:		http://www.bunkus.org/videotools/mkvtoolnix/sources/%{srcname}-%{version}.tar.bz2
Patch1:		mkvtoolnix-01-git-version.diff.bz2
Patch2:		mkvtoolnix-02-rakefile.diff
Patch3:		mkvtoolnix-03-rmff.diff
Patch4:		mkvtoolnix-04-mpegparser.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: runtime/ruby-18

Requires: SFElibebml
Requires: SFElibmatroska
Requires: SFEboost-stdcxx
Requires: expat
Requires: zlib
Requires: ogg-vorbis
Requires: flac

%description

MKVToolnix is a set of tools to create, alter and inspect Matroska files under
Linux, other Unices and Windows. They do for Matroska what the OGMtools do for
the OGM format and then some.

MKVToolnix consists of the tools mkvmerge, mkvinfo, mkvextract, and mkvpropedit.

%prep
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export USER_CXXFLAGS="-g -library=stdcxx4 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ \
-D_POSIX_PTHREAD_SEMANTICS -erroff=identexpected"
export OPTIMIZATION_CFLAGS=""
export USER_LDFLAGS=-library=stdcxx4 

CXXFLAGS=$USER_CXXFLAGS LDFLAGS=$USER_LDFLAGS ./configure --prefix=%{_prefix}
./drake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

rake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%attr (0755, root, other) %{_datadir}/locale
%{_datadir}/mkvtoolnix


%changelog
* Sun Oct 10 2010 - Alex Viskovatoff
- Initial spec
