# TODO
# - merge dstreamserv.spec
%include    /usr/lib/rpm/macros.perl

Summary:	Darwin Streaming Server
Name:		dss
Version:	6.0.3
Release:	0.12
License:	Apple Public Source License
Group:		Networking/Daemons
Source0:	http://dss.macosforge.org/downloads/DarwinStreamingSrvr%{version}-Source.tar
# Source0-md5:	ca676691db8417d05121699c0ca3d549
Source1:	%{name}.init
Source2:	%{name}-admin.init
Source3:	README.utils
Patch0:		%{name}.patch
Patch1:		%{name}-x86_64.patch
Patch2:		optflags.patch
Patch3:		compile.patch
URL:		http://dss.macosforge.org/
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(qtss)
Provides:	user(qtss)
Obsoletes:	DSS
Obsoletes:	dstreamserv
Obsoletes:	dstreamsrv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Darwin Streaming Server lets you stream digital video on the Internet
using industry-standard Internet protocols RTP and RTSP.

Using Darwin Streaming Server you can serve stored files (video on
demand) or reflect live broadcasts to thousands of QuickTime 4 or
later users. With its combination of industry-standard streaming
protocols and cutting-edge compression technologies, QuickTime
delivers perfectly synchronized audio and video streams ideal for
Internet video and live events.

%description -l pl.UTF-8
Serwer strumieni pozwala wysyłać strumienie danych QuickTime do
klientów w Internecie przy użyciu protokołów RTP i RTSP.

%package Proxy
Summary:	Apple's Darwin Streaming Proxy
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description Proxy
The Darwin Streaming Proxy is an application specific proxy which
would normally be run in a border zone or perimeter network. It is
used to give client machines within a protected network access to
streaming servers outside that network, in the case when the firewall
blocks RTSP connections or RTP/UDP data flow. The firewall perimeter
network is usually configured to allow:

- RTSP connections from within the network, as long as the destination
  is the proxy

- RTSP connections to outside the network, as long as the source is
  the proxy

- RTP datagrams to and from the proxy to the inner network

- RTP datagrams to and from the proxy to the outside

%package utils
Summary:	Apple's Darwin Streaming Server Movie inspection utilities
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description utils
Apple's Darwin Streaming Server Movie inspection utilities.

%package samples
Summary:	Darwin Streaming Server - samples
Summary(pl.UTF-8):	Przykłady do Darwin Streaming Servera
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Obsoletes:	dstreamserv-samples

%description samples
Sample files for Streaming Server.

%description samples -l pl.UTF-8
Przykładowe pliki do Darwin Streaming Servera.

%prep
%setup -q -n DarwinStreamingSrvr%{version}-Source
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp -p %{SOURCE3} .

# patch streamingadminserver.pl
%{__sed} -i.bak -e  '
	s|/''usr/local/movies|/var/lib/%{name}/movies|g
	s|/''usr/local/sbin/StreamingServerModules|%{_libdir}/%{name}/|g
	s|/''usr/local/|%{_prefix}/|g
	s|/''etc/streaming|%{_sysconfdir}/%{name}|g
	s|/var/streaming/AdminHtml|%{_datadir}/%{name}/AdminHtml|g
	s|/var/streaming/logs|/var/log/%{name}|g
	s|/var/streaming/|/var/lib/%{name}/|g
    s|<PREF NAME="run_user_name"></PREF>|<PREF NAME="run_user_name">qtss</PREF>|
    s|<PREF NAME="run_group_name"></PREF>|<PREF NAME="run_group_name">qtss</PREF>|
'	DSS_MakeRoot streamingserver.xml-POSIX \
	WebAdmin/src/streamingadminserver.pl \
	WebAdmin/WebAdminHtml/adminprotocol-lib.pl

# patch manpages
%{__sed} -i -e  '
	s|/Library/QuickTimeStreaming/Config/|%{_sysconfdir}/%{name}/|g
	s|/Library/QuickTimeStreaming/Modules|%{_libdir}/%{name}|g
	s|/Library/QuickTimeStreaming/Movies|/var/lib/%{name}/movies|g
	s|/Library/QuickTimeStreaming/Playlists|/var/lib/%{name}/playlists|g
	s|/Library/QuickTimeStreaming/Logs|/var/log/%{name}|g
	s|/Library/QuickTimeStreaming/Docs|%{_docdir}/%{name}-%{version}|g
	s|QuickTimeStreamingServer|DarwinStreamingServer|g
' Documentation/man/qtss/*

cat > defaultPaths.h << 'EOF'
#define DEFAULTPATHS_DIRECTORY_SEPARATOR	"/"
#define DEFAULTPATHS_ROOT_DIR			"/var/lib/%{name}/"
#define DEFAULTPATHS_ETC_DIR			"%{_sysconfdir}/%{name}/"
#define DEFAULTPATHS_ETC_DIR_OLD		"%{_sysconfdir}/"
#define DEFAULTPATHS_SSM_DIR			"%{_libdir}/%{name}/"
#define DEFAULTPATHS_LOG_DIR			"/var/log/%{name}/"
#define DEFAULTPATHS_PID_DIR			"/var/run/"
#define DEFAULTPATHS_MOVIES_DIR			"/var/lib/%{name}/movies/"
EOF

%build
export RPM_OPT_FLAGS="%{rpmcflags}"
export ARCH="%{_target_cpu}"
export CC="%{__cc}"
export CXX="%{__cxx}"

jobs=$(echo %{_smp_mflags} | cut -dj -f2)
./Buildit ${jobs:+--jobs=$jobs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/lib/%{name},%{_mandir}/man{1,8}}
./DSS_MakeRoot \
	$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-admin

# avoid extension
mv $RPM_BUILD_ROOT%{_sbindir}/streamingadminserver{.pl,}

# utils
install -p QTFileTools/QTBroadcaster.tproj/QTBroadcaster $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTFileInfo.tproj/QTFileInfo $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTFileTest.tproj/QTFileTest $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTRTPFileTest.tproj/QTRTPFileTest $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTRTPGen.tproj/QTRTPGen $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTSampleLister.tproj/QTSampleLister $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTSDPGen.tproj/QTSDPGen $RPM_BUILD_ROOT%{_bindir}
install -p QTFileTools/QTTrackInfo.tproj/QTTrackInfo $RPM_BUILD_ROOT%{_bindir}

# modules
install -p APIModules/QTSSRawFileModule.bproj/QTSSRawFileModule $RPM_BUILD_ROOT%{_libdir}/%{name}

# config
cp -a qtaccess $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# Create our default admin user and remove Apple's
# Default login is root/pld -- please change it!
qtpasswd="\
$RPM_BUILD_ROOT%{_bindir}/qtpasswd \
-f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/qtusers
-g $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/qtgroups"
$qtpasswd root -p pld -A admin
$qtpasswd -F -d 'aGFja21l'

mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/relayconfig.xml{-Sample,}
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/streamingserver.xml-sample

# streamingadminserver
cp -a WebAdmin/streamingadminserver.pem $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# doc
cp -a Documentation/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a Documentation/man/qtss/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a Documentation/man/qtss/createuserstreamingdir.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -a Documentation/man/qtss/QuickTimeStreamingServer.8 $RPM_BUILD_ROOT%{_mandir}/man8/DarwinStreamingServer.8
cp -a Documentation/man/qtss/streamingadminserver.pl.8 $RPM_BUILD_ROOT%{_mandir}/man8/streamingadminserver.8
rm $RPM_BUILD_ROOT/var/lib/%{name}/3rdPartyAcknowledgements.rtf
rm $RPM_BUILD_ROOT/var/lib/%{name}/readme.txt

# provide ghost logs...
touch $RPM_BUILD_ROOT/var/log/%{name}/Error.log
touch $RPM_BUILD_ROOT/var/log/%{name}/StreamingServer.log
touch $RPM_BUILD_ROOT/var/log/%{name}/mp3_access.log
touch $RPM_BUILD_ROOT/var/log/%{name}/server_status

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -f -g 148 qtss
%useradd -g qtss -d /tmp -u 148 -s /bin/false qtss

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig --add %{name}-admin
%service %{name} restart
%service %{name}-admin restart

if [ "$1" = "1" ]; then
	%banner %{name} -e <<-EOF
	Default admin username/password is root/pld. Set a password for it or, better
	delete it and create new admin username and password (using qtpasswd)

	Access admin interface at:
	http://localhost:1220/
	EOF
fi

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	%service -q %{name}-admin stop
	/sbin/chkconfig --del %{name}
	/sbin/chkconfig --del %{name}-admin
fi

%postun
if [ "$1" = "0" ]; then
	%userremove qtss
	%groupremove qtss
fi

%files
%defattr(644,root,root,755)
%doc APPLE_LICENSE ReleaseNotes.txt
%doc Documentation/3rdPartyAcknowledgements.rtf
%doc Documentation/AboutQTFileTools.html
%doc Documentation/AboutTheSource.html
%doc Documentation/admin-protocol-README.txt
%doc Documentation/CachingProxyProtocol-README.txt
%doc Documentation/DevNotes.html
%doc Documentation/draft-serenyi-avt-rtp-meta-00.txt
%doc Documentation/DSS_QT_Logo_License.pdf
%doc Documentation/License.rtf
%doc Documentation/QTSSAPIDocs.pdf
%doc Documentation/ReadMe.rtf
%doc Documentation/readme.txt
%doc Documentation/ReliableRTP_WhitePaper.rtf
%doc Documentation/RTSP_Over_HTTP.pdf

%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/qtgroups
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/qtusers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/relayconfig.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/streamingloadtool.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/streamingserver.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/qtaccess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/streamingadminserver.pem

%attr(754,root,root) /etc/rc.d/init.d/dss
%attr(754,root,root) /etc/rc.d/init.d/dss-admin
%attr(755,root,root) %{_bindir}/MP3Broadcaster
%attr(755,root,root) %{_bindir}/PlaylistBroadcaster
%attr(755,root,root) %{_bindir}/StreamingLoadTool
%attr(755,root,root) %{_bindir}/createuserstreamingdir
%attr(755,root,root) %{_bindir}/qtpasswd

%attr(755,root,root) %{_sbindir}/DarwinStreamingServer
%attr(755,root,root) %{_sbindir}/streamingadminserver

%{_mandir}/man1/*
%{_mandir}/man8/*

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/QTSSHomeDirectoryModule
%attr(755,root,root) %{_libdir}/%{name}/QTSSRefMovieModule

%attr(755,root,root) %{_libdir}/dss/QTSSRawFileModule

%dir /var/lib/%{name}
%dir /var/lib/%{name}/movies

%dir /var/log/%{name}
%attr(644,qtss,qtss) %verify(not md5 mtime size) %ghost /var/log/%{name}/Error.log
%attr(644,qtss,qtss) %verify(not md5 mtime size) %ghost /var/log/%{name}/StreamingServer.log
%attr(644,qtss,qtss) %verify(not md5 mtime size) %ghost /var/log/%{name}/mp3_access.log
%attr(644,qtss,qtss) %verify(not md5 mtime size) %ghost /var/log/%{name}/server_status

# admin server (subpackage?)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/AdminHtml
%{_datadir}/%{name}/AdminHtml/html_en
%{_datadir}/%{name}/AdminHtml/images
%{_datadir}/%{name}/AdminHtml/includes
%{_datadir}/%{name}/AdminHtml/*.html
%{_datadir}/%{name}/AdminHtml/*.pl
%attr(755,root,root) %{_datadir}/%{name}/AdminHtml/*.cgi

%files utils
%defattr(644,root,root,755)
%doc README.utils
%attr(755,root,root) %{_bindir}/QTBroadcaster
%attr(755,root,root) %{_bindir}/QTFileInfo
%attr(755,root,root) %{_bindir}/QTFileTest
%attr(755,root,root) %{_bindir}/QTRTPFileTest
%attr(755,root,root) %{_bindir}/QTRTPGen
%attr(755,root,root) %{_bindir}/QTSDPGen
%attr(755,root,root) %{_bindir}/QTSampleLister
%attr(755,root,root) %{_bindir}/QTTrackInfo

%files samples
%defattr(644,root,root,755)
/var/lib/%{name}/movies/*
