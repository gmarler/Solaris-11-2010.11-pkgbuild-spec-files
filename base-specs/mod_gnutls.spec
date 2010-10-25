#
# spec file for package SFEmod-gnutls
#
# includes module(s): mod_gnutls
#

Name:		SFEmod-gnutls
Version:	0.5.6
Summary:	GnuTLS module for the Apache HTTP server
URL:		http://www.outoforder.cc/projects/apache/mod_gnutls
Source:		http://www.outoforder.cc/downloads/mod_gnutls/mod_gnutls-%{version}.tar.bz2
Source1:	mod_gnutls.conf
Patch1:		mod_gnutls-01-extra.diff
Patch2:		mod_gnutls-02-wall.diff
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n mod_gnutls-%{version}
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi

./configure --prefix=%{_prefix}	\
	--disable-static	\
	--disable-srp
make

%install
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	install -m 755 -D src/.libs/libmod_gnutls.so %{buildroot}%{_prefix}/apache2/2.2/libexec/%{_arch64}/mod_gnutls.so
else
	install -m 755 -D src/.libs/libmod_gnutls.so %{buildroot}%{_prefix}/apache2/2.2/libexec/mod_gnutls.so
fi
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/apache2/2.2/conf.d/mod_gnutls.conf
install -d -m 0700 %{buildroot}%{_localstatedir}/cache/mod_gnutls

%clean
rm -rf %{buildroot}

%changelog
* Mon Oct 25 2010 - Milan Jurik
- initial spec based on Fedora
