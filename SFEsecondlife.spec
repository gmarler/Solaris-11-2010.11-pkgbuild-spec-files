#
# spec file for package SFEsecondlife
#
# includes module(s): secondlife
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
%define tarball_version 1.23.4-r124025

Name:                    SFEsecondlife
Group:                   Libraries/Multimedia
Version:                 1.23.4
Vendor:                  Sun Microsystems, Inc.
Summary:                 SecondLife Client
URL:			 http://wiki.secondlife.com/wiki/Source_archive
Source:                  http://secondlife.com/developers/opensource/downloads/2009/06/slviewer-src-viewer-%{tarball_version}.tar.gz
Source2:                 http://secondlife.com/developers/opensource/downloads/2009/06/slviewer-artwork-viewer-%{tarball_version}.zip
Source3:                 http://secondlife.com/developers/opensource/downloads/2009/06/slviewer-linux-libs-viewer-%{tarball_version}.tar.gz
Source4:                 secondlife
Patch1:                  secondlife-01-solaris.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

BuildRequires: SUNWPython26-devel
Requires: SUNWPython26
BuildRequires: SUNWdbus-glib-devel
Requires: SUNWdbus-glib
BuildRequires: SUNWgnome-media-devel
Requires: SUNWgnome-media
BuildRequires: SUNWglib2-devel
Requires: SUNWglib2
BuildRequires: SUNWgtk2-devel
Requires: SUNWgtk2
BuildRequires: SUNWcairo-devel
Requires: SUNWcairo
BuildRequires: SUNWlibatk-devel
Requires: SUNWlibatk
BuildRequires: SUNWpango-devel
Requires: SUNWpango
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SFEc-ares-devel
Requires: SFEc-ares
BuildRequires: SFEopenjpeg
Requires: SFEopenjpeg
BuildRequires: SFExmlrpc-epi-devel
Requires: SFExmlrpc-epi
BuildRequires: SFEbdb
Requires: SFEbdb

# SecondLife uses the GCC compiled version of the boost mt libraries.
BuildRequires: SFEboost-gpp-devel
Requires: SFEboost-gpp
BuildRequires: SFEboost-gpp-mt-devel
Requires: SFEboost-gpp-mt

# This will not build if the Sun Studio verison of boost is installed.
BuildConflicts: SFEboost-devel
BuildConflicts: SFEboost

%include default-depend.inc

%prep
%setup -q -n linden
%patch1 -p1
cd ..
unzip %{SOURCE2}
gunzip -c %{SOURCE3} | tar xf -

%build
export BOOST_LIBRARYDIR=/usr/lib/g++/3.4.3
export BOOST_INCLUDEDIR=/usr/sfw/include/c++/3.4.3
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"

# Need to add location of boost libraries (/usr/lib/g++/3.4.3).  For some
# reason, passing in BOOST_LIBRARYDIR does not seem to work even though
# /usr/share/cmake-2.6/Modules/FindBoost claims it should.
export LDFLAGS="%{_ldflags} -L%{_cxx_libdir} -R%{_cxx_libdir}"

cd indra
./develop.py clean
./develop.py
./develop.py build

%install

rm -rf $RPM_BUILD_ROOT

# The below steps seem wrong.  I suspect that the Manifest file is not being
# set up properly, so that the needed files are not being copied into the
# packaged directory.  But, assembling the files by hand like the following
# seems to sort of work.

mkdir $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/secondlife

cd indra/build-solaris*/newview/packaged
tar -cf - * | (cd $RPM_BUILD_ROOT/%{_libdir}/secondlife; tar xf -)
cd ../../../..
cd indra/newview
tar -cf - app_settings | (cd $RPM_BUILD_ROOT/%{_libdir}/secondlife; tar xf -)
tar -cf - character | (cd $RPM_BUILD_ROOT/%{_libdir}/secondlife; tar xf -)
tar -cf - fonts | (cd $RPM_BUILD_ROOT/%{_libdir}/secondlife; tar xf -)
tar -cf - skins | (cd $RPM_BUILD_ROOT/%{_libdir}/secondlife; tar xf -)

cd ../..
cp scripts/messages/message_template.msg $RPM_BUILD_ROOT/%{_libdir}/secondlife/app_settings
cp indra/newview/featuretable.txt $RPM_BUILD_ROOT/%{_libdir}/secondlife
cp indra/newview/featuretable_solaris.txt $RPM_BUILD_ROOT/%{_libdir}/secondlife
cp indra/newview/gpu_table.txt $RPM_BUILD_ROOT/%{_libdir}/secondlife

cp %{SOURCE4} $RPM_BUILD_ROOT/%{_bindir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0555, root, bin) %{_bindir}/secondlife
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/secondlife
%{_libdir}/secondlife/*

%changelog
* Fri Jan 29 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.7.0.
