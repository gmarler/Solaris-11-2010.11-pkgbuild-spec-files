#
# spec file for package SFEapch22m-proxyhtml
#
# includes module(s): apch22m-proxyhtml (Apache 2.2 mod_proxy_html)
#
%include Solaris.inc

%define apache_major 2
%define apache_minor 2
%define apache_major_minor %apache_major.%apache_minor
%define apache_dir apache%apache_major/%apache_major.%apache_minor
##TODO## set _libdir

Name:                    SFEapch22m-proxyhtml
Summary:                 apch22m-proxyhtml - Module for Apache 2.2 - mod_proxy_html - reverse proxy / proxy-html
Version:                 3.1.2
Source:                  http://apache.webthing.com/mod_proxy_html/mod_proxy_html.tar.bz2
URL:                     http://apache.webthing.com/mod_proxy_html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWapch22u
BuildRequires: SFEapch22m-xml2enc
Requires: SUNWapch22u
Requires: SFEapch22m-xml2enc

%description
make Apache 2.2 a HTML reverse html proxy and/or load balancer.
You may redirect different URLs to different target servers
like http://www.yourdomain.tld/application goes to internal http://192.168.1.100/application
and http://www.yourdomain.tld/contentmanagementsystem goes to internal http://192.168.44.200/cms

Read this tutorial: http://www.apachetutor.org/admin/reverseproxies

%prep
%setup -q -c -n apch22m-proxyhtml-%version

%build
cd mod_proxy_html

# we default to the Sun C-Compiler

export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"

%{_prefix}/%{apache_dir}/bin/apxs -I/usr/include/libxml2 -I. -S LIBEXECDIR=`pwd`/  -c -i mod_proxy_html.c


%install
rm -rf $RPM_BUILD_ROOT
cd mod_proxy_html

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/libexec
cp -p mod_proxy_html.so $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/libexec/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_prefix}/*

%changelog
* Tue Nov 24 2009 - Thomas Wagner
- inital spec verison 3.1.2
