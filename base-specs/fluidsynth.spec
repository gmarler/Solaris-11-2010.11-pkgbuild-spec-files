Summary:	A real-time software synthesizer based on SoundFont 2 specifications.
Name:		fluidsynth
Version:	1.1.1
License:	LGPL
Group:		Sound
Source:		http://download.savannah.gnu.org/releases/fluid/%{name}-%{version}.tar.gz
Patch1:		fluidsynth-01-Wall.diff
Patch2:		fluidsynth-02-oss.diff
URL:		http://www.fluidsynth.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags" 

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export LDFLAGS="$LDFLAGS -Wl,-64"
fi


autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir}
make

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/libquicktime/lib*.*a

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi

%changelog
* Wed May 05 2010 Milan Jurik
- Initial import to SFE
* Mon Aug 25 2003 Josh Green <jgreen@users.sourceforge.net>
- Created initial fluidsynth.spec.in
