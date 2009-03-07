#
# spec file for package SFEpidgin-musictracker
#

%include Solaris.inc

Name:                    SFEpidgin-musictracker
Summary:                 Now playing plugin for pidgin
Group:                   System/GUI/GNOME
Version:                 0.4.16
Source:                  http://pidgin-musictracker.googlecode.com/files/pidgin-musictracker-%{version}.tar.bz2
Patch1:                  pidgin-musictracker-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-im-client
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWgnome-im-client

%prep
rm -rf %name_%version
%setup -q -n pidgin-musictracker-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -xc99" 
export LDFLAGS="%_ldflags       "

touch README

#aclocal -I m4
#automake -a -f
#autoconf -f

./reconf

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --disable-werror

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/pidgin/*.*a
rm -rf $RPM_BUILD_ROOT/%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Oct 29 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
