#
# spec file for package SFEdangerdeep.spec
#
# includes module(s): dangerdeep
#
%include Solaris.inc

%define src_name	dangerdeep
%define src_url		http://jaist.dl.sourceforge.net/sourceforge/%{src_name}
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                   SFEdangerdeep
Summary:                Danger from the Deep Game
Version:                0.3.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Source2:		%{src_url}/%{src_name}-data-%{version}.zip
Patch1:			dangerdeep-01-sconstruct.diff
Patch2:			dangerdeep-02-backtrace.diff
Patch3:			dangerdeep-03-isfinite.diff
Patch4:			dangerdeep-04-filenames.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEscons
BuildRequires: SFEgcc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net
BuildRequires: SFEfftw-devel
Requires: SFEfftw

%package devel
Summary:                 dangerdeep - developer files, /usr
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS=" -O4 "
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export CXX=/usr/gnu/bin/g++
export CXXFLAGS=" -O4 "
%if %option_with_fox
export CXXFLAGS="$CXXFLAGS -I/usr/X11/include"
%endif
export LD_OPTIONS="-i -zdirect -L/usr/gnu/lib -R/usr/gnu/lib"

rm -rf $RPM_BUILD_ROOT
scons installbindir=$RPM_BUILD_ROOT%{_bindir} datadir=%{_datadir}/dangerdeep install -j$CPUS

%install
(  
	mkdir -p $RPM_BUILD_ROOT%{_datadir}
	cd $RPM_BUILD_ROOT%{_datadir}
	unzip -x %SOURCE2
	mv data dangerdeep
	IFS=:
	find . -name '* *' | while read x ; do
		FIXED="$( echo $x | sed 's/ /_/g')"
		mv "$x" "$FIXED"
	done
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dangerdeep

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Bump to 0.3.0. Enable building with SFElibsdl or SFEsdl.
* Mon Apr 23 2006 - dougs@truemail.co.th
- Initial version
