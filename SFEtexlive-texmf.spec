#
# NoCopyright 2009 - Gilles Dauphin 
#
#

%include Solaris.inc

%define texlive_ver	20080822

%define _texmf_dir /usr/texlive

Name:		SFEtexlive-texmf
Version:	%{texlive_ver}
Summary:	Binaries for the TeX formatting system
URL:		http://tug.org/texlive

Group:		Applications/Publishing
License:	GPLv2 and More
URL:		http://tug.org/texlive/

#Source:		http://mirror.ctan.org/systems/texlive/Source/texlive-%{texlive_ver}-source.tar.lzma
#Source:	http://rlworkman.net/pkgs/sources/12.2/texlive/texlive-20080816-source.tar.bz2
# take care it's big
Source:	http://rlworkman.net/pkgs/sources/12.2/texlive/texlive-%{texlive_ver}-texmf.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWflexlex
BuildRequires:	SUNWbison
BuildRequires:	SUNWncurses
BuildRequires:	SUNWzlib
BuildRequires:	SUNWpng
BuildRequires:	SUNWgd2
#BuildRequires:	SUNWlibSM SUNWlibICE
#Requires:	SFEteckit
#Requires:	SFEtexlive-texmf

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
cd texlive-%{version}-texmf
# keep english and french doc ( on est jamais mieux servi que par ...)
rm -rf texmf-doc/doc/bulgarian
rm -rf texmf-doc/doc/czechslovak
rm -rf texmf-doc/doc/dutch
rm -rf texmf-doc/doc/finnish
rm -rf texmf-doc/doc/german
rm -rf texmf-doc/doc/greek
rm -rf texmf-doc/doc/italian
rm -rf texmf-doc/doc/japanese
rm -rf texmf-doc/doc/korean
rm -rf texmf-doc/doc/mongolian
rm -rf texmf-doc/doc/polish
rm -rf texmf-doc/doc/portuguese
rm -rf texmf-doc/doc/russian
rm -rf texmf-doc/doc/slovak
rm -rf texmf-doc/doc/slovenian
rm -rf texmf-doc/doc/spanish
rm -rf texmf-doc/doc/thai
rm -rf texmf-doc/doc/turkish
rm -rf texmf-doc/doc/ukrainian
rm -rf texmf-doc/doc/vietnamese
# done in SFEtexlive.spec
rm texmf/dvipdfmx/dvipdfmx.cfg 
rm texmf/web2c/texmf.cnf
rm texmf/xdvi/XDvi
rm texmf/xdvi/xdvi.cfg
rm texmf-dist/scripts/tex4ht/ht.sh
rm texmf-dist/scripts/tex4ht/mk4ht.pl
#
rm texmf-dist/scripts/bengali/ebong.py
rm texmf-dist/scripts/context/ruby/texmfstart.rb
rm texmf-dist/scripts/context/stubs/unix/context
rm texmf-dist/scripts/context/stubs/unix/ctxtools
rm texmf-dist/scripts/context/stubs/unix/exatools
rm texmf-dist/scripts/context/stubs/unix/luatools
rm texmf-dist/scripts/context/stubs/unix/makempy
rm texmf-dist/scripts/context/stubs/unix/mpstools
rm texmf-dist/scripts/context/stubs/unix/mptopdf
rm texmf-dist/scripts/context/stubs/unix/mtxrun
rm texmf-dist/scripts/context/stubs/unix/mtxtools
rm texmf-dist/scripts/context/stubs/unix/pdftools
rm texmf-dist/scripts/context/stubs/unix/pdftrimwhite
rm texmf-dist/scripts/context/stubs/unix/pstopdf
rm texmf-dist/scripts/context/stubs/unix/rlxtools
rm texmf-dist/scripts/context/stubs/unix/runtools
rm texmf-dist/scripts/context/stubs/unix/texexec
rm texmf-dist/scripts/context/stubs/unix/texfind
rm texmf-dist/scripts/context/stubs/unix/texfont
rm texmf-dist/scripts/context/stubs/unix/texshow
rm texmf-dist/scripts/context/stubs/unix/textools
rm texmf-dist/scripts/context/stubs/unix/texutil
rm texmf-dist/scripts/context/stubs/unix/tmftools
rm texmf-dist/scripts/context/stubs/unix/xmltools
rm texmf-dist/scripts/dviasm/dviasm.py
rm texmf-dist/scripts/epspdf/epspdf
rm texmf-dist/scripts/epspdf/epspdftk
rm texmf-dist/scripts/glossaries/makeglossaries
rm texmf-dist/scripts/mkjobtexmf/mkjobtexmf.pl
rm texmf-dist/scripts/oberdiek/pdfatfi.pl
rm texmf-dist/scripts/pdfcrop/pdfcrop.pl
rm texmf-dist/scripts/perltex/perltex.pl
rm texmf-dist/scripts/ppower4/pdfthumb.texlua
rm texmf-dist/scripts/ppower4/ppower4.texlua
rm texmf-dist/scripts/pst-pdf/ps4pdf
rm texmf-dist/scripts/pst2pdf/pst2pdf.pl
rm texmf-dist/scripts/tex4ht/htcontext.sh
rm texmf-dist/scripts/tex4ht/htlatex.sh
rm texmf-dist/scripts/tex4ht/htmex.sh
rm texmf-dist/scripts/tex4ht/httex.sh
rm texmf-dist/scripts/tex4ht/httexi.sh
rm texmf-dist/scripts/tex4ht/htxelatex.sh
rm texmf-dist/scripts/tex4ht/htxetex.sh
rm texmf-dist/scripts/texcount/TeXcount.pl
rm texmf-dist/scripts/thumbpdf/thumbpdf.pl
rm texmf-dist/scripts/vpe/vpe.pl
rm texmf/doc/bibtex8/00readme.txt
rm texmf/doc/bibtex8/HISTORY
rm texmf/doc/bibtex8/csfile.txt
rm texmf/doc/bibtex8/file_id.diz
rm texmf/doc/tetex/TETEXDOC.pdf
rm texmf/doc/tetex/teTeX-FAQ
rm texmf/dvips/base/color.pro
rm texmf/dvips/base/crop.pro
rm texmf/dvips/base/finclude.pro
rm texmf/dvips/base/hps.pro
rm texmf/dvips/base/special.pro
rm texmf/dvips/base/tex.pro
rm texmf/dvips/base/texc.pro
rm texmf/dvips/base/texps.pro
rm texmf/dvips/gsftopk/render.ps
rm texmf/scripts/a2ping/a2ping.pl
rm texmf/scripts/epstopdf/epstopdf.pl
rm texmf/scripts/pkfix/pkfix.pl
rm texmf/scripts/ps2eps/ps2eps.pl
rm texmf/scripts/simpdftex/simpdftex
rm texmf/scripts/tetex/e2pall.pl
rm texmf/scripts/tetex/texdoctk.pl
rm texmf/scripts/texlive/getnonfreefonts.pl
rm texmf/scripts/texlive/rungs.tlu
rm texmf/scripts/texlive/texdoc.tlu
rm texmf/texconfig/README
rm texmf/texconfig/g/generic
rm texmf/texconfig/generic
rm texmf/texconfig/tcfmgr
rm texmf/texconfig/tcfmgr.map
rm texmf/texconfig/v/vt100
rm texmf/texconfig/x/xterm
rm texmf/web2c/mktex.opt
rm texmf/web2c/mktexdir
rm texmf/web2c/mktexdir.opt
rm texmf/web2c/mktexnam
rm texmf/web2c/mktexnam.opt
rm texmf/web2c/mktexupd
rm texmf/xdvi/pixmaps/toolbar.xpm
rm texmf/xdvi/pixmaps/toolbar2.xpm
# keep here
# texmf/scripts/texlive/tlmgr.pl
# texmf/web2c/fmtutil.cnf



%install
rm -rf ${RPM_BUILD_ROOT}
cd texlive-%{version}-texmf

mkdir -p ${RPM_BUILD_ROOT}/usr/texlive
mv * ${RPM_BUILD_ROOT}/usr/texlive

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr (-,root,bin)
%dir %attr (0755, root, sys) /usr
# config files
%dir %attr (0755, root, bin) %{_texmf_dir}
%{_texmf_dir}/*

%changelog
* Aug 2009 - Gilles Dauphin
- Initial setup .
