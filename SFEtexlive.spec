#
# NoCopyright 2009 - Gilles Dauphin 
#
#

%include Solaris.inc

%define texlive_ver	20080816

%define _texmf_dir /usr/texlive

Name:		SFEtexlive
Version:	%{texlive_ver}
Summary:	Binaries for the TeX formatting system
URL:		http://tug.org/texlive

Group:		Applications/Publishing
License:	GPLv2 and More
URL:		http://tug.org/texlive/

#Source:		http://mirror.ctan.org/systems/texlive/Source/texlive-%{texlive_ver}-source.tar.lzma
Source:	http://rlworkman.net/pkgs/sources/12.2/texlive/texlive-20080816-source.tar.bz2
# take care it's big
Source1:	http://rlworkman.net/pkgs/sources/12.2/texlive/texlive-20080822-texmf.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWflexlex
BuildRequires:	SUNWbison
BuildRequires:	SUNWncurses
BuildRequires:	SUNWzlib
BuildRequires:	SUNWpng
BuildRequires:	SUNWgd2
Requires:	SFEtexlive-texmf

%description
TeXLive is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
printable file as output. Usually, TeX is used in conjunction with
a higher level formatting package like LaTeX or PlainTeX, since TeX by
itself is not very user-friendly.

Install texlive if you want to use the TeX text formatting system. Consider
to install texlive-latex (a higher level formatting package which provides
an easier-to-use interface for TeX).

The TeX documentation is located in the texlive-doc package.

%prep
%setup -q -c -n %{name}-%{version}

%build
set -x
cd texlive-%{version}-source
#TL_WORKDIR=Work
# equiv. --prefix=%{prefix} in configure
# @ install do DESTDIR=make install DESTDIR=$RPM_BUILD_ROOT
#TL_INSTALL_DEST=%{_prefix}/texlive
#export TL_INSTALL_DEST
CFLAGS="$CFLAGS -DZZIP_inline= "
export CFLAGS
TL_TARGET=all
export TL_TARGET
#TODO look at utils/dialog,ps2eps,pdfopen and process DESTDIR in a Makefile.am...
./Build \
	--enable-shared=no \
	--with-x \
	--with-system-ncurses \
	--with-system-zlib \
	--with-system-pnglib \
	--with-system-gd \
	--with-system-freetype2 \
	--with-freetype2-include=%{_includedir}/freetype2 \
	--with-system-t1lib \
	--without-omega \
	--without-aleph 

#	--with_dialog=no \
#	--without-ps2eps \
#	--with_psutils=no \
#	--with-tpic2pdftex=no \


%install
rm -rf ${RPM_BUILD_ROOT}
cd texlive-%{version}-source/Work

#export LD_LIBRARY_PATH=`pwd`/texk/kpathsea/.libs
mkdir -p ${RPM_BUILD_ROOT}/usr/texlive/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/texlive/lib
# don't install kpathsea
# ruse
# mv texk/kpathsea/Makefile texk/kpathsea/Makefile.save
#make install  DESTDIR=$RPM_BUILD_ROOT
make install
mv ../inst/bin/*/* ${RPM_BUILD_ROOT}/usr/texlive/bin
rmdir ../inst/bin/*
rmdir ../inst/bin
mv ../inst/lib/*/* ${RPM_BUILD_ROOT}/usr/texlive/lib
rmdir ../inst/lib/*
rmdir ../inst/lib
mv ../inst/* ${RPM_BUILD_ROOT}/usr/texlive
rm texmf/scripts/texlive/tlmgr.pl
rm texmf/web2c/fmtutil.cnf

# a temporary placeholder for texmf.cnf
#mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/texmf-local/web2c
#cp -a texk/kpathsea/texmf.cnf ${RPM_BUILD_ROOT}%{_datadir}/texmf-local/web2c

%clean
rm -rf ${RPM_BUILD_ROOT}

#%post
#%{_bindir}/texconfig-sys rehash 2> /dev/null
#[ -x /sbin/install-info ] && /sbin/install-info %{_infodir}/web2c.info.gz %{_infodir}/dir
#%{_bindir}/fmtutil-sys --all &> /dev/null
#%{_bindir}/updmap-sys --syncwithtrees &> /dev/null
#if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
#  [ -x /sbin/restorecon ] && /sbin/restorecon -R %{_texmf_var}/
#fi
#:
#############
## slack post doinst.sh
## This one shouldn't be needed, but just in case...
#chroot . /usr/share/texmf/bin/mktexlsr 1>/dev/null 2>&1
## This one is definitely needed
## What I don't know is what happens if the texlive-texmf package is
## not installed yet - maybe we need to run this from it too?
#chroot . /usr/share/texmf/bin/fmtutil-sys --all 1>/dev/null 2>&1
## This one also shouldn't be needed, but again, just in case...
#chroot . /usr/share/texmf/bin/updmap-sys --syncwithtrees 1>/dev/null 2>&1



#%post latex
#[ -x /sbin/install-info ] && /sbin/install-info %{_infodir}/latex.info.gz %{_infodir}/dir
#%{_bindir}/texconfig-sys init &> /dev/null
#%{_bindir}/texconfig-sys rehash 2> /dev/null
#%{_bindir}/fmtutil-sys --all &> /dev/null
#if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
#  [ -x /sbin/restorecon ] && /sbin/restorecon -R %{_texmf_var}/
#fi
#:


#%postun latex
#%{_bindir}/texconfig-sys rehash 2> /dev/null
#if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
#  [ -x /sbin/restorecon ] && /sbin/restorecon -R %{_texmf_var}/
#fi
#:


%files
%defattr (-,root,bin)
%dir %attr (0755, root, sys) /usr
# config files
%dir %attr (0755, root, bin) %{_texmf_dir}
%{_texmf_dir}/*

%changelog
* 17 Aug 2009 - Gilles Dauphin
- check with texmf files.
* Aug 2009 - Gilles Dauphin
- Initial setup, I look at Fedora and Pkgsrc
