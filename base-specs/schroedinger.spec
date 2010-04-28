Version:        1.0.9
Summary:        Library for decoding and encoding video in the Dirac format

Group:          Applications/Multimedia
License:        LGPL/MIT/MPL
URL:            http://diracvideo.org/
Source:         http://diracvideo.org/download/schroedinger/schroedinger-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n schroedinger-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi

# found ORC if install in /opt/SFE
export PKG_CONFIG_PATH="%{_prefix}/lib/pkgconfig"

./configure --prefix=%{_prefix}                 \
            --libdir=%{_libdir}                 \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --enable-shared                     \
            --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Apr 2010 - Gilles Dauphin
- find pkg-config for ORC if in /opt/SFE
* Wed May 7 2008 Christian Schaller <christian.schaller@collabora.co.uk>
- Added Schrovirtframe.h

* Fri Feb 22 2008 David Schleef <ds@schleef.org>
- Update for 1.0

* Fri Feb 1 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- add schromotionest.h
- remove schropredict.h

* Tue Jan 22 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- Update for latest changes

* Thu Apr 05 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- Further updates.

* Thu Apr 27 2006 Christian F.K. Schaller <christian@fluendo.com>
- Updates for carid -> schroedinger change
