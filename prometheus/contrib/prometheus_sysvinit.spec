%define debug_package %{nil}

Name:		prometheus
Version:	1.2.3
Release:	1%{?dist}
Summary:	Prometheus is a systems and service monitoring system.
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://github.com/prometheus/prometheus
Source0:	https://github.com/prometheus/prometheus/releases/download/%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:	prometheus.init
Source2:	prometheus.rules
Source3:	prometheus.sysconfig
Source4:	prometheus.yaml

Requires(pre):  /usr/sbin/useradd
Requires:       daemonize
AutoReqProv:	No

%description

Prometheus is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates
rule expressions, displays the results, and can trigger alerts if
some condition is observed to be true.

%prep
%setup -q -n prometheus-%{version}.linux-amd64

%build
echo "No building needed"

%install
install -m 755 -D %{SOURCE1} %{buildroot}/etc/init.d/prometheus
install -m 644 -D %{SOURCE2} %{buildroot}/etc/prometheus/prometheus.rules
install -m 644 -D %{SOURCE3} %{buildroot}/etc/sysconfig/prometheus
install -m 644 -D %{SOURCE4} %{buildroot}/etc/prometheus/prometheus.yaml
install -m 755 -D prometheus %{buildroot}/usr/bin/prometheus
install -m 755 -D promtool %{buildroot}/usr/bin/promtool

mkdir -p %{buildroot}/usr/share/prometheus
mkdir -p %{buildroot}/var/run/prometheus
mkdir -p %{buildroot}/var/log/prometheus
cp -r console_libraries $RPM_BUILD_ROOT/usr/share/prometheus/consoles_libraries
cp -r consoles $RPM_BUILD_ROOT/usr/share/prometheus/consoles

%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -s /sbin/nologin \
    -d $RPM_BUILD_ROOT/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
#chgrp prometheus /var/run/prometheus
#chmod 774 /var/run/prometheus
#chown prometheus:prometheus /var/log/prometheus
#chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/prometheus
/usr/bin/promtool
%config(noreplace) /etc/prometheus/prometheus.yaml
%config(noreplace) /etc/prometheus/prometheus.rules
/etc/init.d/prometheus
%config(noreplace) /etc/sysconfig/prometheus
/usr/share/prometheus
/var/run/prometheus
/var/log/prometheus
