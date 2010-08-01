# TODO
# - merge dstreamserv.spec
Summary:	Darwin Streaming Server
Name:		dss
Version:	6.0.3
Release:	0.6
License:	Apple Public Source License
Group:		Networking/Daemons
Source0:	http://dss.macosforge.org/downloads/DarwinStreamingSrvr%{version}-Source.tar
# Source0-md5:	ca676691db8417d05121699c0ca3d549
Patch0:		%{name}.patch
Patch1:		%{name}-x86_64.patch
Patch2:		optflags.patch
Patch3:		compile.patch
Source1:	%{name}.init
URL:		http://dss.macosforge.org/
BuildRequires:	libstdc++-devel
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

%package Utils
Summary:	Apple's Darwin Streaming Server Movie inspection utilities
Group:		Applications

%description Utils
- QTBroadcaster Requires a target ip address, a source movie, one or
  more source hint track ids in movie, and an initial port. Every packet
  referenced by the hint track(s) is broadcasted to the specified ip
  address.

- QTFileInfo Requires a movie name. Displays each track id, name,
  create date, and mod date. If the track is a hint track, additional
  information is displayed: the total rtp bytes and packets, the average
  bit rate and packet size, and the total header percentage of the
  stream.

- QTFileTest Requires a movie name. Parses the Movie Header Atom and
  displays a trace of the output.

- QTRTPFileTest Requires a movie and a hint track id in the movie.
  Displays the RTP header (TransmitTime, Cookie, SeqNum, and TimeStamp)
  for each packet.

- QTRTPGen Requires a movie and a hint track id. Displays the number
  of packets in each hint track sample and writes the RTP packets to
  file "track.cache"

- QTSampleLister Requires a movie and a track id. Displays track media
  sample number, media time, Data offset, and sample size for each
  sample in the track.

- QTSDPGen Requires a list of 1 or more movies. Displays the SDP
  information for all of the hinted tracks in each movie. Use -f to save
  the SDP information to the file [movie].sdp in the same directory as
  the source movie.

- QTTrackInfo Requires a movie, sample table atom type, and track id.
  Displays the information in the sample table atom of the specified
  track. Supports "stco", "stsc", "stsz", "stts" as the atom type.

Example: "./QTTrackInfo -T stco /movies/mystery.mov 3" dumps the chunk
offset sample table in track 3.

- StreamingLoadTool

%package samples
Summary:	Darwin Streaming Server - samples
Summary(pl.UTF-8):	Przykłady do Darwin Streaming Servera
Group:		Networking/Daemons
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

# patch streamingadminserver.pl
%{__sed} -i.bak -e  '
	s|/''usr/local/movies|%{_localstatedir}/lib/%{name}/movies|g
	s|/''usr/local/sbin/StreamingServerModules|%{_libdir}/%{name}/|g
	s|/''usr/local/|%{_prefix}/|g
	s|/''etc/streaming|%{_sysconfdir}/%{name}|g
	s|/var/streaming/AdminHtml|%{_datadir}/%{name}/AdminHtml|g
	s|/var/streaming/logs|%{_localstatedir}/log/%{name}|g
	s|/var/streaming/|%{_localstatedir}/lib/%{name}/|g
'	DSS_MakeRoot streamingserver.xml-POSIX \
	WebAdmin/src/streamingadminserver.pl \
	WebAdmin/WebAdminHtml/adminprotocol-lib.pl

# patch manpages
%{__sed} -i -e  '
	s|/Library/QuickTimeStreaming/Config/|%{_sysconfdir}/%{name}/|g
	s|/Library/QuickTimeStreaming/Modules|%{_libdir}/%{name}|g
	s|/Library/QuickTimeStreaming/Movies|%{_localstatedir}/lib/%{name}/movies|g
	s|/Library/QuickTimeStreaming/Playlists|%{_localstatedir}/lib/%{name}/playlists|g
	s|/Library/QuickTimeStreaming/Logs|%{_localstatedir}/log/%{name}|g
	s|/Library/QuickTimeStreaming/Docs|%{_docdir}/%{name}-%{version}|g
	s|QuickTimeStreamingServer|DarwinStreamingServer|g
' Documentation/man/qtss/*

cat > defaultPaths.h << 'EOF'
#define DEFAULTPATHS_DIRECTORY_SEPARATOR	"/"
#define DEFAULTPATHS_ROOT_DIR			"%{_localstatedir}/lib/%{name}/"
#define DEFAULTPATHS_ETC_DIR			"%{_sysconfdir}/%{name}/"
#define DEFAULTPATHS_ETC_DIR_OLD		"%{_sysconfdir}/"
#define DEFAULTPATHS_SSM_DIR			"%{_libdir}/%{name}/"
#define DEFAULTPATHS_LOG_DIR			"%{_localstatedir}/log/%{name}/"
#define DEFAULTPATHS_PID_DIR			"%{_localstatedir}/run/"
#define DEFAULTPATHS_MOVIES_DIR			"%{_localstatedir}/lib/%{name}/movies/"
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
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/lib/%{name}}
./DSS_MakeRoot \
	$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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

rm $RPM_BUILD_ROOT/var/lib/%{name}/3rdPartyAcknowledgements.rtf
rm $RPM_BUILD_ROOT/var/lib/%{name}/readme.txt

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -f -g 148 qtss
%useradd -g qtss -d /tmp -u 148 -s /bin/false qtss

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
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

%attr(754,root,root) /etc/rc.d/init.d/dss
%attr(755,root,root) %{_bindir}/MP3Broadcaster
%attr(755,root,root) %{_bindir}/PlaylistBroadcaster
%attr(755,root,root) %{_bindir}/StreamingLoadTool
%attr(755,root,root) %{_bindir}/createuserstreamingdir
%attr(755,root,root) %{_bindir}/qtpasswd

%attr(755,root,root) %{_sbindir}/DarwinStreamingServer
%attr(755,root,root) %{_sbindir}/streamingadminserver.pl

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/QTSSHomeDirectoryModule
%attr(755,root,root) %{_libdir}/%{name}/QTSSRefMovieModule

%dir /var/lib/%{name}
%dir /var/lib/%{name}/movies

# admin server (subpackage?)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/AdminHtml
%{_datadir}/%{name}/AdminHtml/html_en
%{_datadir}/%{name}/AdminHtml/images
%{_datadir}/%{name}/AdminHtml/includes
%{_datadir}/%{name}/AdminHtml/*.html
%{_datadir}/%{name}/AdminHtml/*.pl
%attr(755,root,root) %{_datadir}/%{name}/AdminHtml/*.cgi

%files samples
%defattr(644,root,root,755)
/var/lib/%{name}/movies/*
