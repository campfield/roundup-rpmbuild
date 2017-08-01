%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Simple and flexible issue-tracking system
Name: roundup
Version: 1.5.1
Release: 1%{dist}
License: MIT
Group: Applications/Engineering
URL: http://roundup-tracker.org/
Source: http://pypi.python.org/packages/source/r/%{name}/%{name}-%{version}.tar.gz
Source1: roundup_httpd.conf
Source2: roundup.service
Source3: README.linux
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
Requires: httpd
Requires: mod_proxy_html
Requires: sqlite
Requires: systemd

%description
Roundup is a simple and flexible issue-tracking system with command line,
web and email interfaces.  It is based on the winning design from Ka-Ping
Yee in the Software Carpentry "Track" design competition.

%package doc
Group: Documentation
Summary: Documentation for the Roundup
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The roundup-doc package contains the documentation for Roundup issue-tracker.

%prep
%setup -q

install -pm 644 %{SOURCE3} .

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
install -p -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/roundup.conf
install -p -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/roundup.service

%find_lang %{name}

%post
useradd -M -r -d /var/lib/roundup -s /sbin/nologin -c "Roundup Issue Tracker" roundup  || :
if [ ! -d /var/lib/roundup ]; then
	install -d /var/lib/roundup/trackers/default/db
	install -d /var/lib/roundup/trackers/default/db/files -m 2770 -o root -g roundup

	# Create Roundup configuration.
	roundup-admin -i /var/lib/roundup/trackers/default install classic sqlite
fi

if [ ! -e /var/log/roundup-server.log ]; then

	touch /var/log/roundup-server.log
	chown roundup:root /var/log/roundup-server.log

fi

/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable roundup
/usr/bin/systemctl restart roundup

%preun
if [ $1 = 0 ]; then
	/usr/bin/systemctl disable roundup
	/usr/bin/systemctl stop roundup
	/usr/bin/systemctl daemon-reload
fi

%clean
#rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/roundup/
%{_mandir}/man1/*
%defattr(-,root,root)
%config(noreplace) %{_unitdir}/roundup.service
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%doc README.linux COPYING.txt

%files doc
%doc %{_defaultdocdir}/%{name}/*
