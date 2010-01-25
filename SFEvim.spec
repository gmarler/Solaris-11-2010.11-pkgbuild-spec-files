#
# spec file for package SFEvim.spec
#
# includes module(s): vim
#
%include Solaris.inc

%define vim_version 72
%define SPROsslnk      %(/usr/bin/pkginfo -q SPROsslnk && echo 1 || echo 0)

Name:         SFEvim
Summary:      Vim - vi improved
Version:      7.2
Release:      344
Source:       ftp://ftp.vim.org/pub/vim/unix/vim-%{version}.tar.bz2
Source1:      ftp://ftp.vim.org/pub/vim/extra/vim-%{version}-lang.tar.gz
Source2:      ftp://ftp.vim.org/pub/vim/extra/vim-%{version}-extra.tar.gz
Source3:      http://cscope.sourceforge.net/cscope_maps.vim
URL:          http://www.vim.org
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWlibms
Requires: SUNWmlib
Requires: SUNWxwrtl
Requires: SUNWTcl
Requires: SUNWPython
#Requires: SFEruby
Requires: SUNWperl584core
BuildRequires: SUNWPython-devel
# See ChangeLog for the following:
#%if %SPROsslnk
#BuildRequires: SPROsslnk
#%else
#BuildRequires: SFEcscope
#%endif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWmlibh
BuildRequires: SUNWxwinc

# Patches 001 < 999 are patches from the base maintainer.
# If you're as lazy as me, generate the list using
# for i in `seq 1 42`; do printf "Patch%03d: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.%03d\n" $i $i; done
# And don't forget to fetch them :)
# for i in `seq 1 42`; do printf "ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.%03d\n" $i; done | wget -P $HOME/packages/SOURCES --input-file=-
Patch001: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.001
Patch002: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.002
Patch003: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.003
Patch004: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.004
Patch005: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.005
Patch006: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.006
Patch007: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.007
Patch008: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.008
Patch009: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.009
Patch010: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.010
Patch011: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.011
Patch012: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.012
Patch013: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.013
Patch014: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.014
Patch015: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.015
Patch016: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.016
Patch017: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.017
Patch018: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.018
Patch019: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.019
Patch020: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.020
Patch021: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.021
Patch022: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.022
Patch023: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.023
Patch024: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.024
Patch025: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.025
Patch026: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.026
Patch027: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.027
Patch028: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.028
Patch029: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.029
Patch030: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.030
Patch031: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.031
Patch032: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.032
Patch033: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.033
Patch034: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.034
Patch035: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.035
Patch036: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.036
Patch037: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.037
Patch038: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.038
Patch039: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.039
Patch040: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.040
Patch041: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.041
Patch042: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.042
Patch043: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.043
Patch044: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.044
Patch045: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.045
Patch046: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.046
Patch047: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.047
Patch048: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.048
Patch049: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.049
Patch050: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.050
Patch051: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.051
Patch052: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.052
Patch053: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.053
Patch054: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.054
Patch055: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.055
Patch056: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.056
Patch057: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.057
Patch058: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.058
Patch059: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.059
Patch060: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.060
Patch061: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.061
Patch062: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.062
Patch063: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.063
Patch064: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.064
Patch065: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.065
Patch066: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.066
Patch067: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.067
Patch068: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.068
Patch069: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.069
Patch070: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.070
Patch071: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.071
Patch072: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.072
Patch073: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.073
Patch074: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.074
Patch075: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.075
Patch076: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.076
Patch077: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.077
Patch078: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.078
Patch079: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.079
Patch080: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.080
Patch081: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.081
Patch082: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.082
Patch083: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.083
Patch084: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.084
Patch085: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.085
Patch086: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.086
Patch087: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.087
Patch088: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.088
Patch089: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.089
Patch090: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.090
Patch091: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.091
Patch092: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.092
Patch093: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.093
Patch094: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.094
Patch095: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.095
Patch096: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.096
Patch097: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.097
Patch098: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.098
Patch099: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.099
Patch100: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.100
Patch101: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.101
Patch102: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.102
Patch103: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.103
Patch104: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.104
Patch105: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.105
Patch106: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.106
Patch107: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.107
Patch108: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.108
Patch109: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.109
Patch110: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.110
Patch111: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.111
Patch112: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.112
Patch113: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.113
Patch114: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.114
Patch115: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.115
Patch116: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.116
Patch117: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.117
Patch118: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.118
Patch119: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.119
Patch120: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.120
Patch121: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.121
Patch122: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.122
Patch123: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.123
Patch124: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.124
Patch125: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.125
Patch126: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.126
Patch127: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.127
Patch128: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.128
Patch129: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.129
Patch130: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.130
Patch131: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.131
Patch132: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.132
Patch133: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.133
Patch134: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.134
Patch135: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.135
Patch136: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.136
Patch137: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.137
Patch138: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.138
Patch139: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.139
Patch140: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.140
Patch141: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.141
Patch142: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.142
Patch143: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.143
Patch144: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.144
Patch145: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.145
Patch146: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.146
Patch147: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.147
Patch148: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.148
Patch149: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.149
Patch150: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.150
Patch151: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.151
Patch152: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.152
Patch153: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.153
Patch154: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.154
Patch155: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.155
Patch156: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.156
Patch157: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.157
Patch158: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.158
Patch159: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.159
Patch160: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.160
Patch161: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.161
Patch162: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.162
Patch163: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.163
Patch164: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.164
Patch165: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.165
Patch166: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.166
Patch167: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.167
Patch168: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.168
Patch169: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.169
Patch170: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.170
Patch171: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.171
Patch172: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.172
Patch173: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.173
Patch174: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.174
Patch175: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.175
Patch176: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.176
Patch177: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.177
Patch178: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.178
Patch179: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.179
Patch180: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.180
Patch181: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.181
Patch182: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.182
Patch183: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.183
Patch184: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.184
Patch185: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.185
Patch186: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.186
Patch187: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.187
Patch188: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.188
Patch189: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.189
Patch190: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.190
Patch191: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.191
Patch192: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.192
Patch193: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.193
Patch194: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.194
Patch195: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.195
Patch196: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.196
Patch197: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.197
Patch198: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.198
Patch199: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.199
Patch200: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.200
Patch201: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.201
Patch202: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.202
Patch203: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.203
Patch204: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.204
Patch205: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.205
Patch206: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.206
Patch207: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.207
Patch208: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.208
Patch209: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.209
Patch210: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.210
Patch211: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.211
Patch212: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.212
Patch213: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.213
Patch214: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.214
Patch215: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.215
Patch216: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.216
Patch217: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.217
Patch218: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.218
Patch219: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.219
Patch220: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.220
Patch221: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.221
Patch222: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.222
Patch223: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.223
Patch224: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.224
Patch225: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.225
Patch226: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.226
Patch227: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.227
Patch228: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.228
Patch229: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.229
Patch230: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.230
Patch231: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.231
Patch232: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.232
Patch233: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.233
Patch234: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.234
Patch235: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.235
Patch236: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.236
Patch237: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.237
Patch238: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.238
Patch239: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.239
Patch240: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.240
Patch241: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.241
Patch242: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.242
Patch243: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.243
Patch244: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.244
Patch245: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.245
Patch246: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.246
Patch247: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.247
Patch248: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.248
Patch249: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.249
Patch250: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.250
Patch251: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.251
Patch252: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.252
Patch253: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.253
Patch254: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.254
Patch255: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.255
Patch256: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.256
Patch257: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.257
Patch258: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.258
Patch259: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.259
Patch260: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.260
Patch261: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.261
Patch262: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.262
Patch263: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.263
Patch264: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.264
Patch265: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.265
Patch266: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.266
Patch267: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.267
Patch268: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.268
Patch269: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.269
Patch270: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.270
Patch271: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.271
Patch272: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.272
Patch273: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.273
Patch274: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.274
Patch275: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.275
Patch276: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.276
Patch277: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.277
Patch278: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.278
Patch279: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.279
Patch280: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.280
Patch281: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.281
Patch282: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.282
Patch283: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.283
Patch284: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.284
Patch285: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.285
Patch286: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.286
Patch287: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.287
Patch288: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.288
Patch289: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.289
Patch290: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.290
Patch291: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.291
Patch292: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.292
Patch293: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.293
Patch294: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.294
Patch295: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.295
Patch296: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.296
Patch297: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.297
Patch298: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.298
Patch299: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.299
Patch300: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.300
Patch301: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.301
Patch302: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.302
Patch303: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.303
Patch304: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.304
Patch305: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.305
Patch306: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.306
Patch307: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.307
Patch308: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.308
Patch309: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.309
Patch310: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.310
Patch311: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.311
Patch312: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.312
Patch313: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.313
Patch314: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.314
Patch315: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.315
Patch316: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.316
Patch317: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.317
Patch318: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.318
Patch319: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.319
Patch320: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.320
Patch321: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.321
Patch322: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.322
Patch323: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.323
Patch324: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.324
Patch325: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.325
Patch326: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.326
Patch327: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.327
Patch328: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.328
Patch329: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.329
Patch330: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.330
Patch331: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.331
Patch332: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.332
Patch333: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.333
Patch334: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.334
Patch335: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.335
Patch336: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.336
Patch337: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.337
Patch338: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.338
Patch339: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.339
Patch340: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.340
Patch341: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.341
Patch342: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.342
Patch343: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.343
Patch344: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.344

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
%setup -q -D -T -b 1 -c -n %name-%version
%setup -q -D -T -b 2 -c -n %name-%version

# Base patches...
# for i in `seq 1 42`; do printf "%%patch%03d -p0 \n" $i; done
# Undefine _patch_options, because with the default of --fuzz=0 --unified,
# the patches fail to apply.
%define _patch_options 
cd vim%{vim_version}
%patch001 -p0 
%patch002 -p0 
%patch003 -p0 
%patch004 -p0 
%patch005 -p0 
%patch006 -p0 
%patch007 -p0 
%patch008 -p0 
%patch009 -p0 
%patch010 -p0 
%patch011 -p0 
%patch012 -p0 
%patch013 -p0 
%patch014 -p0 
%patch015 -p0 
%patch016 -p0 
%patch017 -p0 
%patch018 -p0 
%patch019 -p0 
%patch020 -p0 
%patch021 -p0 
%patch022 -p0 
%patch023 -p0 
%patch024 -p0 
%patch025 -p0 
%patch026 -p0 
%patch027 -p0 
%patch028 -p0 
%patch029 -p0 
%patch030 -p0 
%patch031 -p0 
%patch032 -p0 
%patch033 -p0 
%patch034 -p0 
%patch035 -p0 
%patch036 -p0 
%patch037 -p0 
%patch038 -p0 
%patch039 -p0 
%patch040 -p0 
%patch041 -p0 
%patch042 -p0 
%patch043 -p0 
%patch044 -p0 
%patch045 -p0 
%patch046 -p0 
%patch047 -p0 
%patch048 -p0 
%patch049 -p0 
%patch050 -p0 
%patch051 -p0 
%patch052 -p0 
%patch053 -p0 
%patch054 -p0 
%patch055 -p0 
%patch056 -p0 
%patch057 -p0 
%patch058 -p0 
%patch059 -p0 
%patch060 -p0 
%patch061 -p0 
%patch062 -p0 
%patch063 -p0 
%patch064 -p0 
%patch065 -p0 
%patch066 -p0 
%patch067 -p0 
%patch068 -p0 
%patch069 -p0 
%patch070 -p0 
%patch071 -p0 
%patch072 -p0 
%patch073 -p0 
%patch074 -p0 
%patch075 -p0 
%patch076 -p0 
%patch077 -p0 
%patch078 -p0 
%patch079 -p0 
%patch080 -p0 
%patch081 -p0 
%patch082 -p0 
%patch083 -p0 
%patch084 -p0 
%patch085 -p0 
%patch086 -p0 
%patch087 -p0 
%patch088 -p0 
%patch089 -p0 
%patch090 -p0 
%patch091 -p0 
%patch092 -p0 
%patch093 -p0 
%patch094 -p0 
%patch095 -p0 
%patch096 -p0 
%patch097 -p0 
%patch098 -p0 
%patch099 -p0 
%patch100 -p0 
%patch101 -p0 
%patch102 -p0 
%patch103 -p0 
%patch104 -p0 
%patch105 -p0 
%patch106 -p0 
%patch107 -p0 
%patch108 -p0 
%patch109 -p0 
%patch110 -p0 
%patch111 -p0 
%patch112 -p0 
%patch113 -p0 
%patch114 -p0 
%patch115 -p0 
%patch116 -p0 
%patch117 -p0 
%patch118 -p0 
%patch119 -p0 
%patch120 -p0 
%patch121 -p0 
%patch122 -p0 
%patch123 -p0 
%patch124 -p0 
%patch125 -p0 
%patch126 -p0 
%patch127 -p0 
%patch128 -p0 
%patch129 -p0 
%patch130 -p0 
%patch131 -p0 
%patch132 -p0 
%patch133 -p0 
%patch134 -p0 
%patch135 -p0 
%patch136 -p0 
%patch137 -p0 
%patch138 -p0 
%patch139 -p0 
%patch140 -p0 
%patch141 -p0 
%patch142 -p0 
%patch143 -p0 
%patch144 -p0 
%patch145 -p0 
%patch146 -p0 
%patch147 -p0 
%patch148 -p0 
%patch149 -p0 
%patch150 -p0 
%patch151 -p0 
%patch152 -p0 
%patch153 -p0 
%patch154 -p0 
%patch155 -p0 
%patch156 -p0 
%patch157 -p0 
%patch158 -p0 
%patch159 -p0 
%patch160 -p0 
%patch161 -p0 
%patch162 -p0 
%patch163 -p0 
%patch164 -p0 
%patch165 -p0 
%patch166 -p0 
%patch167 -p0 
%patch168 -p0 
%patch169 -p0 
%patch170 -p0 
%patch171 -p0 
%patch172 -p0 
%patch173 -p0 
%patch174 -p0 
%patch175 -p0 
%patch176 -p0 
%patch177 -p0 
%patch178 -p0 
%patch179 -p0 
%patch180 -p0 
%patch181 -p0 
%patch182 -p0 
%patch183 -p0 
%patch184 -p0 
%patch185 -p0 
%patch186 -p0 
%patch187 -p0 
%patch188 -p0 
%patch189 -p0 
%patch190 -p0 
%patch191 -p0 
%patch192 -p0 
%patch193 -p0 
%patch194 -p0 
%patch195 -p0 
%patch196 -p0 
%patch197 -p0 
%patch198 -p0 
%patch199 -p0 
%patch200 -p0 
%patch201 -p0 
%patch202 -p0 
%patch203 -p0 
%patch204 -p0 
%patch205 -p0 
%patch206 -p0 
%patch207 -p0 
%patch208 -p0 
%patch209 -p0 
%patch210 -p0 
%patch211 -p0 
%patch212 -p0 
%patch213 -p0 
%patch214 -p0 
%patch215 -p0 
%patch216 -p0 
%patch217 -p0 
%patch218 -p0 
%patch219 -p0 
%patch220 -p0 
%patch221 -p0 
%patch222 -p0 
%patch223 -p0 
%patch224 -p0 
%patch225 -p0 
%patch226 -p0 
%patch227 -p0 
%patch228 -p0 
%patch229 -p0 
%patch230 -p0 
%patch231 -p0 
%patch232 -p0 
%patch233 -p0 
%patch234 -p0 
%patch235 -p0 
%patch236 -p0 
%patch237 -p0 
%patch238 -p0 
%patch239 -p0 
%patch240 -p0 
%patch241 -p0 
%patch242 -p0 
%patch243 -p0 
%patch244 -p0 
%patch245 -p0 
%patch246 -p0 
%patch247 -p0 
%patch248 -p0 
%patch249 -p0 
%patch250 -p0 
%patch251 -p0 
%patch252 -p0 
%patch253 -p0 
%patch254 -p0 
%patch255 -p0 
%patch256 -p0 
%patch257 -p0 
%patch258 -p0 
%patch259 -p0 
%patch260 -p0 
%patch261 -p0 
%patch262 -p0 
%patch263 -p0 
%patch264 -p0 
%patch265 -p0 
%patch266 -p0 
%patch267 -p0 
%patch268 -p0 
%patch269 -p0 
%patch270 -p0 
%patch271 -p0 
%patch272 -p0 
%patch273 -p0 
%patch274 -p0 
%patch275 -p0 
%patch276 -p0 
%patch277 -p0 
%patch278 -p0 
%patch279 -p0 
%patch280 -p0 
%patch281 -p0 
%patch282 -p0 
%patch283 -p0 
%patch284 -p0 
%patch285 -p0 
%patch286 -p0 
%patch287 -p0 
%patch288 -p0 
%patch289 -p0 
%patch290 -p0 
%patch291 -p0 
%patch292 -p0 
%patch293 -p0 
%patch294 -p0 
%patch295 -p0 
%patch296 -p0 
%patch297 -p0 
%patch298 -p0 
%patch299 -p0 
%patch300 -p0 
%patch301 -p0 
%patch302 -p0 
%patch303 -p0 
%patch304 -p0 
%patch305 -p0 
%patch306 -p0 
%patch307 -p0 
%patch308 -p0 
%patch309 -p0 
%patch310 -p0 
%patch311 -p0 
%patch312 -p0 
%patch313 -p0 
%patch314 -p0 
%patch315 -p0 
%patch316 -p0 
%patch317 -p0 
%patch318 -p0 
%patch319 -p0 
%patch320 -p0 
%patch321 -p0 
%patch322 -p0 
%patch323 -p0 
%patch324 -p0 
%patch325 -p0 
%patch326 -p0 
%patch327 -p0 
%patch328 -p0 
%patch329 -p0 
%patch330 -p0 
%patch331 -p0 
%patch332 -p0 
%patch333 -p0 
%patch334 -p0 
%patch335 -p0 
%patch336 -p0 
%patch337 -p0 
%patch338 -p0 
%patch339 -p0 
%patch340 -p0 
%patch341 -p0 
%patch342 -p0 
%patch343 -p0 
%patch344 -p0 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/sfw/lib"
cd vim%{vim_version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}	     \
            --enable-perlinterp \
            --enable-pythoninterp \
            --enable-tclinterp \
            --with-tclsh=/usr/bin/tclsh8.4 \
            --enable-rubyinterp \
            --enable-multibyte \
            --disable-hangulinput \
            --enable-cscope \
            --enable-gui=gnome2 \
            --disable-fontset \
            --enable-netbeans \
            --with-compiledby="`id -un`" \
            --with-features=huge

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd vim%{vim_version}
make DESTDIR=$RPM_BUILD_ROOT install
install --mode=0644 %SOURCE3 $RPM_BUILD_ROOT%{_datadir}/vim/vim%{vim_version}/plugin
rm $RPM_BUILD_ROOT%{_mandir}/man1/ex.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/view.1

rm -f $RPM_BUILD_ROOT%{_bindir}/ex
rm -f $RPM_BUILD_ROOT%{_bindir}/view
ln -s vim gvim

mkdir -p $RPM_BUILD_ROOT%{_prefix}/gnu/bin
cd $RPM_BUILD_ROOT%{_prefix}/gnu/bin
ln -s ../../bin/vim ex
ln -s ../../bin/vim view

find $RPM_BUILD_ROOT%{_mandir} -name view.1 -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_mandir} -name ex.1 -exec rm -f {} \;

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1gnu
cd $RPM_BUILD_ROOT%{_mandir}
for d in *; do
    test $d = man1 && continue
    test -f $d/man1/vim.1 || continue
    mkdir -p $d/man1gnu && \
	cd $d/man1gnu && \
	ln -s ../man1/vim.1 view.1gnu && \
	ln -s ../man1/vim.1 ex.1gnu && \
	cd ../..
done
	

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/vim/vim%{vim_version}/lang
rm -rf $RPM_BUILD_ROOT%{_mandir}/[a-z][a-z]
rm -rf $RPM_BUILD_ROOT%{_mandir}/[a-z][a-z].*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/gnu
%dir %attr (0755, root, bin) %{_prefix}/gnu/bin
%{_prefix}/gnu/bin/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vim
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vim/vim%{vim_version}/lang
%{_mandir}/[a-z][a-z]
%{_mandir}/[a-z][a-z].*
%endif

%changelog
* Mon Jan 25 2010 - jedy.wang@sun.com
- Bump to release 344.
* Tue Aug 04 2009 - jedy.wang@sun.com
- Bump to release 245.
* Wed May 27 2009 - jedy.wang@sun.com
- Bump to release 191.
* Fri Mar 13 2008 - jedy.wang@sun.com
- Bump to release 141.
* Tue Nov 19 2008 - alexander@skwar.name
- Bump to 7.2, and apply the 42 patches that are there in 
  ftp://ftp.vim.org/pub/vim/patches/7.2
- Use vim-7.2-extra
- Set tclsh to tclsh8.4
- Add compiledby information
- Add build dependency on SUNWxwinc, as without that, GUI won't be built
- Comment out Build dependency on SFEcscope or SPROsslnk; it's provided
  by pkg sunstudioexpress - and it's not a *BUILD* dependency to begin with.
- Build a binary with "huge" features (and not just "normal")
* Tue Jul 17 2007 - halton.huo@sun.com
- Bump to 7.1
* Fri Jul 13 2007 - dougs@truemail.co.th
- Fixed cscope requirement clash
* Mon Sep 11 2006 - halton.huo@sun.com
- Correct remove l10n files part
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEvim
- bump to 7.0
- delete -share subpkg, add -l10n subpkg
- update file attributes
- enable a bunch of features, add dependencies
* Wed Jun 28 2006 - halton.huo@sun.com
- Enable cscope plugin.
* Thu Apr  6 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Fri Jan 27 2005 - glynn.foster@sun.com
- Initial version
