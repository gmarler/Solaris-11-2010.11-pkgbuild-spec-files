#
# spec file for package SFEliveMedia
#
# includes module(s): liveMedia
#


%include Solaris.inc

#%define src_version 2009.07.09
#extract example: 2009.07.09
%define src_version %( wget  -O - "http://www.live555.com/liveMedia/public" 2>/dev/null  | /usr/xpg4/bin/egrep -i "<a href.*live\.[0-9]{4}" | sed -e 's,^.*href=\"live\.,,' -e 's,\.tar\.gz\">.*,,' )

#remove leading zero(s) from version-string for IPS compat
#version example: 2009.7.9
%define version %( /bin/echo %{src_version} | sed -e 's,\.0,.,' | sed -e 's,\.0,.,' )
##TODO## eventually build fallback solution like this: if three wget retries fail, look at SOURCES/live*tar.gz and use these numbers, volunteers welcome. To refresh one would have to just enable internet connection. To eliminate version jumps, create switch --disable-livemedia-download.


Name:                    SFEliveMedia
Summary:                 liveMedia - live555 Streaming Media
Version:                 %{version}
Source:                  http://www.live555.com/liveMedia/public/live.%{src_version}.tar.gz
Patch1:                  liveMedia-01-SOLARIS-macro.diff
Patch2:                  liveMedia-02-config.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{src_version}-build
%include default-depend.inc

BuildRequires: SUNWwgetu
BuildRequires: SUNWxcu4

%prep
%setup -q -n live
ln -s config.solaris-32bit config.solaris
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./genMakefiles solaris
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/live
gtar fcp - liveMedia/include groupsock/include UsageEnvironment/include BasicUsageEnvironment/include liveMedia/libliveMedia.so groupsock/libgroupsock.so UsageEnvironment/libUsageEnvironment.so BasicUsageEnvironment/libBasicUsageEnvironment.so  | gtar -x -v -C $RPM_BUILD_ROOT/usr/lib/live -f -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Mar 2010 - Gilles Dauphin
- sed 2 times for version for ips compat versioning.
* Thr Sep 17 2009 - Thomas Wagner
- use /usr/xpg4/bin/egrep and set BuildRequire SUNWxcu4
* Sat Aug 08 2009 - Thomas Wagner
- external wget-fetch to extract downloadversion and calculate package version
  number with leading zero(s) removed
* Sat Jul 18 - Milan Jurik
- to 2009.07.09
* Sun Jul 05 - Milan Jurik
- upgrade to 2009.06.02
* April 2009 - Gilles dauphin
- Bump to 2009.04.06
- link to config.solaris (32bits)
* Thu Mar 05 2009 - sobotkap@gmail.com
- Bump to 2009.02.23 version and polite main version tag to be 
-		compatible with IPS
* Sun Dec 21 2008 - Thomas Wagner
- bump to 2008.12.20
* Wed Oct 22 2008 - dick@nagual.nl
- bump to version 2008.10.07
* Fri Jul 31 2008 - dick@nagual.nl
- bump to version 2008.07.25
* Mon Jun 30 2008 - oninoshiko@gmail.com
- Bump to 2008.06.26 - consider mirroring since Live555 removes older versions
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- Bump to 2008.06.05 - consider mirroring since Live555 removes older versions
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2008.02.08
* Thu Dec 27 2007 - Thomas Wagner
- bump to 2007.12.27
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 2007.11.01.  Add patch2 to use /usr/gnu/bin/ld and build
- shared libraries instead of static.
* Tue Sep 04 2007 - ananth@sun.com
- Bump to 2007.08.03a
* Wed Jul 25 2007 - daymobrew@users.sourceforge.net
- Bump to 2007.07.25.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Bump to 2007.07.10.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Bump to 2007.05.24.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Bump to 2007.04.20.
* Fri Mar 30 2007 - daymobrew@users.souceforge.net
- Bump to 2007.02.20.
* Wed Jan 11 2007 - laca@sun.com
- bump to 2007.01.11
* Wed Jan  3 2007 - laca@sun.com
- bump to 2006.12.31, add patch SOLARIS-macro.diff
* Thu Dec 14 2006 - daymobrew@users.sourceforge.net
- Bump to 2006.12.08.
* Mon Nov  6 2006 - laca@sun.com
- bump to 2006.10.27
* Thu Sep 26 2006 - halton.huo@sun.com
- Bump to version 2006.09.20.
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump to version 2006.07.04.
* Fri Jun 23 2006 - laca@sun.com
- Bumped to version 2006.06.22
- updated file attributes
- renamed to SFEliveMedia
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Bumped version to 2006.05.17
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
