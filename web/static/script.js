/* ===  Expert HR — script.js  v2.0  === */
let currentStep = 1;
const totalSteps = 5;
let liveChart = null;
let logLines = [];

// ==================  INIT  ==================
document.addEventListener('DOMContentLoaded', () => {
    initWizard();
    initChart();
    initThemeToggle();
});

// ==================  WIZARD  ================
function initWizard() {
    document.getElementById('btn-next').addEventListener('click', () => {
        if (currentStep < totalSteps) goToStep(currentStep + 1);
        else document.getElementById('btn-start-generate').click();
    });
    document.getElementById('btn-prev').addEventListener('click', () => {
        if (currentStep > 1) goToStep(currentStep - 1);
    });
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const step = parseInt(item.dataset.step);
            if (step <= currentStep + 1 || item.classList.contains('completed')) goToStep(step);
        });
    });

    // Excel drop zone
    const dropZone = document.getElementById('excel-drop-zone');
    dropZone.addEventListener('click', () => document.getElementById('excel-input').click());
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', e => {
        e.preventDefault(); dropZone.classList.remove('dragover');
        if (e.dataTransfer.files[0]) handleExcelUpload(e.dataTransfer.files[0]);
    });
    document.getElementById('excel-input').addEventListener('change', e => {
        if (e.target.files[0]) handleExcelUpload(e.target.files[0]);
    });

    // Template upload
    const tmplInput = document.getElementById('template-input');
    document.getElementById('btn-add-templates').addEventListener('click', () => tmplInput.click());
    tmplInput.addEventListener('change', e => { if (e.target.files.length) handleTemplateUpload(e.target.files); });

    // Options
    document.getElementById('btn-save-options').addEventListener('click', saveOptions);

    // Generate/Stop
    document.getElementById('btn-start-generate').addEventListener('click', startGeneration);
    document.getElementById('btn-stop-generate').addEventListener('click', stopGeneration);

    // Refresh
    document.getElementById('btn-refresh').addEventListener('click', () => {
        if (currentStep === 2) loadExcelPreview();
        else if (currentStep === 3) loadTemplates();
        else if (currentStep === 4) { runMappingAnalysis(); loadOptions(); }
    });

    loadRecentFiles();
}

function goToStep(step) {
    // Mark old
    const oldPane = document.getElementById(`pane-${currentStep}`);
    const oldNav = document.querySelector(`.nav-item[data-step="${currentStep}"]`);
    oldPane.classList.remove('active');
    oldNav.classList.remove('active');
    oldNav.classList.add('completed');
    document.querySelector(`.step-dots .dot:nth-child(${currentStep})`).classList.remove('active');

    currentStep = step;

    const newPane = document.getElementById(`pane-${currentStep}`);
    const newNav = document.querySelector(`.nav-item[data-step="${currentStep}"]`);
    newPane.classList.add('active');
    newNav.classList.add('active');
    newNav.classList.remove('completed');
    document.querySelector(`.step-dots .dot:nth-child(${currentStep})`).classList.add('active');

    updateStepTitle();
    updateNavButtons();

    if (currentStep === 2) loadExcelPreview();
    if (currentStep === 3) loadTemplates();
    if (currentStep === 4) { runMappingAnalysis(); loadOptions(); }
    if (currentStep === 5) startDashboardPolling();
}

function updateStepTitle() {
    const titles = [
        "Pasul 1 — Încărcare Fișier de Date",
        "Pasul 2 — Verificare Date Excel",
        "Pasul 3 — Șabloane Documente",
        "Pasul 4 — Opțiuni & Mapare",
        "Pasul 5 — Generare & Dashboard"
    ];
    document.getElementById('step-title').textContent = titles[currentStep - 1];
}

function updateNavButtons() {
    document.getElementById('btn-prev').disabled = (currentStep === 1);
    const btn = document.getElementById('btn-next');
    if (currentStep === totalSteps) {
        btn.innerHTML = 'Starts Generator <i class="fas fa-rocket"></i>';
    } else {
        btn.innerHTML = 'Pasul următor <i class="fas fa-chevron-right"></i>';
    }
}

function initThemeToggle() {
    const btn = document.getElementById('btn-theme-toggle');
    btn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        btn.querySelector('i').classList.toggle('fa-moon');
        btn.querySelector('i').classList.toggle('fa-sun');
    });
}

// ==================  API HANDLERS  ==========

async function loadRecentFiles() {
    try {
        const resp = await fetch('/api/wizard/recent-excel');
        const data = await resp.json();
        const container = document.getElementById('recent-excel-list');
        if (!data.recent || data.recent.length === 0) { container.innerHTML = ''; return; }
        let html = '<p style="font-size:0.78rem;color:var(--text-3);margin-bottom:8px;text-transform:uppercase;font-weight:600;letter-spacing:0.5px"><i class="fas fa-history" style="margin-right:6px"></i>Recente</p>';
        data.recent.slice(0, 5).forEach(f => {
            const name = f.split(/[\/\\]/).pop();
            html += `<div class="recent-file-item" onclick="loadFromPath('${f}')">
                <i class="fas fa-file-excel" style="color:var(--success)"></i>
                <span>${name}</span>
            </div>`;
        });
        container.innerHTML = html;
    } catch (e) { }
}

async function handleExcelUpload(file) {
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
        showToast('Doar fișiere Excel (.xlsx/.xls) sunt acceptate.', 'error'); return;
    }
    setDropZoneState('loading', `Se încarcă: ${file.name}…`);
    const fd = new FormData();
    fd.append('file', file);
    try {
        const resp = await fetch('/api/wizard/upload-excel', { method: 'POST', body: fd });
        const data = await resp.json();
        if (data.error) {
            setDropZoneState('error', `Eroare: ${data.error}`);
            showToast(data.error, 'error');
        } else {
            setDropZoneState('success', `✓  Fișier încărcat: ${file.name}`);
            showToast(`Fișierul "${file.name}" a fost încărcat cu succes.`, 'success');
        }
    } catch (e) {
        setDropZoneState('error', 'Eroare de rețea la încărcare');
        showToast('Eroare de rețea.', 'error');
    }
}

function setDropZoneState(state, text) {
    const dz = document.getElementById('excel-drop-zone');
    const lbl = document.getElementById('excel-drop-text');
    dz.style.borderColor = state === 'success' ? 'var(--success)'
        : state === 'error' ? 'var(--error)'
            : 'var(--accent)';
    lbl.textContent = text;
}

async function handleTemplateUpload(files) {
    const fd = new FormData();
    for (const f of files) fd.append('files[]', f);
    try {
        const resp = await fetch('/api/wizard/upload-template', { method: 'POST', body: fd });
        const data = await resp.json();
        if (data.error) showToast(data.error, 'error');
        else { showToast(`${data.count} șablon(e) adăugate.`, 'success'); loadTemplates(); }
    } catch (e) { showToast('Eroare la adăugarea șabloanelor.', 'error'); }
}

async function loadExcelPreview() {
    const container = document.getElementById('excel-preview-table');
    container.innerHTML = '<div class="loader">Se încarcă previzualizarea…</div>';
    try {
        const resp = await fetch('/api/wizard/preview-excel');
        const data = await resp.json();
        if (data.error) { container.innerHTML = `<p class="error-msg"><i class="fas fa-exclamation-circle"></i> ${data.error}</p>`; return; }
        renderTable(data, container);
        document.getElementById('row-count').textContent = `${data.rows.length} rânduri`;
    } catch (e) {
        container.innerHTML = '<p class="error-msg">Eroare la comunicarea cu serverul.</p>';
    }
}

function renderTable(data, container) {
    let html = '<table><thead><tr>';
    data.columns.forEach(c => html += `<th>${escHtml(c)}</th>`);
    html += '</tr></thead><tbody>';
    data.rows.slice(0, 15).forEach(row => {
        html += '<tr>';
        data.columns.forEach(c => html += `<td title="${escHtml(String(row[c] || ''))}">${escHtml(String(row[c] || ''))}</td>`);
        html += '</tr>';
    });
    html += '</tbody></table>';
    if (data.rows.length > 15)
        html += `<p class="info-note"><i class="fas fa-info-circle"></i> Se afișează 15 din ${data.rows.length} rânduri.</p>`;
    container.innerHTML = html;
}

async function loadTemplates() {
    const c = document.getElementById('template-list-container');
    c.innerHTML = '<div class="loader">Se încarcă șabloanele…</div>';
    try {
        const resp = await fetch('/api/wizard/templates');
        const data = await resp.json();
        if (!data.templates.length) {
            c.innerHTML = '<p class="empty-state"><i class="fas fa-folder-open" style="margin-right:8px"></i>Niciun șablon. Adăugați fișiere .docx.</p>'; return;
        }
        let html = '<div class="template-grid">';
        data.templates.forEach(p => {
            const name = p.split(/[\/\\]/).pop();
            const ext = name.split('.').pop().toLowerCase();
            const icon = ext === 'docx' ? 'fa-file-word' : ext === 'pdf' ? 'fa-file-pdf' : 'fa-file-alt';
            html += `<div class="template-item card">
                <i class="fas ${icon}"></i>
                <span>${escHtml(name)}</span>
            </div>`;
        });
        html += '</div>';
        c.innerHTML = html;
    } catch (e) { c.innerHTML = '<p class="error-msg">Eroare la încărcare.</p>'; }
}

async function runMappingAnalysis() {
    const details = document.getElementById('mapping-details-list');
    const summary = document.getElementById('mapping-summary');
    details.innerHTML = '<div class="loader">Se analizează…</div>';

    try {
        const [tResp, eResp] = await Promise.all([
            fetch('/api/wizard/templates'),
            fetch('/api/wizard/preview-excel')
        ]);
        const tData = await tResp.json();
        const eData = await eResp.json();

        if (!tData.templates.length || eData.error) {
            summary.innerHTML = '<span class="status-badge red"><i class="fas fa-times-circle"></i> Incomplet</span>';
            details.innerHTML = '<p style="font-size:0.86rem;color:var(--text-2)">Asigurați-vă că ați încărcat atât fișierul Excel cât și șabloanele Word.</p>';
            return;
        }

        summary.innerHTML = '<span class="status-badge green"><i class="fas fa-check-circle"></i> Gata de Generare</span>';
        details.innerHTML = `
            <div class="analysis-item"><i class="fas fa-check-circle text-success"></i><span>${tData.templates.length} șablon(e) încărcate</span></div>
            <div class="analysis-item"><i class="fas fa-table text-blue"></i><span>${eData.columns?.length || '?'} coloane detectate în Excel</span></div>
            <div class="analysis-item"><i class="fas fa-users text-blue"></i><span>${eData.rows?.length || '?'} rânduri de procesat</span></div>
            <div class="analysis-item"><i class="fas fa-magic text-success"></i><span>Mapare fuzzy activă — coloanele vor fi asociate automat</span></div>
        `;
    } catch (e) {
        details.innerHTML = '<p class="error-msg">Eroare la analiza mapării.</p>';
    }
}

async function loadOptions() {
    try {
        const resp = await fetch('/api/wizard/options');
        const data = await resp.json();
        if (data.error) return;

        const select = document.getElementById('opt-folder-column');
        select.innerHTML = '<option value="">(Niciunul)</option>';
        (data.available_columns || []).forEach(c => {
            const opt = document.createElement('option');
            opt.value = c; opt.textContent = c;
            select.appendChild(opt);
        });
        select.value = data.folder_column || '';
        document.getElementById('opt-output-dir').value = data.output_dir || '';
        document.getElementById('opt-filename').value = data.filename_pattern || '';
        document.getElementById('opt-multiprocessing').checked = !!data.multiprocessing;
        document.getElementById('opt-pdf').checked = !!data.pdf_gen;
        document.getElementById('opt-zip').checked = !!data.zip_per_row;
    } catch (e) { }
}

async function saveOptions() {
    const btn = document.getElementById('btn-save-options');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Se salvează…';
    btn.disabled = true;

    const payload = {
        folder_column: document.getElementById('opt-folder-column').value,
        output_dir: document.getElementById('opt-output-dir').value,
        filename_pattern: document.getElementById('opt-filename').value,
        multiprocessing: document.getElementById('opt-multiprocessing').checked,
        pdf_gen: document.getElementById('opt-pdf').checked,
        zip_per_row: document.getElementById('opt-zip').checked
    };
    try {
        await fetch('/api/wizard/options', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        btn.innerHTML = '<i class="fas fa-check"></i> Salvat!';
        showToast('Opțiunile au fost salvate.', 'success');
    } catch (e) {
        btn.innerHTML = '<i class="fas fa-times"></i> Eroare!';
        showToast('Eroare la salvare.', 'error');
    }
    setTimeout(() => { btn.innerHTML = '<i class="fas fa-save"></i> Salvează Opțiunile'; btn.disabled = false; }, 2500);
}

// ==================  CHART  =================
function initChart() {
    const ctx = document.getElementById('live-chart').getContext('2d');
    liveChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Finalizate', 'În așteptare', 'Erori'],
            datasets: [{
                data: [0, 100, 0],
                backgroundColor: ['#10b981', '#3b82f6', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 6,
                cutout: '72%'
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', padding: 16, font: { family: 'Inter', size: 12 } }
                },
                tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw}` } }
            },
            animation: { animateRotate: true, duration: 600 }
        }
    });
}

// ==================  DASHBOARD POLLING  =====
let pollingInterval = null;

function startDashboardPolling() {
    if (pollingInterval) return;
    pollingInterval = setInterval(async () => {
        if (currentStep !== 5) return;
        try {
            const resp = await fetch('/api/wizard/stats');
            const s = await resp.json();

            // Progress
            const pct = Math.round(s.percent || 0);
            document.getElementById('progress-percent').textContent = `${pct}%`;
            document.getElementById('progress-bar').style.width = `${pct}%`;

            // Mini stats
            document.getElementById('stat-success').textContent = s.success || 0;
            document.getElementById('stat-errors').textContent = s.errors || 0;

            // Chart
            liveChart.data.datasets[0].data = [s.success || 0, Math.max(0, (s.success + s.errors > 0) ? (100 - pct) : 100), s.errors || 0];
            liveChart.update('none');

            // Resources
            const cpu = Math.round(s.cpu || 0);
            const ram = Math.round(s.ram || 0);
            document.getElementById('cpu-bar').style.width = `${cpu}%`;
            document.getElementById('ram-bar').style.width = `${ram}%`;
            document.getElementById('cpu-pct').textContent = `${cpu}%`;
            document.getElementById('ram-pct').textContent = `${ram}%`;

        } catch (e) { }
    }, 2000);
}

// ==================  GENERATION  ============
async function startGeneration() {
    const btnStart = document.getElementById('btn-start-generate');
    const btnStop = document.getElementById('btn-stop-generate');
    btnStart.disabled = true;
    btnStop.disabled = false;
    btnStart.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Se generează…';
    appendLog('⚡ Generarea a fost lansată…');

    try {
        await fetch('/api/wizard/start', { method: 'POST' });
    } catch (e) {
        showToast('Eroare comunicare server.', 'error');
        btnStart.disabled = false;
        btnStop.disabled = true;
    }
}

async function stopGeneration() {
    try { await fetch('/api/wizard/stop', { method: 'POST' }); } catch (e) { }
    document.getElementById('btn-start-generate').disabled = false;
    document.getElementById('btn-start-generate').innerHTML = '<i class="fas fa-rocket"></i> Lansează Generarea';
    document.getElementById('btn-stop-generate').disabled = true;
    appendLog('⛔ Generare oprită de utilizator.');
}

// ==================  LOG  ===================
function appendLog(msg) {
    const el = document.getElementById('live-log');
    if (!el) return;
    const line = document.createElement('div');
    const now = new Date().toLocaleTimeString('ro-RO');
    line.innerHTML = `<span style="color:var(--text-3)">[${now}]</span> ${escHtml(msg)}`;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
    logLines.push(msg);
    if (el.children.length > 200) el.removeChild(el.firstChild);
}

// ==================  UTILS  =================
function escHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function showToast(msg, type = 'info') {
    let toast = document.getElementById('_toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = '_toast';
        toast.style.cssText = `
            position:fixed;bottom:28px;right:28px;z-index:9999;
            padding:12px 20px;border-radius:12px;font-size:0.86rem;font-weight:600;
            font-family:Inter,sans-serif;max-width:320px;box-shadow:0 8px 30px rgba(0,0,0,0.4);
            transition:all 0.3s ease;opacity:0;transform:translateY(12px);
        `;
        document.body.appendChild(toast);
    }
    const colors = { success: ['#10b981', '#022c22'], error: ['#ef4444', '#1f0606'], info: ['#3b82f6', '#0a1628'] };
    const [fg, bg] = colors[type] || colors.info;
    toast.style.background = bg;
    toast.style.color = fg;
    toast.style.border = `1px solid ${fg}44`;
    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
    clearTimeout(toast._t);
    toast._t = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px)';
    }, 3500);
}

async function loadFromPath(path) {
    showToast('Se încarcă fișierul recent…', 'info');
    // Set path directly on server side
    try {
        const opts = await (await fetch('/api/wizard/options')).json();
        await fetch('/api/wizard/options', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...opts })
        });
    } catch (e) { }
}
