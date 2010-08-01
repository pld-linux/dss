Summary:	Darwin Streaming Server
Name:		dss
Version:	6.0.3
Release:	0.1
License:	Apple Public Source License
Group:		Applications
Source0:	http://dss.macosforge.org/downloads/DarwinStreamingSrvr%{version}-Source.tar
# Source0-md5:	ca676691db8417d05121699c0ca3d549
Patch0:		%{name}.patch
Patch1:		%{name}-x86_64.patch
URL:		http://dss.macosforge.org/
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
Group:		Daemons

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

%package Samples
Summary:	Apple's Darwin Streaming Samples
Group:		Daemons

%description Samples
Sample files for the Darwin Streaming Server.

%prep
%setup -q -n DarwinStreamingSrvr%{version}-Source
%patch0 -p1
%patch1 -p1

# patch streamingadminserver.pl
%{__sed} -i -e  "s|/usr/local/|/usr/|g" WebAdmin/src/streamingadminserver.pl
%{__sed} -i -e  "s|/etc/streaming/|/etc/dss/|g" WebAdmin/src/streamingadminserver.pl
%{__sed} -i -e  "s|/var/streaming/logs/|/var/log/dss/|g" WebAdmin/src/streamingadminserver.pl
%{__sed} -i -e  "s|/var/streaming/|/var/dss/|g" WebAdmin/src/streamingadminserver.pl
%{__sed} -i -e  "s|/usr/local/|/usr/|g" WebAdmin/src/streamingadminserver.pl

# patch manpages
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Config/|/etc/dss/|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Modules|/usr/lib/dss|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Movies|/var/dss/movies|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Playlists|/var/dss/playlists|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Logs|/var/log/dss|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|/Library/QuickTimeStreaming/Docs|%{_docdir}/%{name}-%{version}|g" Documentation/man/qtss/*
%{__sed} -i -e  "s|QuickTimeStreamingServer|DarwinStreamingServer|g" Documentation/man/qtss/*

cat > defaultPaths.h << EOF
#define DEFAULTPATHS_DIRECTORY_SEPARATOR	"/"
#define DEFAULTPATHS_ROOT_DIR			"%{_localstatedir}/dss/"
#define DEFAULTPATHS_ETC_DIR			"%{_sysconfdir}/dss/"
#define DEFAULTPATHS_ETC_DIR_OLD		"%{_sysconfdir}/"
#define DEFAULTPATHS_SSM_DIR			"%{_libdir}/dss/"
#define DEFAULTPATHS_LOG_DIR			"%{_localstatedir}/log/dss/"
#define DEFAULTPATHS_PID_DIR			"%{_localstatedir}/run/"
#define DEFAULTPATHS_MOVIES_DIR			"%{_localstatedir}/dss/movies/"
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
./DSS_MakeRoot \
	$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc APPLE_LICENSE ReleaseNotes.txt
