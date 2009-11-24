#
# spec file for package SFEapch22m-xml2enc
#
# includes module(s): apch22m-xml2enc (Apache 2.2 mod_xml2enc )
#
%include Solaris.inc

%define apache_major 2
%define apache_minor 2
%define apache_major_minor %apache_major.%apache_minor
%define apache_dir apache%apache_major/%apache_major.%apache_minor
##TODO## set _libdir

Name:                    SFEapch22m-xml2enc
Summary:                 apch22m-xml2enc - Module for Apache 2.2 - mod_proxy_html - reverse proxy / proxy-html
Version:                 1.0.3
Source:                  http://apache.webthing.com/svn/apache/filters/mod_xml2enc.c
Source2:                 http://apache.webthing.com/svn/apache/filters/mod_xml2enc.h
URL:                     http://apache.webthing.com/mod_xml2enc/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWapch22u
Requires: SUNWapch22u

%description
make Apache 2.2 a HTML reverse html proxy and/or load balancer.
You may redirect different URLs to different target servers
like http://www.yourdomain.tld/application goes to internal http://192.168.1.100/application
and http://www.yourdomain.tld/contentmanagementsystem goes to internal http://192.168.44.200/cms

Read this tutorial: http://www.apachetutor.org/admin/reverseproxies

%prep
#read http://www.rpm.org/max-rpm/s1-rpm-specref-macros.html
%setup -c -T 
cp -p %SOURCE .
cp -p %SOURCE2 .


%build

# we default to the Sun C-Compiler

export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"

%{_prefix}/%{apache_dir}/bin/apxs -I/usr/include/libxml2 -I. -S LIBEXECDIR=`pwd`/  -c -i mod_xml2enc.c


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/libexec
cp -p mod_xml2enc.so $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/libexec/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/include
cp -p mod_xml2enc.h $RPM_BUILD_ROOT%{_prefix}/%{apache_dir}/include/ 




%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_prefix}/*

%changelog
* Tue Nov 24 2009 - Thomas Wagner
- inital spec 1.0.3 (used by mod_proxy_html)
