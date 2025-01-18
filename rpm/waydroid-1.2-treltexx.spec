Name:           waydroid-1.2-treltexx
Version:        1.0.0
Release:        1
Summary:        waydroid-1.2-treltexx installs Waydroid version 1.2 & its configs for the Samsung Galaxy Note4 (SM-N910C) (treltexx).
License:        GPLv3
URL:            https://github.com/waydroid
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  systemd
Requires:       lxc
Requires:       dnsmasq
Requires:       python3-gbinder
Requires:       python3-gobject
Requires:       waydroid-sensors
Requires:       waydroid-gbinder-config-hybris-treltexx

%description
Waydroid uses Linux namespaces (user, pid, uts, net, mount, ipc) to run a full Android system in a container and provide Android applications on any GNU/Linux-based platform.

The Android system inside the container has direct access to any needed hardware.

The Android runtime environment ships with a minimal customized Android system image based on LineageOS. The image is currently based on Android 10.

%prep
%setup

%install
mkdir -p %{buildroot}/opt/waydroid
mkdir -p %{buildroot}/home/waydroid
cp -r upstream-1.2/* %{buildroot}/opt/waydroid
mkdir -p %{buildroot}/var/lib/
ln -sf /home/waydroid %{buildroot}/var/lib/waydroid
mkdir -p %{buildroot}/usr/bin
ln -sf /opt/waydroid/waydroid.py %{buildroot}/usr/bin/waydroid

# Install container & session services
install -D -m644 config/waydroid-container.service %{buildroot}/usr/lib/systemd/system/waydroid-container.service
install -D -m644 config/waydroid-session.service %{buildroot}/usr/lib/systemd/user/waydroid-session.service

# Install waydroid modules
install -D -m644 config/waydroid.conf %{buildroot}/etc/modules-load.d/waydroid.conf

# Install treltexx specific waydroid confing files
install -D -m644 config/config %{buildroot}/home/waydroid/lxc/waydroid/config
install -D -m644 config/config_nodes %{buildroot}/home/waydroid/lxc/waydroid/config_nodes
install -D -m644 config/waydroid.cfg %{buildroot}/home/waydroid/waydroid.cfg
install -D -m644 config/waydroid_base.prop %{buildroot}/home/waydroid/waydroid_base.prop
install -D -m644 config/waydroid.prop %{buildroot}/home/waydroid/waydroid.prop

# Install Desktop file
install -D -m644 config/Waydroid.desktop %{buildroot}/usr/share/applications/Waydroid.desktop

# Install waydroid icon for app drawer
install -D -m644 config/waydroid.png %{buildroot}/usr/share/icons/hicolor/172x172/apps/waydroid.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
systemctl daemon-reload
systemctl-user daemon-reload
systemctl enable waydroid-container
chmod 777 /home/waydroid

%files
%defattr(-,root,root,-)
/opt/waydroid
%attr(-, defaultuser, users)/home/waydroid
%{_sharedstatedir}/waydroid
%{_sysconfdir}/modules-load.d/waydroid.conf
%{_bindir}/waydroid
%{_unitdir}/waydroid-container.service
%{_userunitdir}/waydroid-session.service
%{_datadir}/applications/Waydroid.desktop
%{_datadir}/icons/hicolor/172x172/apps/waydroid.png
