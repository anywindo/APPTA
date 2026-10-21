document.addEventListener('DOMContentLoaded', async () => {
  const btnAppBenchmark = document.getElementById('btn-app-benchmark');
  const btnAppChat = document.getElementById('btn-app-chat');
  const dotApp = document.getElementById('dot-app');
  const dotChat = document.getElementById('dot-chat');

  const btnReloadView = document.getElementById('btn-reload-view');
  const btnRestartBackend = document.getElementById('btn-restart-backend');
  const btnOpenBrowser = document.getElementById('btn-open-browser');
  const btnToggleLogs = document.getElementById('btn-toggle-logs');
  const btnClearLogs = document.getElementById('btn-clear-logs');
  const btnCloseLogs = document.getElementById('btn-close-logs');
  const chkAutoscroll = document.getElementById('chk-autoscroll');
  const logFilterButtons = document.querySelectorAll('.log-filter');

  const statusPill = document.getElementById('status-pill');
  const statusText = document.getElementById('status-text');

  const viewApp = document.getElementById('view-app');
  const containerChat = document.getElementById('container-chat');
  const viewChatAlice = document.getElementById('view-chat-alice');
  const viewChatBob = document.getElementById('view-chat-bob');
  const btnReloadAlice = document.getElementById('btn-reload-alice');
  const btnReloadBob = document.getElementById('btn-reload-bob');

  const splashApp = document.getElementById('splash-app');
  const splashChat = document.getElementById('splash-chat');
  const splashLogApp = document.getElementById('splash-log-app');
  const splashLogChat = document.getElementById('splash-log-chat');

  const fullLogStream = document.getElementById('full-log-stream');
  const logsDrawer = document.getElementById('logs-drawer');
  const drawerBody = logsDrawer.querySelector('.drawer-body');

  let activeTab = 'app';
  let isSplitMode = true;
  let activeLogFilter = 'all';
  const logEntries = [];

  const servicesState = {
    app: { status: 'starting', url: 'http://127.0.0.1:7860', port: 7860 },
    chat: { status: 'starting', url: 'http://127.0.0.1:7861', port: 7861 }
  };

  function updateSplashVisibility() {
    if (activeTab === 'app') {
      splashChat.classList.add('hidden');
      if (servicesState.app.status === 'ready') {
        splashApp.classList.add('hidden');
      } else {
        splashApp.classList.remove('hidden');
      }
    } else {
      splashApp.classList.add('hidden');
      if (servicesState.chat.status === 'ready') {
        splashChat.classList.add('hidden');
      } else {
        splashChat.classList.remove('hidden');
      }
    }
  }

  // Switch between tabs
  function selectTab(appKey) {
    activeTab = appKey;
    window.electronAPI.setActiveApp(appKey);

    if (appKey === 'app') {
      btnAppBenchmark.classList.add('active');
      btnAppBenchmark.setAttribute('aria-selected', 'true');
      btnAppChat.classList.remove('active');
      btnAppChat.setAttribute('aria-selected', 'false');

      viewApp.classList.add('active');
      containerChat.classList.remove('active');
    } else {
      btnAppChat.classList.add('active');
      btnAppChat.setAttribute('aria-selected', 'true');
      btnAppBenchmark.classList.remove('active');
      btnAppBenchmark.setAttribute('aria-selected', 'false');

      containerChat.classList.add('active');
      viewApp.classList.remove('active');
    }

    updateHeaderStatusPill();
    updateSplashVisibility();
  }

  function updateHeaderStatusPill() {
    if (!statusPill || !statusText) return;
    const s = servicesState[activeTab];
    if (!s) return;

    statusPill.className = 'status-badge ' + s.status;
    if (s.status === 'ready') {
      statusText.textContent = `${activeTab === 'app' ? 'Benchmark' : 'Chat (Alice & Bob)'} Online :${s.port}`;
    } else if (s.status === 'starting') {
      statusText.textContent = `Starting ${s.script || activeTab} (:${s.port})...`;
    } else if (s.status === 'stopping') {
      statusText.textContent = `Restarting ${activeTab}...`;
    } else if (s.status === 'error') {
      statusText.textContent = `Error in ${activeTab}`;
    } else {
      statusText.textContent = `Stopped`;
    }
  }

  function updateTabDot(appKey, status) {
    const dot = appKey === 'app' ? dotApp : dotChat;
    if (!dot) return;
    dot.className = 'tab-indicator dot-' + status;
  }

  function handleServiceStatus(data) {
    if (!data || !data.app) return;
    const appKey = data.app;
    servicesState[appKey] = { ...servicesState[appKey], ...data };

    updateTabDot(appKey, data.status);
    if (activeTab === appKey) {
      updateHeaderStatusPill();
    }

    if (data.status === 'ready' && data.url) {
      if (appKey === 'app') {
        if (!viewApp.src || viewApp.src === 'about:blank' || viewApp.src !== data.url) {
          viewApp.src = data.url;
        }
      } else if (appKey === 'chat') {
        const aliceUrl = `${data.url}/?user=Alice`;
        const bobUrl = `${data.url}/?user=Bob`;

        if (!viewChatAlice.src || viewChatAlice.src === 'about:blank' || !viewChatAlice.src.includes('user=Alice')) {
          viewChatAlice.src = aliceUrl;
        }
        if (!viewChatBob.src || viewChatBob.src === 'about:blank' || !viewChatBob.src.includes('user=Bob')) {
          viewChatBob.src = bobUrl;
        }
      }
    }

    updateSplashVisibility();
  }

  // Webview lifecycle listeners
  if (viewApp) {
    viewApp.addEventListener('dom-ready', () => {
      if (activeTab === 'app') splashApp.classList.add('hidden');
    });
  }
  if (viewChatAlice) {
    viewChatAlice.addEventListener('dom-ready', () => {
      if (activeTab === 'chat') splashChat.classList.add('hidden');
    });
  }
  if (viewChatBob) {
    viewChatBob.addEventListener('dom-ready', () => {
      if (activeTab === 'chat') splashChat.classList.add('hidden');
    });
  }

  // Reload Individual Panes (if buttons present)
  if (btnReloadAlice) {
    btnReloadAlice.addEventListener('click', () => {
      if (viewChatAlice) {
        const url = servicesState.chat.url ? `${servicesState.chat.url}/?user=Alice` : viewChatAlice.src;
        viewChatAlice.src = url;
      }
    });
  }

  if (btnReloadBob) {
    btnReloadBob.addEventListener('click', () => {
      if (viewChatBob) {
        const url = servicesState.chat.url ? `${servicesState.chat.url}/?user=Bob` : viewChatBob.src;
        viewChatBob.src = url;
      }
    });
  }

  // Tab switcher click handlers
  btnAppBenchmark.addEventListener('click', () => selectTab('app'));
  btnAppChat.addEventListener('click', () => selectTab('chat'));

  // Global Action Buttons
  if (btnReloadView) {
    btnReloadView.addEventListener('click', () => {
      if (activeTab === 'app') {
        if (viewApp) viewApp.reload();
      } else {
        if (viewChatAlice) viewChatAlice.reload();
        if (viewChatBob) viewChatBob.reload();
      }
    });
  }

  btnRestartBackend.addEventListener('click', async () => {
    const splash = activeTab === 'app' ? splashApp : splashChat;
    splash.classList.remove('hidden');
    await window.electronAPI.restartBackend(activeTab);
  });

  if (btnOpenBrowser) {
    btnOpenBrowser.addEventListener('click', () => {
      const s = servicesState[activeTab];
      if (s && s.url) {
        window.electronAPI.openExternal(s.url);
      }
    });
  }

  // Logs Drawer
  function toggleLogs() {
    const isOpen = logsDrawer.classList.toggle('open');
    btnToggleLogs.classList.toggle('active', isOpen);
    btnToggleLogs.setAttribute('aria-expanded', isOpen);
  }

  btnToggleLogs.addEventListener('click', toggleLogs);
  btnCloseLogs.addEventListener('click', () => {
    logsDrawer.classList.remove('open');
    btnToggleLogs.classList.remove('active');
    btnToggleLogs.setAttribute('aria-expanded', 'false');
  });

  btnClearLogs.addEventListener('click', () => {
    logEntries.length = 0;
    fullLogStream.textContent = '';
    splashLogApp.textContent = '';
    splashLogChat.textContent = '';
  });

  logFilterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      logFilterButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');
      activeLogFilter = btn.dataset.filter;
      renderLogs();
    });
  });

  function renderLogs() {
    const filtered = activeLogFilter === 'all'
      ? logEntries
      : logEntries.filter(entry => entry.app === activeLogFilter);
    fullLogStream.textContent = filtered.map(e => e.text).join('');
    if (chkAutoscroll.checked) {
      drawerBody.scrollTop = drawerBody.scrollHeight;
    }
  }

  // Handle Backend Logs
  window.electronAPI.onBackendLog((payload) => {
    const appKey = typeof payload === 'object' ? payload.app : activeTab;
    const logText = typeof payload === 'object' ? payload.text : payload;

    logEntries.push({ app: appKey, text: logText });
    if (logEntries.length > 2000) logEntries.shift();

    const targetSplashLog = appKey === 'app' ? splashLogApp : splashLogChat;
    if (targetSplashLog) {
      const lines = logText.trim().split('\n');
      targetSplashLog.textContent = lines.slice(-3).join('\n') || logText;
    }

    if (activeLogFilter === 'all' || activeLogFilter === appKey) {
      fullLogStream.textContent += logText;
      if (chkAutoscroll.checked) {
        drawerBody.scrollTop = drawerBody.scrollHeight;
      }
    }
  });

  window.electronAPI.onBackendStatus(handleServiceStatus);

  if (window.electronAPI.onSwitchTab) {
    window.electronAPI.onSwitchTab((appKey) => selectTab(appKey));
  }

  if (window.electronAPI.onInitialState) {
    window.electronAPI.onInitialState((state) => {
      if (state.activeApp) selectTab(state.activeApp);
      if (state.services) {
        if (state.services.app) handleServiceStatus(state.services.app.status);
        if (state.services.chat) handleServiceStatus(state.services.chat.status);
      }
    });
  }

  try {
    const init = await window.electronAPI.getState();
    if (init) {
      if (init.activeApp) selectTab(init.activeApp);
      if (init.services) {
        if (init.services.app) handleServiceStatus(init.services.app.status);
        if (init.services.chat) handleServiceStatus(init.services.chat.status);
      }
    }
  } catch (e) {
    console.error('Failed to get state:', e);
  }
});
