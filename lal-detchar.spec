#
# Conditional build
%bcond_with	python	# Python 2.x module (dependencies obsolete)

Summary:	LAL routines for detector chracterisation
Summary(pl.UTF-8):	Procedury LAL do charakterystyki detektorów
Name:		lal-detchar
Version:	0.3.5
Release:	3
License:	GPL v2+
Group:		Libraries
Source0:	http://software.igwn.org/lscsoft/source/lalsuite/laldetchar-%{version}.tar.xz
# Source0-md5:	1a82ba51de4bad71e8d2b7d2bad6988d
Patch0:		%{name}-env.patch
Patch1:		lal-metaio-detect.patch
Patch2:		%{name}-lal-swig.patch
Patch3:		%{name}-octave.patch
URL:		https://wiki.ligo.org/Computing/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	help2man
BuildRequires:	lal-burst-devel >= 1.4.4
BuildRequires:	lal-devel >= 6.18.0
BuildRequires:	lal-metaio-devel >= 1.3.1
BuildRequires:	lal-simulation-devel >= 1.7.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel >= 1:3.2.0
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-numpy-devel >= 1:1.7
%endif
BuildRequires:	swig >= 4.1.0
BuildRequires:	swig-python >= 2.0.12
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	lal >= 6.18.0
Requires:	lal-burst >= 1.4.4
Requires:	lal-metaio >= 1.3.1
Requires:	lal-simulation >= 1.7.0
%if %{without python}
Obsoletes:	python-laldetchar < %{version}-%{release}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LAL routines for detector chracterisation.

%description -l pl.UTF-8
Procedury LAL do charakterystyki detektorów.

%package devel
Summary:	Header files for lal-detchar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lal-detchar
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	gsl-devel >= 1.13
Requires:	lal-burst-devel >= 1.4.4
Requires:	lal-devel >= 6.18.0
Requires:	lal-metaio-devel >= 1.3.1
Requires:	lal-simulation-devel >= 1.7.0

%description devel
Header files for lal-detchar library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lal-detchar.

%package static
Summary:	Static lal-detchar library
Summary(pl.UTF-8):	Statyczna biblioteka lal-detchar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lal-detchar library.

%description static -l pl.UTF-8
Statyczna biblioteka lal-detchar.

%package -n octave-laldetchar
Summary:	Octave interface for LAL DetChar
Summary(pl.UTF-8):	Interfejs Octave do biblioteki LAL DetChar
Group:		Applications/Math
Requires:	%{name} = %{version}-%{release}
Requires:	octave-lal >= 6.18.0

%description -n octave-laldetchar
Octave interface for LAL DetChar.

%description -n octave-laldetchar -l pl.UTF-8
Interfejs Octave do biblioteki LAL DetChar.

%package -n python-laldetchar
Summary:	Python bindings for LAL DetChar
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LAL DetChar
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-gstreamer0.10 >= 0.10
Requires:	python-lal >= 6.18.0
Requires:	python-lalburst >= 1.4.4
Requires:	python-lalmetaio >= 1.3.1
Requires:	python-lalsimulation >= 1.7.0
Requires:	python-lscsoft-glue
Requires:	python-modules >= 1:2.6
Requires:	python-matplotlib
Requires:	python-numpy >= 1:1.7
Requires:	python-pygobject >= 2.0
Requires:	python-pygtk-gtk >= 2:2.0
Requires:	python-scipy
#python-ROOT

%description -n python-laldetchar
Python bindings for LAL DetChar.

%description -n python-laldetchar -l pl.UTF-8
Wiązania Pythona do biblioteki LAL DetChar.

%prep
%setup -q -n laldetchar-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I gnuscripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python} \
	--disable-dependency-tracking \
	%{!?with_python:--disable-python} \
	--disable-silent-rules \
	--enable-swig \
	%{!?with_python:--disable-swig-python}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblaldetchar.la

install -d $RPM_BUILD_ROOT/etc/shrc.d
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/laldetchar-idq-append-file-to-cache
%attr(755,root,root) %{_bindir}/laldetchar_version
%attr(755,root,root) %{_libdir}/liblaldetchar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblaldetchar.so.3
/etc/shrc.d/laldetchar-user-env.csh
/etc/shrc.d/laldetchar-user-env.fish
/etc/shrc.d/laldetchar-user-env.sh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblaldetchar.so
%{_includedir}/lal/LALDetChar*.h
%{_includedir}/lal/SWIGLALDetChar*.h
%{_includedir}/lal/SWIGLALDetChar*.i
%{_includedir}/lal/swiglaldetchar.i
%{_pkgconfigdir}/laldetchar.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblaldetchar.a

%files -n octave-laldetchar
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/octave/*/site/oct/*/laldetchar.oct

%if %{with python}
%files -n python-laldetchar
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/laldetchar-hveto
%attr(755,root,root) %{_bindir}/laldetchar-hveto-summary-page
%attr(755,root,root) %{_bindir}/laldetchar-idq-add-excluded-vars
%attr(755,root,root) %{_bindir}/laldetchar-idq-build-auxmvc-vectors
%attr(755,root,root) %{_bindir}/laldetchar-idq-convertkwtosb
%attr(755,root,root) %{_bindir}/laldetchar-idq-evaluate-times
%attr(755,root,root) %{_bindir}/laldetchar-idq-calibration
%attr(755,root,root) %{_bindir}/laldetchar-idq-gdb-alert-handler
%attr(755,root,root) %{_bindir}/laldetchar-idq-gdb-glitch-tables
%attr(755,root,root) %{_bindir}/laldetchar-idq-gdb-processor
%attr(755,root,root) %{_bindir}/laldetchar-idq-gdb-timeseries
%attr(755,root,root) %{_bindir}/laldetchar-idq-prepare-training-auxmvc-samples
%attr(755,root,root) %{_bindir}/laldetchar-idq-realtime
%attr(755,root,root) %{_bindir}/laldetchar-idq-select-channels-from-kw-config
%attr(755,root,root) %{_bindir}/laldetchar-idq-summary
%attr(755,root,root) %{_bindir}/laldetchar-idq-svm-evaluate
%attr(755,root,root) %{_bindir}/laldetchar-idq-svm-train
%attr(755,root,root) %{_bindir}/laldetchar-idq-train
%attr(755,root,root) %{_bindir}/laldetchar-segments-from-data
%attr(755,root,root) %{_bindir}/laldetchar-idq-ann-convert
%attr(755,root,root) %{_bindir}/laldetchar-idq-ann-train
%attr(755,root,root) %{_bindir}/laldetchar-idq-ann-evaluate
%attr(755,root,root) %{_bindir}/laldetchar-idq-frames-to-segments
%attr(755,root,root) %{_bindir}/laldetchar-idq-gst-sender
%attr(755,root,root) %{_bindir}/laldetchar-idq-gst-relay
%attr(755,root,root) %{_bindir}/laldetchar-idq-gst-listener
%attr(755,root,root) %{_bindir}/laldetchar-idq-gdb-local-performance
%dir %{py_sitedir}/laldetchar
%attr(755,root,root) %{py_sitedir}/laldetchar/_laldetchar.so
%{py_sitedir}/laldetchar/*.py[co]
%{py_sitedir}/laldetchar/hveto
%{py_sitedir}/laldetchar/idq
%{py_sitedir}/laldetchar/triggers
%{_mandir}/man1/laldetchar-*.1*
%endif
