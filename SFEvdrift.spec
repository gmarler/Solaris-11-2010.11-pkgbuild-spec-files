#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define        year       2009
%define        month      06
%define        day        15 

#
# Due to a bug to run first 'unset LANG' for running the vdrift
#

# Download manually
%define src_url http://downloads.sourceforge.net/vdrift

# If SFEasio is not install. Make sure all files are installed
%define SFEasio	%(/usr/bin/pkginfo -q SFEasio && echo 1 || echo 0)

Name:                SFEvdrift
Summary:             VDrift is a cross-platform, open source driving simulation made with drift racing in mind
Version:             %{year}.%{month}.%{day}
IPS_component_version: %{year}%{month}%{day}
License:             http://www.gnu.org/copyleft/gpl.html
Source:              %{src_url}/vdrift-%{year}-%{month}-%{day}-src.tar.bz2
Patch1:		     vdrift-01-ncpu.diff
Patch2:		     vdrift-02-opt.diff
URL:                 https://sourceforge.net/projects/vdrift/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEboost-gpp
Requires: SFEasio-gpp
Requires: SFEopenal
# Currently in pending repository
Requires: glew

%prep
%setup -q -n vdrift-%{year}-%{month}-%{day}
%patch1 -p1 
%patch2 -p1 
mv data/cars/TC6/_tc6\ performance\ notes.txt data/cars/TC6/tc6_performance_notes.txt

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%gcc_optflags"
export CXXFLAGS="%gcc_cxx_optflags"
export LD_OPTIONS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} -lGL -lsocket -lnls"

scons prefix=%{_prefix} os_cxxflags=1 release=1 -j 4

%install
export CC=gcc
export CXX=g++
export CFLAGS="%gcc_optflags"
export CXXFLAGS="%gcc_cxx_optflags"
export LD_OPTIONS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} -lGL -lsocket -lnls"
rm -rf $RPM_BUILD_ROOT
scons install release=1 prefix=%{_prefix} destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/games

%changelog
* Tue Sep 08 2009 - drdoug007@gmail.com
- Initial version
