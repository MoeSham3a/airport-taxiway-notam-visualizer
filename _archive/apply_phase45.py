import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert CSS
css_to_insert = """
  /* RESPONSIVE & PWA */
  .mobile-menu-btn { display: none; background: none; border: none; color: var(--accent); font-size: 24px; cursor: pointer; padding: 0 10px; margin-left:-10px; }
  .sidebar-backdrop { display: none; position: absolute; top: 48px; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 15; }
  .manager-modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 100; align-items: center; justify-content: center; }
  .manager-content { background: var(--bg2); border: 1px solid var(--border); border-radius: 6px; width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; padding: 20px; font-family: var(--body); }
  .manager-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  .manager-title { font-family: var(--cond); font-size: 18px; color: var(--accent); letter-spacing: 0.1em; text-transform: uppercase; }
  .close-modal { background: none; border: none; color: var(--text2); font-size: 20px; cursor: pointer; padding:0 5px; }
  .airport-card { background: var(--bg3); border: 1px solid var(--border); border-radius: 4px; padding: 12px; margin-bottom: 12px; }
  .airport-card-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
  .ac-icao { font-family: var(--mono); font-size: 16px; color: var(--amber); font-weight: bold; }
  .ac-name { color: var(--text); font-size: 14px; }
  .ac-status { font-family: var(--mono); font-size: 11px; color: var(--text2); }
  .ac-status.loaded { color: var(--green); }
  .ac-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; flex-wrap: wrap; }
  .mgr-btn { font-family: var(--cond); font-size: 12px; padding: 6px 12px; border-radius: 3px; cursor: pointer; text-transform: uppercase; border: 1px solid var(--border); background: var(--bg4); color: var(--text); transition: all 0.15s; }
  .mgr-btn:hover { background: var(--border); }
  .mgr-btn.primary { background: var(--accent2); border-color: var(--accent); color: var(--accent); }
  .mgr-btn.danger { background: var(--red-bg); border-color: var(--red); color: var(--red); }
  
  /* Touch target sizes */
  @media (pointer: coarse) {
    .calib-action, .tab-btn, .parse-btn, .calib-btn, .calib-export, .airport-select, .mgr-btn { min-height: 44px; font-size: 14px; }
    .notam-item { min-height: 52px; padding: 12px 16px; }
    .sidebar-section { padding: 12px 16px; }
  }

  @media (max-width: 999px) {
    .app { grid-template-columns: 1fr; }
    .mobile-menu-btn { display: block; }
    .sidebar { position: absolute; top: 48px; left: 0; bottom: 0; width: 300px; transform: translateX(-100%); transition: transform 0.3s ease; z-index: 20; border-right: 1px solid var(--border); }
    .sidebar.open { transform: translateX(0); }
    .sidebar-backdrop.visible { display: block; }
    .topbar-logo span { display: none; }
    .airport-badge { display: none; }
    .topbar { gap: 10px; padding: 0 10px; }
  }
</style>"""

html = html.replace('</style>', css_to_insert)

# touch-action none
html = html.replace('id="overlay-svg"', 'id="overlay-svg" style="touch-action: none;"')

# 2. Insert Hamburger & Airports Button
topbar_orig = """  <div class="topbar">
    <div class="topbar-logo">GND<span>/</span>NOTAM"""
topbar_new = """  <div class="topbar">
    <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
    <div class="topbar-logo">GND<span>/</span>NOTAM"""
html = html.replace(topbar_orig, topbar_new)

btn_orig = """    <select class="airport-select" id="airport-select" onchange="switchAirport(this.value)">
      <option value="OMDB">OMDB — Dubai International</option>
    </select>"""
btn_new = """    <select class="airport-select" id="airport-select" onchange="switchAirport(this.value)">
    </select>
    <button class="calib-btn" onclick="openAirportManager()" style="margin-left:-5px;">⊞</button>"""
html = html.replace(btn_orig, btn_new)

# 3. Insert Modal HTML before closing </div> for .app
modal_html = """  <!-- Airport Manager Modal -->
  <div class="manager-modal" id="manager-modal">
    <div class="manager-content">
      <div class="manager-header">
        <div class="manager-title">Airport Manager</div>
        <button class="close-modal" onclick="closeAirportManager()">✕</button>
      </div>
      <div id="manager-list"></div>
      <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid var(--border);">
        <div class="section-label" style="margin-bottom: 12px;">Add Custom Airport</div>
        <div class="window-row">
          <div class="wf"><label>ICAO</label><input type="text" id="custom-icao" placeholder="e.g. OOMS" maxlength="4" style="text-transform:uppercase;"></div>
          <div class="wf"><label>Name</label><input type="text" id="custom-name" placeholder="Muscat Intl"></div>
        </div>
        <div class="window-row" style="grid-template-columns: 1fr;">
          <div class="wf"><label>Chart Image (.jpg/.png)</label><input type="file" id="custom-chart" accept="image/*"></div>
          <div class="wf"><label>Taxiway Data (.json)</label><input type="file" id="custom-twy" accept=".json"></div>
        </div>
        <button class="mgr-btn primary" style="width: 100%; margin-top: 10px;" onclick="importCustomAirport()">+ Add Airport</button>
      </div>
    </div>
  </div>
  <div class="sidebar-backdrop" id="sidebar-backdrop" onclick="toggleSidebar()"></div>
</div>

<script>"""

if '</div>\n\n\n<script>' in html:
    html = html.replace('</div>\n\n\n<script>', modal_html)
elif '</div>\n\n<script>' in html:
    html = html.replace('</div>\n\n<script>', modal_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied Phase 4 and 5 UI")
